# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
"""
ML Analysis — Multi-server architecture with 4-level fallback:

Level 1:  Redis cache (in-process dict when Redis unavailable)
Level 2:  ML Server 1 — fine-tuned RoBERTa-base (Bharat2004/factcheckai-model-a)
          Configured via ML_SERVER_1_URL environment variable
Level 3:  ML Server 2 — RoBERTa ensemble (model-a + model-b, 0.6/0.4 weight)
          Configured via ML_SERVER_2_URL environment variable (HuggingFace Space with Gradio)
Level 4:  Local TF-IDF + Logistic Regression (model.joblib)
          Always available, ~50ms, no external dependency
Default:  0.5 neutral score if all levels fail (surfaces as "uncertain")
"""

from __future__ import annotations
import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ML Server URLs (from environment)
ML_SERVER_1_URL = os.getenv("ML_SERVER_1_URL")  # Primary: RoBERTa model-a (HF Space or self-hosted)
ML_SERVER_2_URL = os.getenv("ML_SERVER_2_URL")  # Backup: RoBERTa ensemble model-a+b (HF Space with Gradio)
ML_API_KEY      = os.getenv("ML_API_KEY")        # Shared Bearer token for both servers

# Gradio client for HF Spaces (lazy import)
_gradio_client = None

# ── TF-IDF fallback (always available, lightweight) ──────────
_model = None
_vectorizer = None


def _load_tfidf():
    global _model, _vectorizer
    if _model is not None:
        return True
    import joblib
    model_path = os.path.join(DATA_DIR, "model.joblib")
    vec_path   = os.path.join(DATA_DIR, "vectorizer.joblib")
    if not os.path.exists(model_path) or not os.path.exists(vec_path):
        return False
    try:
        _model      = joblib.load(model_path)
        _vectorizer = joblib.load(vec_path)
        logger.info("TF-IDF model loaded from %s", DATA_DIR)
        return True
    except Exception as e:
        logger.warning("TF-IDF load failed: %s", e)
        return False


def _tfidf_score(text: str) -> float | None:
    if not _load_tfidf():
        return None
    try:
        vec  = _vectorizer.transform([text])
        prob = _model.predict_proba(vec)[0][1]
        return round(float(prob), 3)
    except Exception as e:
        logger.warning("TF-IDF inference failed: %s", e)
        return None


# ── External ML Server Calls (synchronous httpx — safe inside uvicorn worker threads) ──

def _call_ml_server_1_sync(text: str) -> float | None:
    """Call DeBERTa server on Oracle Cloud (ML Server 1) — synchronous."""
    if not ML_SERVER_1_URL or not ML_API_KEY:
        logger.debug("ML Server 1 not configured")
        return None
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{ML_SERVER_1_URL}/predict",
                json={"text": text, "api_key": ML_API_KEY}
            )
            if response.status_code == 200:
                data = response.json()
                score = data.get("fake_probability")
                logger.info("ML Server 1 (DeBERTa): %.3f in %dms",
                            score, data.get("inference_time_ms", 0))
                return score
            else:
                logger.warning("ML Server 1 returned status %d", response.status_code)
    except httpx.TimeoutException:
        logger.warning("ML Server 1 timeout")
    except Exception as e:
        logger.warning("ML Server 1 failed: %s", e)
    return None


def _call_ml_server_2_sync(text: str) -> float | None:
    """Call Ensemble server on HuggingFace Space (Gradio) — synchronous."""
    global _gradio_client
    if not ML_SERVER_2_URL:
        logger.debug("ML Server 2 not configured")
        return None
    try:
        # Lazy import and initialize Gradio client
        if _gradio_client is None:
            from gradio_client import Client
            _gradio_client = Client(ML_SERVER_2_URL)
            logger.info("Initialized Gradio client for ML Server 2")
        
        # Call the predict function (first tab, first function)
        result = _gradio_client.predict(
            text,  # text input
            ML_API_KEY or "",  # api_key input
            api_name="/predict"
        )
        
        if isinstance(result, dict):
            score = result.get("fake_probability")
            logger.info("ML Server 2 (HF Gradio): %.3f in %dms sources=%s",
                        score, result.get("inference_ms", 0), result.get("model_sources"))
            return score
        else:
            logger.warning("ML Server 2 unexpected response format: %s", result)
    except Exception as e:
        logger.warning("ML Server 2 error: %s", e)
        # Reset client on error
        _gradio_client = None
    except Exception as e:
        logger.warning("ML Server 2 failed: %s", e)
    return None


# ── Public API ────────────────────────────────────────────────
def run_ml_analysis(text: str) -> dict:
    """
    Returns {"fake": float, "source": "deberta-ml1"|"ensemble-ml2"|"tfidf"|"default"}

    Priority order:
      1. External ML Server 1 (Oracle Cloud - DeBERTa, most accurate)
      2. External ML Server 2 (HuggingFace - Ensemble, backup)
      3. Local TF-IDF + Logistic Regression (always available, ~90% accuracy)
      4. Default 0.5 if everything fails
    """
    
    # Try cache first
    try:
        from app.cache import partial_cache
        cached = partial_cache.get_ml_score(text)
        if cached is not None:
            logger.debug("ML cache hit")
            return {"fake": cached, "source": "cache"}
    except Exception as e:
        logger.debug(f"Cache lookup failed: {e}")
    
    score = None
    source = "default"
    
    # Try ML Server 1 (Oracle Cloud - DeBERTa)
    if ML_SERVER_1_URL:
        score = _call_ml_server_1_sync(text)
        if score is not None:
            source = "deberta-ml1"
    
    # Try ML Server 2 (HuggingFace - Ensemble) if ML1 failed
    if score is None and ML_SERVER_2_URL:
        score = _call_ml_server_2_sync(text)
        if score is not None:
            source = "ensemble-ml2"
    
    # Try local TF-IDF if both ML servers failed
    if score is None:
        score = _tfidf_score(text)
        if score is not None:
            source = "tfidf-local"
    
    # Ultimate fallback
    if score is None:
        logger.warning("All ML methods failed, returning default 0.5")
        score = 0.5
        source = "default"
    else:
        # Cache successful result
        try:
            from app.cache import partial_cache
            partial_cache.set_ml_score(text, score)
        except Exception as e:
            logger.debug(f"Cache set failed: {e}")
    
    return {"fake": score, "source": source}
