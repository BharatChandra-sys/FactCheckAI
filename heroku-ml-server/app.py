"""
Heroku ML Inference Server for FactCheckAI
==========================================
Dedicated FastAPI server for heavy ML processing.
Deployed on Heroku Eco dyno (always-on, no cold starts).

This server handles:
- DeBERTa transformer inference
- Heavy NLP operations  
- Ensemble ML predictions
- Bulk text analysis

Main backend (Render) sends requests here for ML processing.
"""

import os
import time
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import torch
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FactCheckAI ML Server",
    description="Specialized ML inference server for fake news detection",
    version="1.0.0"
)

# Global model storage
_model = None
_tokenizer = None
_model_loaded = False

# Security
security = HTTPBearer()
ML_API_KEY = os.getenv("ML_API_KEY", "")

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify API key for requests"""
    if ML_API_KEY and credentials.credentials != ML_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return credentials.credentials

# Request/Response models
class MLRequest(BaseModel):
    text: str
    model_type: str = "deberta"
    confidence_threshold: float = 0.5

class MLResponse(BaseModel):
    fake_probability: float
    confidence: float
    model_used: str
    inference_time_ms: int
    text_length: int

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    memory_usage_mb: int
    uptime_seconds: int

# Model loading
def load_ml_model():
    """Load DeBERTa model for inference"""
    global _model, _tokenizer, _model_loaded
    
    try:
        logger.info("Loading DeBERTa model...")
        
        # Import here to handle missing dependencies gracefully
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        # Your fine-tuned model on HuggingFace
        model_name = os.getenv("DEBERTA_MODEL", "Bharat2004/out")
        
        logger.info(f"Loading model: {model_name}")
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSequenceClassification.from_pretrained(model_name)
        _model.eval()  # Set to evaluation mode
        
        _model_loaded = True
        logger.info(f"Model loaded successfully: {model_name}")
        
        # Log memory usage
        memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
        logger.info(f"Memory usage after model load: {memory_mb:.1f} MB")
        
    except Exception as e:
        logger.error(f"Failed to load ML model: {e}")
        _model_loaded = False

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize ML model on startup"""
    load_ml_model()

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check with system stats"""
    import time
    
    # Get memory usage
    memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
    
    return HealthResponse(
        status="healthy" if _model_loaded else "unhealthy",
        model_loaded=_model_loaded,
        memory_usage_mb=int(memory_mb),
        uptime_seconds=int(time.time() - startup_time)
    )

# ML inference endpoint
@app.post("/ml/predict", response_model=MLResponse)
async def predict_fake_news(
    request: MLRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Main ML inference endpoint for fake news detection
    """
    if not _model_loaded:
        raise HTTPException(
            status_code=503, 
            detail="ML model not loaded. Server may be starting up."
        )
    
    start_time = time.time()
    
    try:
        # Preprocess text
        text = request.text.strip()[:512]  # Truncate to model max length
        
        if not text:
            raise HTTPException(status_code=400, detail="Empty text provided")
        
        # Tokenize
        inputs = _tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        
        # Inference
        with torch.no_grad():
            outputs = _model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)[0]
            
            # Assuming binary classification: [Real, Fake]
            fake_prob = float(probs[1])
            confidence = float(torch.max(probs))
        
        inference_time = int((time.time() - start_time) * 1000)
        
        logger.info(
            f"ML inference completed: "
            f"fake_prob={fake_prob:.3f}, "
            f"confidence={confidence:.3f}, "
            f"time={inference_time}ms, "
            f"length={len(text)}"
        )
        
        return MLResponse(
            fake_probability=round(fake_prob, 4),
            confidence=round(confidence, 4),
            model_used="deberta-finetuned",
            inference_time_ms=inference_time,
            text_length=len(request.text)
        )
        
    except Exception as e:
        logger.error(f"ML inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

# Batch prediction endpoint
@app.post("/ml/predict-batch")
async def predict_batch(
    texts: list[str],
    api_key: str = Depends(verify_api_key)
):
    """
    Batch prediction for multiple texts
    More efficient for bulk processing
    """
    if not _model_loaded:
        raise HTTPException(status_code=503, detail="ML model not loaded")
    
    if len(texts) > 100:
        raise HTTPException(status_code=400, detail="Batch size too large (max 100)")
    
    start_time = time.time()
    results = []
    
    try:
        # Process all texts at once for efficiency
        processed_texts = [text.strip()[:512] for text in texts]
        
        # Tokenize batch
        inputs = _tokenizer(
            processed_texts,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        
        # Batch inference
        with torch.no_grad():
            outputs = _model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            
            for i, (text, prob_tensor) in enumerate(zip(texts, probs)):
                fake_prob = float(prob_tensor[1])
                confidence = float(torch.max(prob_tensor))
                
                results.append({
                    "text_index": i,
                    "fake_probability": round(fake_prob, 4),
                    "confidence": round(confidence, 4),
                    "text_length": len(text)
                })
        
        total_time = int((time.time() - start_time) * 1000)
        
        return {
            "results": results,
            "batch_size": len(texts),
            "total_inference_time_ms": total_time,
            "average_time_per_text_ms": round(total_time / len(texts), 1)
        }
        
    except Exception as e:
        logger.error(f"Batch inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch inference failed: {str(e)}")

# Model info endpoint
@app.get("/ml/info")
async def model_info():
    """Get information about the loaded model"""
    if not _model_loaded:
        return {"model_loaded": False}
    
    try:
        # Get model configuration
        config = _model.config
        
        return {
            "model_loaded": True,
            "model_name": getattr(config, '_name_or_path', 'deberta-finetuned'),
            "num_labels": config.num_labels,
            "max_position_embeddings": getattr(config, 'max_position_embeddings', 512),
            "vocab_size": config.vocab_size,
            "model_type": config.model_type,
            "memory_usage_mb": int(psutil.Process().memory_info().rss / 1024 / 1024)
        }
    except Exception as e:
        return {"error": str(e)}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "FactCheckAI ML Server",
        "status": "running",
        "model_loaded": _model_loaded,
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /ml/predict",
            "batch_predict": "POST /ml/predict-batch", 
            "model_info": "GET /ml/info"
        },
        "authentication": "Bearer token required" if ML_API_KEY else "No authentication"
    }

# Store startup time for uptime calculation
startup_time = time.time()

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )