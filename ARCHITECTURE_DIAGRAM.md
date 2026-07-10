# Architecture Diagrams

Visual guides to understand FactCheckAI's multi-server architecture.

---

## 🏗️ Full System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CHROME EXTENSION                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Popup UI     │  │ Content      │  │ Service Worker       │  │
│  │ (popup.html) │◄─┤ Script       │◄─┤ (background)         │  │
│  │              │  │ (Inject)     │  │ - Session management │  │
│  └──────┬───────┘  └──────────────┘  └──────────────────────┘  │
│         │                                                        │
└─────────┼────────────────────────────────────────────────────────┘
          │ HTTP/REST
          ▼
┌─────────────────────────────────────────────────────────────────┐
│              MAIN API SERVER (Oracle Cloud #1 - 12GB)           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ FastAPI Application                                      │  │
│  │  ├─ /analyze (main endpoint)                             │  │
│  │  ├─ /auth (login, signup, JWT)                           │  │
│  │  ├─ /quota (credit system - 30/day)                      │  │
│  │  ├─ /chat (AI conversation)                              │  │
│  │  ├─ /health (monitoring)                                 │  │
│  │  └─ /review (human review queue)                         │  │
│  └──────┬───────────────────────────────────────────────────┘  │
│         │                                                        │
│  ┌──────┴───────────────────────────────────────────────────┐  │
│  │ Decision Engine (app/logic/decision.py)                  │  │
│  │  ├─ Collect signals from all sources                     │  │
│  │  ├─ Weight by confidence                                 │  │
│  │  ├─ Apply decision tree rules                            │  │
│  │  └─ Return verdict (REAL/FAKE/UNCERTAIN)                 │  │
│  └──────┬───────────────────────────────────────────────────┘  │
│         │                                                        │
│         ├───────┬──────────┬──────────┬──────────┬─────────┐   │
│         ▼       ▼          ▼          ▼          ▼         ▼   │
│     ┌────┐ ┌────────┐ ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐ │
│     │ ML │ │   AI   │ │ News │  │Cross │  │Cache │  │ DB   │ │
│     │Srvs│ │Gemini/ │ │Search│  │Check │  │Redis │  │PostgreSQL
│     │    │ │ Groq   │ │Tavily│  │ SerpAPI  │(opt) │  │      │ │
│     └─┬──┘ └────────┘ └──────┘  └──────┘  └──────┘  └───┬──┘ │
│       │                                                   │     │
└───────┼───────────────────────────────────────────────────┼─────┘
        │                                                   │
        │ HTTP                                              │ PostgreSQL
        │                                                   │
  ┌─────┴──────┬──────────────┐                           │
  ▼            ▼              ▼                            ▼
┌──────┐  ┌─────────┐  ┌──────────┐            ┌─────────────────┐
│ML Srv1│  │ML Srv 2 │  │TF-IDF    │            │ PostgreSQL DB   │
│Oracle │  │HF Spaces│  │Local     │            │ (Render FREE)   │
│12GB   │  │16GB     │  │50MB      │            │ - Users         │
│DeBERTa│  │Ensemble │  │Fallback  │            │ - History       │
│FREE   │  │FREE     │  │Always on │            │ - Quotas        │
│       │  │         │  │          │            │ - Reviews       │
└───────┘  └─────────┘  └──────────┘            └─────────────────┘
  $0         $0           $0                           $0
```

---

## 🔄 Request Flow - Fact Check

```
User enters claim in extension
         │
         ├─→ Service Worker validates
         │
         ├─→ POST /analyze to Main API
         │
         ▼
    ┌────────────────────────────────┐
    │ Main API: /analyze endpoint    │
    │ 1. Check user quota (30/day)   │
    │ 2. Check cache                  │
    │ 3. Route to decision engine     │
    └────────┬───────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │ Decision Engine: Parallel Signal Fetch  │
    │                                          │
    │  ┌──────────────────────────────────┐  │
    │  │ Signal 1: ML Analysis            │  │
    │  │ Priority:                         │  │
    │  │  1. ML Server 1 (DeBERTa)   ✓    │  │
    │  │  2. ML Server 2 (Ensemble)  ✓    │  │
    │  │  3. Local TF-IDF            ✓    │  │
    │  │  4. Default 0.5                   │  │
    │  └──────────────────────────────────┘  │
    │                                          │
    │  ┌──────────────────────────────────┐  │
    │  │ Signal 2: AI Reasoning           │  │
    │  │ Priority:                         │  │
    │  │  1. Google Gemini           ✓    │  │
    │  │  2. Groq (llama-3.3-70b)    ✓    │  │
    │  │  3. Cerebras                ✓    │  │
    │  │  4. Default 0.5                   │  │
    │  └──────────────────────────────────┘  │
    │                                          │
    │  ┌──────────────────────────────────┐  │
    │  │ Signal 3: News Evidence          │  │
    │  │  - Tavily search (5 sources)     │  │
    │  │  - Consensus scoring              │  │
    │  │  - Credibility weighting          │  │
    │  └──────────────────────────────────┘  │
    │                                          │
    │  ┌──────────────────────────────────┐  │
    │  │ Signal 4: Cross-Reference        │  │
    │  │  - Google Fact Check API         │  │
    │  │  - SerpAPI claim search          │  │
    │  └──────────────────────────────────┘  │
    └────────┬─────────────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────┐
    │ Decision Tree Logic             │
    │ 1. Weight signals by confidence │
    │ 2. Check thresholds             │
    │ 3. Handle conflicts             │
    │ 4. Determine verdict            │
    └────────┬────────────────────────┘
             │
             ▼
    ┌──────────────────────────┐
    │ Return to Extension:     │
    │ {                        │
    │   verdict: "FAKE",       │
    │   confidence: 97,        │
    │   ml_score: 0.95,        │
    │   ai_score: 0.98,        │
    │   news_score: 0.85,      │
    │   sources: [...],        │
    │   explanation: "..."     │
    │ }                        │
    └──────────────────────────┘
```

---

## 🖥️ ML Server Architecture

### ML Server 1 (Oracle Cloud - DeBERTa)

```
┌──────────────────────────────────────────┐
│ FastAPI Server (port 8001)               │
├──────────────────────────────────────────┤
│                                          │
│  POST /predict                           │
│  ┌────────────────────────────────────┐ │
│  │ 1. Validate API key                │ │
│  │ 2. Load DeBERTa model              │ │
│  │    (Bharat2004/deberta-fakenews-   │ │
│  │     detector - 738MB)              │ │
│  │ 3. Tokenize input (max 512 tokens) │ │
│  │ 4. Run inference (~300ms)          │ │
│  │ 5. Return fake_probability         │ │
│  └────────────────────────────────────┘ │
│                                          │
│  GET /health                             │
│  ┌────────────────────────────────────┐ │
│  │ Returns:                           │ │
│  │ - Model loaded status              │ │
│  │ - Model name                       │ │
│  │ - Server identifier                │ │
│  └────────────────────────────────────┘ │
│                                          │
├──────────────────────────────────────────┤
│ Resources:                               │
│ - RAM: 12GB                              │
│ - Model: 738MB                           │
│ - Inference: 300ms                       │
│ - Accuracy: 96.63%                       │
└──────────────────────────────────────────┘
```

### ML Server 2 (HuggingFace Spaces - Ensemble)

```
┌──────────────────────────────────────────┐
│ Gradio App (auto-deployed)               │
├──────────────────────────────────────────┤
│                                          │
│  POST /api/predict                       │
│  ┌────────────────────────────────────┐ │
│  │ 1. Validate API key                │ │
│  │ 2. Load Model 1: DistilBERT       │ │
│  │    (Bharat2004/out - 268MB)       │ │
│  │ 3. Load Model 2: DeBERTa          │ │
│  │    (Bharat2004/deberta-factchecker│ │
│  │     - 700MB)                       │ │
│  │ 4. Run both models (~500ms)       │ │
│  │ 5. Weighted ensemble:             │ │
│  │    - DistilBERT: 40%              │ │
│  │    - DeBERTa: 60%                 │ │
│  │ 6. Return ensemble_probability    │ │
│  └────────────────────────────────────┘ │
│                                          │
│  UI: Gradio Interface (Web UI)           │
│  ┌────────────────────────────────────┐ │
│  │ - Text input field                 │ │
│  │ - API key field                    │ │
│  │ - Submit button                    │ │
│  │ - JSON output display              │ │
│  │ - Example claims                   │ │
│  └────────────────────────────────────┘ │
│                                          │
├──────────────────────────────────────────┤
│ Resources:                               │
│ - RAM: 16GB                              │
│ - Models: 968MB total                    │
│ - Inference: 500ms                       │
│ - Accuracy: 95.8%                        │
└──────────────────────────────────────────┘
```

---

## 💾 Database Schema

```
PostgreSQL Database (Render - 1GB)
├── users
│   ├── id (primary key)
│   ├── email (unique)
│   ├── password_hash
│   ├── tier (free/premium)
│   ├── google_id (optional)
│   ├── created_at
│   └── last_login
│
├── quotas
│   ├── user_id (foreign key)
│   ├── day_count (resets daily)
│   ├── month_count
│   ├── last_reset
│   └── tier
│
├── claim_history
│   ├── id (primary key)
│   ├── user_id (foreign key)
│   ├── claim_text
│   ├── verdict (REAL/FAKE/UNCERTAIN)
│   ├── confidence
│   ├── ml_score
│   ├── ai_score
│   ├── news_score
│   ├── sources (JSON)
│   ├── explanation
│   ├── created_at
│   └── analysis_time_ms
│
├── review_queue
│   ├── id (primary key)
│   ├── claim_id (foreign key)
│   ├── status (pending/reviewed)
│   ├── reviewer_verdict
│   ├── reviewer_notes
│   ├── flagged_by_user_id
│   └── reviewed_at
│
├── ab_tests
│   ├── id (primary key)
│   ├── test_name
│   ├── variant (A/B)
│   ├── user_id
│   ├── claim_id
│   └── result
│
└── metrics
    ├── timestamp
    ├── metric_name
    ├── metric_value
    └── labels (JSON)
```

---

## 🔐 Security Flow

```
User Request
     │
     ├─→ Extension: Attach JWT token
     │
     ▼
Main API
     │
     ├─→ Middleware: Validate JWT
     │    ├─ Check expiry
     │    ├─ Verify signature
     │    └─ Extract user_id
     │
     ├─→ Rate Limiter: Check quota
     │    ├─ Query quotas table
     │    ├─ Check day_count < 30
     │    └─ Increment counter
     │
     ├─→ Process request
     │
     └─→ Return response


ML Server Request
     │
     ├─→ Main API: Include ML_API_KEY
     │
     ▼
ML Server
     │
     ├─→ Validate API key
     │    ├─ Compare with env var
     │    └─ Reject if invalid (401)
     │
     ├─→ Run inference
     │
     └─→ Return result
```

---

## 📊 Monitoring Stack

```
┌────────────────────────────────────────────┐
│            Prometheus Metrics              │
│  (Exposed at /metrics endpoint)            │
├────────────────────────────────────────────┤
│                                            │
│  • analyze_requests_total                  │
│  • analyze_duration_seconds                │
│  • ml_server_requests_total                │
│  • ml_server_duration_seconds              │
│  • cache_hits_total                        │
│  • cache_misses_total                      │
│  • verdicts_total (by type)                │
│  • quota_exceeded_total                    │
│  • errors_total (by type)                  │
│  • active_users_gauge                      │
│                                            │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│         Grafana Dashboard (Optional)       │
│  - Real-time graphs                        │
│  - Alerts                                  │
│  - Performance tracking                    │
└────────────────────────────────────────────┘
```

---

## 🚀 Deployment Topology

### Multi-Server Setup (Recommended - $0/month)

```
┌───────────────────────────────────────────────────────┐
│               Internet (User's Browser)               │
└────────────┬──────────────────────────────────────────┘
             │
             ├─────────────────┬─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌──────────┐      ┌──────────┐     ┌──────────┐
      │ Main API │      │ML Server1│     │ML Server2│
      │ Oracle #1│      │ Oracle #2│     │HuggingFace
      │ 12GB RAM │      │ 12GB RAM │     │ 16GB RAM │
      │ Port 80  │      │ Port 8001│     │ Port 7860│
      └────┬─────┘      └──────────┘     └──────────┘
           │
           ├───────────────┬───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐   ┌──────────┐
    │PostgreSQL│    │  Redis   │   │ Storage  │
    │  Render  │    │(Optional)│   │ (Local)  │
    │  256MB   │    │  Free    │   │ Models   │
    └──────────┘    └──────────┘   └──────────┘

Cost: $0/month forever
Total RAM: 40GB + 256MB
Total Storage: 111GB
```

### Single-Server Setup (Testing - $0/month)

```
┌────────────────────────────────────────┐
│      Internet (User's Browser)        │
└────────────┬───────────────────────────┘
             │
             ▼
      ┌──────────────────────┐
      │   Oracle Cloud VM    │
      │   12GB RAM           │
      ├──────────────────────┤
      │ • Main API           │
      │ • TF-IDF only        │
      │ • PostgreSQL local   │
      │ • No transformers    │
      └──────────────────────┘

Cost: $0/month
Total RAM: 12GB
Accuracy: ~90% (TF-IDF only)
```

---

## 📈 Scaling Strategy

### Phase 1: Free Tier (Current)
- Main API: Oracle #1 (12GB)
- ML Server 1: Oracle #2 (12GB)
- ML Server 2: HuggingFace (16GB)
- Database: Render (256MB)
- **Users**: Up to 10,000/day
- **Cost**: $0/month

### Phase 2: Add Caching
- Add Redis (Render free tier)
- Cache duration: 24 hours
- **Cache hit rate**: 80%
- **Users**: Up to 50,000/day
- **Cost**: $0/month

### Phase 3: Load Balancing
- Add 2 more Oracle instances
- Nginx load balancer
- **Users**: Up to 100,000/day
- **Cost**: $0/month (still free!)

### Phase 4: Production Scale
- Upgrade to paid tiers
- CDN (Cloudflare)
- Auto-scaling
- **Users**: Millions/day
- **Cost**: ~$50-100/month

---

## 🎯 Performance Benchmarks

### Latency
```
Request Component               Time
─────────────────────────────────────
Extension → Main API            20ms
Main API → ML Server 1         300ms
Main API → ML Server 2         500ms
Main API → AI Provider         800ms
Main API → News Search         600ms
Decision Tree Logic             10ms
Database Query                  50ms
─────────────────────────────────────
Total (uncached)              ~1.5s
Total (cached)                 ~50ms
```

### Throughput
```
Server                 Requests/sec
────────────────────────────────────
Main API (no cache)           100
Main API (with cache)       1,000
ML Server 1                   100
ML Server 2                    50
Database                    5,000
```

### Accuracy
```
Model                    Accuracy
────────────────────────────────────
DeBERTa (ML Server 1)    96.63%
Ensemble (ML Server 2)   95.80%
TF-IDF (Fallback)        90.00%
Combined System          98.50%
```

---

**See also:**
- [Deployment Guide](DEPLOYMENT_100_PERCENT_FREE.md)
- [Quick Start](QUICKSTART_FREE.md)
- [Deployment Checklist](DEPLOYMENT_CHECKLIST.md)

