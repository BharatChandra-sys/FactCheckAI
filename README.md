<!-- Copyright 2027 Bodapati Bharat Chandra. All rights reserved. -->
<!-- Licensed under the Apache License, Version 2.0 | SPDX-License-Identifier: Apache-2.0 -->

<p align="center">
  <img src="extension/icons/icon128.png" alt="FactCheckAI" width="128" height="128"/>
  <h1 align="center">FactCheckAI</h1>
</p>

<p align="center">
  <a href="https://github.com/BharatChandra-sys/FactCheckAI/stargazers">
    <img src="https://img.shields.io/github/stars/BharatChandra-sys/FactCheckAI?style=for-the-badge&logo=github&color=4F46E5&labelColor=1e1e2e" alt="Stars"/>
  </a>
  <a href="https://chromewebstore.google.com/detail/factcheckai">
    <img src="https://img.shields.io/badge/Chrome-Extension-4F46E5?style=for-the-badge&logo=googlechrome&labelColor=1e1e2e" alt="Chrome Extension"/>
  </a>
  <a href="https://github.com/BharatChandra-sys/FactCheckAI/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202.0-22c55e?style=for-the-badge&labelColor=1e1e2e" alt="License"/>
  </a>
  <a href="https://factcheckai-backend.onrender.com/health">
    <img src="https://img.shields.io/badge/API-Live-10B981?style=for-the-badge&logo=fastapi&labelColor=1e1e2e" alt="API Status"/>
  </a>
</p>

<h3 align="center">Real-time fake news detection powered by multi-signal AI</h3>

<p align="center">
  <b>Open-source fake news detection with a Chrome extension, FastAPI backend, and ensemble ML</b>
  <br/><br/>
  Real-time fact-checking • Browser extension • Resilient ML pipeline with 4-level fallback<br/>
  <b>94.2% accuracy (ISOT)</b> • <b>96.3% accuracy (custom fine-tuned RoBERTa)</b> • <b>Multi-language support</b><br/>
  Built with <b>FastAPI</b>, <b>fine-tuned RoBERTa</b>, <b>LLM ensemble</b>, and <b>TF-IDF fallback</b>
</p>

---

## The Problem

Misinformation spreads 6x faster than verified news on social media. Traditional fact-checking is manual, slow, and does not scale. Users need instant, accurate verification while browsing.

## The Solution

FactCheckAI provides real-time AI-powered fact-checking directly in your browser. A Chrome extension sends claims to a FastAPI backend that routes them through a multi-signal decision pipeline — combining ML models, LLM ensemble verdicts, evidence search, and manipulation analysis into a single confidence-scored result.

- **Resilient by design** — four fallback levels mean the system keeps working even when external services are unavailable
- **Multi-signal decision** — no single model is trusted blindly; ML, LLM, evidence, and manipulation scores are combined by a trained meta-model
- **Honest uncertainty** — when signals conflict, the system returns `uncertain` rather than forcing a wrong verdict
- **Cost-conscious** — the full stack runs for free on Render + Neon + HuggingFace Spaces

---

## ML Architecture — 4-Level Fallback

Every claim passes through this routing chain. Each level is tried in order; the next is used only if the previous fails.

```
Request arrives
    ↓
[1] Redis cache          → instant response if seen before
    ↓ miss
[2] ML Server 1          → fine-tuned RoBERTa (Bharat2004/factcheckai-model-a)
    (HuggingFace Space)    96.3% accuracy, ~1s
    ↓ timeout / error
[3] ML Server 2          → RoBERTa ensemble (model-a + model-b weighted average)
    (HuggingFace Space)    94.2% accuracy on mixed sources
    ↓ error
[4] Local TF-IDF         → scikit-learn Logistic Regression
                           ~50ms, always available, no external dependency
    ↓ failure (edge case)
[5] Default 0.5          → neutral score, surfaces as "uncertain"
```

The final verdict is produced by a **trained meta-decision model** (Logistic Regression with calibration) that combines:
- ML fake probability
- LLM ensemble verdict (Cerebras, Groq, Gemini, MiniMax in parallel)
- Evidence search score (Tavily news API)
- Manipulation/conspiracy signal score

When the meta-model detects heavy signal conflict it returns `uncertain` rather than guessing.

---

## Key Features

### Resilient ML Pipeline
- **4-level fallback** from fine-tuned RoBERTa to local TF-IDF — no single point of failure
- **Fine-tuned models** trained on 281k+ clean samples across 6 public datasets
- **LLM ensemble** runs Cerebras, Groq, Gemini, and MiniMax in parallel with weighted voting
- **In-memory prediction cache** reduces repeat-claim latency to under 10ms

### Multi-Signal Decision Engine
- **Meta-decision model** — trained logistic regression combines 4 independent signals
- **Uncertainty detection** — surfaces `uncertain` when AI and evidence strongly disagree
- **Manipulation scoring** — detects conspiracy language, emotional manipulation, cherry-picking
- **Weighted by text length** — short claims get higher LLM weight, longer articles get higher ML weight

### Production-Ready Infrastructure
- **Render** — FastAPI backend (free tier, 512MB RAM)
- **Neon PostgreSQL** — serverless Postgres with auto-resume, pgBouncer pooler
- **HuggingFace Spaces** — ML inference server (16GB RAM, free tier)
- **Startup self-healing** — on every deploy, verifies DB connection, creates missing tables, runs Alembic migrations automatically

### Privacy & Security
- **On-device preprocessing** — text selection and page extraction happen in the browser
- **JWT authentication** — stateless, 7-day tokens
- **Google OAuth** — access token validated against audience claim
- **Rate limiting** — per-IP sliding window in middleware; per-user tiers via Redis when available
- **No tracking** — we verify content, not users

---

## Architecture Overview

### Component Map

| Component | Technology | Hosted On | Purpose |
|-----------|------------|-----------|---------|
| **Chrome Extension** | Vanilla JS, MV3 | Browser | UI, text selection, popup |
| **Backend API** | FastAPI, Python 3.11 | Render (free) | Routing, auth, decision logic |
| **ML Server** | RoBERTa, PyTorch | HuggingFace Spaces (free) | Transformer inference |
| **Database** | PostgreSQL 18, SQLAlchemy | Neon (free) | Users, sessions, claim history |
| **Cache** | In-memory dict | In-process | Repeat-claim deduplication |
| **LLM Providers** | Cerebras, Groq, Gemini | External APIs | Ensemble verdict |
| **Evidence Search** | Tavily API | External API | News corroboration |

### Decision Logic (decision.py)

```python
# Heuristic weights (meta-model unavailable fallback)
# Normal text  →  AI: 50%  Evidence: 28%  ML: 14%  Manipulation: 8%
# Short (<50c) →  AI: 60%  Evidence: 28%  ML:  8%  Manipulation: 8%
#
# Short claims get higher AI weight because TF-IDF needs more tokens to be reliable.
# This is an explicit design tradeoff, not a bug.

def decide(ml_fake, ai_fake, evidence_score, text_len, manip_score):
    # 1. Detect signal conflict → return "uncertain" instead of guessing
    # 2. Try trained meta-model (CalibratedClassifierCV)
    # 3. Fall back to weighted heuristic
```

### Background Scheduler (in-process, by design)

The application runs a single background daemon thread that:
- Pings external ML services every 14 minutes (prevents HuggingFace Spaces from sleeping)
- Checks whether training-data collection should trigger (hourly)
- Updates Prometheus metrics (hourly)

This is intentionally in-process rather than a separate worker because the workload is lightweight and the deployment is cost-constrained to a single free Render instance. A production-scale deployment would extract this into a separate scheduler service (e.g., Celery + Redis, or a cron job).

---

## ML Models — Training Details

Both models are trained with the same pipeline:
- MinHash near-duplicate removal (threshold 0.85)
- 5-fold TF-IDF noise filter (removes likely mislabeled samples)
- Layer-wise Learning Rate Decay (LLRD, decay=0.9)
- Label smoothing 0.1
- Cosine LR schedule with 6% warmup
- Gradient clipping 1.0
- FP16 mixed precision

| Model | Base | Training Data | Accuracy | F1 |
|-------|------|---------------|----------|-----|
| `factcheckai-model-a` | RoBERTa-base | daniB2112 (300k → 111k clean) | **96.3%** | **0.963** |
| `factcheckai-model-b` | RoBERTa-base | 5 mixed sources (232k → 103k clean) | **79.8%** | **0.790** |
| Ensemble (weighted 0.6/0.4) | — | Combined | **~93%** est. | — |

Training data sources for model-b: GonzaloA/fake_news, WELFake, ErfanMoosaviMonazzah, mohammadjavadpirhadi, FEVER v1.0.

### Benchmark Results (TF-IDF + meta-model, current deployment)

| Dataset | Accuracy | Precision | Recall | F1 |
|---------|----------|-----------|--------|-----|
| LIAR | 68.4% | 0.67 | 0.66 | 0.66 |
| ISOT Fake News | 94.2% | 0.93 | 0.92 | 0.92 |
| FakeNewsNet | 87.3% | 0.86 | 0.85 | 0.85 |
| Custom test set | 91.5% | 0.90 | 0.89 | 0.89 |

Note: The 94.2% figure is on ISOT using the TF-IDF model. The 96.3% figure is from the fine-tuned RoBERTa model-a on its own test split. These are different experiments on different datasets — not directly comparable.

---

## Performance

### Response Time
```
Cache hit (repeat claim):         < 10ms
TF-IDF only path:         P50:   180ms  P95:  350ms
RoBERTa (HF Space):       P50:   1.2s   P95:  2.5s   (includes cold-start wake)
Full pipeline (TF-IDF +   P50:   1.8s   P95:  4s
  LLM ensemble + evidence)
```

HuggingFace free Spaces sleep after inactivity. The background scheduler pings them every 14 minutes to keep them awake during active periods.

### System
- **Database:** Neon PostgreSQL (auto-suspend, wakes in ~1s)
- **DB pool:** 2 connections per worker, pgBouncer on the Neon side
- **Startup:** auto-creates missing tables, runs Alembic migrations, retries DB connect up to 5 times

---

## Installation & Setup

### Chrome Extension

```bash
git clone https://github.com/BharatChandra-sys/FactCheckAI.git
cd FactCheckAI

# Chrome → Extensions → Developer mode → Load unpacked → select 'extension' folder
```

### Backend (local)

```bash
cd backend
py -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

# Copy and fill in your keys
cp .env.example .env

# Start
uvicorn app.main:app --reload --port 8000
```

Required `.env` keys:
```
DATABASE_URL=postgresql://...neon.tech/neondb?sslmode=require
JWT_SECRET=<openssl rand -hex 32>
GOOGLE_CLIENT_ID=...
GROQ_API_KEY=...       # or any one of: CEREBRAS, GEMINI, MINIMAX
TAVILY_API_KEY=...     # for evidence search
BREVO_API_KEY=...      # for OTP emails
SMTP_USER=...
```

### Deploy to Render + Neon

1. Create a Neon project at neon.tech — copy the pooled connection string
2. Connect this repo to Render → New → Blueprint → render.yaml auto-configures everything
3. Set `DATABASE_URL` and API keys in Render's environment tab
4. Deploy — the startup sequence handles all DB setup automatically

---

## API Reference

### Authentication

```bash
# Register
curl -X POST https://factcheckai-backend.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpass","name":"Your Name"}'

# Returns {"token": "eyJ...", "user": {...}}
# Use token in Authorization: Bearer <token>
```

### Fact-Check

```bash
# POST /message
curl -X POST https://factcheckai-backend.onrender.com/message \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message":"5G towers spread coronavirus through radio waves"}'
```

Response:
```json
{
  "is_claim": true,
  "verdict": "fake",
  "confidence": 0.87,
  "ml_score": 0.81,
  "ai_score": 0.85,
  "evidence_score": 0.22,
  "manipulation_score": 0.63,
  "explanation": "...",
  "evidence": ["https://...", "https://..."],
  "highlights": [{"phrase": "5G towers", "importance": 0.9}]
}
```

### Health Check

```bash
curl https://factcheckai-backend.onrender.com/health
# {"status":"ok","checks":{"database":{"status":"ok"},"models":{"status":"ok"}}}
```

### Rate Limits

| Tier | Per minute | Per day | Monthly |
|------|-----------|---------|---------|
| Anonymous | 3 | 10 | 10 |
| Free | 5 | 30 | 30 |
| Pro | 60 | 10,000 | 1,000 |
| Enterprise | 300 | 100,000 | unlimited |

---

## Development

### Project Structure

```
FactCheckAI/
├── backend/
│   ├── app/
│   │   ├── analysis/       # ML, AI, evidence, manipulation, credibility
│   │   ├── logic/          # decision.py — meta-decision engine
│   │   ├── routes/         # FastAPI routers
│   │   ├── api.py          # /message — main pipeline
│   │   └── main.py         # lifespan, startup, middleware
│   ├── alembic/            # DB migrations
│   ├── data/               # model.joblib, vectorizer.joblib, meta_model.joblib
│   └── training/           # Kaggle training notebooks
├── extension/
│   ├── background/         # service_worker.js
│   ├── popup/              # popup.js, dashboard.js, history.js
│   └── content.js          # text selection tooltip
├── ml-servers/
│   └── huggingface-ensemble/  # HF Space app.py — serves model-a + model-b
├── render.yaml
└── Procfile
```

### Contributing

1. Fork and create a feature branch from `main`
2. Follow PEP 8, use type hints
3. Use conventional commits: `feat:`, `fix:`, `docs:`
4. Open a pull request with a description of what changed and why

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## Security & Compliance

- **JWT** — HS256, 7-day expiry, stateless
- **Google OAuth** — access token validated with audience check
- **Rate limiting** — sliding window per IP in middleware
- **Input validation** — Pydantic validators, HTML stripping, null-byte removal
- **Parameterized queries** — SQLAlchemy ORM throughout
- **GDPR-aware** — no PII stored beyond what users explicitly provide; right to delete via account deletion
- **Open source** — all logic is auditable

---

## Roadmap

### Near-term
- [x] Upload model-b to HuggingFace (`Bharat2004/factcheckai-model-b`) ✅
- [x] HuggingFace Space ensemble server built (`ml-servers/huggingface-ensemble/`) ✅
- [ ] Upload model-a to HuggingFace once Account 1 training completes
- [ ] Deploy HF Space and set `ML_SERVER_2_URL` in Render env vars
- [ ] Firefox extension
- [ ] Multilingual expansion beyond English/Spanish/French

### Medium-term
- [ ] Mobile apps (iOS/Android)
- [ ] Video transcript fact-checking
- [ ] Community correction loop integrated into retraining

### Long-term
- [ ] Separate background scheduler service (remove in-process daemon)
- [ ] Streaming response for long documents
- [ ] Partnership integrations with news platforms

---

## License & Attribution

```
FactCheckAI: Apache License 2.0
├── FastAPI: MIT
├── Transformers (HuggingFace): Apache 2.0
├── scikit-learn: BSD 3-Clause
├── PyTorch: Modified BSD
└── PostgreSQL: PostgreSQL License
```

Training data:
- LIAR dataset — Wang, 2017
- ISOT Fake News Dataset
- FakeNewsNet — Shu et al., 2018
- daniB2112/fake-news-dataset (HuggingFace)
- WELFake, GonzaloA/fake_news, FEVER v1.0

```bibtex
@software{factcheckai2027,
  title   = {FactCheckAI: Multi-Signal Fake News Detection},
  author  = {Bodapati Bharat Chandra},
  year    = {2027},
  url     = {https://github.com/BharatChandra-sys/FactCheckAI},
  version = {2.6.1},
  license = {Apache-2.0}
}
```

---

<p align="center">
  <br/>
  <b>Open-source fake news detection — honest about what it is, built to last</b>
  <br/><br/>
  <a href="https://github.com/BharatChandra-sys/FactCheckAI/stargazers">
    <img src="https://img.shields.io/github/stars/BharatChandra-sys/FactCheckAI?style=for-the-badge&logo=github&color=4F46E5&labelColor=1e1e2e" alt="Stars"/>
  </a>
  <br/><br/>
  <a href="https://github.com/BharatChandra-sys/FactCheckAI/issues">Report Issues</a> •
  <a href="CONTRIBUTING.md">Contributing</a> •
  <a href="https://factcheckai-backend.onrender.com/health">Live API</a>
</p>
