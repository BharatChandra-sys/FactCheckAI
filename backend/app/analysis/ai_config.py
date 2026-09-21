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
                # Exclude oversized models (groq/compound is too large - 413 errors)
                if "compound" in m:
                    continue
                filtered.append(m)
            
            import time
            _MODEL_CACHE[cache_key] = (time.time(), filtered)
            logger.info(f"Discovered {len(filtered)} Groq models (filtered from {len(models)})")
            return filtered
    except Exception as e:
        logger.warning(f"Groq model discovery failed: {e}")
    
    # Fallback to known working models
    return ["llama-3.3-70b-specdec", "llama-3.1-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"]


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
    
    # Fallback
    return ["llama-3.3-70b-specdec", "llama-3.1-8b", "llama3.1-8b"]


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
    
    # Fallback
    return ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]


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
            logger.info(f"Cached {len(models)} Cerebras models")
        except Exception as e:
            logger.warning(f"Cerebras cache warmup failed: {e}")
    
    if keys.get("gemini"):
        try:
            models = discover_gemini_models(keys["gemini"])
            logger.info(f"Cached {len(models)} Gemini models")
        except Exception as e:
            logger.warning(f"Gemini cache warmup failed: {e}")
    
    logger.info("Model cache warmup complete")
