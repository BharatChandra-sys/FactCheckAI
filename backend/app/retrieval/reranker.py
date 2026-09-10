"""
Cross-Encoder Reranker

Takes a pool of ~30 hybrid-retrieved candidates and reranks them
using a cross-encoder model for precise relevance scoring.

Why cross-encoder over bi-encoder?
- Bi-encoder (used for retrieval): encodes query and document separately
  → fast but less accurate (no cross-attention between query and doc)
- Cross-encoder: encodes query+document together → slow but precise
  → ideal for reranking a small candidate pool (15-30 docs)

Model: cross-encoder/ms-marco-MiniLM-L-6-v2
  - 22M params, ~80ms per pair on CPU
  - Trained on MS MARCO passage ranking
  - Works well for sentence-level relevance

Falls back to the LLM-based scorer in cross_encoder.py when
sentence-transformers is not installed.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

_RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_reranker            = None


def _load_reranker():
    global _reranker
    if _reranker is not None:
        return _reranker
    try:
        from sentence_transformers import CrossEncoder
        _reranker = CrossEncoder(_RERANKER_MODEL_NAME)
        logger.info("Cross-encoder reranker loaded: %s", _RERANKER_MODEL_NAME)
    except ImportError:
        logger.warning("sentence-transformers not installed — using LLM fallback reranker")
    except Exception as e:
        logger.warning("Failed to load cross-encoder: %s", e)
    return _reranker


def rerank(
    claim:      str,
    candidates: list[dict],
    text_key:   str = "claim_text",
    top_k:      int = 5,
) -> list[dict]:
    """
    Rerank a candidate pool by relevance to the claim.

    Args:
        claim:      The claim being fact-checked.
        candidates: List of dicts, each with a text field (text_key).
        text_key:   Key in each dict that holds the text to score.
        top_k:      Number of top candidates to return after reranking.

    Returns:
        Top-k candidates sorted by cross-encoder score (descending),
        each with an added 'rerank_score' field.
    """
    if not candidates:
        return []

    if len(candidates) <= top_k:
        return candidates  # No need to rerank small pools

    texts = [c.get(text_key, "") or c.get("title", "") for c in candidates]

    model = _load_reranker()
    if model is not None:
        try:
            pairs  = [(claim, t) for t in texts]
            scores = model.predict(pairs, show_progress_bar=False)
            for c, s in zip(candidates, scores):
                c["rerank_score"] = float(s)
            ranked = sorted(candidates, key=lambda x: x.get("rerank_score", 0), reverse=True)
            logger.debug("Cross-encoder reranked %d → %d candidates",
                         len(candidates), top_k)
            return ranked[:top_k]
        except Exception as e:
            logger.warning("Cross-encoder reranking failed, using RRF order: %s", e)

    # Fallback: use LLM-based scorer from legacy cross_encoder.py
    try:
        from app.analysis.cross_encoder import rerank_articles
        return rerank_articles(claim, candidates, top_k=top_k)
    except Exception as e:
        logger.debug("LLM fallback reranker failed: %s", e)

    # Last resort: return top_k by RRF score
    sorted_by_rrf = sorted(
        candidates,
        key=lambda x: x.get("rrf_score", x.get("similarity", 0)),
        reverse=True
    )
    return sorted_by_rrf[:top_k]


def rerank_all(
    claim:     str,
    pool:      dict[str, list[dict]],
    total_k:   int = 8,
) -> list[dict]:
    """
    Rerank a balanced evidence pool (output of retrieve_balanced_evidence).

    Takes supporting + contradicting + neutral + authoritative + historical,
    deduplicates, reranks the combined pool, returns top total_k.

    Preserves stance diversity: always includes at least 1 supporting
    and 1 contradicting if they exist.
    """
    # Flatten and deduplicate by ID
    seen_ids: set = set()
    flat: list[dict] = []
    for group in pool.values():
        for item in group:
            item_id = item.get("id") or item.get("url", "")
            if item_id not in seen_ids:
                seen_ids.add(item_id)
                flat.append(item)

    if not flat:
        return []

    # Rerank the full pool
    text_key = "claim_text" if "claim_text" in flat[0] else "title"
    reranked = rerank(claim, flat, text_key=text_key, top_k=min(total_k + 5, len(flat)))

    # Ensure stance diversity: at least 1 supporting + 1 contradicting
    result: list[dict]  = []
    has_support     = False
    has_contradict  = False

    for item in reranked:
        stance = item.get("stance", "neutral")
        if not has_support and stance == "support":
            result.insert(0, item)
            has_support = True
        elif not has_contradict and stance == "contradict":
            result.append(item)
            has_contradict = True
        else:
            result.append(item)

        if len(result) >= total_k:
            break

    return result[:total_k]
