# Copyright 2027 Bodapati Bharat Chandra. All rights reserved.
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
# Project: FactCheckAI � https://github.com/BharatChandra-sys/fake-news-extension
"""
ML Analysis — Multi-server architecture:

Primary:  External ML Server 1 (Oracle Cloud - DeBERTa)
          HTTP endpoint at ML_SERVER_1_URL
Backup:   External ML Server 2 (HuggingFace - Ensemble)
          HTTP endpoint at ML_SERVER_2_URL
Fallback: Local TF-IDF + Logistic Regression from model.joblib
          Always available, lightweight (50MB)
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
ML_SERVER_1_URL = os.getenv("ML_SERVER_1_URL")  # Oracle Cloud DeBERTa
ML_SERVER_2_URL = os.getenv("ML_SERVER_2_URL")  # HuggingFace Ensemble
ML_API_KEY = os.getenv("ML_API_KEY")  # Shared API key for ML servers

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
    """Call Ensemble server on HuggingFace Space (FastAPI mode) — synchronous."""
    if not ML_SERVER_2_URL or not ML_API_KEY:
        logger.debug("ML Server 2 not configured")
        return None
    try:
        with httpx.Client(timeout=20.0) as client:
            response = client.post(
                f"{ML_SERVER_2_URL}/predict",
                json={"text": text, "use_cache": True},
                headers={"Authorization": f"Bearer {ML_API_KEY}"},
            )
            if response.status_code == 200:
                data  = response.json()
                score = data.get("fake_probability")
                logger.info("ML Server 2 (HF Ensemble): %.3f in %dms sources=%s",
                            score, data.get("inference_ms", 0), data.get("model_sources"))
                return score
            else:
                logger.warning("ML Server 2 returned status %d: %s",
                               response.status_code, response.text[:100])
    except httpx.TimeoutException:
        logger.warning("ML Server 2 timeout (HF Space may be cold-starting)")
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
