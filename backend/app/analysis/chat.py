# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(_env_path)

# Import central AI config for dynamic model discovery
from app.analysis.ai_config import (
    get_api_keys, get_all_working_models, get_first_working_model,
    CEREBRAS_URL, GROQ_URL, MINIMAX_URL, OPENROUTER_URL, GEMINI_URL_BASE
)

CHAT_SYSTEM = (
    "You are a helpful, knowledgeable assistant specializing in media literacy and fact-checking. "
    "Answer questions clearly and concisely. Be friendly and factual. Never fabricate sources or statistics. "
    "When discussing news or claims, always encourage users to verify information from multiple trusted sources."
)

CLAIM_DETECT_PROMPT = (
    "Classify the following input as either 'claim' or 'other'.\n"
    "A 'claim' is a statement that asserts something as true or false and can be fact-checked "
    "(e.g. news headlines, assertions about events, scientific claims, political statements).\n"
    "'other' includes greetings, questions asking for information, opinions, casual conversation, "
    "or anything that is not a verifiable factual assertion.\n\n"
    "Reply with ONLY one word: claim or other.\n\n"
    "Input: {text}"
)


def _get_keys():
    """Wrapper for backward compatibility."""
    return get_api_keys()


def _call_openai_compat(url: str, key: str, model: str, messages: list, max_tokens=400, temperature=0.7) -> str:
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
        timeout=15
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def _call_gemini(messages: list, max_tokens=400, temperature=0.7) -> str:
    key = _get_keys()["gemini"]
    if not key:
        raise ValueError("Gemini API key missing")
    
    # Use dynamic model discovery - try first available model
    from app.analysis.ai_config import discover_gemini_models
    models = discover_gemini_models(key)
    if not models:
        models = ["gemini-1.5-flash", "gemini-1.5-pro"]
    
    contents = []
    system_text = ""
    for m in messages:
        if m["role"] == "system":
            system_text = m["content"]
            continue
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    if contents and contents[0]["role"] == "user" and system_text:
        contents[0]["parts"][0]["text"] = system_text + "\n\n" + contents[0]["parts"][0]["text"]
    
    # Try models until one works
    for model in models[:3]:
        try:
            url = f"{GEMINI_URL_BASE}/{model}:generateContent"
            r = requests.post(
                f"{url}?key={key}",
                headers={"Content-Type": "application/json"},
                json={"contents": contents, "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}},
                timeout=12
            )
            r.raise_for_status()
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            if model == models[-1] or model == models[2]:  # Last attempt
                raise
            continue
    raise ValueError("All Gemini models failed")


def _call_minimax_chat(messages: list, max_tokens=400, temperature=0.7) -> str:
    """MiniMax M2.7 for chat — fast, high quality, OpenAI-compatible."""
    key = _get_keys()["minimax"]
    if not key:
        raise ValueError("MiniMax API key missing")
    # Try M2.7-highspeed first for chat (lower latency), fall back to M2.7
    for model in ["MiniMax-M2.7-highspeed", "MiniMax-M2.7"]:
        try:
            r = requests.post(
                MINIMAX_URL,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
                timeout=15
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            continue
    raise ValueError("MiniMax chat failed")


def _first_success(fn_list):
    """Run list of (name, callable) in parallel, return first success."""
    errors = []
    with ThreadPoolExecutor(max_workers=len(fn_list)) as executor:
        futures = {executor.submit(fn): name for name, fn in fn_list}
        for future in as_completed(futures):
            try:
                return future.result()
            except Exception as e:
                errors.append(f"{futures[future]}: {e}")
    raise RuntimeError(" | ".join(errors))


def is_claim(text: str) -> bool:
    """Ask AI to classify if the input is a verifiable claim."""
    prompt = CLAIM_DETECT_PROMPT.format(text=text)
    messages = [{"role": "user", "content": prompt}]
    keys = _get_keys()

    fns = []
    # Prioritize FREE providers
    if keys["openrouter"]:
        fns.append(("OpenRouter", lambda: _call_openai_compat(OPENROUTER_URL, keys["openrouter"], "google/gemma-2-9b-it:free", messages, max_tokens=5, temperature=0)))
    
    # Groq - use dynamic model discovery
    if keys["groq"]:
        groq_models = get_all_working_models("groq")
        if groq_models:
            model = groq_models[0]  # Use first available
            fns.append((f"Groq-{model}", lambda m=model: _call_openai_compat(GROQ_URL, keys["groq"], m, messages, max_tokens=5, temperature=0)))
    
    # Gemini as backup (may have quota limits)
    if keys["gemini"]:
        fns.append(("Gemini", lambda: _call_gemini(messages, max_tokens=5, temperature=0)))
    
    # Cerebras - use dynamic model discovery
    if keys["cerebras"]:
        cerebras_models = get_all_working_models("cerebras")
        if cerebras_models:
            model = cerebras_models[0]
            fns.append((f"Cerebras-{model}", lambda m=model: _call_openai_compat(CEREBRAS_URL, keys["cerebras"], m, messages, max_tokens=5, temperature=0)))
    
    if keys["minimax"]:
        fns.append(("MiniMax", lambda: _call_minimax_chat(messages, max_tokens=5, temperature=0)))

    try:
        result = _first_success(fns)
        return result.strip().lower().startswith("claim")
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.warning(f"All AI providers failed for claim detection: {e}")
        # Default: treat as chat (not claim) if all AI providers fail
        return False


def run_chat(message: str, history: list) -> str:
    msgs = [{"role": "system", "content": CHAT_SYSTEM}]
    for h in history[-6:]:
        msgs.append({"role": h["role"], "content": h["content"]})
    msgs.append({"role": "user", "content": message})

    keys = _get_keys()
    fns = []
    # Prioritize FREE providers
    if keys["openrouter"]:
        fns.append(("OpenRouter", lambda: _call_openai_compat(OPENROUTER_URL, keys["openrouter"], "google/gemma-2-9b-it:free", msgs)))
    
    # Groq - use dynamic model discovery
    if keys["groq"]:
        groq_models = get_all_working_models("groq")
        if groq_models:
            model = groq_models[0]  # Use first available
            fns.append((f"Groq-{model}", lambda m=model: _call_openai_compat(GROQ_URL, keys["groq"], m, msgs)))
    
    # Gemini as backup (may have quota limits)
    if keys["gemini"]:
        fns.append(("Gemini", lambda: _call_gemini(msgs)))
    
    # MiniMax M2.7-highspeed for chat — fastest with high quality
    if keys["minimax"]:
        fns.append(("MiniMax", lambda: _call_minimax_chat(msgs)))
    
    # Cerebras - use dynamic model discovery
    if keys["cerebras"]:
        cerebras_models = get_all_working_models("cerebras")
        if cerebras_models:
            model = cerebras_models[0]
            fns.append((f"Cerebras-{model}", lambda m=model: _call_openai_compat(CEREBRAS_URL, keys["cerebras"], m, msgs)))

    try:
        return _first_success(fns)
    except Exception as e:
        import logging
        logging.warning(f"All AI providers failed for chat: {e}")
        return "I'm having trouble connecting right now. Please try again in a moment."
    