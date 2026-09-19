"""
Hybrid Retrieval

Combines lexical (BM25) and semantic (vector) retrieval for maximum recall,
then deduplicates and scores the merged candidate pool.

Why hybrid?
- BM25 is strong for exact phrases, entity names, numbers, dates
- Vector search is strong for paraphrases, conceptual similarity
- Neither alone covers all retrieval needs for fact-checking

Pipeline:
  CLAIM
    ↓
  ┌────────────────┬──────────────────┐
  ↓                ↓                  ↓
BM25 on          Vector search      Vector search
claim_records    (similar claims)   (evidence docs)
  ↓                ↓                  ↓
  └────────────────┴──────────────────┘
                   ↓
            Reciprocal Rank Fusion
                   ↓
            Deduplicated pool
                   ↓
            Top-K candidates
                   ↓
            (Reranker in reranker.py)
"""
from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def _bm25_search_claims(
    db:         Session,
    claim_text: str,
    top_k:      int = 15,
) -> list[dict]:
    """
    BM25 lexical search over stored fact_checks.

    Uses PostgreSQL full-text search (ts_vector) which is always available.
    Falls back to simple ILIKE for short queries.
    """
    from sqlalchemy import text as sa_text
    from app.models import VerificationStatus

    try:
        # PostgreSQL full-text search
        rows = db.execute(
            sa_text("""
                SELECT id, claim_text, verdict, confidence, verification_status,
                       ts_rank_cd(
                           to_tsvector('english', claim_text),
                           plainto_tsquery('english', :q)
                       ) AS rank
                FROM fact_checks
                WHERE verification_status IN (:v1, :v2)
                  AND to_tsvector('english', claim_text) @@ plainto_tsquery('english', :q)
                ORDER BY rank DESC
                LIMIT :k
            """),
            {
                "q":  claim_text[:200],
                "v1": VerificationStatus.VERIFIED,
                "v2": VerificationStatus.HUMAN_REVIEWED,
                "k":  top_k,
            },
        ).fetchall()
        return [
            {
                "id":                  r.id,
                "claim_text":          r.claim_text,
                "verdict":             r.verdict,
                "confidence":          r.confidence,
                "verification_status": r.verification_status,
                "bm25_rank":           float(r.rank),
                "retrieval_method":    "bm25",
            }
            for r in rows
        ]
    except Exception as e:
        logger.debug("BM25 search failed: %s", e)
        return []


def _bm25_search_evidence(
    db:         Session,
    claim_text: str,
    top_k:      int            = 15,
    stance:     Optional[str]  = None,
    max_tier:   int            = 3,
) -> list[dict]:
    """BM25 lexical search over evidence_documents."""
    from sqlalchemy import text as sa_text

    try:
        stance_clause = "AND stance = :stance" if stance else ""
        rows = db.execute(
            sa_text(f"""
                SELECT id, url, title, domain, stance, trust_score, source_tier, published_at,
                       ts_rank_cd(
                           to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,'')),
                           plainto_tsquery('english', :q)
                       ) AS rank
                FROM evidence_documents
                WHERE source_tier <= :max_tier
                  AND to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))
                      @@ plainto_tsquery('english', :q)
                  {stance_clause}
                ORDER BY rank DESC
                LIMIT :k
            """),
            {
                "q":        claim_text[:200],
                "max_tier": max_tier,
                "stance":   stance,
                "k":        top_k,
            },
        ).fetchall()
        return [
            {
                "id":           r.id,
                "url":          r.url,
                "title":        r.title,
                "domain":       r.domain,
                "stance":       r.stance,
                "trust_score":  r.trust_score,
                "source_tier":  r.source_tier,
                "published_at": r.published_at.isoformat() if r.published_at else None,
                "bm25_rank":    float(r.rank),
                "retrieval_method": "bm25",
            }
            for r in rows
        ]
    except Exception as e:
        logger.debug("BM25 evidence search failed: %s", e)
        return []


def _reciprocal_rank_fusion(
    lists:  list[list[dict]],
    id_key: str = "id",
    k:      int = 60,
) -> list[dict]:
    """
    Reciprocal Rank Fusion (RRF) to merge multiple ranked lists.

    RRF score = Σ 1/(k + rank_i)

    Higher k → less aggressive fusion; k=60 is the standard.
    Documents appearing in multiple lists get boosted.
    """
    scores: dict[int, float]  = {}
    items:  dict[int, dict]   = {}

    for ranked_list in lists:
        for rank, item in enumerate(ranked_list, start=1):
            doc_id = item[id_key]
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
            if doc_id not in items:
                items[doc_id] = item

    merged = sorted(scores.keys(), key=lambda d: scores[d], reverse=True)
    result = []
    for doc_id in merged:
        item = items[doc_id].copy()
        item["rrf_score"] = round(scores[doc_id], 6)
        result.append(item)
    return result


def retrieve_similar_claims(
    db:                 Session,
    claim_text:         str,
    top_k:              int   = 10,
    min_confidence:     float = 0.0,
) -> list[dict]:
    """
    Hybrid retrieval for historical fact-checks.

    Runs BM25 + vector search in parallel, merges with RRF,
    returns top_k deduplicated candidates.
    """
    from app.retrieval.vector_store import search_similar_claims

    # Parallel fetch
    bm25_results   = _bm25_search_claims(db, claim_text, top_k=15)
    vector_results = search_similar_claims(
        db, claim_text, top_k=15, min_confidence=min_confidence
    )

    if not bm25_results and not vector_results:
        return []

    merged = _reciprocal_rank_fusion([bm25_results, vector_results])
    return merged[:top_k]


def retrieve_evidence(
    db:          Session,
    claim_text:  str,
    top_k:       int          = 8,
    stance:      Optional[str] = None,
    max_tier:    int           = 3,
) -> list[dict]:
    """
    Hybrid retrieval for evidence documents.

    Supports evidence-aware retrieval:
    - Call with stance='support'    to get supporting evidence
    - Call with stance='contradict' to get contradicting evidence
    - Call with stance=None         to get all relevant evidence

    The plan recommends fetching supporting + contradicting separately
    so the LLM sees both sides (prevents confirmation bias in retrieval).
    """
    from app.retrieval.vector_store import search_evidence

    bm25_results   = _bm25_search_evidence(db, claim_text, top_k=15,
                                            stance=stance, max_tier=max_tier)
    vector_results = search_evidence(db, claim_text, stance=stance,
                                     top_k=15, max_tier=max_tier)

    if not bm25_results and not vector_results:
        return []

    merged = _reciprocal_rank_fusion([bm25_results, vector_results])
    return merged[:top_k]


def retrieve_balanced_evidence(
    db:         Session,
    claim_text: str,
    n_each:     int = 3,
    max_tier:   int = 3,
) -> dict[str, list[dict]]:
    """
    Retrieve balanced evidence: n_each supporting + n_each contradicting +
    n_each historical + up to 2 authoritative sources (tier 1–2).

    This is the evidence-aware retrieval described in docs/plan.md section 9.
    """
    supporting    = retrieve_evidence(db, claim_text, top_k=n_each,
                                       stance="support",    max_tier=max_tier)
    contradicting = retrieve_evidence(db, claim_text, top_k=n_each,
                                       stance="contradict", max_tier=max_tier)
    neutral       = retrieve_evidence(db, claim_text, top_k=n_each,
                                       stance="neutral",    max_tier=max_tier)
    authoritative = retrieve_evidence(db, claim_text, top_k=2, max_tier=2)
    historical    = retrieve_similar_claims(db, claim_text, top_k=n_each)

    return {
        "supporting":    supporting,
        "contradicting": contradicting,
        "neutral":       neutral,
        "authoritative": authoritative,
        "historical":    historical,
    }
