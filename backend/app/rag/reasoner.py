"""
RAG Reasoner

Sends retrieved context + claim to an LLM for structured evidence-grounded
reasoning. The LLM does NOT classify the claim from memory — it reasons
over the specific retrieved evidence. This is genuine RAG, not retrieval-only.

Output schema (from plan.md section 11):
{
  "assessment":            "SUPPORTED" | "CONTRADICTED" | "INSUFFICIENT" | "UNCERTAIN",
  "confidence":            0.0–1.0,
  "supporting_evidence":   [str],
  "contradicting_evidence":[str],
  "key_facts":             [str],
  "uncertainty":           [str],
  "citations":             [{"claim": str, "source": str}]
}
"""
from __future__ import annotations

import json
import logging
import re

logger = logging.getLogger(__name__)

_RAG_SYSTEM_PROMPT = """You are a professional fact-checker. You will be given:
1. A CLAIM to evaluate
2. RETRIEVED EVIDENCE from a knowledge base

Your task is to reason over the evidence and produce a structured assessment.

Rules:
- Base your assessment ONLY on the provided evidence, not your training data
- If the evidence is insufficient, say INSUFFICIENT — do NOT guess
- Cite specific sources using the format: [Source: domain or title]
- Be precise and factual — no speculation, no hedging language
- Return ONLY valid JSON, no markdown fences

Output JSON schema (strictly follow):
{
  "assessment": "SUPPORTED" | "CONTRADICTED" | "INSUFFICIENT" | "UNCERTAIN",
  "confidence": <float 0.0-1.0>,
  "supporting_evidence": ["<specific fact from evidence>"],
  "contradicting_evidence": ["<specific fact from evidence>"],
  "key_facts": ["<important facts relevant to the claim>"],
  "uncertainty": ["<what is unclear or contested>"],
  "citations": [{"claim": "<specific claim>", "source": "<source identifier>"}],
  "explanation": "<2-3 sentence factual summary>"
}"""

_RAG_USER_TEMPLATE = """CLAIM: {claim}

RETRIEVED EVIDENCE:
{context}

Provide your structured assessment based solely on the evidence above."""


def reason_over_context(claim: str, context: str) -> dict:
    """
    Run RAG reasoning: claim + retrieved context → structured assessment.

    Tries Groq first (fastest), then Gemini, then Cerebras.
    Returns empty dict if all providers fail (caller handles gracefully).
    """
    if not context or context == "No relevant evidence found.":
        return {
            "assessment":  "INSUFFICIENT",
            "confidence":  0.0,
            "explanation": "No relevant evidence was retrieved.",
        }

    prompt = _RAG_USER_TEMPLATE.format(
        claim   = claim[:400],
        context = context[:3000],
    )
    messages = [{"role": "user", "content": prompt}]

    try:
        from app.analysis.chat import _call_openai_compat, _call_gemini, _get_keys, _first_success

        keys = _get_keys()
        fns  = []

        if keys.get("groq"):
            fns.append(("Groq", lambda: _call_openai_compat(
                "https://api.groq.com/openai/v1/chat/completions",
                keys["groq"], "llama-3.3-70b-versatile",
                [{"role": "system", "content": _RAG_SYSTEM_PROMPT}] + messages,
                max_tokens=600, temperature=0.1,
            )))
        if keys.get("gemini"):
            fns.append(("Gemini", lambda: _call_gemini(
                [{"role": "system", "content": _RAG_SYSTEM_PROMPT}] + messages,
                max_tokens=600, temperature=0.1,
            )))
        if keys.get("cerebras"):
            fns.append(("Cerebras", lambda: _call_openai_compat(
                "https://api.cerebras.ai/v1/chat/completions",
                keys["cerebras"], "llama3.1-8b",
                [{"role": "system", "content": _RAG_SYSTEM_PROMPT}] + messages,
                max_tokens=600, temperature=0.1,
            )))

        if not fns:
            return {}

        raw = _first_success(fns)
        return _parse_rag_response(raw)

    except Exception as e:
        logger.warning("RAG reasoning failed: %s", e)
        return {}


def _parse_rag_response(raw: str) -> dict:
    """Parse JSON response from the LLM, handle minor formatting issues."""
    try:
        raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            # Normalise assessment value
            assessment = data.get("assessment", "UNCERTAIN").upper()
            if assessment not in {"SUPPORTED", "CONTRADICTED", "INSUFFICIENT", "UNCERTAIN"}:
                assessment = "UNCERTAIN"
            data["assessment"] = assessment
            return data
    except Exception as e:
        logger.debug("RAG response parse failed: %s — raw: %s", e, raw[:200])
    return {}
