<!-- Copyright 2027 Bodapati Bharat Chandra. All rights reserved. -->
<!-- Licensed under the Apache License, Version 2.0 | SPDX-License-Identifier: Apache-2.0 -->

# FactCheckAI — Optimized Hybrid Infrastructure Plan

**Date:** July 11, 2026  
**UPDATED:** Render + Heroku + GitHub Student Pack Hybrid Architecture  

---

## 🎯 **FINAL DISTRIBUTED ARCHITECTURE: Smart ML Load Balancing**

**Total monthly cost: $0** (using GitHub Student Pack benefits strategically)

```
┌──────────────────────────────────────────────────────────────────┐
│  Chrome Extension (user's browser)                               │
│  Calls: https://your-app.onrender.com                           │
└────────────────────────┬─────────────────────────────────────────┘
                         │ HTTPS
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│  SERVER 1 — Render Free ($0/month)                              │
│  FastAPI Main Backend + ML Router                               │
│  • All API calls (Gemini, News, Search APIs)                   │
│  • User management, analytics, WebSocket                        │
│  • ML Request Router (decides which ML server to use)          │
│  • Handles: 90% of requests (lightweight operations)            │
└─────────┬────────────────┬────────────────┬────────────────────────┘
          │ Light ML       │ Medium ML      │ Heavy ML + SQL queries
          ▼                ▼                ▼                       
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│ SERVER 2        │ │ SERVER 3        │ │ SERVER 4        │ │ DATABASE         │
│ HEROKU Student  │ │ AZURE Student   │ │ HUGGINGFACE     │ │ Aiven PostgreSQL │
│ ($0 for 24mo)   │ │ ($0 for 12mo)   │ │ Spaces (FREE)   │ │ Free Forever     │
│                 │ │                 │ │                 │ │                  │
│ Light ML:       │ │ Medium ML:      │ │ Heavy ML:       │ │ • 1 CPU, 1GB RAM │
│ • TF-IDF        │ │ • DeBERTa-small │ │ • DeBERTa-large │ │ • 5GB storage    │
│ • Basic NLP     │ │ • Sentiment     │ │ • Ensemble      │ │ • SSL, backups   │
│ • Quick scoring │ │ • Multi-lang    │ │ • Batch process │ │ • Always on      │
│ • <200ms        │ │ • <1s response  │ │ • <5s response  │ │ • Cost: $0/mo    │
│                 │ │                 │ │                 │ │                  │
│ Resources:      │ │ Resources:      │ │ Resources:      │ └──────────────────┘
│ • 512MB RAM     │ │ • 1GB RAM       │ │ • 16GB RAM      │
│ • Always-on     │ │ • Always-on     │ │ • Auto-sleep    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 💡 **SMART ML WORKLOAD DISTRIBUTION**

### **🎯 ML Server Specialization Strategy**

| Server | ML Workload | Response Time | Use Cases | Resource Limits |
|--------|-------------|---------------|-----------|-----------------|
| **Heroku Eco** | Light ML (30%) | <200ms | TF-IDF, basic NLP, quick scoring | 512MB RAM |
| **Azure B1s** | Medium ML (50%) | <1s | DeBERTa-small, sentiment, multilingual | 1GB RAM |  
| **HuggingFace** | Heavy ML (20%) | <5s | DeBERTa-large, ensemble, batch processing | 16GB RAM |

### **📊 Request Routing Logic**

**Render FastAPI Backend (ML Router):**
```python
# Smart ML request routing based on complexity
def route_ml_request(text: str, analysis_type: str):
    
    # Light ML → Heroku (30% of requests)
    if analysis_type in ["quick_check", "basic_sentiment", "language_detect"]:
        if len(text) < 200:  # Short text
            return "heroku_ml_server"
    
    # Medium ML → Azure (50% of requests)  
    elif analysis_type in ["fact_check", "bias_detection", "credibility"]:
        if len(text) < 1000:  # Medium text
            return "azure_ml_server"
    
    # Heavy ML → HuggingFace (20% of requests)
    else:  # ensemble, batch, long text analysis
        return "huggingface_ml_server"
    
    # Fallback to Azure for medium complexity
    return "azure_ml_server"
```

---

## 🛠️ **DETAILED SERVER CONFIGURATIONS**

### **Server 1: Render Free — Main Backend + ML Router**

**Core Responsibilities:**
```python
✅ User authentication & management
✅ API integrations (Gemini, News, Search APIs)
✅ WebSocket connections & real-time features
✅ Analytics, history, chat functionality
✅ ML request routing and load balancing
✅ Response aggregation and caching
```

**ML Router Implementation:**
```python
# backend/app/analysis/ml_router.py
class MLRouter:
    def __init__(self):
        self.heroku_url = os.getenv("HEROKU_ML_URL")
        self.azure_url = os.getenv("AZURE_ML_URL") 
        self.hf_url = os.getenv("HF_ML_URL")
    
    async def predict(self, text: str, priority: str = "medium"):
        # Route based on text complexity and server availability
        server = self.select_server(text, priority)
        return await self.call_ml_server(server, text)
    
    def select_server(self, text: str, priority: str):
        text_len = len(text)
        
        # Light processing → Heroku (fast, limited RAM)
        if priority == "fast" or text_len < 200:
            return "heroku"
            
        # Heavy processing → HuggingFace (powerful, may sleep)
        elif priority == "accuracy" or text_len > 2000:
            return "huggingface"
            
        # Default → Azure (balanced performance)
        else:
            return "azure"
```

---

### **Server 2: Heroku Eco Dyno — Light ML Processing**

**Optimized for:** Fast, lightweight ML operations
**GitHub Student Benefit:** $13/month × 24 months = $312 value

```python
# Heroku ML Server - Lightweight Models Only
class HerokuMLServer:
    models = {
        "tfidf": "Pre-trained TF-IDF vectorizer (200MB)",
        "basic_sentiment": "Lightweight BERT-tiny (50MB)", 
        "language_detect": "FastText language model (100MB)",
        "quick_scorer": "Logistic regression ensemble (10MB)"
    }
    
    # Total RAM usage: ~400MB (within 512MB Eco limit)
    
    def predict_quick(self, text: str):
        # Ultra-fast TF-IDF prediction
        return self.tfidf_model.predict(text)  # ~50ms
        
    def detect_language(self, text: str):
        # Fast language detection  
        return self.lang_model.predict(text)   # ~20ms
```

**Heroku Configuration:**
```yaml
# Eco Dyno Resources
RAM: 512MB
CPU: 0.5 vCPU shared
Uptime: Always-on (no sleep)
Network: Fast (US-based)
Cost: $5/month (covered by student credits)
```

---

### **Server 3: Azure B1s VM — Medium ML Processing** 

**Optimized for:** Balanced ML workload, main inference server
**GitHub Student Benefit:** $100 credit × 12 months

```python
# Azure ML Server - Medium Complexity Models
class AzureMLServer:
    models = {
        "deberta_small": "microsoft/deberta-v3-small (400MB)",
        "sentiment_xlm": "cardiffnlp/twitter-xlm-roberta-base (500MB)",
        "bias_detector": "unitary/toxic-bert (400MB)",
        "credibility_scorer": "Custom fine-tuned model (300MB)"
    }
    
    # Total RAM usage: ~800MB (within 1GB B1s limit)
    
    def predict_medium(self, text: str):
        # Main fact-checking pipeline
        return self.deberta_small.predict(text)  # ~800ms
        
    def analyze_bias(self, text: str):
        # Bias and toxicity detection
        return self.bias_detector.predict(text)  # ~600ms
```

**Azure B1s Configuration:**
```yaml
# Azure for Students VM
RAM: 1GB  
CPU: 1 vCPU
Uptime: 750 hours/month (always-on within limit)
Network: Global regions available
Cost: ~$8/month (covered by $100 student credit)
```

---

### **Server 4: HuggingFace Spaces — Heavy ML Processing**

**Optimized for:** Most accurate models, complex ensemble predictions
**Cost:** Free forever (community plan)

```python
# HuggingFace Spaces - Heavy Models
class HuggingFaceMLServer:
    models = {
        "deberta_large": "microsoft/deberta-v3-large (1.4GB)",
        "ensemble_model": "Multiple models for voting (3GB)",
        "fact_checker_xl": "Your fine-tuned XL model (2GB)", 
        "multi_modal": "CLIP + OCR models (2GB)"
    }
    
    # Total RAM usage: ~8GB (within 16GB HF Spaces limit)
    
    def predict_ensemble(self, text: str):
        # Most accurate prediction using multiple models
        predictions = []
        for model in self.ensemble_models:
            pred = model.predict(text)
            predictions.append(pred)
        return self.vote(predictions)  # ~4s
        
    def analyze_multimodal(self, text: str, image_url: str):
        # Text + image analysis  
        return self.multimodal_model.predict(text, image_url)  # ~6s
```

**HuggingFace Spaces Configuration:**
```yaml
# Community Spaces (Free)
RAM: 16GB
CPU: 2 vCPU  
GPU: None (CPU inference)
Uptime: Auto-sleep after inactivity (kept alive by requests)
Network: Global CDN
Cost: FREE forever
```

---

## 📊 **PERFORMANCE & LOAD DISTRIBUTION**

### **Expected Request Distribution**
```
Daily Usage (1000 users × 10 requests = 10,000 requests):

┌─────────────────────────────────────────────────────────────┐
│ Light ML (30%) → Heroku:     3,000 requests               │
│ • Quick fact-checks          • Language detection          │
│ • Basic sentiment            • TF-IDF scoring             │
│ • Average: 100ms response    • Always available           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Medium ML (50%) → Azure:     5,000 requests               │  
│ • Standard fact-checking     • Bias detection              │
│ • Credibility analysis       • Multilingual support       │
│ • Average: 800ms response    • Reliable uptime            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Heavy ML (20%) → HuggingFace: 2,000 requests              │
│ • Ensemble predictions       • Complex analysis            │
│ • Multimodal processing      • Batch operations           │
│ • Average: 4s response       • May have cold starts       │
└─────────────────────────────────────────────────────────────┘
```

### **Failover Strategy**
```python
# Intelligent failover system
async def predict_with_fallback(text: str):
    try:
        # Try optimal server first
        optimal_server = select_optimal_server(text)
        return await call_server(optimal_server, text)
        
    except ServerUnavailableError:
        # Fallback to next best server
        fallback_server = get_fallback_server(optimal_server)
        return await call_server(fallback_server, text)
        
    except AllServersDownError:
        # Final fallback to local/cached model
        return await local_model_predict(text)
```

---

## 💰 **REVISED COST BREAKDOWN**

### **Monthly Costs with Student Benefits**
| Service | Regular Cost | Student Benefit | Effective Cost | Coverage |
|---------|--------------|-----------------|----------------|----------|
| Render Free | $0 | N/A | $0 | Forever |
| Heroku Eco | $5/month | $13/month credit | $0 | 24 months |
| Azure B1s VM | $8/month | $100 credit | $0 | 12 months |  
| HuggingFace Spaces | $0 | N/A | $0 | Forever |
| Aiven PostgreSQL | $0 | N/A | $0 | Forever |
| **TOTAL** | **$13/month** | **Various** | **$0** | **12-24 months** |

### **After Student Credits Expire**
| Scenario | Cost | Alternative |
|----------|------|-------------|
| Keep all servers | $13/month | Continue if profitable |
| Optimize costs | $0/month | Migrate Heroku → HF Spaces, Azure → Oracle Always Free |
| Scale up | $20+/month | Upgrade for growth |

---

## 💰 **COST BREAKDOWN & COVERAGE**

### **Monthly Costs**
| Service | Plan | Cost | Student Coverage |
|---------|------|------|------------------|
| Render Web Service | Free | $0 | Forever |
| Heroku Eco Dyno | $5/month | $0 | 24 months ($13 credit) |
| Heroku Mini Postgres | $5/month | $0 | 24 months (backup DB) |
| Aiven PostgreSQL | Free | $0 | Forever |
| Additional Services | Various | $0 | Student pack benefits |
| **TOTAL** | | **$0** | **24+ months** |

### **After Student Credits Expire (Month 25+)**
| Service | Cost | Alternative |
|---------|------|-------------|
| Render Free | $0 | Continue |
| Aiven PostgreSQL | $0 | Continue |
| Heroku ML Server | $10/month | Migrate to HuggingFace Spaces (free) |
| **TOTAL** | **$0-10/month** | **Fully scalable** |

---

## 🚀 **DEPLOYMENT ARCHITECTURE DETAILS**

### **Server 1: Render Free — Main Backend**

**Configuration:**
```yaml
# render.yaml (already configured)
services:
  - type: web
    name: factcheckai-main
    env: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    
# Environment Variables:
DATABASE_URL: postgresql://aiven-connection-string
ML_SERVER_URL: https://your-heroku-ml.herokuapp.com
GEMINI_API_KEY: your_key
GROQ_API_KEY: your_key (fallback)
NEWS_API_KEY: your_key
TAVILY_API_KEY: your_key
```

**Handles Routes:**
```python
# Main FastAPI routes on Render
/auth/*          # Authentication & user management
/analytics/*     # Analytics and reporting  
/history/*       # User history
/chat/*          # Chat functionality
/upload/*        # File uploads
/health          # Health checks
/ws/*            # WebSocket connections
```

---

### **Server 2: Heroku — ML Inference Server**

**Configuration:**
```python
# Specialized ML server on Heroku
# File: ml_server.py (deploy separately)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = FastAPI()
model = None
tokenizer = None

@app.on_event("startup")
def load_ml_models():
    global model, tokenizer
    model_name = "Bharat2004/out"  # Your fine-tuned model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()

class MLRequest(BaseModel):
    text: str
    api_key: str

@app.post("/ml/predict")
def predict_fake_news(request: MLRequest):
    # ML inference logic here
    inputs = tokenizer(request.text[:512], return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        fake_prob = float(probs[0][1])
    
    return {"fake_probability": fake_prob, "model": "deberta-finetuned"}

# Procfile for Heroku ML server:
# web: uvicorn ml_server:app --host 0.0.0.0 --port $PORT
```

---

### **Database: Aiven PostgreSQL**

**Why Aiven for Database:**
- ✅ **Free forever** (no time limits like Render's 90-day DB)
- ✅ **Professional features** (SSL, automated backups)
- ✅ **5GB storage** (sufficient for app data)
- ✅ **No credit card required**
- ✅ **Stays awake** (your apps keep it active)

---

## 🛠️ **ADDITIONAL GITHUB STUDENT PACK SERVICES**

### **Monitoring & Analytics Stack**
```
📊 Datadog (2 years free Pro)
├── Infrastructure monitoring
├── APM (Application Performance)  
├── Log aggregation
└── Custom dashboards

🔍 New Relic (Free forever for students)
├── Full-stack observability
├── Error tracking
├── Performance insights  
└── Real user monitoring

🚨 Sentry (Free with 50K events)
├── Error tracking
├── Performance monitoring
├── Release tracking
└── Issue alerting
```

### **Caching & Storage**
```
🗄️ MongoDB Atlas ($50 credit)
├── Analytics data caching
├── User session storage
├── Search result caching
└── Temporary file storage

📁 Microsoft Azure (Age 18+: $100 credit)
├── Blob Storage for files
├── Redis Cache alternative
├── Background job processing
└── Additional compute if needed
```

### **Domain & SSL**
```
🌐 Namecheap (1 year free)
├── .me domain registration
├── SSL certificate
├── DNS management
└── Email forwarding

🔧 Name.com (Free premium domains)
├── .dev, .app, .live domains
├── Professional email
├── Advanced DNS
└── Domain privacy
```

---

## 🔄 **REQUEST FLOW ARCHITECTURE**

### **Lightweight Requests (90%) → Render**
```
User Request → Render FastAPI → Response
└── Auth, CRUD, API calls, WebSocket
```

### **Heavy ML Requests (10%) → Heroku**
```
User Request → Render FastAPI → Heroku ML Server → Response
└── Text analysis → DeBERTa inference → Fake news score
```

### **Database Operations → Aiven**
```
All Servers → Aiven PostgreSQL → Data Storage/Retrieval
└── User data, history, analytics, cache
```

---

## 📈 **SCALABILITY & PERFORMANCE**

### **Traffic Distribution**
```
┌─────────────────────────────────────────────────────────────┐
│ Expected Daily Usage:                                       │
│ • 1000 users × 10 requests = 10,000 requests/day          │
│ • 9,000 lightweight (Render) - auth, history, chat        │
│ • 1,000 heavy ML (Heroku) - fact-checking inference       │
│                                                            │
│ Performance:                                               │
│ • Render: <200ms response time (CRUD operations)           │
│ • Heroku: <2s response time (ML inference)                │
│ • Aiven: <50ms query time (database operations)           │
└─────────────────────────────────────────────────────────────┘
```

### **Growth Path**
```
Phase 1 (0-1K users): Current hybrid architecture (Free)
Phase 2 (1K-10K users): Upgrade Render to Starter ($7/mo)
Phase 3 (10K+ users): Scale Heroku dynos, add Redis caching
Phase 4 (Enterprise): Migrate to dedicated infrastructure
```

---

## 🎯 **SUCCESS METRICS & MONITORING**

### **Performance Targets**
- ✅ **99.5% Uptime** (with UptimeRobot + Heroku always-on)
- ✅ **<3s Total Response Time** (including ML inference)
- ✅ **<2s Authentication** (cached on Render)
- ✅ **<5s Fact-Check Analysis** (optimized ML pipeline)

### **Monitoring Stack**
```
🔍 Real-time Monitoring:
├── UptimeRobot (external uptime monitoring)
├── Datadog (infrastructure metrics)
├── New Relic (application performance)
├── Sentry (error tracking)
└── Built-in platform metrics (Render + Heroku)
```

---

## 🚀 **DEPLOYMENT SEQUENCE**

### **Phase 1: Core Infrastructure (Day 1)**
1. **Setup Aiven PostgreSQL** (15 minutes)
   - Create free account, provision database
   - Configure SSL connections
   
2. **Deploy Render Main Backend** (20 minutes)
   - Connect GitHub repository
   - Configure environment variables
   - Deploy with existing render.yaml

3. **Setup UptimeRobot** (5 minutes)
   - Create free account
   - Add HTTP monitor for Render app
   - Configure 5-minute ping interval

### **Phase 2: ML Server (Day 2)**
1. **Activate Heroku Student Pack** (10 minutes)
   - Connect GitHub Student Pack account
   - Activate $13/month credit for 24 months

2. **Deploy ML Server to Heroku** (30 minutes)
   - Create specialized ML FastAPI app
   - Deploy with Procfile and requirements
   - Test ML inference endpoints

3. **Connect Services** (15 minutes)
   - Update Render app with Heroku ML server URL
   - Configure API authentication between servers
   - Test end-to-end ML pipeline

### **Phase 3: Enhanced Services (Week 1)**
1. **Activate Additional Student Benefits**
   - Datadog (monitoring)
   - New Relic (observability)  
   - Sentry (error tracking)
   - Namecheap (custom domain)

2. **Configure Monitoring**
   - Setup dashboards and alerts
   - Configure error notifications
   - Performance baseline establishment

---

## 🏆 **FINAL ARCHITECTURE ADVANTAGES**

### **Cost Efficiency**
- ✅ **$0/month for 24+ months**
- ✅ **$312 in Heroku student credits**
- ✅ **$50+ in additional service credits**
- ✅ **Professional monitoring worth $300+/month**

### **Performance Optimization**  
- ✅ **Specialized servers** for different workloads
- ✅ **No cold starts** for ML inference (Heroku Eco)
- ✅ **Always-on database** (Aiven)
- ✅ **Keep-alive strategy** for Render free tier

### **Professional Features**
- ✅ **Full observability stack** (monitoring, logging, errors)
- ✅ **Custom domain** with SSL
- ✅ **Automated deployments** from GitHub
- ✅ **Database backups** and security
- ✅ **Horizontal scaling** capabilities

### **Learning Value**
- ✅ **Multi-platform DevOps** experience
- ✅ **Microservices architecture** patterns
- ✅ **Production monitoring** setup
- ✅ **Cost optimization** strategies
- ✅ **Resume-worthy** technology stack

**This hybrid architecture maximizes your GitHub Student Pack benefits while delivering professional-grade performance and reliability!** 🎉

---

## Server 1 — Render Free (FastAPI Backend)

### Specs
| Resource | Value |
|---|---|
| RAM | 512 MB |
| CPU | 0.1 vCPU (shared) |
| Bandwidth | 100 GB/month |
| Sleep | After 15 minutes of inactivity |
| Wake time | 2–3 minutes cold start |
| Free hours | 750/month (enough for 1 always-on service) |
| Cost | **$0/mo forever** |

### The sleep problem — solved with UptimeRobot

Render's free tier sleeps after 15 minutes. You **cannot** prevent this from inside Render itself (self-pings are blocked). The solution is an external free pinger.

**UptimeRobot** (free plan):
- 50 monitors, 5-minute check interval — free forever
- Go to [uptimerobot.com](https://uptimerobot.com) → Add Monitor → HTTP(S)
- URL: `https://<your-app>.onrender.com/health`
- Interval: 5 minutes
- This keeps your app permanently awake at zero cost

The background scheduler in `main.py` handles the HF Spaces keep-alive separately (pings ML Server 2 every 14 minutes from inside the app).

### Deployment steps

1. Push code to GitHub (secrets removed, `.env` untracked)
2. Go to [render.com](https://render.com) → New → Blueprint
3. Connect your GitHub repo → Render reads `render.yaml` automatically
4. Set these env vars manually in Render Dashboard → Environment:
   ```
   DATABASE_URL      = postgresql://avnadmin:<pw>@<host>:<port>/<db>?sslmode=require
   CEREBRAS_API_KEY  = <rotated key>
   GROQ_API_KEY      = <rotated key>
   GEMINI_API_KEY    = <rotated key>
   TAVILY_API_KEY    = <rotated key>
   NEWS_API_KEY      = <rotated key>
   SERPAPI_KEY       = <rotated key>
   GOOGLE_FACTCHECK_API_KEY = <rotated key>
   GOOGLE_CLIENT_ID  = <your OAuth client ID>
   BREVO_API_KEY     = <rotated key>
   SMTP_USER         = factcheckai2@gmail.com
   ML_SERVER_1_URL   = http://<your-DO-ip>:8001
   ML_SERVER_2_URL   = https://<user>-<space>.hf.space
   ML_API_KEY        = <openssl rand -hex 32>
   HF_TOKEN          = <new HF token>
   ```
5. JWT_SECRET is auto-generated by Render (from `generateValue: true` in render.yaml)
6. Set up UptimeRobot ping to `/health` every 5 minutes

---

## Database — Aiven PostgreSQL Free

### Specs (confirmed from Aiven docs)
| Resource | Value |
|---|---|
| RAM | 1 GB |
| CPU | 1 vCPU |
| Storage | 5 GB |
| Max connections | ~25 (1GB RAM tier) — enough for your app |
| SSL | Required (enforced) |
| Backups | Automated daily |
| Time limit | **None — free forever** |
| Credit card | **Not required** |
| Inactivity shutdown | Yes — powers off if unused. Your running app prevents this |
| Cost | **$0/mo forever** |

### One important caveat
Aiven **can power off the DB if it detects inactivity** (they send an email warning first). Since your Render app is always running and making queries, this will never trigger in practice. If you ever pause the app for weeks, just log into Aiven console and click Power On — data is preserved.

### Setup steps

1. Go to [aiven.io](https://aiven.io) → Sign up (no credit card)
2. Create Service → PostgreSQL → Free tier
3. Wait ~2 minutes for provisioning
4. Go to Service → Overview → Connection information
5. Copy the **Service URI** — it looks like:
   ```
   postgresql://avnadmin:<password>@<host>.aivencloud.com:<port>/defaultdb?sslmode=require
   ```
6. Paste this as `DATABASE_URL` in Render's environment variables
7. Run migrations: Alembic runs automatically on first Render deploy (`alembic upgrade head` in start command)

### Connection pool setting
Your `database.py` already has `pool_size=5`, `max_overflow=10`. With ~25 max connections on Aiven free tier, reduce max_overflow to stay safe:

```python
# database.py — change for Aiven free tier
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=3,          # reduced from 5
    max_overflow=5,       # reduced from 10
    pool_timeout=30,
    pool_recycle=1800,
)
```

---

## Server 2 — DigitalOcean Droplet (ML Inference)

### What to deploy
A lightweight FastAPI inference server that loads DeBERTa once and serves `/predict` requests. Your `ml.py` already calls this as `ML_SERVER_1_URL`.

### Recommended droplet
**Basic 4GB — $24/month** → your $200 DO student credit covers **8 months**

| Resource | Value |
|---|---|
| RAM | 4 GB |
| vCPU | 2 vCPU |
| Storage | 80 GB SSD |
| DeBERTa model RAM usage | ~2–3 GB |
| Remaining for OS/FastAPI | ~1 GB |
| Always-on | ✅ Yes — VPS never sleeps |
| Cost | $0 from $200 credit (8 months) |

### Setup on DigitalOcean

**Step 1 — Create droplet:**
- Dashboard → Create → Droplets
- Ubuntu 24.04 LTS, Basic, 4GB/2vCPU ($24/mo)
- Add SSH key or use password
- Region: nearest to your users (Singapore, Frankfurt, NYC)

**Step 2 — Install and run inference server:**
```bash
# SSH into droplet
ssh root@<your-do-ip>

# Install Python and dependencies
apt update && apt install -y python3.11 python3-pip git nginx

# Clone repo or upload just the inference server files
git clone https://github.com/<you>/<repo>.git
cd <repo>/backend

# Install inference-only requirements (no torch GPU, CPU only)
pip install fastapi uvicorn httpx transformers torch --extra-index-url \
  https://download.pytorch.org/whl/cpu

# Create a simple inference server
cat > /root/ml_server.py << 'EOF'
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
_model = None
_tokenizer = None
ML_API_KEY = os.getenv("ML_API_KEY", "")

def load_model():
    global _model, _tokenizer
    if _model is None:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch
        model_name = os.getenv("DEBERTA_MODEL", "Bharat2004/out")
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSequenceClassification.from_pretrained(model_name)
        _model.eval()

class PredictRequest(BaseModel):
    text: str
    api_key: str

@app.on_event("startup")
def startup():
    load_model()

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": _model is not None}

@app.post("/predict")
def predict(req: PredictRequest):
    if ML_API_KEY and req.api_key != ML_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    import torch, time
    t0 = time.time()
    inputs = _tokenizer(req.text[:512], return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = _model(**inputs).logits
        probs = torch.softmax(logits, dim=1)[0]
    fake_prob = float(probs[1])
    ms = int((time.time() - t0) * 1000)
    return {"fake_probability": round(fake_prob, 4), "inference_time_ms": ms}
EOF

# Run as systemd service (survives reboots)
cat > /etc/systemd/system/mlserver.service << 'EOF'
[Unit]
Description=FactCheckAI ML Inference Server
After=network.target

[Service]
User=root
WorkingDirectory=/root
Environment="ML_API_KEY=<your-ml-api-key>"
Environment="DEBERTA_MODEL=Bharat2004/out"
ExecStart=/usr/bin/python3 -m uvicorn ml_server:app --host 0.0.0.0 --port 8001 --workers 1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable mlserver
systemctl start mlserver

# Firewall — only allow port 8001 from Render's IPs (or all IPs for simplicity)
ufw allow 22
ufw allow 8001
ufw enable
```

**Step 3 — Set in Render:**
```
ML_SERVER_1_URL = http://<your-do-ip>:8001
ML_API_KEY      = <same key as in systemd service>
```

---

## Server 3 — Azure for Students (Background Workers)

### What you get
- **$100 credit**, valid 12 months (no credit card needed for students)
- **B1s VM free**: 1 vCPU, 1 GB RAM, 750 hours/month = always-on
- **Azure PostgreSQL Flexible Server free**: 750 hours/month B1MS instance, 32 GB storage

### Best use for this project
Use Azure as the **backup database** and **background worker** host:

| Service | Azure tier | Cost from credit |
|---|---|---|
| B1s VM (workers, Redis, cron) | Free 750h/month | ~$0 |
| PostgreSQL Flexible Server B1MS | Free 750h/month | ~$0 |
| Blob Storage | 5 GB LRS free always | $0 |

**Priority:** Get Render + Aiven working first. Add Azure in week 2 for Redis (proper rate limiting across multiple workers) and Celery background jobs.

---

## HuggingFace Spaces — Backup ML Server

Run your transformer model as a Gradio app on HF Spaces free tier:
- 16 GB RAM, 2 vCPU — enough for DeBERTa
- Sleeps after inactivity — your app's keep-alive ping every 14 min prevents this
- Set as `ML_SERVER_2_URL` (backup when DO droplet is down)
- Cost: **$0/mo forever**

---

## Complete Cost Summary

| Service | Provider | Monthly cost | Notes |
|---|---|---|---|
| FastAPI backend | Render Free | **$0** | Keep-alive via UptimeRobot |
| PostgreSQL DB | Aiven Free | **$0** | No time limit, 5GB storage |
| ML inference (primary) | DigitalOcean | **$0** | $200 student credit, 8 months |
| ML inference (backup) | HuggingFace Spaces | **$0** | Free forever, 16GB RAM |
| Background workers | Azure for Students | **$0** | $100 credit, 12 months |
| Keep-alive pinger | UptimeRobot Free | **$0** | 50 monitors free |
| **TOTAL** | | **$0/mo** | |

**After all credits expire:**
- Render + Aiven + HF Spaces: still $0
- DO inference server: $24/mo (or switch to HF Spaces primary)
- Azure workers: ~$15/mo for B1s VM

---

## Deployment Order

### Day 1 — Database
1. Sign up at [aiven.io](https://aiven.io) — no card needed
2. Create free PostgreSQL service
3. Copy connection URI

### Day 1 — Backend
1. Ensure all secrets removed from git (`.env` untracked)
2. Commit `render.yaml` and model `.joblib` files
3. Sign up at [render.com](https://render.com)
4. New → Blueprint → connect repo → Render reads `render.yaml`
5. Set all env vars in Render dashboard
6. Deploy — watch logs for `Alembic migrations applied`
7. Set up UptimeRobot ping to `/health` every 5 minutes

### Day 2 — ML Server
1. Create DO droplet (Basic 4GB, Ubuntu 24.04) using your $200 credit
2. SSH in, follow setup steps above
3. Add `ML_SERVER_1_URL` to Render env vars
4. Redeploy Render service (or env var change triggers redeploy automatically)

### Day 3 — Extension
1. Update `extension/popup/config.js` with your Render URL (already done in this branch)
2. Update `extension/manifest.json` host_permissions with Render URL
3. Package extension: `zip -r factcheckai-extension.zip extension/`
4. Submit to Chrome Web Store

### Week 2 — Azure
1. Activate Azure for Students via GitHub Student Pack
2. Create B1s VM in East US or West Europe
3. Install Redis + Celery for proper async workers
4. Optionally migrate DB to Azure PostgreSQL for more headroom

---

## Files Changed by This Plan

| File | Change |
|---|---|
| `render.yaml` | Created — Render auto-deploy config |
| `backend/app/main.py` | Keep-alive scheduler, async subprocess, Alembic migrations |
| `backend/app/analysis/ml.py` | Removed `asyncio.run()`, switched to sync httpx |
| `backend/app/auth.py` | JWT_SECRET fail-fast, no insecure default |
| `extension/popup/config.js` | Production URL uncommented |
| `backend/database.py` | Reduce pool_size/max_overflow for Aiven free tier |
| `INFRASTRUCTURE_PLAN.md` | This file |

## 🚀 **DISTRIBUTED DEPLOYMENT SEQUENCE**

### **Phase 1: Core Infrastructure (Day 1)**

#### 1.1 **Setup Aiven PostgreSQL** (15 minutes)
```bash
# 1. Create free Aiven account (no credit card)
# Visit: https://aiven.io/
# 2. Create PostgreSQL service (Free tier)  
# 3. Copy connection string for all servers
DATABASE_URL="postgresql://user:pass@host:port/db?sslmode=require"
```

#### 1.2 **Deploy Render Main Backend** (20 minutes)
```bash
# Main backend with ML routing logic
git add .
git commit -m "Add distributed ML architecture"  

# Deploy to Render (using existing render.yaml)
# Set environment variables:
DATABASE_URL=postgresql://aiven-connection
HEROKU_ML_URL=https://your-ml-heroku.herokuapp.com
AZURE_ML_URL=https://your-ml-azure.azurewebsites.net
HF_ML_URL=https://your-username-ml.hf.space
```

#### 1.3 **Setup UptimeRobot Keep-Alive** (5 minutes)
```bash
# Visit: https://uptimerobot.com (free account)
# Add monitor: https://your-app.onrender.com/health  
# Interval: 5 minutes
```

---

### **Phase 2: Light ML Server - Heroku (Day 2)**

#### 2.1 **Activate Heroku Student Pack** (10 minutes)
```bash
# 1. Visit: https://www.heroku.com/github-students
# 2. Connect GitHub Student account
# 3. Verify $13/month credit for 24 months
```

#### 2.2 **Deploy Heroku ML Server** (30 minutes)
```bash
# Create specialized light ML server
cd heroku-ml-server/

# Create Heroku app
heroku create your-ml-heroku

# Add minimal Postgres for caching (covered by credits)
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set \
  ML_API_KEY="$(openssl rand -hex 32)" \
  DEBERTA_MODEL="distilbert-base-uncased" \
  ENVIRONMENT="production"

# Deploy
git add .
git commit -m "Light ML server for Heroku"
git push heroku main

# Test endpoint
curl https://your-ml-heroku.herokuapp.com/health
```

---

### **Phase 3: Medium ML Server - Azure (Day 3)**

#### 3.1 **Activate Azure for Students** (15 minutes)
```bash
# 1. Visit: https://azure.microsoft.com/en-us/free/students/
# 2. Verify with GitHub Student Pack
# 3. Get $100 credit for 12 months (age 18+)
```

#### 3.2 **Create Azure App Service** (45 minutes)
```bash
# Create Resource Group
az group create --name factcheckai-rg --location "East US"

# Create App Service Plan (B1 Basic tier)
az appservice plan create \
  --name factcheckai-plan \
  --resource-group factcheckai-rg \
  --sku B1 \
  --is-linux

# Create Web App (Python 3.11)
az webapp create \
  --name your-ml-azure \
  --resource-group factcheckai-rg \
  --plan factcheckai-plan \
  --runtime "PYTHON|3.11"

# Configure deployment from GitHub
az webapp deployment source config \
  --name your-ml-azure \
  --resource-group factcheckai-rg \
  --repo-url https://github.com/yourusername/azure-ml-server \
  --branch main \
  --manual-integration

# Set environment variables  
az webapp config appsettings set \
  --name your-ml-azure \
  --resource-group factcheckai-rg \
  --settings \
    ML_API_KEY="same_as_heroku" \
    DEBERTA_MODEL="microsoft/deberta-v3-small" \
    DATABASE_URL="aiven_connection_string"
```

---

### **Phase 4: Heavy ML Server - HuggingFace Spaces (Day 4)**

#### 4.1 **Create HuggingFace Space** (20 minutes)
```python
# 1. Visit: https://huggingface.co/spaces
# 2. Create new Space: "your-username/factcheckai-ml"
# 3. Choose: Gradio, Python SDK
# 4. Upload files: app.py, requirements.txt

# app.py for HuggingFace Spaces
import gradio as gr
from transformers import pipeline

# Load heavy models
ensemble_models = [
    pipeline("text-classification", "microsoft/deberta-v3-large"),
    pipeline("text-classification", "your-finetuned-model"),
]

def predict_ensemble(text):
    predictions = []
    for model in ensemble_models:
        pred = model(text)
        predictions.append(pred[0]['score'])
    
    # Ensemble voting
    final_score = sum(predictions) / len(predictions)
    return {"fake_probability": final_score}

# Create Gradio interface  
demo = gr.Interface(
    fn=predict_ensemble,
    inputs="text", 
    outputs="json",
    title="FactCheckAI Heavy ML Server"
)

if __name__ == "__main__":
    demo.launch()
```

#### 4.2 **Test HuggingFace Deployment**
```bash
# Space will be available at:
# https://your-username-factcheckai-ml.hf.space

# Test API endpoint
curl -X POST https://your-username-factcheckai-ml.hf.space/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["This is a test article about politics"]}'
```

---

### **Phase 5: Connect & Test Full Pipeline (Day 5)**

#### 5.1 **Update Render with All ML Endpoints**
```bash
# Update environment variables in Render
HEROKU_ML_URL=https://your-ml-heroku.herokuapp.com
AZURE_ML_URL=https://your-ml-azure.azurewebsites.net  
HF_ML_URL=https://your-username-factcheckai-ml.hf.space
ML_API_KEY=shared_key_across_all_servers

# Redeploy Render app
git add .
git commit -m "Connect all ML servers"
git push origin main  # Auto-deploys to Render
```

#### 5.2 **End-to-End Testing**
```bash
# Test light ML (should route to Heroku)
curl -X POST https://your-app.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Quick test", "priority": "fast"}'

# Test medium ML (should route to Azure)  
curl -X POST https://your-app.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a longer article that needs deeper analysis...", "priority": "medium"}'

# Test heavy ML (should route to HuggingFace)
curl -X POST https://your-app.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Very long complex article...", "priority": "accuracy"}'
```

---

## 📊 **MONITORING & OPTIMIZATION**

### **Performance Monitoring**
```python
# ML Router with performance tracking
class MLRouter:
    def __init__(self):
        self.performance_stats = {
            "heroku": {"avg_time": 0, "success_rate": 0, "load": 0},
            "azure": {"avg_time": 0, "success_rate": 0, "load": 0}, 
            "hf": {"avg_time": 0, "success_rate": 0, "load": 0}
        }
    
    def select_optimal_server(self, text: str):
        # Choose based on current load and performance
        if len(text) < 200 and self.performance_stats["heroku"]["load"] < 80:
            return "heroku"
        elif self.performance_stats["azure"]["success_rate"] > 0.95:
            return "azure"  
        else:
            return "hf"  # Fallback to most powerful
```

### **Load Balancing Strategy**
```yaml
Traffic Distribution Goals:
- Heroku (Light): 30% of requests, <200ms response
- Azure (Medium): 50% of requests, <1s response  
- HuggingFace (Heavy): 20% of requests, <5s response

Auto-scaling Triggers:
- If Heroku load > 80%: Route light requests to Azure
- If Azure unavailable: Route medium requests to HuggingFace
- If HuggingFace sleeping: Wake with ping, queue requests
```

---

## 🎯 **FINAL ARCHITECTURE ADVANTAGES**

### **Optimal Resource Utilization**
- ✅ **Light ML on Heroku**: Perfect for 512MB RAM constraint
- ✅ **Medium ML on Azure**: Ideal for 1GB RAM B1s instance  
- ✅ **Heavy ML on HuggingFace**: Leverages 16GB RAM for complex models
- ✅ **Smart routing**: Automatic load balancing based on request complexity

### **Cost Efficiency**  
- ✅ **$0/month for 12-24 months** using student credits strategically
- ✅ **Forever free fallback** (Render + HuggingFace + Aiven)
- ✅ **No over-provisioning** - each server optimized for its workload
- ✅ **Graceful scaling** - can upgrade individual components as needed

### **Performance & Reliability**
- ✅ **No single point of failure** - multiple ML servers with failover
- ✅ **Optimized response times** - right model for right complexity
- ✅ **Always-on core services** - Heroku Eco + Azure B1s never sleep
- ✅ **Intelligent caching** - results cached across all servers

### **Professional Development Experience**
- ✅ **Microservices architecture** patterns and best practices
- ✅ **Multi-cloud deployment** experience (Render + Heroku + Azure + HF)
- ✅ **Load balancing** and distributed systems knowledge
- ✅ **ML operations** (MLOps) pipeline management
- ✅ **Production monitoring** and optimization skills

**This distributed architecture maximizes your GitHub Student Pack benefits while delivering enterprise-grade performance, reliability, and learning value!** 🎉