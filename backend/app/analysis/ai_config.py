"""
Central AI Provider Configuration
Automatically discovers and caches available models from each provider.
No more hardcoded model IDs!
"""
import os
import logging
import requests
from typing import List, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

# API URLs
CEREBRAS_URL = "https://api.cerebras.ai/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
MINIMAX_URL = "https://api.minimax.io/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


@lru_cache(maxsize=10)
def get_api_keys() -> dict:
    """Get API keys from environment (cached)."""
    return {
        "cerebras": os.getenv("CEREBRAS_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
        "gemini": os.getenv("GEMINI_API_KEY"),
        "minimax": os.getenv("MINIMAX_API_KEY"),
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
        "gemini_proxy": os.getenv("GEMINI_WEB2API_URL", "https://factcheckai-gemini-proxy.onrender.com"),
    }


# Global model cache with TTL
_MODEL_CACHE = {}
_CACHE_TTL_SECONDS = 3600  # 1 hour


def _is_cache_valid(cache_key: str) -> bool:
    """Check if cached models are still valid."""
    import time
    if cache_key not in _MODEL_CACHE:
        return False
    timestamp, _ = _MODEL_CACHE[cache_key]
    return (time.time() - timestamp) < _CACHE_TTL_SECONDS


def discover_groq_models(api_key: str) -> List[str]:
    """Discover available Groq models via API."""
    cache_key = f"groq_{api_key[:10]}"
    
    if _is_cache_valid(cache_key):
        return _MODEL_CACHE[cache_key][1]
    
    try:
        r = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        if r.status_code == 200:
            models = [m["id"] for m in r.json().get("data", [])]
            # Filter out problematic models
            filtered = []
            for m in models:
                m_lower = m.lower()
                # Exclude non-chat models
                if any(x in m_lower for x in ["whisper", "vision", "embed", "guard"]):
                    continue
                # Exclude models requiring terms acceptance (canopylabs/orpheus-*)
                if "canopylabs" in m or "orpheus" in m:
                    continue
                # Exclude oversized models (groq/compound causes 413 errors)
                if "compound" in m:
                    continue
                filtered.append(m)
            
            # Sort by priority: gpt-oss-120b > gpt-oss-20b > qwen > allam > rest
            priority_order = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "allam-2-7b"]
            sorted_models = []
            for p in priority_order:
                if p in filtered:
                    sorted_models.append(p)
                    filtered.remove(p)
            sorted_models.extend(filtered)  # Add remaining models
            
            import time
            _MODEL_CACHE[cache_key] = (time.time(), sorted_models)
            logger.info(f"Discovered {len(sorted_models)} Groq models (filtered from {len(models)})")
            return sorted_models
    except Exception as e:
        logger.warning(f"Groq model discovery failed: {e}")
    
    # Fallback to verified working models (2026-09-22 - all tested working)
    return [
        "openai/gpt-oss-120b",      # 120B reasoning - BEST (0.99 confidence, 3s)
        "openai/gpt-oss-20b",        # 20B fast - GREAT (0.99 confidence, 2s)
        "qwen/qwen3.8-27b",          # 27B - GOOD (1.0 confidence, 3s)
        "allam-2-7b"                 # 7B - OK (works, low confidence)
    ]


def discover_cerebras_models(api_key: str) -> List[str]:
    """Discover available Cerebras models via API."""
    cache_key = f"cerebras_{api_key[:10]}"
    
    if _is_cache_valid(cache_key):
        return _MODEL_CACHE[cache_key][1]
    
    try:
        r = requests.get(
            "https://api.cerebras.ai/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        if r.status_code == 200:
            models = [m["id"] for m in r.json().get("data", [])]
            import time
            _MODEL_CACHE[cache_key] = (time.time(), models)
            logger.info(f"Discovered {len(models)} Cerebras models")
            return models
    except Exception as e:
        logger.warning(f"Cerebras model discovery failed: {e}")
    
    # Fallback (verified 2026-09-22 - Cerebras requires payment now)
    return []  # No free tier available anymore


def discover_gemini_models(api_key: str) -> List[str]:
    """Discover available Gemini models via API."""
    cache_key = f"gemini_{api_key[:10]}"
    
    if _is_cache_valid(cache_key):
        return _MODEL_CACHE[cache_key][1]
    
    try:
        r = requests.get(
            "https://generativelanguage.googleapis.com/v1beta/models",
            params={"key": api_key},
            timeout=10
        )
        if r.status_code == 200:
            all_models = r.json().get("models", [])
            # Filter to generateContent models
            models = [m["name"].replace("models/", "") for m in all_models 
                     if "generateContent" in m.get("supportedGenerationMethods", [])]
            
            # Filter out invalid/broken model names
            filtered = []
            for m in models:
                m_lower = m.lower()
                # Exclude TTS models (wrong API endpoint)
                if "tts" in m_lower or "text-to-speech" in m_lower:
                    continue
                # Exclude models with invalid naming patterns
                if "gemini-2.5" in m_lower:  # 2.5 doesn't exist yet
                    continue
                filtered.append(m)
            
            import time
            _MODEL_CACHE[cache_key] = (time.time(), filtered)
            logger.info(f"Discovered {len(filtered)} Gemini models (filtered from {len(models)})")
            return filtered
    except Exception as e:
        logger.warning(f"Gemini model discovery failed: {e}")
    
    # Fallback (verified 2026-09-22 via proxy)
    return [
        "gemini-3.7-flash",              # Latest - WORKS
        "gemini-3.6-flash",              # Fast - WORKS
        "gemini-3.5-flash",              # Stable - WORKS
        "gemini-3.5-flash-thinking",     # Thinking mode - WORKS
        "gemini-3.1-pro"                 # Pro tier - WORKS
    ]


def discover_gemini_proxy_models(proxy_url: str) -> List[str]:
    """Discover available Gemini Proxy models."""
    cache_key = f"gemini_proxy_{proxy_url[-20:]}"
    
    if _is_cache_valid(cache_key):
        return _MODEL_CACHE[cache_key][1]
    
    try:
        r = requests.get(f"{proxy_url}/v1/models", timeout=10)
        if r.status_code == 200:
            models = [m["id"] for m in r.json().get("data", [])]
            
            # Sort by priority: 3.7 > 3.6 > 3.5 > 3.5-thinking > 3.1-pro > rest
            priority_order = [
                "gemini-3.7-flash",
                "gemini-3.6-flash", 
                "gemini-3.5-flash",
                "gemini-3.5-flash-thinking",
                "gemini-3.1-pro",
                "gemini-auto"
            ]
            sorted_models = []
            for p in priority_order:
                if p in models:
                    sorted_models.append(p)
                    models.remove(p)
            sorted_models.extend(models)  # Add remaining models
            
            import time
            _MODEL_CACHE[cache_key] = (time.time(), sorted_models)
            logger.info(f"Discovered {len(sorted_models)} Gemini Proxy models")
            return sorted_models
    except Exception as e:
        logger.warning(f"Gemini Proxy model discovery failed: {e}")
    
    # Fallback to verified working models (2026-09-22 - all 8/8 tested working, 1.0 confidence)
    return [
        "gemini-3.7-flash",              # Latest - BEST (1.0 confidence, 2s, perfect JSON)
        "gemini-3.6-flash",              # Fast - GREAT (1.0 confidence, 2s)
        "gemini-3.5-flash",              # Stable - GOOD (1.0 confidence, 2-3s)
        "gemini-3.5-flash-thinking",     # Thinking mode - GOOD (1.0 confidence)
        "gemini-3.1-pro",                # Pro tier - GOOD (1.0 confidence)
        "gemini-auto"                    # Auto-selection - GOOD
    ]


def discover_openrouter_models(api_key: str) -> List[str]:
    """Discover available FREE OpenRouter models."""
    cache_key = f"openrouter_{api_key[:10]}"
    
    if _is_cache_valid(cache_key):
        return _MODEL_CACHE[cache_key][1]
    
    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        if r.status_code == 200:
            all_models = r.json().get("data", [])
            # Filter to free models only
            free_models = [m["id"] for m in all_models 
                          if m.get("pricing", {}).get("prompt", "0") == "0"]
            
            # Filter out problematic models
            filtered = []
            for m in free_models:
                m_lower = m.lower()
                # Exclude agentic-only models
                if "inkling" in m:
                    continue
                # Exclude rate-limited models
                if "qwen3.8-27b" in m:
                    continue
                # Exclude broken models
                if "ling-3.0-flash-fin" in m:
                    continue
                # Exclude slow models (>120s timeout)
                if "nemotron" in m:
                    continue
                filtered.append(m)
            
            # Sort by priority: nex-pro > ling-vl > liquid > nex-mini > ling-sante > rest
            priority_order = [
                "nex-agi/nex-n2.5-pro:free",
                "inclusionai/ling-3.0-flash-vl:free",
                "liquid/lfm-2.5-2.6b:free",
                "nex-agi/nex-n2.5-mini:free",
                "inclusionai/ling-3.0-flash-sante:free"
            ]
            sorted_models = []
            for p in priority_order:
                if p in filtered:
                    sorted_models.append(p)
                    filtered.remove(p)
            sorted_models.extend(filtered)  # Add remaining models
            
            import time
            _MODEL_CACHE[cache_key] = (time.time(), sorted_models)
            logger.info(f"Discovered {len(sorted_models)} OpenRouter free models (filtered from {len(free_models)})")
            return sorted_models
    except Exception as e:
        logger.warning(f"OpenRouter model discovery failed: {e}")
    
    # Fallback to verified working models (2026-09-22 - 7/10 tested working)
    return [
        "nex-agi/nex-n2.5-pro:free",              # BEST (0.99 confidence, fast)
        "inclusionai/ling-3.0-flash-vl:free",     # VL - GREAT (1.0 confidence)
        "liquid/lfm-2.5-2.6b:free",               # LFM - GOOD (works with JSON)
        "nex-agi/nex-n2.5-mini:free",             # Mini - OK (1.0 confidence)
        "inclusionai/ling-3.0-flash-sante:free"   # Sante - OK (1.0 confidence)
    ]


def get_first_working_model(provider: str) -> Optional[str]:
    """
    Get the first working model for a provider.
    Returns None if no models available or API key missing.
    """
    keys = get_api_keys()
    
    if provider == "groq" and keys["groq"]:
        models = discover_groq_models(keys["groq"])
        return models[0] if models else None
    
    elif provider == "cerebras" and keys["cerebras"]:
        models = discover_cerebras_models(keys["cerebras"])
        return models[0] if models else None
    
    elif provider == "gemini" and keys["gemini"]:
        models = discover_gemini_models(keys["gemini"])
        return models[0] if models else None
    
    elif provider == "gemini_proxy" and keys["gemini_proxy"]:
        models = discover_gemini_proxy_models(keys["gemini_proxy"])
        return models[0] if models else None
    
    elif provider == "openrouter" and keys["openrouter"]:
        models = discover_openrouter_models(keys["openrouter"])
        return models[0] if models else None
    
    return None


def get_all_working_models(provider: str) -> List[str]:
    """Get all available models for a provider."""
    keys = get_api_keys()
    
    if provider == "groq" and keys["groq"]:
        return discover_groq_models(keys["groq"])
    
    elif provider == "cerebras" and keys["cerebras"]:
        return discover_cerebras_models(keys["cerebras"])
    
    elif provider == "gemini" and keys["gemini"]:
        return discover_gemini_models(keys["gemini"])
    
    elif provider == "gemini_proxy" and keys["gemini_proxy"]:
        return discover_gemini_proxy_models(keys["gemini_proxy"])
    
    elif provider == "openrouter" and keys["openrouter"]:
        return discover_openrouter_models(keys["openrouter"])
    
    return []


def warmup_model_cache():
    """
    Warm up model cache on startup (for production).
    Call this during app initialization to pre-populate cache.
    """
    keys = get_api_keys()
    logger.info("Warming up model cache...")
    
    if keys.get("groq"):
        try:
            models = discover_groq_models(keys["groq"])
            logger.info(f"Cached {len(models)} Groq models")
        except Exception as e:
            logger.warning(f"Groq cache warmup failed: {e}")
    
    if keys.get("cerebras"):
        try:
            models = discover_cerebras_models(keys["cerebras"])
            logger.info(f"Cached {len(models)} Cerebras models (may be 0 if payment required)")
        except Exception as e:
            logger.warning(f"Cerebras cache warmup failed: {e}")
    
    if keys.get("gemini"):
        try:
            models = discover_gemini_models(keys["gemini"])
            logger.info(f"Cached {len(models)} Gemini models")
        except Exception as e:
            logger.warning(f"Gemini cache warmup failed: {e}")
    
    if keys.get("gemini_proxy"):
        try:
            models = discover_gemini_proxy_models(keys["gemini_proxy"])
            logger.info(f"Cached {len(models)} Gemini Proxy models")
        except Exception as e:
            logger.warning(f"Gemini Proxy cache warmup failed: {e}")
    
    if keys.get("openrouter"):
        try:
            models = discover_openrouter_models(keys["openrouter"])
            logger.info(f"Cached {len(models)} OpenRouter free models")
        except Exception as e:
            logger.warning(f"OpenRouter cache warmup failed: {e}")
    
    logger.info("Model cache warmup complete")
