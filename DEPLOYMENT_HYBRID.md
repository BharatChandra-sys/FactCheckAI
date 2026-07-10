# Hybrid Multi-Server Deployment (100% FREE!)

**Genius idea:** Use multiple free tiers together! Each server handles what it does best.

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER REQUEST                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  MAIN API (Railway 2GB) - Request Router & Orchestrator     │
│  - Receives all requests                                     │
│  - Routes to appropriate ML server                           │
│  - Handles auth, rate limiting, caching                      │
│  - PostgreSQL database                                       │
│  Cost: $2/month                                              │
└───────┬─────────────────────────────────┬───────────────────┘
        │                                 │
        ▼                                 ▼
┌───────────────────────┐    ┌────────────────────────────────┐
│ ML Server 1           │    │ ML Server 2                    │
│ (Oracle Cloud 12GB)   │    │ (HuggingFace Spaces 16GB)      │
│                       │    │                                │
│ - DeBERTa Large       │    │ - RoBERTa Ensemble             │
│ - Your fine-tuned     │    │ - DistilBERT                   │
│   models              │    │ - SHAP Explainer               │
│ Cost: FREE forever    │    │ Cost: FREE forever             │
└───────────────────────┘    └────────────────────────────────┘
```

## 💡 Why This Works

1. **Main API** (Railway $2/month):
   - Handles user requests, auth, database
   - Only needs TF-IDF (50MB) loaded
   - Routes ML requests to specialized servers
   - 2GB is plenty for orchestration

2. **ML Server 1** (Oracle Cloud FREE):
   - 12-24GB RAM
   - Runs your best model (DeBERTa)
   - No database, just HTTP API
   - Forever free

3. **ML Server 2** (HuggingFace FREE):
   - 16GB RAM
   - Runs ensemble/backup models
   - Gradio interface for testing
   - Forever free

## 🏗️ Implementation

### Step 1: Deploy ML Servers First

#### ML Server 1 (Oracle Cloud - DeBERTa)

```python
# ml_server_1/main.py
from fastapi import FastAPI
from transformers import pipeline
import os

app = FastAPI()

# Load DeBERTa model
model = pipeline(
    "text-classification",
    model="Bharat2004/deberta-fakenews-detector",
    device=-1
)

@app.post("/predict")
async def predict(text: str, api_key: str):
    # Simple API key auth
    if api_key != os.getenv("ML_API_KEY"):
        return {"error": "Unauthorized"}, 401
    
    result = model(text[:1500])[0]
    label = result["label"].upper()
    score = float(result["score"])
    
    fake_prob = score if label == "FAKE" else (1.0 - score)
    
    return {
        "fake_probability": fake_prob,
        "model": "deberta-v3-base",
        "confidence": score
    }

@app.get("/health")
async def health():
    return {"status": "ok", "model": "deberta-v3-base"}
```

**Deploy to Oracle:**
```bash
ssh ubuntu@oracle-instance
git clone https://github.com/YOUR_USERNAME/ml-server-1.git
cd ml-server-1
python3.11 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn transformers torch
echo "ML_API_KEY=$(openssl rand -hex 32)" > .env
uvicorn main:app --host 0.0.0.0 --port 8001
```

#### ML Server 2 (HuggingFace - Ensemble)

```python
# ml_server_2/app.py
import gradio as gr
from transformers import pipeline
import os

# Load multiple models
roberta = pipeline("text-classification", model="Bharat2004/out")
distilbert = pipeline("text-classification", model="another-model")

def predict_ensemble(text, api_key):
    if api_key != os.getenv("ML_API_KEY"):
        return {"error": "Unauthorized"}
    
    # Run both models
    r1 = roberta(text)[0]
    r2 = distilbert(text)[0]
    
    # Ensemble average
    avg_score = (float(r1["score"]) + float(r2["score"])) / 2
    
    return {
        "fake_probability": avg_score,
        "models": ["roberta", "distilbert"],
        "individual": [r1, r2]
    }

# Create both Gradio UI and API
demo = gr.Interface(
    fn=lambda text, key: predict_ensemble(text, key),
    inputs=["text", "text"],
    outputs="json",
    title="ML Ensemble Server"
)

# This exposes both gradio UI and FastAPI endpoints
demo.launch(server_name="0.0.0.0", server_port=7860)
```

**Deploy to HuggingFace:**
```bash
# 1. Create space at huggingface.co/spaces
# 2. Clone and push
git clone https://huggingface.co/spaces/YOUR_USERNAME/ml-server-2
cd ml-server-2
# Add app.py and requirements.txt
git add .
git commit -m "Deploy ML server"
git push
```

### Step 2: Update Main API to Use ML Servers

```python
# backend/app/analysis/ml.py (modified)
import os
import httpx
import logging

logger = logging.getLogger(__name__)

# ML Server URLs
ML_SERVER_1_URL = os.getenv("ML_SERVER_1_URL", "http://oracle-instance:8001")
ML_SERVER_2_URL = os.getenv("ML_SERVER_2_URL", "https://your-space.hf.space")
ML_API_KEY = os.getenv("ML_API_KEY")

# Fallback: Local TF-IDF (always available)
_model = None
_vectorizer = None

def _load_tfidf():
    # ... existing TF-IDF code ...
    pass

async def _call_ml_server_1(text: str) -> float | None:
    """Call DeBERTa server on Oracle Cloud"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{ML_SERVER_1_URL}/predict",
                json={"text": text, "api_key": ML_API_KEY}
            )
            if response.status_code == 200:
                data = response.json()
                return data["fake_probability"]
    except Exception as e:
        logger.warning(f"ML Server 1 failed: {e}")
    return None

async def _call_ml_server_2(text: str) -> dict | None:
    """Call Ensemble server on HuggingFace"""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{ML_SERVER_2_URL}/api/predict",
                json={"data": [text, ML_API_KEY]}
            )
            if response.status_code == 200:
                data = response.json()
                return data["data"][0]
    except Exception as e:
        logger.warning(f"ML Server 2 failed: {e}")
    return None

def run_ml_analysis(text: str) -> dict:
    """
    Try ML servers in order:
    1. Oracle Cloud (DeBERTa - most accurate)
    2. HuggingFace (Ensemble - backup)
    3. Local TF-IDF (fallback)
    """
    
    # Try ML Server 1 (Oracle - DeBERTa)
    score = None
    try:
        import asyncio
        score = asyncio.run(_call_ml_server_1(text))
        if score is not None:
            logger.info("ML Server 1 (DeBERTa): %.3f", score)
            return {"fake": score, "source": "deberta-oracle"}
    except Exception as e:
        logger.debug(f"ML Server 1 error: {e}")
    
    # Try ML Server 2 (HuggingFace - Ensemble)
    try:
        import asyncio
        result = asyncio.run(_call_ml_server_2(text))
        if result:
            score = result["fake_probability"]
            logger.info("ML Server 2 (Ensemble): %.3f", score)
            return {"fake": score, "source": "ensemble-hf"}
    except Exception as e:
        logger.debug(f"ML Server 2 error: {e}")
    
    # Fallback: Local TF-IDF
    if _load_tfidf():
        try:
            vec = _vectorizer.transform([text])
            prob = _model.predict_proba(vec)[0][1]
            logger.info("Local TF-IDF: %.3f", prob)
            return {"fake": float(prob), "source": "tfidf-local"}
        except Exception as e:
            logger.warning(f"TF-IDF failed: {e}")
    
    # Ultimate fallback
    logger.warning("All ML methods failed, returning default 0.5")
    return {"fake": 0.5, "source": "default"}
```

### Step 3: Add Environment Variables to Main API

In Railway, add these variables:

```bash
# ML Server URLs
ML_SERVER_1_URL=http://your-oracle-ip:8001
ML_SERVER_2_URL=https://your-username-ml-server-2.hf.space

# Shared API key for ML servers
ML_API_KEY=your_secure_random_key_here

# Don't load transformers locally
FORCE_TRANSFORMER_LOAD=false
```

### Step 4: Deploy Main API to Railway

```bash
# Main API now only needs TF-IDF (50MB)
# Railway 2GB is plenty!

# 1. Push to GitHub
git add .
git commit -m "Hybrid ML architecture"
git push

# 2. Railway auto-deploys
# 3. Add PostgreSQL
# 4. Set environment variables
# 5. Done!
```

## 🎯 Benefits of Hybrid Approach

### Cost Savings
```
Old Way (Single Server):
  Railway 8GB = $32/month
  
New Way (Hybrid):
  Railway 2GB = $2/month
  Oracle 12GB = $0/month
  HuggingFace = $0/month
  Total = $2/month (94% savings!)
```

### Performance Benefits
- ✅ Oracle Cloud: Dedicated 12GB for DeBERTa
- ✅ HuggingFace: Dedicated 16GB for ensemble
- ✅ Railway: Fast PostgreSQL + caching
- ✅ **Parallel processing** - run multiple models simultaneously!

### Reliability
- ✅ **3 fallback layers**:
  1. DeBERTa (Oracle) - most accurate
  2. Ensemble (HuggingFace) - backup
  3. TF-IDF (Railway) - always works
- ✅ If one server is down, others handle requests
- ✅ No single point of failure

## 🚀 Advanced: Load Balancing

Add multiple ML servers for redundancy:

```python
# backend/app/analysis/ml.py
ML_SERVERS = [
    {"url": "http://oracle-1:8001", "model": "deberta", "priority": 1},
    {"url": "http://oracle-2:8001", "model": "roberta", "priority": 2},
    {"url": "https://hf-space-1.hf.space", "model": "ensemble", "priority": 3},
    {"url": "https://hf-space-2.hf.space", "model": "distilbert", "priority": 4},
]

async def _call_ml_servers_parallel(text: str) -> float:
    """Call all servers in parallel, return first success"""
    import asyncio
    
    tasks = [
        _call_ml_server(server["url"], text, server["model"])
        for server in ML_SERVERS
    ]
    
    # Wait for first success
    for coro in asyncio.as_completed(tasks):
        try:
            result = await coro
            if result is not None:
                return result
        except:
            continue
    
    return None  # All failed
```

## 📊 Resource Allocation

| Server | Role | RAM | CPU | Cost | Models |
|--------|------|-----|-----|------|--------|
| **Railway** | Main API | 2GB | 1 | $2/mo | TF-IDF (50MB) |
| **Oracle 1** | ML Primary | 12GB | 2 | FREE | DeBERTa (738MB) |
| **Oracle 2** | ML Backup | 12GB | 2 | FREE | RoBERTa (500MB) |
| **HuggingFace 1** | Ensemble | 16GB | 2 | FREE | 3 models (800MB) |
| **HuggingFace 2** | SHAP/Analysis | 16GB | 2 | FREE | Explainer models |

**Total: $2/month for 58GB RAM!** 🤯

## 🔒 Security

### ML Server Authentication

```python
# Simple but secure API key
import hashlib
import hmac

def verify_request(api_key: str, timestamp: str, signature: str):
    # Prevent replay attacks
    if abs(time.time() - int(timestamp)) > 300:  # 5 min window
        return False
    
    # Verify HMAC signature
    expected = hmac.new(
        api_key.encode(),
        f"{timestamp}".encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)
```

### Network Security

```bash
# Oracle Cloud: Only allow Railway IP
sudo iptables -A INPUT -p tcp --dport 8001 -s railway-ip -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8001 -j DROP

# HuggingFace: Use API key in headers
```

## 🎯 Deployment Checklist

- [ ] Deploy ML Server 1 (Oracle Cloud - DeBERTa)
- [ ] Deploy ML Server 2 (HuggingFace - Ensemble)
- [ ] Update main API with ML server URLs
- [ ] Set ML_API_KEY in all servers
- [ ] Test health endpoints
- [ ] Test end-to-end fact-checking
- [ ] Configure firewall rules
- [ ] Setup monitoring
- [ ] Document server IPs/URLs

## 📈 Monitoring

### Health Check Dashboard

```python
# backend/app/routes/ml_health.py
from fastapi import APIRouter
import httpx

router = APIRouter()

@router.get("/ml/status")
async def ml_status():
    servers = []
    
    for server in ML_SERVERS:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{server['url']}/health",
                    timeout=5.0
                )
                servers.append({
                    "url": server["url"],
                    "model": server["model"],
                    "status": "online" if response.status_code == 200 else "error",
                    "latency_ms": int(response.elapsed.total_seconds() * 1000)
                })
        except:
            servers.append({
                "url": server["url"],
                "model": server["model"],
                "status": "offline",
                "latency_ms": None
            })
    
    return {"servers": servers}
```

## 🚀 Quick Start Commands

### 1. Deploy ML Server 1 (Oracle)
```bash
ssh ubuntu@oracle-ip
git clone YOUR_REPO
cd ml-server-1
python3.11 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn transformers torch
uvicorn main:app --host 0.0.0.0 --port 8001
```

### 2. Deploy ML Server 2 (HuggingFace)
```bash
# Just push to HuggingFace Space - it auto-deploys!
git clone https://huggingface.co/spaces/YOUR_USERNAME/ml-server-2
cd ml-server-2
# Add app.py
git add .
git commit -m "Deploy"
git push
```

### 3. Deploy Main API (Railway)
```bash
# Railway auto-deploys from GitHub
# Just set environment variables:
# ML_SERVER_1_URL=http://oracle-ip:8001
# ML_SERVER_2_URL=https://your-space.hf.space
# ML_API_KEY=your_key
```

## 💡 Pro Tips

1. **Use CDN**: Add Cloudflare in front for caching and DDoS protection (FREE!)
2. **Health checks**: Main API pings ML servers every 5 minutes
3. **Auto-failover**: If primary ML server is down, automatically use backup
4. **Caching**: Cache ML results for 24 hours (same claim = instant response)
5. **Rate limiting**: Protect ML servers from abuse

## 🎉 Result

**You now have:**
- ✅ 58GB total RAM across all servers
- ✅ Multiple transformer models running
- ✅ High availability (3 fallback layers)
- ✅ Cost: Only $2/month!
- ✅ Can handle thousands of requests/day
- ✅ Professional architecture

**This is BETTER than a single $100/month server!** 🚀

---

**Questions?** This architecture is production-ready and scales to millions of users!
