"""
ML Server 1 - DeBERTa on Oracle Cloud
Dedicated server for running DeBERTa transformer model
"""

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from transformers import pipeline
import os
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ML Server 1 - DeBERTa")

# Load model on startup
ML_API_KEY = os.getenv("ML_API_KEY", "change-me-in-production")
MODEL_NAME = os.getenv("DEBERTA_MODEL", "Bharat2004/deberta-fakenews-detector")

model_pipeline = None

@app.on_event("startup")
async def load_model():
    global model_pipeline
    logger.info(f"Loading model: {MODEL_NAME}")
    start = time.time()
    
    model_pipeline = pipeline(
        "text-classification",
        model=MODEL_NAME,
        device=-1,  # CPU
        truncation=True,
        max_length=512,
    )
    
    logger.info(f"Model loaded in {time.time() - start:.2f}s")


class PredictRequest(BaseModel):
    text: str
    api_key: str


@app.post("/predict")
async def predict(request: PredictRequest):
    """Run DeBERTa prediction"""
    
    # Auth check
    if request.api_key != ML_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Run model
    start = time.time()
    result = model_pipeline(request.text[:1500])[0]
    inference_time = time.time() - start
    
    # Parse result
    label = result["label"].upper()
    score = float(result["score"])
    
    # Convert to fake probability
    # Bharat2004 models: LABEL_0=real, LABEL_1=fake
    # Handle both formats
    if label in ("LABEL_1", "FAKE"):
        fake_prob = score
    else:  # LABEL_0, REAL
        fake_prob = 1.0 - score
    
    logger.info(f"Prediction: {fake_prob:.3f} in {inference_time:.3f}s")
    
    return {
        "fake_probability": round(fake_prob, 3),
        "model": MODEL_NAME,
        "confidence": score,
        "inference_time_ms": int(inference_time * 1000),
        "server": "ml-server-1-oracle"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "server": "ml-server-1-oracle",
        "model_loaded": model_pipeline is not None
    }


@app.get("/")
async def root():
    return {
        "service": "ML Server 1 - DeBERTa",
        "model": MODEL_NAME,
        "endpoints": ["/predict", "/health"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
