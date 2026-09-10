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

<h3 align="center">Memory-augmented, agentic fact-verification powered by RAG and multi-signal AI</h3>

<p align="center">
  <b>Open-source fake news detection with a Chrome extension, FastAPI backend, RAG pipeline, and LangGraph orchestration</b>
  <br/><br/>
  Real-time fact-checking • Persistent fact memory • Hybrid retrieval • Agentic re-search<br/>
  <b>94.2% on ISOT (TF-IDF, current deployment)</b> • <b>96.3% on fine-tuned RoBERTa held-out split</b><br/>
  Built with <b>FastAPI</b>, <b>fine-tuned RoBERTa</b>, <b>LangGraph</b>, <b>pgvector</b>, and <b>LLM ensemble</b>
</p>

---

## The Problem

Traditional fact-checking is manual and does not scale to the volume of content published daily. Users need a way to verify claims while browsing without leaving the page. A pure ML classifier learns patterns from training data but has no persistent memory of past verifications and no ability to reason over retrieved evidence.

## The Solution

FactCheckAI combines trained ML classifiers with a persistent knowledge base and an agentic orchestration layer. A Chrome extension sends claims to a FastAPI backend that runs a stateful LangGraph workflow — normalizing the claim, running ML models, retrieving similar historical fact-checks and evidence from a pgvector knowledge base, doing RAG reasoning over the retrieved context, and writing the result back to memory for future retrieval.

- **Owned ML intelligence** — fine-tuned RoBERTa models remain the primary classification signal
- **Persistent fact memory** — every qualified fact-check is stored with vector embeddings in PostgreSQL + pgvector, enabling semantic retrieval across restarts
- **Hybrid retrieval** — BM25 (lexical) + vector search merged with Reciprocal Rank Fusion, then cross-encoder reranked
- **RAG reasoning** — LLM reasons over retrieved evidence, not from memory; hallucinated citations are validated
- **Agentic re-search** — if initial evidence is insufficient, the workflow calls live search tools and re-evaluates
- **Calibrated meta-decision** — a trained logistic regression combines all signals; signals conflict returns `uncertain`
- **4-level ML fallback** — the system keeps working even when external services are unavailable

---

## Full Architecture

```
USER CLAIM
    |
    v
Claim Extraction + Normalization
    |
    +-----------------------------+
    |                             |
    v                             v
YOUR ML LAYER                KNOWLEDGE LAYER
    |                             |
RoBERTa-a (96.3%)            pgvector (Neon)
RoBERTa-b (79.8%)            fact_checks table
TF-IDF fallback              evidence_documents table
    |                             |
    |                        Hybrid Retrieval
    |                        BM25 + Vector
    |                             |
    |                        Cross-Encoder Rerank
    |                             |
    +-----------------------------+
                |
                v
         LangGraph Workflow
                |
    +-----------+-----------+
    |           |           |
ML Analyst  RAG Reasoner  Evidence Agent
    |           |           |
    +-----------+-----------+
                |
         Conflict Detection
         (sufficient evidence?)
                |
         +------+------+
         |             |
       YES             NO
         |             |
         |          Live Search Tools
         |          (search_news, search_web)
         |             |
         +------+------+
                |
        Manipulation Analysis
                |
         Meta-Decision Model
         (calibrated LR, 4 signals)
                |
       +--------+--------+
       |        |        |
     REAL     FAKE  UNCERTAIN
                |
         Citation Validation
                |
         Memory Write
         (VERIFIED / MODEL_ONLY / DISPUTED)
```

---

## ML Architecture — 4-Level Fallback

Every claim passes through this routing chain. Each level is tried in order; the next is used only if the previous fails.

```
Request arrives
    |
[1] Redis cache          -> instant response if seen before
    | miss
[2] ML Server 1          -> fine-tuned RoBERTa (Bharat2004/factcheckai-model-a)
    (HuggingFace Space)     96.3% accuracy on held-out split, ~1s
    | timeout / error
[3] ML Server 2          -> RoBERTa ensemble (model-a + model-b, 0.6/0.4 weight)
    (HuggingFace Space)     deployed to Bharat2004/factcheckai-model-b
    | error
[4] Local TF-IDF         -> scikit-learn Logistic Regression
                            ~50ms, always available, no external dependency
    | failure (edge case)
[5] Default 0.5          -> neutral score, surfaces as "uncertain"
```

The ML score is one signal among four in the meta-decision model. RAG provides grounded evidence context. Neither alone determines the final verdict.

---

## Key Features

### Persistent Fact Memory (pgvector)
- **fact_checks table** — every qualified result stored with 384-dim vector embedding
- **evidence_documents table** — news articles and sources stored with embeddings and source tier ranking
- **Verification status** — VERIFIED / MODEL_ONLY / HUMAN_REVIEWED / DISPUTED
- **Temporal metadata** — published_at, retrieved_at fields enable temporal reasoning (old verdict vs current truth)

### Hybrid Retrieval
- **BM25** — PostgreSQL full-text search (ts_vector) for exact phrases, entity names, dates
- **Vector search** — pgvector cosine similarity for paraphrases and conceptual similarity
- **Reciprocal Rank Fusion** — merges both ranked lists; documents appearing in both get boosted
- **Cross-encoder reranker** — ms-marco-MiniLM-L-6-v2 scores each candidate against the claim; falls back to LLM-based scoring

### Agentic RAG via LangGraph
- **FactCheckState TypedDict** — all signals flow through shared state across nodes
- **Conditional edges** — graph routes to live search if retrieved evidence is insufficient
- **RAG reasoner** — structured LLM output: assessment, supporting/contradicting evidence, citations
- **Citation validator** — checks each cited claim against retrieved source content; invalid citations suppressed
- **Memory writer** — persists result with verification status after each run

### Multi-Signal Decision Engine
- **Meta-decision model** — CalibratedClassifierCV trained to fuse ML + LLM + evidence + manipulation scores
- **Uncertainty detection** — returns `uncertain` when signals conflict or evidence balance is near 50/50
- **RAG score integration** — RAG assessment adjusts evidence score before meta-model inference
- **Manipulation scoring** — conspiracy language, emotional manipulation, cherry-picking detected independently

### Resilient Infrastructure
- **Render** — FastAPI backend (free tier, 512MB RAM)
- **Neon PostgreSQL** — serverless Postgres with pgvector, auto-resume, pgBouncer pooler
- **HuggingFace Spaces** — RoBERTa inference server (16GB RAM, free tier)
- **Startup self-healing** — on every deploy: verifies DB connection (5 retries), creates missing tables, runs Alembic migrations

---

## Architecture Components

| Component | Technology | Hosted On | Purpose |
|-----------|------------|-----------|---------|
| Chrome Extension | Vanilla JS, MV3 | Browser | UI, text selection, popup |
| Backend API | FastAPI, Python 3.11 | Render (free) | Routing, auth, LangGraph entry |
| LangGraph Workflow | langgraph 0.4.8 | In-process | Stateful fact-check orchestration |
| ML Server | RoBERTa-base, PyTorch | HuggingFace Spaces (free) | Transformer inference |
| Vector Store | PostgreSQL + pgvector | Neon (free) | Persistent embeddings + hybrid search |
| RAG Retriever | BM25 + pgvector + reranker | In-process | Hybrid retrieval pipeline |
| LLM Providers | Cerebras, Groq, Gemini, MiniMax | External APIs | Ensemble verdict + RAG reasoning |
| Evidence Search | Tavily / NewsAPI | External APIs | Live news corroboration |

### Directory Structure

```
FactCheckAI/
├── backend/
│   ├── app/
│   │   ├── analysis/       # ML, AI, evidence, manipulation, credibility
│   │   ├── retrieval/      # embeddings.py, hybrid.py, vector_store.py, reranker.py
│   │   ├── rag/            # reasoner.py, citation_validator.py
│   │   ├── agents/         # tools.py — structured agent tool definitions
│   │   ├── graph/          # state.py, nodes.py, workflow.py — LangGraph
│   │   ├── logic/          # decision.py — calibrated meta-decision model
│   │   ├── routes/         # FastAPI routers
│   │   ├── api.py          # /message — main pipeline entry
│   │   └── main.py         # lifespan, startup, middleware
│   ├── alembic/            # DB migrations (includes pgvector tables)
│   ├── data/               # model.joblib, vectorizer.joblib, meta_model.joblib
│   └── training/           # Kaggle training notebooks
├── extension/
│   ├── background/         # service_worker.js
│   ├── popup/              # popup.js, dashboard.js, history.js
│   └── content.js          # text selection tooltip
├── ml-servers/
│   └── huggingface-ensemble/   # HF Space app.py — serves model-a + model-b ensemble
├── render.yaml
└── Procfile
```

### Background Scheduler

The application runs a single background daemon thread that pings external ML services every 14 minutes (prevents HuggingFace Spaces from sleeping), checks whether training-data collection should trigger (hourly), and updates Prometheus metrics (hourly).

This is intentionally in-process rather than a separate worker because the workload is lightweight and the deployment is cost-constrained to a single free Render instance. A production-scale deployment would extract this into a dedicated scheduler service.

---

## ML Models — Training Details

Both models use the same pipeline: MinHash near-duplicate removal (threshold 0.85), 5-fold TF-IDF noise filter, Layer-wise Learning Rate Decay (decay=0.9), label smoothing 0.1, cosine LR with 6% warmup, gradient clipping 1.0, FP16 mixed precision.

| Model | Base | Training Data | Accuracy | F1 |
|-------|------|---------------|----------|-----|
| `factcheckai-model-a` | RoBERTa-base | daniB2112 (300k raw, 111k clean) | **96.3%** | **0.963** |
| `factcheckai-model-b` | RoBERTa-base | 5 mixed sources (232k raw, 103k clean) | **79.8%** | **0.790** |
| Weighted ensemble (0.6 / 0.4) | — | Combined | ~93% est. | — |

Training sources for model-b: GonzaloA/fake_news, WELFake, ErfanMoosaviMonazzah, mohammadjavadpirhadi, FEVER v1.0.

### Benchmark Results (TF-IDF + meta-model, current production)

| Dataset | Accuracy | Precision | Recall | F1 |
|---------|----------|-----------|--------|-----|
| LIAR | 68.4% | 0.67 | 0.66 | 0.66 |
| ISOT Fake News | 94.2% | 0.93 | 0.92 | 0.92 |
| FakeNewsNet | 87.3% | 0.86 | 0.85 | 0.85 |
| Custom test set | 91.5% | 0.90 | 0.89 | 0.89 |

Note: 94.2% is on ISOT using TF-IDF. 96.3% is from the fine-tuned RoBERTa model-a on its own held-out test split. These are different experiments on different datasets and are not directly comparable.

---

## Performance

```
Cache hit (repeat claim):                    < 10ms
TF-IDF only:              P50: 180ms   P95: 350ms
RoBERTa (HF Space):       P50: 1.2s    P95: 2.5s   (includes cold-start wake)
Full pipeline with RAG:   P50: 2.2s    P95: 5s
```

HuggingFace free Spaces sleep after inactivity. The background scheduler pings them every 14 minutes. Neon PostgreSQL auto-suspends and wakes in ~1s on first query.

---

## Installation & Setup

### Chrome Extension

```bash
git clone https://github.com/BharatChandra-sys/FactCheckAI.git
cd FactCheckAI

# Chrome -> Extensions -> Developer mode -> Load unpacked -> select 'extension' folder
```

### Backend (local)

```bash
cd backend
py -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

cp .env.example .env
# Fill in keys

uvicorn app.main:app --reload --port 8000
```

Required `.env` keys:
```
DATABASE_URL=postgresql://...neon.tech/neondb?sslmode=require
JWT_SECRET=<openssl rand -hex 32>
GOOGLE_CLIENT_ID=...
GROQ_API_KEY=...
TAVILY_API_KEY=...
BREVO_API_KEY=...
SMTP_USER=...
```

### Deploy to Render + Neon

1. Create a Neon project at neon.tech — copy the pooled connection string
2. Connect repo to Render → New → Blueprint → render.yaml handles everything
3. Set `DATABASE_URL` and API keys in Render's environment tab
4. Deploy — startup sequence runs DB connection check, creates tables, applies migrations

---

## API Reference

### Authentication

```bash
curl -X POST https://factcheckai-backend.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpass","name":"Your Name"}'

# Returns {"token": "eyJ...", "user": {...}}
# Use in: Authorization: Bearer <token>
```

### Fact-Check

```bash
curl -X POST https://factcheckai-backend.onrender.com/message \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message":"5G towers spread coronavirus through radio waves"}'
```

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
```

### Rate Limits

| Tier | Per minute | Per day | Monthly |
|------|-----------|---------|---------|
| Anonymous | 3 | 10 | 10 |
| Free | 5 | 30 | 30 |
| Pro | 60 | 10,000 | 1,000 |
| Enterprise | 300 | 100,000 | unlimited |

---

## Development & Contributing

1. Fork and create a feature branch from `main`
2. Follow PEP 8, use type hints throughout
3. Use conventional commits: `feat:`, `fix:`, `docs:`
4. Open a pull request with a clear description

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## Security & Compliance

- **JWT** — HS256, 7-day expiry, stateless
- **Google OAuth** — access token validated with audience claim check
- **Rate limiting** — per-IP sliding window in middleware; per-user tier limits via Redis
- **Input validation** — Pydantic validators, HTML stripping, null-byte removal
- **Parameterized queries** — SQLAlchemy ORM throughout; no raw SQL with user input
- **GDPR-aware** — no PII stored beyond what users explicitly provide
- **Open source** — all logic is auditable

---

## Roadmap

### Near-term
- [x] fine-tuned RoBERTa model-b uploaded to `Bharat2004/factcheckai-model-b`
- [x] HuggingFace Space ensemble server built (`ml-servers/huggingface-ensemble/`)
- [x] pgvector persistent memory schema + Alembic migration deployed to Neon
- [x] Hybrid retrieval (BM25 + vector + RRF + cross-encoder reranker)
- [x] LangGraph workflow orchestration (9 nodes, conditional edges)
- [x] RAG reasoner + citation validator
- [x] Agent tool definitions (search_news, retrieve_evidence, run_ml_analysis, etc.)
- [ ] Upload model-a after training completes; set `ML_SERVER_1_URL` in Render
- [ ] Deploy HF Space; set `ML_SERVER_2_URL` in Render

### Medium-term
- [ ] Evaluation ablation study (TF-IDF vs hybrid vs hybrid+RAG vs full)
- [ ] Firefox extension support
- [ ] Multilingual expansion (German, Portuguese, French)

### Long-term
- [ ] Separate background scheduler service (Celery or cron)
- [ ] LangSmith observability traces (per-node latency and token cost)
- [ ] Streaming response for long documents

---

## License & Attribution

```
FactCheckAI: Apache License 2.0
├── FastAPI: MIT
├── LangChain / LangGraph: MIT
├── Transformers (HuggingFace): Apache 2.0
├── scikit-learn: BSD 3-Clause
├── pgvector: MIT
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
  title   = {FactCheckAI: Memory-Augmented Agentic Fact Verification},
  author  = {Bodapati Bharat Chandra},
  year    = {2027},
  url     = {https://github.com/BharatChandra-sys/FactCheckAI},
  version = {2.7.0},
  license = {Apache-2.0}
}
```

---

<p align="center">
  <br/>
  <b>Open-source fact-checking — owned ML, persistent memory, agentic RAG</b>
  <br/><br/>
  <a href="https://github.com/BharatChandra-sys/FactCheckAI/stargazers">
    <img src="https://img.shields.io/github/stars/BharatChandra-sys/FactCheckAI?style=for-the-badge&logo=github&color=4F46E5&labelColor=1e1e2e" alt="Stars"/>
  </a>
  <br/><br/>
  <a href="https://github.com/BharatChandra-sys/FactCheckAI/issues">Report Issues</a> •
  <a href="CONTRIBUTING.md">Contributing</a> •
  <a href="https://factcheckai-backend.onrender.com/health">Live API</a>
</p>
