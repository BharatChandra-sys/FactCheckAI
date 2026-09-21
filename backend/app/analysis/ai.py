# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
from __future__ import annotations

import os
import re
import json
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FutureTimeoutError
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

# Module-level thread pool — created once, reused for every request
# Avoids the 20-50ms overhead of spawning/joining a pool per call
_POOL = ThreadPoolExecutor(max_workers=5, thread_name_prefix="ai-provider")

CEREBRAS_URL  = "https://api.cerebras.ai/v1/chat/completions"
GROQ_URL      = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_URL    = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"
# MiniMax M2.7 — 229B MoE, recursive self-improvement, SOTA real-world engineering
# OpenAI-compatible endpoint. Falls back to M2.7-highspeed for lower latency.
MINIMAX_URL   = "https://api.minimax.io/v1/chat/completions"
# Gemma 4 31B-it — Google's latest open model, 256K context, reasoning mode
# Uses the same Google AI Studio key as Gemini (GEMINI_API_KEY)
GEMMA4_MODEL  = "gemma-4-31B-it"
# OpenRouter — FREE tier with multiple models (Google Gemma 2 9B, Meta Llama 3.1 8B, etc)
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ── Structured JSON prompt ────────────────────────────────────
SYSTEM_PROMPT = """You are a professional fact-checker. Analyze the given claim and respond with ONLY a JSON object — no markdown, no extra text.

JSON format:
{
  "verdict": "fake" | "real" | "uncertain",
  "confidence": <float 0.0–1.0>,
  "explanation": "<3–5 sentence factual explanation>"
}

Rules:
- verdict must be exactly one of: fake, real, uncertain
- confidence is how certain you are (0.0 = no idea, 1.0 = certain)
- explanation must be factual, calm, and natural — no AI disclaimers
- Do NOT include markdown fences or any text outside the JSON"""

# ── Cached API keys and models (lazy init) ──────────────────
_KEYS: Optional[dict] = None
_MODEL_CACHE: dict = {}  # Cache discovered models: {provider: [model_list]}
_CACHE_TTL = 3600  # Cache models for 1 hour


def _get_keys() -> dict:
    global _KEYS
    if _KEYS is None:
        _KEYS = {
            "cerebras":     os.getenv("CEREBRAS_API_KEY"),
            "groq":         os.getenv("GROQ_API_KEY"),
            "gemini":       os.getenv("GEMINI_API_KEY"),
            "minimax":      os.getenv("MINIMAX_API_KEY"),
            "openrouter":   os.getenv("OPENROUTER_API_KEY"),
            "gemini_proxy": os.getenv("GEMINI_WEB2API_URL", "https://factcheckai-gemini-proxy.onrender.com"),
        }
    return _KEYS


def _discover_models(provider: str, api_url: str, api_key: str, timeout: int = 10) -> List[str]:
    """
    Dynamically discover available models from a provider.
    Returns list of model IDs, caching results for 1 hour.
    """
    import time
    
    # Check cache first
    cache_key = f"{provider}_{int(time.time() // _CACHE_TTL)}"
    if cache_key in _MODEL_CACHE:
        return _MODEL_CACHE[cache_key]
    
    models = []
    
    try:
        if provider == "groq":
            # Groq: GET /openai/v1/models
            r = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=timeout
            )
            if r.status_code == 200:
                models = [m["id"] for m in r.json().get("data", [])]
                # Filter to chat models only
                models = [m for m in models if not any(x in m.lower() for x in ["whisper", "vision", "embed"])]
        
        elif provider == "cerebras":
            # Cerebras: GET /v1/models
            r = requests.get(
                "https://api.cerebras.ai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=timeout
            )
            if r.status_code == 200:
                models = [m["id"] for m in r.json().get("data", [])]
        
        elif provider == "openrouter":
            # OpenRouter: GET /api/v1/models
            r = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=timeout
            )
            if r.status_code == 200:
                # Filter to free models only
                all_models = r.json().get("data", [])
                models = [m["id"] for m in all_models if m.get("pricing", {}).get("prompt", "0") == "0"]
        
        elif provider == "gemini":
            # Gemini: GET /v1beta/models
            r = requests.get(
                "https://generativelanguage.googleapis.com/v1beta/models",
                params={"key": api_key},
                timeout=timeout
            )
            if r.status_code == 200:
                all_models = r.json().get("models", [])
                # Filter to generateContent models only
                models = [m["name"].replace("models/", "") for m in all_models 
                         if "generateContent" in m.get("supportedGenerationMethods", [])]
        
        elif provider == "gemini_proxy":
            # Gemini Proxy: GET /v1/models
            r = requests.get(
                f"{api_url}/v1/models",
                timeout=timeout
            )
            if r.status_code == 200:
                models = [m["id"] for m in r.json().get("data", [])]
        
        # Cache the discovered models
        if models:
            _MODEL_CACHE[cache_key] = models
            logger.info(f"Discovered {len(models)} models from {provider}: {models[:3]}...")
    
    except Exception as e:
        logger.warning(f"Model discovery failed for {provider}: {e}")
    
    return models


def _parse_structured(raw: str) -> dict:
    """Extract JSON from LLM response, handling minor formatting issues."""
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError(f"No JSON found in response: {raw[:200]}")


def _verdict_to_score(verdict: str) -> float:
    """Convert structured verdict to a fake probability score."""
    v = verdict.lower().strip()
    if v == "fake":      return 0.85
    if v == "real":      return 0.15
    if v == "uncertain": return 0.5
    return 0.5


def _call_openai_compat(url: str, key: str, model: str, text: str,
                         timeout: int = 12, max_tokens: int = 500) -> dict:
    """Shared helper for OpenAI-compatible chat completion endpoints."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Claim: {text}"}
        ],
        "temperature": 0.1,
        "max_tokens": max_tokens,
    }
    
    # Disable reasoning mode for reasoning models to avoid token waste
    if "gpt-oss" in model or "qwen" in model:
        payload["reasoning_effort"] = "none"
    
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    
    # Log failures for debugging
    if r.status_code != 200:
        error_detail = r.text[:300]
        logger.warning("%s failed: %s %s", model, r.status_code, error_detail)
        
        # Check for specific error types
        if r.status_code == 400:
            # Check if model requires terms acceptance
            if "terms" in error_detail.lower() or "accept" in error_detail.lower():
                raise ValueError(f"Model {model} requires terms acceptance")
        elif r.status_code == 402:
            raise ValueError(f"Model {model} requires payment (quota exhausted)")
        elif r.status_code == 413:
            raise ValueError(f"Model {model} payload too large")
        elif r.status_code == 404:
            raise ValueError(f"Model {model} not found or unavailable")
    
    r.raise_for_status()
    raw = r.json()["choices"][0]["message"]["content"].strip()
    return _parse_structured(raw)


def _call_cerebras(text: str) -> dict:
    key = _get_keys()["cerebras"]
    if not key:
        raise ValueError("Cerebras API key missing")
    
    # Try to discover available models
    models = _discover_models("cerebras", CEREBRAS_URL, key)
    
    # Fallback to known models if discovery fails
    if not models:
        models = ["llama-3.3-70b-specdec", "llama-3.1-70b-versatile", "llama-3.1-8b-instant"]
    
    # Try each model until one works
    for model in models:
        try:
            return _call_openai_compat(CEREBRAS_URL, key, model, text)
        except Exception as e:
            logger.debug(f"Cerebras {model} failed: {e}")
            continue
    
    raise ValueError("All Cerebras models failed")


def _call_groq(text: str) -> dict:
    key = _get_keys()["groq"]
    if not key:
        raise ValueError("Groq API key missing")
    
    # Try to discover available models
    models = _discover_models("groq", GROQ_URL, key)
    
    # Fallback to known models if discovery fails
    if not models:
        models = ["llama-3.3-70b-specdec", "llama-3.1-70b-versatile", "gemma2-9b-it"]
    
    # Try each model until one works
    for model in models:
        try:
            return _call_openai_compat(GROQ_URL, key, model, text)
        except Exception as e:
            logger.debug(f"Groq {model} failed: {e}")
            continue
    
    raise ValueError("All Groq models failed")


def _call_gemini(text: str) -> dict:
    """
    Gemini via web2api proxy (supports AQ. session tokens) OR direct API.
    Automatically discovers available models.
    """
    key = _get_keys()["gemini"]
    proxy_url = _get_keys()["gemini_proxy"]
    
    if not key:
        raise ValueError("Gemini API key missing")
    
    # Try web2api proxy first (supports AQ. tokens + anonymous)
    if proxy_url:
        try:
            # Discover available models from proxy
            models = _discover_models("gemini_proxy", proxy_url, "")
            if not models:
                models = ["gemini-3.5-flash", "gemini-3.6-flash", "gemini-3.7-flash"]
            
            for model in models[:3]:  # Try first 3 models
                try:
                    r = requests.post(
                        f"{proxy_url}/v1/chat/completions",
                        headers={"Content-Type": "application/json"},
                        json={
                            "model": model,
                            "messages": [
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": f"Claim: {text}"}
                            ],
                            "temperature": 0.1,
                            "max_tokens": 300
                        },
                        timeout=15
                    )
                    if r.status_code == 200:
                        raw = r.json()["choices"][0]["message"]["content"].strip()
                        return _parse_structured(raw)
                    logger.debug(f"Proxy {model} returned {r.status_code}")
                except Exception as e:
                    logger.debug(f"Proxy {model} failed: {e}")
                    continue
        except Exception as e:
            logger.warning(f"Gemini proxy error: {e}")
    
    # Fallback to direct API (for AIzaSy keys only)
    if not key.startswith("AQ."):
        # Discover available models
        models = _discover_models("gemini", "", key)
        if not models:
            models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
        
        prompt = f"{SYSTEM_PROMPT}\n\nClaim: {text}"
        
        for model in models[:3]:  # Try first 3 models
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
                r = requests.post(
                    f"{url}?key={key}",
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 300}
                    },
                    timeout=12
                )
                if r.status_code == 200:
                    raw = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return _parse_structured(raw)
                logger.debug(f"Gemini {model} returned {r.status_code}")
            except Exception as e:
                logger.debug(f"Gemini {model} failed: {e}")
                continue
    
    raise ValueError("All Gemini models failed")


def _call_minimax(text: str) -> dict:
    """
    MiniMax M2.7 — 229B MoE model, recursive self-improvement, SOTA real-world engineering.
    OpenAI-compatible endpoint at api.minimax.io.
    Falls back to MiniMax-M2.7-highspeed for lower latency if the flagship times out.
    """
    key = _get_keys()["minimax"]
    if not key:
        raise ValueError("MiniMax API key missing")

    for model in ["MiniMax-M2.7", "MiniMax-M2.7-highspeed"]:
        try:
            return _call_openai_compat(MINIMAX_URL, key, model, text,
                                       timeout=20, max_tokens=500)
        except Exception:
            continue
    raise ValueError("MiniMax M2.7 and M2.7-highspeed both failed")


def _call_gemma4(text: str) -> dict:
    """
    Google Gemma 4 31B-it — 256K context, multimodal, reasoning mode (April 2026).
    Uses the same Google AI Studio key as Gemini (GEMINI_API_KEY).
    Superior multilingual understanding and nuanced fact-checking.
    Falls back through model chain if a specific version isn't available yet on the API.
    """
    key = _get_keys()["gemini"]
    if not key:
        raise ValueError("Gemini/Gemma API key missing")
    prompt = f"{SYSTEM_PROMPT}\n\nClaim: {text}"
    # Try newest Gemma 4 first, then Gemma 3 27B, then Gemini 3.5 Flash (current as of Sept 2026)
    for model in ["gemma-4-31b-it", "gemma-3-27b-it", "gemini-3.5-flash"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            r = requests.post(
                f"{url}?key={key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.1,
                        "maxOutputTokens": 400,
                    }
                },
                timeout=15
            )
            if r.status_code != 200:
                logger.warning("Gemma/Gemini model %s failed: %s", model, r.status_code)
                continue
            r.raise_for_status()
            raw = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            return _parse_structured(raw)
        except Exception:
            continue
    raise ValueError("Gemma 4 31B / Gemma 3 27B / Gemini 3.5 Flash all failed")


def _call_openrouter(text: str) -> dict:
    """
    OpenRouter — FREE tier with access to multiple free models.
    Dynamically discovers available free models.
    """
    key = _get_keys()["openrouter"]
    if not key:
        raise ValueError("OpenRouter API key missing")
    
    # Discover free models
    models = _discover_models("openrouter", OPENROUTER_URL, key)
    
    # Fallback to known free models if discovery fails
    if not models:
        models = ["google/gemma-2-9b-it:free", "meta-llama/llama-3-8b-instruct:free", "mistralai/mistral-7b-instruct:free"]
    
    # Try each model until one works
    for model in models[:5]:  # Try first 5 free models
        try:
            return _call_openai_compat(OPENROUTER_URL, key, model, text)
        except Exception as e:
            logger.debug(f"OpenRouter {model} failed: {e}")
            continue
    
    raise ValueError("All OpenRouter free models failed")


def _call_huggingface(text: str) -> dict:
    """
    HuggingFace Inference API — 100% FREE, works without API key for public models.
    Uses Meta Llama 3.2 3B Instruct (small but capable).
    Optional: Get token at https://huggingface.co/settings/tokens for higher rate limits.
    """
    token = _get_keys().get("huggingface", "")
    prompt = f"{SYSTEM_PROMPT}\n\nClaim: {text}"
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        r = requests.post(
            HUGGINGFACE_URL,
            headers=headers,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 300, "temperature": 0.1}},
            timeout=20  # HF can be slow on first request (model loading)
        )
        r.raise_for_status()
        raw = r.json()[0]["generated_text"]
        # Extract only the model's response (remove the prompt)
        if prompt in raw:
            raw = raw.replace(prompt, "").strip()
        return _parse_structured(raw)
    except Exception as e:
        raise ValueError(f"HuggingFace inference failed: {str(e)}")


def _ensemble_vote(results: List[dict]) -> dict:
    """
    Weighted ensemble voting across multiple LLM verdicts.
    
    Weights by model capability tier:
    - MiniMax M2.7 (229B reasoning): 2.5x
    - Gemma 4 31B (reasoning mode): 2.0x
    - OpenRouter Gemma 2 9B: 1.3x
    - Gemini 2.0 Flash: 1.2x
    - Groq / Cerebras (8B models): 1.0x
    
    Returns the consensus verdict with blended confidence and
    the explanation from the highest-weighted agreeing model.
    """
    if not results:
        return {"verdict": "uncertain", "confidence": 0.5, "explanation": ""}
    if len(results) == 1:
        return results[0]

    weights = {
        "minimax":    2.5,   # MiniMax M2.7 — 229B, SOTA real-world engineering
        "gemma4":     2.0,   # Gemma 4 31B — 256K ctx, reasoning mode
        "openrouter": 1.3,   # OpenRouter Gemma 2 9B — FREE
        "gemini":     1.2,   # Gemini 2.0 Flash
        "groq":       1.0,   # Llama 3 8B via Groq
        "cerebras":   1.0,   # Llama 3.1 8B via Cerebras
    }

    vote_scores = {"fake": 0.0, "real": 0.0, "uncertain": 0.0}
    total_weight = 0.0
    best_explanation = ""
    best_weight = 0.0

    for r in results:
        v = r.get("verdict", "uncertain").lower()
        conf = float(r.get("confidence", 0.5))
        src = r.get("_source", "groq")
        w = weights.get(src, 1.0) * conf  # weight by model tier × confidence
        vote_scores[v] = vote_scores.get(v, 0.0) + w
        total_weight += w
        if w > best_weight and r.get("explanation"):
            best_weight = w
            best_explanation = r["explanation"]

    winner = max(vote_scores, key=vote_scores.get)
    winner_weight = vote_scores[winner]
    ensemble_confidence = (winner_weight / total_weight) if total_weight > 0 else 0.5
    # Clamp to [0.3, 0.97] — never be overconfident or underconfident
    ensemble_confidence = max(0.3, min(0.97, ensemble_confidence))

    return {
        "verdict": winner,
        "confidence": ensemble_confidence,
        "explanation": best_explanation,
    }


def _run_all_parallel(text: str):
    """
    Run all available providers in parallel using the module-level thread pool.
    Each provider has a 25-second wall-clock timeout to prevent hung providers
    from blocking the entire pipeline.
    """
    keys = _get_keys()
    providers = []

    # Add free providers (prioritize those that work)
    if keys["openrouter"]:
        providers.append(("openrouter", _call_openrouter))
    if keys["cerebras"]:
        providers.append(("cerebras", _call_cerebras))
    if keys["groq"]:
        providers.append(("groq", _call_groq))
    if keys["gemini"]:
        providers.append(("gemini", _call_gemini))
        providers.append(("gemma4", _call_gemma4))
    if keys["minimax"]:
        providers.append(("minimax", _call_minimax))

    if not providers:
        return [], {"all": "No API keys configured"}

    successes = []
    errors = {}

    # Submit to module-level pool (no create/destroy overhead)
    futures = {_POOL.submit(fn, text): name for name, fn in providers}

    # as_completed with 25s total wall-clock timeout
    try:
        for future in as_completed(futures, timeout=25):
            name = futures[future]
            try:
                result = future.result()
                result["_source"] = name
                successes.append(result)
            except Exception as e:
                errors[name] = str(e)
    except FutureTimeoutError:
        # Cancel any still-running futures
        for future, name in futures.items():
            if not future.done():
                future.cancel()
                errors[name] = "timeout"
        logger.warning("AI providers timed out: %s", list(errors.keys()))

    return successes, errors


def run_ai_analysis(text: str):
    """
    Runs all configured LLM providers in parallel (Cerebras, Groq, Gemini,
    Gemma 4 31B-it, MiniMax M2.7) and returns an ensemble-voted verdict.

    If NO AI providers are available, falls back to rule-based analysis.

    Returns: (ai_fake_score: float | None, explanation: str)
    """
    # Try cache first
    try:
        from app.cache import partial_cache
        cached = partial_cache.get_ai_score(text)
        if cached is not None:
            logger.debug("AI analysis cache hit")
            return cached.get("score"), cached.get("explanation", "")
    except Exception as e:
        logger.debug("Cache lookup failed: %s", e)

    successes, errors = _run_all_parallel(text)

    # If AI providers available, use them
    if successes:
        ensemble = _ensemble_vote(successes)
        verdict = ensemble.get("verdict", "uncertain")
        llm_conf = float(ensemble.get("confidence", 0.5))
        explanation = ensemble.get("explanation", "")

        # Convert verdict → fake probability score
        score = _verdict_to_score(verdict)
        if verdict == "fake":
            score = max(score, llm_conf * 0.95)
        elif verdict == "real":
            score = min(score, 1.0 - llm_conf * 0.95)

        logger.info(
            "AI ensemble: verdict=%s conf=%.2f score=%.3f providers=%s errors=%s",
            verdict, llm_conf, score,
            [r.get("_source") for r in successes],
            list(errors.keys()) if errors else "none"
        )

        # Cache the result
        try:
            from app.cache import partial_cache
            partial_cache.set_ai_score(text, score, explanation)
        except Exception as e:
            logger.debug("Cache set failed: %s", e)

        return score, explanation

    # FALLBACK: NO AI PROVIDERS AVAILABLE
    # Use rule-based analysis as fallback
    logger.warning("No AI providers available, using rule-based fallback")
    
    # Simple rule-based fake news indicators
    text_lower = text.lower()
    fake_score = 0.5  # Start neutral
    indicators = []
    
    # Sensational keywords (increase fake score)
    sensational = ["shocking", "unbelievable", "you won't believe", "doctors hate", 
                   "miracle", "secret they don't want", "breaking", "exclusive"]
    for word in sensational:
        if word in text_lower:
            fake_score += 0.05
            indicators.append(f"sensational language: '{word}'")
    
    # All caps words (often clickbait)
    caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
    if len(caps_words) > 2:
        fake_score += 0.1
        indicators.append(f"{len(caps_words)} all-caps words")
    
    # Emotional manipulation
    emotional = ["outraged", "furious", "devastated", "terrified", "horrified"]
    for word in emotional:
        if word in text_lower:
            fake_score += 0.05
            indicators.append(f"emotional manipulation: '{word}'")
    
    # Clamp score to [0.3, 0.7] - rule-based shouldn't be too confident
    fake_score = max(0.3, min(0.7, fake_score))
    
    explanation = (
        f"AI analysis unavailable. Rule-based detection found: {', '.join(indicators) if indicators else 'no strong indicators'}. "
        f"Recommendation: Verify with trusted sources."
    )
    
    return fake_score, explanation
