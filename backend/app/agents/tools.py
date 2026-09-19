"""
Agent Tools (Phase 7)

Structured tool definitions for the agentic fact-checking workflow.
Each tool returns a typed dict — never a plain string.

Tools exposed (from docs/plan.md section 15):
  search_news(claim)
  retrieve_similar_claims(claim)
  retrieve_evidence(claim, stance)
  get_source_metadata(url)
  run_ml_analysis(claim)
  analyze_manipulation(claim)
"""
from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def search_news(claim: str, max_results: int = 8) -> dict:
    """
    Search for recent news articles about the claim.
    Returns structured evidence, not raw text.
    """
    try:
        from app.analysis.evidence import fetch_evidence
        score, urls, articles = fetch_evidence(claim)
        return {
            "tool":           "search_news",
            "claim":          claim[:200],
            "evidence_score": score,
            "article_count":  len(articles),
            "articles": [
                {
                    "title":       a.get("title", ""),
                    "url":         a.get("url", ""),
                    "source":      a.get("source", ""),
                    "stance":      a.get("stance", "neutral"),
                    "trust_score": a.get("trust_score", 0.5),
                }
                for a in articles[:max_results]
            ],
        }
    except Exception as e:
        logger.warning("search_news tool failed: %s", e)
        return {"tool": "search_news", "error": str(e), "articles": []}


def retrieve_similar_claims(claim: str, db=None, top_k: int = 5) -> dict:
    """
    Find similar historical fact-checks in persistent memory.
    Uses hybrid retrieval (BM25 + vector).
    """
    if db is None:
        return {"tool": "retrieve_similar_claims", "claims": [], "note": "no_db"}
    try:
        from app.retrieval.hybrid import retrieve_similar_claims as _retrieve
        results = _retrieve(db, claim, top_k=top_k)
        return {
            "tool":   "retrieve_similar_claims",
            "claim":  claim[:200],
            "count":  len(results),
            "claims": [
                {
                    "claim_text":          r.get("claim_text", "")[:150],
                    "verdict":             r.get("verdict"),
                    "confidence":          r.get("confidence"),
                    "verification_status": r.get("verification_status"),
                    "similarity":          r.get("rrf_score", r.get("similarity", 0)),
                }
                for r in results
            ],
        }
    except Exception as e:
        logger.warning("retrieve_similar_claims tool failed: %s", e)
        return {"tool": "retrieve_similar_claims", "error": str(e), "claims": []}


def retrieve_evidence(
    claim:  str,
    db:     None       = None,
    stance: Optional[str] = None,
    top_k:  int        = 6,
) -> dict:
    """
    Retrieve relevant evidence documents from the persistent corpus.
    Optionally filter by stance: 'support' | 'contradict' | 'neutral'
    """
    if db is None:
        return {"tool": "retrieve_evidence", "documents": [], "note": "no_db"}
    try:
        from app.retrieval.hybrid import retrieve_evidence as _retrieve
        results = _retrieve(db, claim, top_k=top_k, stance=stance)
        return {
            "tool":      "retrieve_evidence",
            "claim":     claim[:200],
            "stance":    stance,
            "count":     len(results),
            "documents": [
                {
                    "title":        r.get("title", "")[:120],
                    "url":          r.get("url", ""),
                    "domain":       r.get("domain", ""),
                    "stance":       r.get("stance"),
                    "trust_score":  r.get("trust_score"),
                    "source_tier":  r.get("source_tier"),
                    "published_at": r.get("published_at"),
                    "relevance":    r.get("rrf_score", r.get("similarity", 0)),
                }
                for r in results
            ],
        }
    except Exception as e:
        logger.warning("retrieve_evidence tool failed: %s", e)
        return {"tool": "retrieve_evidence", "error": str(e), "documents": []}


def get_source_metadata(url: str) -> dict:
    """
    Return trust score, bias label, and tier for a given URL/domain.
    """
    try:
        from app.analysis.credibility    import get_trust_score, get_trust_label
        from app.analysis.publisher_bias import get_bias_label, get_bias_weight
        from urllib.parse import urlparse

        domain = urlparse(url).netloc.replace("www.", "")
        return {
            "tool":         "get_source_metadata",
            "url":          url,
            "domain":       domain,
            "trust_score":  get_trust_score(url),
            "trust_label":  get_trust_label(url),
            "bias_label":   get_bias_label(url),
            "bias_weight":  get_bias_weight(url),
        }
    except Exception as e:
        logger.warning("get_source_metadata tool failed: %s", e)
        return {"tool": "get_source_metadata", "url": url, "error": str(e)}


def run_ml_analysis(claim: str) -> dict:
    """
    Run the ML analysis pipeline (TF-IDF / RoBERTa) for the claim.
    """
    try:
        from app.analysis.ml import run_ml_analysis as _run
        result = _run(claim)
        return {
            "tool":        "run_ml_analysis",
            "claim":       claim[:200],
            "fake_score":  result.get("fake", 0.5),
            "source":      result.get("source", "unknown"),
        }
    except Exception as e:
        logger.warning("run_ml_analysis tool failed: %s", e)
        return {"tool": "run_ml_analysis", "fake_score": 0.5, "error": str(e)}


def analyze_manipulation(claim: str) -> dict:
    """
    Detect manipulation techniques, conspiracy language, emotional appeals.
    """
    try:
        from app.analysis.manipulation import analyze_manipulation as _analyze
        score, signals = _analyze(claim)
        return {
            "tool":     "analyze_manipulation",
            "claim":    claim[:200],
            "score":    score,
            "signals":  signals,
            "flagged":  score > 0.4,
        }
    except Exception as e:
        logger.warning("analyze_manipulation tool failed: %s", e)
        return {"tool": "analyze_manipulation", "score": 0.0, "signals": [], "error": str(e)}


# ── Tool registry ─────────────────────────────────────────────

ALL_TOOLS = {
    "search_news":             search_news,
    "retrieve_similar_claims": retrieve_similar_claims,
    "retrieve_evidence":       retrieve_evidence,
    "get_source_metadata":     get_source_metadata,
    "run_ml_analysis":         run_ml_analysis,
    "analyze_manipulation":    analyze_manipulation,
}


def call_tool(name: str, **kwargs) -> dict:
    """Dispatch a tool call by name. Returns error dict if tool not found."""
    fn = ALL_TOOLS.get(name)
    if fn is None:
        return {"tool": name, "error": f"Unknown tool: {name}"}
    try:
        return fn(**kwargs)
    except Exception as e:
        logger.error("Tool %s raised: %s", name, e)
        return {"tool": name, "error": str(e)}
