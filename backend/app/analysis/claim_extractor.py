# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
"""
Claim Extraction

For long inputs (articles, paragraphs), extracts atomic verifiable claims
instead of sending the whole blob to the fact-checker.

Short inputs (<= 200 chars) are returned as-is (already a single claim).
Long inputs use sentence splitting + LLM extraction.

Returns: list of claim strings (1–5 max)
"""

import re
import os
import requests
from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(_env_path)

# Threshold: inputs shorter than this are treated as a single claim
SHORT_THRESHOLD = 220

EXTRACT_PROMPT = """Extract the key verifiable factual claims from the text below.
Return ONLY a numbered list of short, atomic claims (one fact per line, max 5).
Each claim must be independently verifiable. Ignore opinions and questions.
Do NOT include explanations or commentary.

Text: {text}

Claims:"""


def _split_sentences(text: str) -> list:
    """Simple sentence splitter — no NLTK dependency."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def _call_llm_extract(text: str) -> list:
    """Use first available LLM to extract claims (dynamic model discovery)."""
    from app.analysis.chat import _call_openai_compat, _call_gemini, _get_keys, _first_success
    from app.analysis.ai_config import discover_cerebras_models, discover_groq_models, CEREBRAS_URL, GROQ_URL
    
    keys = _get_keys()
    prompt = EXTRACT_PROMPT.format(text=text[:1500])
    messages = [{"role": "user", "content": prompt}]

    fns = []
    
    # Try Cerebras with dynamic model discovery
    if keys.get("cerebras"):
        cerebras_models = discover_cerebras_models(keys["cerebras"])
        for model in cerebras_models[:2]:
            try:
                fns.append((f"Cerebras-{model}", lambda m=model: _call_openai_compat(
                    CEREBRAS_URL,
                    keys["cerebras"], m, messages, max_tokens=200, temperature=0
                )))
            except Exception:
                continue
                
    # Try Groq with dynamic model discovery
    if keys.get("groq"):
        groq_models = discover_groq_models(keys["groq"])
        for model in groq_models[:2]:
            try:
                fns.append((f"Groq-{model}", lambda m=model: _call_openai_compat(
                    GROQ_URL,
                    keys["groq"], m, messages, max_tokens=200, temperature=0
                )))
            except Exception:
                continue
                
    # Try Gemini
    if keys.get("gemini"):
        fns.append(("Gemini", lambda: _call_gemini(messages, max_tokens=200, temperature=0)))

    if not fns:
        return []

    try:
        raw = _first_success(fns)
        return _parse_numbered_list(raw)
    except Exception:
        return []


def _parse_numbered_list(text: str) -> list:
    """Parse '1. claim\n2. claim' format into a list."""
    lines = text.strip().splitlines()
    claims = []
    for line in lines:
        # Strip leading numbers, bullets, dashes
        clean = re.sub(r"^[\d\.\-\*\•]+\s*", "", line).strip()
        if len(clean) > 15:
            claims.append(clean)
    return claims[:5]


def extract_claims(text: str) -> list:
    """
    Main entry point.

    Short text  → [text]  (single claim, no processing)
    Long text   → LLM extraction → list of atomic claims
    Fallback    → first 3 sentences as claims
    """
    text = text.strip()

    if len(text) <= SHORT_THRESHOLD:
        return [text]

    # Try LLM extraction
    claims = _call_llm_extract(text)
    if claims:
        return claims

    # Fallback: use first 3 sentences
    sentences = _split_sentences(text)
    return sentences[:3] if sentences else [text[:SHORT_THRESHOLD]]
