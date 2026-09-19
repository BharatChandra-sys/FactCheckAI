"""
LangGraph Shared State — FactCheckState

This is the single shared state object that flows through the entire
fact-checking workflow graph. Every node reads from and writes to this state.

Design principles (from docs/plan.md):
- State is immutable within a node — nodes return updated state dicts
- All signals are optional so nodes can handle partial state gracefully
- The final_verdict field is only set by the meta-decision node
"""
from __future__ import annotations

from typing import Optional, TypedDict


class FactCheckState(TypedDict, total=False):
    # ── Input ──────────────────────────────────────────────────
    claim:             str           # Original user claim
    normalized_claim:  str           # Language-normalized, cleaned claim
    language:          str           # Detected language
    was_translated:    bool          # True if non-English input was translated
    claim_hash:        str           # SHA-256 of normalized claim
    text_len:          int           # Char length of normalized claim

    # ── ML signals ─────────────────────────────────────────────
    ml_result:         dict          # {"fake": float, "source": str}
    ml_score:          float         # ml_result["fake"]

    # ── LLM ensemble signals ───────────────────────────────────
    ai_result:         tuple         # (score: float, explanation: str)
    ai_score:          float
    ai_explanation:    str

    # ── Evidence signals ───────────────────────────────────────
    live_evidence:     list[dict]    # From Brave/Tavily/NewsAPI (real-time)
    evidence_score:    float         # Weighted consistency score
    evidence_urls:     list[str]
    evidence_articles: list[dict]

    # ── RAG memory retrieval ───────────────────────────────────
    retrieved_claims:    list[dict]  # Similar historical fact-checks
    retrieved_evidence:  list[dict]  # Relevant evidence documents (reranked)
    rag_context:         str         # Formatted context string for LLM
    rag_assessment:      dict        # Structured output from RAG reasoner

    # ── Manipulation ───────────────────────────────────────────
    manipulation_score:  float
    manipulation_signals: list[str]

    # ── Conflict / uncertainty ────────────────────────────────
    conflicts:           list[str]   # List of identified conflicts
    needs_live_search:   bool        # True if retrieval was insufficient
    evidence_sufficient: bool        # True if enough evidence to decide

    # ── Final decision ─────────────────────────────────────────
    final_verdict:     str           # real / fake / uncertain
    final_confidence:  float
    final_explanation: str

    # ── Memory write ───────────────────────────────────────────
    fact_check_id:     int           # ID of the FactCheck record written
    memory_written:    bool

    # ── Metadata ───────────────────────────────────────────────
    session_id:        Optional[int]
    user_id:           Optional[int]
    latency_ms:        int
    node_trace:        list[str]     # List of nodes executed (for observability)
