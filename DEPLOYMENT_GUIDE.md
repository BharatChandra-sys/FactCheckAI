# 🚀 FactCheckAI Deployment Guide (100% Free, No Credit Card)

## Overview

This guide shows how to deploy FactCheckAI using **only free services** without requiring a credit card.

```
┌─────────────────────────────────────────────────────────┐
│ Chrome Extension (User's Browser)                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Backend API: Render.com (Free Tier)                     │
│ • FastAPI + LangGraph orchestration                     │
│ • 512MB RAM, auto-sleep after 15min                     │
│ • Internal keep-alive pinger (every 14 min)             │
└─────────────────────────────────────────────────────────┘
    ↓                    ↓                    ↓
┌──────────────┐ ┌─────────────────┐ ┌──────────────────┐
│ Neon DB      │ │ HuggingFace     │ │ Free LLM APIs    │
│ PostgreSQL   │ │ Spaces          │ │ • Groq           │
│ + pgvector   │ │ • RoBERTa A+B   │ │ • Cerebras       │
│              │ │ • 16GB RAM      │ │ • Gemini Flash   │
└──────────────┘ └─────────────────┘ └──────────────────┘
    ↓ (woken by)        ↓ (woken by)        
┌──────────────┐ ┌─────────────────┐
│ UptimeRobot  │ │ Cron-Job.org    │
│ (free)       │ │ (free)          │
│ Pings every  │ │ Pings every     │
│ 5 minutes    │ │ 10 minutes      │
└──────────────┘ └─────────────────┘
```

---

## 🗄️ Step 1: Deploy Database (Neon PostgreSQL)

### Why Neon?
- ✅ **No credit card required**
- ✅ **pgvector support** (for RAG embeddings)
- ✅ **Auto-suspend** (saves resources)
- ✅ **0.5GB storage free**
- ✅ **Pooled connections** (pgBouncer)

### Setup Steps:

1. **Sign up**: Go to [neon.tech](https://neon.tech) (GitHub login, no card needed)

2. **Create project**: Click "New Project"
   - Name: `factcheckai-db`
   - Region: Choose closest to your users
   - PostgreSQL version: 16 (latest)

3. **Enable pgvector**:
   ```sql
   -- This is done automatically in your Alembic migrations
   -- But you can verify with:
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

4. **Get connection string**:
   - Dashboard → Connection Details → **Pooled connection** (recommended)
   - Copy the full URL:
   ```
   postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

5. **Save for later**: You'll paste this into Render's environment variables

---

## 🤖 Step 2: Deploy ML Models (HuggingFace Spaces)

### Why HuggingFace Spaces?
- ✅ **No credit card required**
- ✅ **Free CPU inference** (always-on)
- ✅ **Free GPU hours** (limited, but auto-fallback to CPU)
- ✅ **16GB RAM** on free tier
- ✅ **Direct model hosting**

### Setup Steps:

1. **Sign up**: [huggingface.co](https://huggingface.co) (GitHub login)

2. **Upload your models**:
   ```bash
   # Install Hugging Face CLI
   pip install huggingface_hub
   
   # Login (creates token)
   huggingface-cli login
   
   # Upload model-a (your best fine-tuned RoBERTa)
   cd backend/training
   # After training completes, upload with:
   # huggingface-cli upload Bharat2004/factcheckai-model-a ./model-a
   ```

3. **Create a Space for inference**:
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click **Create New Space**
   - Name: `factcheckai-ml-server`
   - SDK: **Gradio** (free, works with FastAPI)
   - Hardware: **CPU Basic - ZeroGPU** (free, always-on)

4. **Deploy inference server**:
   - Copy files from `ml-servers/huggingface-ensemble/` to your Space
   - **Important**: Rename `app.py` to `app_fastapi.py`
   - Create a new `app.py` (Gradio wrapper):
   
   ```python
   import gradio as gr
   import requests
   
   # Import your FastAPI app
   from app_fastapi import app as fastapi_app
   
   # Create Gradio interface that wraps FastAPI
   def predict(text):
       response = requests.post(
           "http://localhost:7860/predict",
           json={"text": text}
       )
       return response.json()
   
   # Launch FastAPI in background
   import uvicorn
   import threading
   threading.Thread(
       target=lambda: uvicorn.run(fastapi_app, host="0.0.0.0", port=7860),
       daemon=True
   ).start()
   
   # Gradio interface
   interface = gr.Interface(
       fn=predict,
       inputs=gr.Textbox(label="Enter claim to verify"),
       outputs=gr.JSON(label="Prediction"),
       title="FactCheckAI ML Server",
       description="RoBERTa ensemble for fake news detection"
   )
   
   interface.launch()
   ```
   
   - Your Space will have a URL like:
   ```
   https://bharat2004-factcheckai-ml-server.hf.space
   ```

5. **Add health endpoint** to your Space's `app.py`:
   ```python
   @app.get("/health")
   def health():
       return {"status": "ok"}
   ```

6. **Test your Space**:
   ```bash
   curl https://YOUR-USERNAME-factcheckai-ml-server.hf.space/health
   ```

---

## 🌐 Step 3: Deploy Backend (Render.com)

### Why Render?
- ✅ **No credit card required**
- ✅ **512MB RAM free tier**
- ✅ **Auto-deploy from GitHub**
- ✅ **Built-in health checks**
- ✅ **Free SSL**

### Setup Steps:

1. **Sign up**: [render.com](https://render.com) (GitHub login)

2. **Connect repository**:
   - Dashboard → New → Blueprint
   - Connect your GitHub repo
   - Render will detect `render.yaml` automatically

3. **Set environment variables**:
   - Before deploying, go to Environment tab
   - Add these variables:

   ```bash
   # Database
   DATABASE_URL=postgresql://... (from Neon)
   
   # ML Servers
   ML_SERVER_2_URL=https://YOUR-USERNAME-factcheckai-ml-server.hf.space
   ML_API_KEY=<generate with: openssl rand -hex 32>
   
   # LLM Providers (all have free tiers without credit card)
   GROQ_API_KEY=<from console.groq.com>
   CEREBRAS_API_KEY=<from cloud.cerebras.ai>
   GEMINI_API_KEY=<from aistudio.google.com>
   
   # Evidence Search
   TAVILY_API_KEY=<from tavily.com> (1000 free searches/month)
   NEWS_API_KEY=<from newsapi.org> (100 free requests/day)
   
   # Optional: Google OAuth
   GOOGLE_CLIENT_ID=<optional, for user auth>
   
   # Security
   JWT_SECRET=<auto-generated by Render>
   ```

4. **Deploy**:
   - Click "Apply" → Render starts building
   - First deploy takes ~5 minutes
   - Watch logs for any errors

5. **Verify deployment**:
   ```bash
   curl https://factcheckai-backend.onrender.com/health
   ```

---

## ⏰ Step 4: Keep Services Awake (Free Monitoring)

### Problem:
- **Render** sleeps after 15 minutes of inactivity
- **HuggingFace Spaces** (CPU) sleep after 48 hours of inactivity
- **Neon** auto-suspends after inactivity

### Solution: External Pinging

Your backend already has **internal keep-alive** (pings every 14 min), but Render blocks self-pings. We need **external services** to wake Render.

---

### Option A: Cron-Job.org (Recommended) ⭐

**Why Cron-Job.org?**
- ✅ **No credit card required**
- ✅ **Unlimited free jobs**
- ✅ **Flexible intervals** (every 5-10 minutes)
- ✅ **Simple setup** (no email verification needed)

**Setup:**

1. Sign up: [cron-job.org](https://cron-job.org) (free account)

2. Create jobs:
   - **Job 1: Keep HuggingFace Space Awake**
     ```
     Title: FactCheckAI ML Server Keep-Alive
     URL: https://bharat2004-factcheckai-ml-serve.hf.space
     Interval: Every 10 minutes
     HTTP Method: GET
     Notifications: None (optional)
     ```
   
   - **Job 2: Keep Render Backend Awake**
     ```
     Title: FactCheckAI Backend Keep-Alive
     URL: https://factcheckai-backend.onrender.com/health
     Interval: Every 10 minutes
     HTTP Method: GET
     Notifications: Email on failure (optional)
     ```

3. **Activate both jobs** - they'll start pinging immediately

**Result**: Both services will stay awake during daytime hours, minimal cold starts.

---

### Option B: UptimeRobot (Alternative)

### Option B: UptimeRobot (Alternative)

**Why UptimeRobot?**
- ✅ **No credit card required**
- ✅ **50 monitors free**
- ✅ **Pings every 5 minutes** (keeps Render awake)
- ✅ **Email alerts** on downtime

**Setup:**

1. Sign up: [uptimerobot.com](https://uptimerobot.com)

2. Add monitors:
   - **Monitor 1: Render Backend**
     ```
     Type: HTTP(s)
     URL: https://factcheckai-backend.onrender.com/health
     Interval: 5 minutes
     ```
   
   - **Monitor 2: HuggingFace Space**
     ```
     Type: HTTP(s)
     URL: https://YOUR-USERNAME-factcheckai-ml-server.hf.space/health
     Interval: 5 minutes
     ```

3. **Enable alerts**: Get notified if services go down

---

### Option B: Cron-Job.org (Alternative)

**Why Cron-Job.org?**
- ✅ **No credit card required**
- ✅ **Unlimited free jobs**
- ✅ **Flexible intervals**

**Setup:**

1. Sign up: [cron-job.org](https://cron-job.org)

2. Create jobs:
   - **Job 1: Ping Render**
     ```
     URL: https://factcheckai-backend.onrender.com/health
     Schedule: */5 * * * * (every 5 minutes)
     ```
   
   - **Job 2: Ping HuggingFace**
     ```
     URL: https://YOUR-USERNAME-factcheckai-ml-server.hf.space/health
     Schedule: */10 * * * * (every 10 minutes)
     ```

---

### Option C: GitHub Actions (Free, Runs in Your Repo)

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Services Awake

on:
  schedule:
    # Runs every 10 minutes
    - cron: '*/10 * * * *'
  workflow_dispatch: # Manual trigger

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render Backend
        run: |
          curl -f https://factcheckai-backend.onrender.com/health || echo "Backend ping failed"
      
      - name: Ping HuggingFace Space
        run: |
          curl -f https://${{ secrets.HF_SPACE_URL }}/health || echo "HF Space ping failed"
```

**Note**: GitHub Actions free tier gives you 2,000 minutes/month (enough for this).

---

### Recommendation: Use Cron-Job.org + Internal Pinger ⭐

```
External (Cron-Job.org)
    → Pings HF Space every 10 min
    → Pings Render every 10 min
    → Keeps both services awake

Internal (your backend)
    → Pings HuggingFace every 14 min
    → Keeps HF Space awake (redundant)
    → Pings Neon DB on every request
    → Auto-wakes Neon
```

**Result**: 99%+ uptime, <1 second cold start if both pingers fail.

---

## 🔑 Step 5: Get Free API Keys

### LLM Providers (for RAG reasoning)

1. **Groq** (fastest inference)
   - Sign up: [console.groq.com](https://console.groq.com)
   - Free tier: 14,400 requests/day
   - Models: Llama 3.3 70B, Mixtral 8x7B
   - **No credit card needed**

2. **Cerebras** (ultra-fast inference)
   - Sign up: [cloud.cerebras.ai](https://cloud.cerebras.ai)
   - Free tier: Generous (not disclosed)
   - Models: Llama 3.3 70B
   - **No credit card needed**

3. **Google Gemini** (best for reasoning)
   - Sign up: [aistudio.google.com](https://aistudio.google.com)
   - Free tier: 1,500 requests/day
   - Models: Gemini 2.0 Flash (free)
   - **No credit card needed**

### Evidence Search

4. **Tavily** (best for fact-checking)
   - Sign up: [tavily.com](https://tavily.com)
   - Free tier: 1,000 searches/month
   - **No credit card needed**

5. **NewsAPI** (news articles)
   - Sign up: [newsapi.org](https://newsapi.org)
   - Free tier: 100 requests/day
   - **No credit card needed**

---

## 📊 Step 6: Monitor Your Deployment

### Check Service Status

```bash
# Backend health
curl https://factcheckai-backend.onrender.com/health

# ML Server health
curl https://YOUR-USERNAME-factcheckai-ml-server.hf.space/health

# Database connection (requires auth)
curl -X POST https://factcheckai-backend.onrender.com/message \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}'
```

### Render Logs

- Dashboard → Your Service → Logs
- Watch for:
  - ✅ `Database connected successfully`
  - ✅ `ML Server 2 keep-alive successful`
  - ⚠️ Any errors or timeouts

### UptimeRobot Dashboard

- Check uptime percentage (should be >99%)
- Review response times
- Monitor downtime alerts

---

## 🔧 Troubleshooting

### Issue 1: Render Shows "Service Unavailable"

**Cause**: Cold start (service was asleep)

**Solution**:
- Wait 10-30 seconds, try again
- Verify UptimeRobot is pinging every 5 minutes
- Check Render logs for errors

---

### Issue 2: HuggingFace Space Returns 503

**Cause**: Space is starting up (cold start)

**Solution**:
- HF Spaces take 30s-2min to wake
- Your backend has retry logic built-in
- Falls back to TF-IDF if ML server fails

---

### Issue 3: Database Connection Fails

**Cause**: Neon DB suspended, connection string wrong

**Solution**:
```bash
# Test Neon connection
psql "postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Verify in Render environment variables
# Make sure DATABASE_URL is the POOLED connection string
```

---

### Issue 4: "ML Server 2 keep-alive failed"

**Cause**: HF Space URL wrong or Space not deployed

**Solution**:
```bash
# Test HF Space directly
curl https://YOUR-USERNAME-factcheckai-ml-server.hf.space/health

# Check Space status in HF dashboard
# Verify ML_SERVER_2_URL in Render env vars
```

---

## 💰 Cost Breakdown (All Free!)

| Service | Free Tier | Cost |
|---------|-----------|------|
| **Neon PostgreSQL** | 0.5GB storage, 3GB transfer/month | $0 |
| **Render** | 512MB RAM, 750 hours/month | $0 |
| **HuggingFace Spaces** | CPU inference, 16GB RAM | $0 |
| **UptimeRobot** | 50 monitors, 5-min intervals | $0 |
| **Groq API** | 14,400 requests/day | $0 |
| **Cerebras API** | Generous free tier | $0 |
| **Gemini API** | 1,500 requests/day | $0 |
| **Tavily API** | 1,000 searches/month | $0 |
| **NewsAPI** | 100 requests/day | $0 |
| **Total** | | **$0/month** |

---

## 🚀 Upgrade Path (When You Have Budget)

### When to Upgrade:

1. **Render sleeps too often** → Upgrade to Render Starter ($7/month) for always-on
2. **HF Space is slow** → Use Modal ($30 free credits/month) or Together.ai
3. **Database too small** → Neon Scale ($19/month for 3GB)
4. **Need faster ML** → Deploy on Fly.io with persistent GPU

### Estimated Costs After Upgrade:
- **Render Starter**: $7/month (always-on, 512MB RAM)
- **Neon Scale**: $19/month (3GB storage, better uptime)
- **Modal/Together**: ~$30/month (faster ML inference)
- **Total**: ~$56/month for production-grade

---

## ✅ Deployment Checklist

- [ ] Neon PostgreSQL created, `DATABASE_URL` copied
- [ ] HuggingFace Space deployed, `/health` endpoint works
- [ ] Render backend deployed, environment variables set
- [ ] UptimeRobot monitors created (Render + HF Space)
- [ ] All API keys obtained (Groq, Cerebras, Gemini, Tavily, NewsAPI)
- [ ] Extension updated with backend URL
- [ ] Test fact-check: Extension → Backend → ML Server → DB
- [ ] Monitor logs for 24 hours to verify stability

---

## 📚 Additional Resources

- [Neon Documentation](https://neon.tech/docs)
- [HuggingFace Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Render Documentation](https://render.com/docs)
- [UptimeRobot API](https://uptimerobot.com/api)

---

## 🛟 Need Help?

1. **Check logs**: Render dashboard → Logs tab
2. **Test endpoints**: Use `curl` commands above
3. **Verify env vars**: Render dashboard → Environment tab
4. **Review README**: [README.md](README.md) for architecture details

---

**Built with ❤️ using 100% free services. No credit card required!**
