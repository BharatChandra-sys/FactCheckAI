"""
FactCheckAI — HuggingFace Spaces ML Inference Server
=====================================================
Deployed as a Gradio Space (FastAPI mode).
Free tier: 16GB RAM, 2 vCPU — enough for 2× RoBERTa models.

Models loaded:
  model_A — trained on daniB2112 (300k, ~96% accuracy)
  model_B — trained on mixed datasets (232k, ~80% accuracy)

Ensemble: weighted average (model_A × 0.6 + model_B × 0.4)
  model_A gets higher weight — significantly more accurate.

Security: Bearer token (ML_API_KEY env var in Space secrets).
"""

import os
import time
import json
import logging
import hashlib
from typing import Optional
from functools import lru_cache

import torch
import fastapi
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────
ML_API_KEY   = os.getenv("ML_API_KEY", "")
MODEL_A_REPO = os.getenv("MODEL_A_REPO", "Bharat2004/factcheckai-model-a")
MODEL_B_REPO = os.getenv("MODEL_B_REPO", "Bharat2004/factcheckai-model-b")
HF_TOKEN     = os.getenv("HF_TOKEN", "")
WEIGHT_A     = float(os.getenv("WEIGHT_A", "0.6"))
WEIGHT_B     = float(os.getenv("WEIGHT_B", "0.4"))
DEVICE       = "cuda" if torch.cuda.is_available() else "cpu"

# ── App ───────────────────────────────────────────────────────
app = FastAPI(title="FactCheckAI ML Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

security = HTTPBearer(auto_error=False)

def verify_key(creds: Optional[HTTPAuthorizationCredentials] = Security(security)):
    if ML_API_KEY and (not creds or creds.credentials != ML_API_KEY):
        raise HTTPException(status_code=403, detail="Invalid API key")

# ── Model state ───────────────────────────────────────────────
_models: dict = {}          # {"A": (model, tokenizer), "B": (model, tokenizer)}
_load_errors: dict = {}     # {"A": "error msg"} if load failed
_startup_time = time.time()

# Simple in-memory prediction cache (hash → result)
_pred_cache: dict = {}
_CACHE_MAX = 2000


def _cache_key(text: str) -> str:
    return hashlib.sha256(text[:500].lower().strip().encode()).hexdigest()[:16]


def _load_model(name: str, repo: str):
    """Load a RoBERTa model from HuggingFace Hub into _models dict."""
    if not repo:
        logger.warning("Model %s: no repo configured — skipping", name)
        _load_errors[name] = "No repo configured"
        return
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        logger.info("Loading model_%s from %s on %s ...", name, repo, DEVICE)
        tok = AutoTokenizer.from_pretrained(
            repo, token=HF_TOKEN or None
        )
        mdl = AutoModelForSequenceClassification.from_pretrained(
            repo, token=HF_TOKEN or None
        )
        mdl.eval()
        mdl.to(DEVICE)
        _models[name] = (mdl, tok)
        mem = torch.cuda.memory_allocated() / 1e6 if DEVICE == "cuda" else 0
        logger.info("model_%s loaded. GPU mem: %.0f MB", name, mem)
    except Exception as e:
        logger.error("model_%s load FAILED: %s", name, e)
        _load_errors[name] = str(e)


@app.on_event("startup")
def startup():
    _load_model("A", MODEL_A_REPO)
    _load_model("B", MODEL_B_REPO)
    loaded = list(_models.keys())
    logger.info("Startup complete. Loaded models: %s", loaded)


# ── Schemas ───────────────────────────────────────────────────
class PredictRequest(BaseModel):
    text: str
    use_cache: bool = True


class PredictResponse(BaseModel):
    fake_probability: float
    confidence: float
    verdict: str
    model_a_score: Optional[float] = None
    model_b_score: Optional[float] = None
    ensemble_weights: dict
    model_sources: list
    cached: bool
    inference_ms: int


# ── Inference helpers ─────────────────────────────────────────

def _infer_single(model, tokenizer, text: str) -> float:
    """Return fake probability (0–1) for a single text."""
    inputs = tokenizer(
        text, return_tensors="pt",
        truncation=True, max_length=512, padding=True
    ).to(DEVICE)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs  = torch.softmax(logits, dim=-1)[0]
    # label 1 = FAKE (matches our training convention)
    return float(probs[1])


# ── Endpoints ─────────────────────────────────────────────────

@app.get("/health")
def health():
    loaded = list(_models.keys())
    errors = {k: v for k, v in _load_errors.items()}
    status = "healthy" if loaded else "degraded"
    return {
        "status":       status,
        "loaded_models": loaded,
        "load_errors":  errors,
        "device":       DEVICE,
        "uptime_s":     int(time.time() - _startup_time),
        "cache_size":   len(_pred_cache),
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest, _=Depends(verify_key)):
    if not _models:
        raise HTTPException(503, "No models loaded. Check HF Space logs.")

    text = req.text.strip()
    if not text:
        raise HTTPException(400, "text cannot be empty")
    text = text[:2000]

    # Cache hit
    if req.use_cache:
        ck = _cache_key(text)
        if ck in _pred_cache:
            cached = _pred_cache[ck]
            cached["cached"] = True
            return PredictResponse(**cached)

    t0 = time.perf_counter()

    score_a: Optional[float] = None
    score_b: Optional[float] = None

    if "A" in _models:
        try:
            score_a = _infer_single(*_models["A"], text)
        except Exception as e:
            logger.warning("model_A inference error: %s", e)

    if "B" in _models:
        try:
            score_b = _infer_single(*_models["B"], text)
        except Exception as e:
            logger.warning("model_B inference error: %s", e)

    # Weighted ensemble — fallback gracefully if one model missing
    if score_a is not None and score_b is not None:
        fake_prob = WEIGHT_A * score_a + WEIGHT_B * score_b
        sources   = ["model_A", "model_B"]
        weights   = {"model_A": WEIGHT_A, "model_B": WEIGHT_B}
    elif score_a is not None:
        fake_prob = score_a
        sources   = ["model_A"]
        weights   = {"model_A": 1.0}
    elif score_b is not None:
        fake_prob = score_b
        sources   = ["model_B"]
        weights   = {"model_B": 1.0}
    else:
        raise HTTPException(500, "Both models failed inference")

    confidence = abs(fake_prob - 0.5) * 2
    verdict    = "fake" if fake_prob >= 0.5 else "real"
    ms         = int((time.perf_counter() - t0) * 1000)

    result = {
        "fake_probability": round(fake_prob, 4),
        "confidence":       round(confidence, 4),
        "verdict":          verdict,
        "model_a_score":    round(score_a, 4) if score_a is not None else None,
        "model_b_score":    round(score_b, 4) if score_b is not None else None,
        "ensemble_weights": weights,
        "model_sources":    sources,
        "cached":           False,
        "inference_ms":     ms,
    }

    # Store in cache (evict oldest if full)
    if req.use_cache:
        if len(_pred_cache) >= _CACHE_MAX:
            oldest = next(iter(_pred_cache))
            del _pred_cache[oldest]
        _pred_cache[_cache_key(text)] = result

    logger.info("predict: fake=%.3f conf=%.3f verdict=%s ms=%d sources=%s",
                fake_prob, confidence, verdict, ms, sources)

    return PredictResponse(**result)


@app.get("/")
def root():
    return {
        "service":  "FactCheckAI ML Ensemble Server",
        "status":   "running",
        "models":   list(_models.keys()),
        "endpoint": "POST /predict",
    }
