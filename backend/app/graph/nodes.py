"""
LangGraph Nodes — Each node is a pure function: state → updated state dict

Nodes:
  normalize_claim     → clean, detect language, hash
  run_ml              → TF-IDF / RoBERTa via ml.py
  retrieve_memory     → hybrid retrieval from fact_checks + evidence_documents
  retrieve_live       → live evidence from Brave/Tavily/NewsAPI
  rag_reason          → structured LLM reasoning over retrieved context
  detect_conflicts    → check if evidence is sufficient / signals conflict
  analyze_manipulation → manipulation + adversarial signals
  meta_decide         → combine all signals with the calibrated meta-model
  write_memory        → persist result to fact_checks table
"""
from __future__ import annotations

import hashlib
import logging
import time
from typing import Any

from app.graph.state import FactCheckState

logger = logging.getLogger(__name__)


# ── Helper ────────────────────────────────────────────────────

def _trace(state: FactCheckState, node: str) -> list[str]:
    trace = list(state.get("node_trace") or [])
    trace.append(node)
    return trace


# ── Node 1: Normalize claim ───────────────────────────────────

def normalize_claim(state: FactCheckState) -> dict:
    claim = (state.get("claim") or "").strip()
    language = "en"
    was_translated = False
    normalized = claim

    try:
        from app.analysis.multilingual import normalize_claim as _norm
        normalized, language, was_translated = _norm(claim)
    except Exception:
        pass

    claim_hash = hashlib.sha256(normalized.lower().strip().encode()).hexdigest()

    return {
        "normalized_claim": normalized,
        "language":         language,
        "was_translated":   was_translated,
        "claim_hash":       claim_hash,
        "text_len":         len(normalized),
        "node_trace":       _trace(state, "normalize_claim"),
    }


# ── Node 2: Run ML models ─────────────────────────────────────

def run_ml(state: FactCheckState) -> dict:
    claim = state.get("normalized_claim") or state.get("claim", "")
    try:
        from app.analysis.ml import run_ml_analysis
        result = run_ml_analysis(claim)
    except Exception as e:
        logger.warning("ML analysis failed in graph node: %s", e)
        result = {"fake": 0.5, "source": "default"}

    return {
        "ml_result":   result,
        "ml_score":    result.get("fake", 0.5),
        "node_trace":  _trace(state, "run_ml"),
    }


# ── Node 3: Retrieve from persistent memory ──────────────────

def retrieve_memory(state: FactCheckState, db=None) -> dict:
    if db is None:
        return {"node_trace": _trace(state, "retrieve_memory_skipped")}

    claim = state.get("normalized_claim") or state.get("claim", "")

    try:
        from app.retrieval.hybrid import retrieve_balanced_evidence
        from app.retrieval.reranker import rerank_all

        pool        = retrieve_balanced_evidence(db, claim)
        reranked    = rerank_all(claim, pool, total_k=8)
        similar     = pool.get("historical", [])

        return {
            "retrieved_claims":   similar,
            "retrieved_evidence": reranked,
            "node_trace":         _trace(state, "retrieve_memory"),
        }
    except Exception as e:
        logger.warning("Memory retrieval failed: %s", e)
        return {
            "retrieved_claims":   [],
            "retrieved_evidence": [],
            "node_trace":         _trace(state, "retrieve_memory_error"),
        }


# ── Node 4: Retrieve live evidence ───────────────────────────

def retrieve_live(state: FactCheckState) -> dict:
    claim = state.get("normalized_claim") or state.get("claim", "")

    try:
        from app.analysis.evidence import fetch_evidence
        score, urls, articles = fetch_evidence(claim)
    except Exception as e:
        logger.warning("Live evidence fetch failed: %s", e)
        score, urls, articles = None, [], []

    return {
        "live_evidence":    articles,
        "evidence_score":   score,
        "evidence_urls":    urls,
        "evidence_articles": articles,
        "node_trace":       _trace(state, "retrieve_live"),
    }


# ── Node 5: RAG reasoning ─────────────────────────────────────

def rag_reason(state: FactCheckState) -> dict:
    claim             = state.get("normalized_claim") or state.get("claim", "")
    retrieved         = state.get("retrieved_evidence", [])
    live              = state.get("live_evidence", [])
    historical        = state.get("retrieved_claims", [])

    # Build context string
    context_parts = []

    if historical:
        context_parts.append("SIMILAR HISTORICAL FACT-CHECKS:")
        for h in historical[:3]:
            context_parts.append(
                f"  Claim: {h.get('claim_text', '')[:120]}\n"
                f"  Verdict: {h.get('verdict')} (confidence: {h.get('confidence', 0):.2f})"
            )

    if retrieved:
        context_parts.append("\nRELEVANT EVIDENCE (from knowledge base):")
        for r in retrieved[:4]:
            stance = r.get("stance", "neutral")
            context_parts.append(
                f"  [{stance.upper()}] {r.get('title', r.get('claim_text', ''))[:120]}"
                f" — {r.get('domain', 'unknown')} (tier {r.get('source_tier', 4)})"
            )

    if live:
        context_parts.append("\nLIVE NEWS EVIDENCE:")
        for a in live[:4]:
            stance = a.get("stance", "neutral")
            context_parts.append(
                f"  [{stance.upper()}] {a.get('title', '')[:120]}"
                f" — {a.get('source', 'unknown')}"
            )

    rag_context = "\n".join(context_parts) if context_parts else "No relevant evidence found."

    # Structured LLM reasoning over retrieved context
    rag_assessment: dict[str, Any] = {}
    if context_parts:
        try:
            from app.rag.reasoner import reason_over_context
            rag_assessment = reason_over_context(claim, rag_context)
        except Exception as e:
            logger.debug("RAG reasoner failed: %s", e)

    return {
        "rag_context":    rag_context,
        "rag_assessment": rag_assessment,
        "node_trace":     _trace(state, "rag_reason"),
    }


# ── Node 6: Detect conflicts ──────────────────────────────────

def detect_conflicts(state: FactCheckState) -> dict:
    evidence_score = state.get("evidence_score")
    ml_score       = state.get("ml_score", 0.5)
    rag            = state.get("rag_assessment") or {}

    conflicts: list[str] = []

    # Check evidence balance
    retrieved = state.get("retrieved_evidence", [])
    if retrieved:
        n_support   = sum(1 for r in retrieved if r.get("stance") == "support")
        n_contradict= sum(1 for r in retrieved if r.get("stance") == "contradict")
        if n_support > 0 and n_contradict > 0:
            ratio = min(n_support, n_contradict) / max(n_support, n_contradict)
            if ratio > 0.5:
                conflicts.append(f"evidence_balanced: {n_support} supporting vs {n_contradict} contradicting")

    # ML vs evidence conflict
    if evidence_score is not None:
        ml_says_fake = ml_score > 0.65
        ev_says_real = evidence_score > 0.65
        if ml_says_fake and ev_says_real:
            conflicts.append("ml_evidence_conflict: ML says fake, evidence says real")

    # RAG assessment conflict
    rag_verdict = rag.get("assessment", "")
    if rag_verdict == "CONTRADICTED" and ml_score < 0.35:
        conflicts.append("rag_ml_conflict: RAG contradicted, but ML says real")

    # Evidence sufficiency check
    total_evidence = (
        len(state.get("retrieved_evidence", [])) +
        len(state.get("live_evidence", []))
    )
    evidence_sufficient = total_evidence >= 2

    needs_live_search = (
        not evidence_sufficient
        and not state.get("live_evidence")
    )

    return {
        "conflicts":          conflicts,
        "evidence_sufficient": evidence_sufficient,
        "needs_live_search":  needs_live_search,
        "node_trace":         _trace(state, "detect_conflicts"),
    }


# ── Node 7: Manipulation analysis ────────────────────────────

def analyze_manipulation(state: FactCheckState) -> dict:
    claim = state.get("normalized_claim") or state.get("claim", "")
    try:
        from app.analysis.manipulation import analyze_manipulation as _analyze
        score, signals = _analyze(claim)
    except Exception as e:
        logger.warning("Manipulation analysis failed: %s", e)
        score, signals = 0.0, []

    return {
        "manipulation_score":   score,
        "manipulation_signals": signals,
        "node_trace":           _trace(state, "analyze_manipulation"),
    }


# ── Node 8: Meta-decision ─────────────────────────────────────

def meta_decide(state: FactCheckState) -> dict:
    ml_score    = state.get("ml_score")
    ai_score    = state.get("ai_score")
    ev_score    = state.get("evidence_score")
    manip_score = state.get("manipulation_score", 0.0)
    text_len    = state.get("text_len", 0)

    # Incorporate RAG assessment into evidence score
    rag = state.get("rag_assessment") or {}
    if rag.get("confidence") is not None:
        rag_confidence = float(rag["confidence"])
        rag_verdict    = rag.get("assessment", "")
        if rag_verdict == "SUPPORTED":
            ev_score = max(ev_score or 0.5, rag_confidence)
        elif rag_verdict == "CONTRADICTED":
            ev_score = min(ev_score or 0.5, 1.0 - rag_confidence)

    try:
        from app.logic.decision import decide
        verdict, confidence = decide(
            ml_fake        = ml_score,
            ai_fake        = ai_score,
            evidence_score = ev_score,
            text_len       = text_len,
            manip_score    = manip_score,
        )
    except Exception as e:
        logger.error("Meta-decision failed: %s", e)
        verdict, confidence = "uncertain", 0.5

    explanation = state.get("ai_explanation") or rag.get("explanation") or ""

    return {
        "final_verdict":     verdict,
        "final_confidence":  confidence,
        "final_explanation": explanation,
        "node_trace":        _trace(state, "meta_decide"),
    }


# ── Node 9: Write to persistent memory ───────────────────────

def write_memory(state: FactCheckState, db=None) -> dict:
    if db is None:
        return {"node_trace": _trace(state, "write_memory_skipped")}

    verdict    = state.get("final_verdict", "uncertain")
    confidence = state.get("final_confidence", 0.5)

    # Only write if verdict is not uncertain (uncertain = insufficient data)
    if verdict == "uncertain" and confidence < 0.6:
        return {
            "memory_written": False,
            "node_trace":     _trace(state, "write_memory_skipped_uncertain"),
        }

    try:
        from app.retrieval.vector_store import upsert_fact_check, upsert_evidence, link_evidence
        import os

        fc = upsert_fact_check(
            db,
            claim_hash        = state.get("claim_hash", ""),
            claim_text        = state.get("normalized_claim") or state.get("claim", ""),
            verdict           = verdict,
            confidence        = confidence,
            tfidf_score       = state.get("ml_score"),
            llm_verdict       = (
                "fake" if (state.get("ai_score") or 0.5) > 0.5 else "real"
            ) if state.get("ai_score") is not None else None,
            llm_confidence    = state.get("ai_score"),
            evidence_score    = state.get("evidence_score"),
            manipulation_score= state.get("manipulation_score"),
            rag_assessment    = state.get("rag_assessment"),
            language          = state.get("language", "en"),
            model_version     = os.getenv("MODEL_VERSION", "2.6.1"),
        )

        # Persist live evidence articles as EvidenceDocument records
        for article in (state.get("evidence_articles") or [])[:5]:
            url = article.get("url", "")
            if not url:
                continue
            try:
                doc = upsert_evidence(
                    db,
                    url         = url,
                    title       = article.get("title"),
                    domain      = article.get("source", ""),
                    stance      = article.get("stance"),
                    trust_score = article.get("trust_score", 0.5),
                    source_tier = 3,  # News article default
                    source_type = "news",
                )
                link_evidence(
                    db,
                    fact_check_id        = fc.id,
                    evidence_document_id = doc.id,
                    relevance_score      = article.get("relevance_score"),
                    stance               = article.get("stance"),
                )
            except Exception as e:
                logger.debug("Evidence doc write failed: %s", e)

        return {
            "fact_check_id": fc.id,
            "memory_written": True,
            "node_trace":    _trace(state, "write_memory"),
        }

    except Exception as e:
        logger.warning("Memory write failed: %s", e)
        return {
            "memory_written": False,
            "node_trace":    _trace(state, "write_memory_error"),
        }
