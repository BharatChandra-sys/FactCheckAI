"""
Citation Validator

Prevents a key RAG failure mode: the LLM claiming a source says something
that the source doesn't actually say (hallucinated citations).

For each citation in the RAG assessment, we check whether the cited claim
appears (exactly or semantically) in the retrieved source content.

Result: VALID | INVALID | UNVERIFIABLE
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def validate_citations(
    citations:  list[dict],
    evidence:   list[dict],
    threshold:  float = 0.65,
) -> list[dict]:
    """
    Validate each citation against retrieved evidence content.

    Args:
        citations:  List of {"claim": str, "source": str} from RAG assessment.
        evidence:   Retrieved evidence documents (each has "title", "content", "domain").
        threshold:  Minimum cosine similarity to consider a citation valid.

    Returns:
        List of citations with added "valid" (bool) and "validation_method" fields.
    """
    if not citations:
        return []

    results = []
    for citation in citations:
        cited_claim  = citation.get("claim", "")
        cited_source = citation.get("source", "").lower()
        status       = "unverifiable"
        method       = "none"

        # Find matching evidence document
        matching_docs = [
            e for e in evidence
            if (
                cited_source in (e.get("domain") or "").lower()
                or cited_source in (e.get("title") or "").lower()
                or (e.get("domain") or "") in cited_source
            )
        ]

        if matching_docs:
            doc = matching_docs[0]
            content = f"{doc.get('title', '')} {doc.get('content', '')}".strip()

            # 1. Exact substring check (fast)
            if cited_claim[:50].lower() in content.lower():
                status = "valid"
                method = "exact_match"

            # 2. Semantic similarity check (if embeddings available)
            elif content:
                try:
                    from app.retrieval.embeddings import embed, cosine_similarity
                    claim_vec   = embed(cited_claim[:200])
                    content_vec = embed(content[:500])
                    sim = cosine_similarity(claim_vec, content_vec)
                    if sim >= threshold:
                        status = "valid"
                        method = f"semantic_similarity_{sim:.2f}"
                    else:
                        status = "invalid"
                        method = f"semantic_similarity_{sim:.2f}"
                except Exception:
                    status = "unverifiable"
                    method = "embedding_unavailable"
        else:
            status = "unverifiable"
            method = "source_not_retrieved"

        results.append({
            **citation,
            "valid":             status == "valid",
            "validation_status": status,
            "validation_method": method,
        })

    return results


def filter_valid_citations(citations: list[dict]) -> list[dict]:
    """Return only verified citations. Invalid ones are dropped."""
    return [c for c in citations if c.get("valid", False)]


def has_sufficient_valid_citations(
    citations: list[dict],
    min_valid: int = 1,
) -> bool:
    """Check if at least min_valid citations are verified."""
    return sum(1 for c in citations if c.get("valid", False)) >= min_valid
