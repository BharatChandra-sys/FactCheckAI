# Free Deployment with Transformer Models (2GB+ RAM)

FactCheckAI uses transformer models (DeBERTa/RoBERTa) that require **at least 2GB RAM**. Here are the best FREE hosting options that can handle this.

## 🎯 Best FREE Options (With Transformer Support)

### Option 1: Render.com (RECOMMENDED) ✅

**Free Tier Specs:**
- ✅ **512MB RAM** (not enough for transformers alone)
- ✅ **But with swap: Can run DeBERTa!**
- ✅ Automatic deployments from GitHub
- ✅ Free PostgreSQL database
- ✅ Free SSL
- ✅ No credit card required
- ⚠️ Spins down after 15 min inactivity (cold start)

**Workaround for Transformers:**
- Use lightweight model: `Bharat2004/out` (268 MB DistilBERT)
- Enable swap file
- Optimize with model quantization
- Falls back to TF-IDF if OOM

**Setup:**

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/FactCheckAI.git
git push -u origin main

# 2. Create Render Account
# Go to https://render.com and sign up with GitHub

# 3. Create Web Service
# - New → Web Service
# - Connect your GitHub repo
# - Name: factcheck-api
# - Environment: Python 3
# - Build Command: pip install -r requirements.txt
# - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1

# 4. Add Environment Variables
DEBERTA_MODEL=Bharat2004/out
FORCE_TRANSFORMER_LOAD=true
HF_TOKEN=your_huggingface_token
CEREBRAS_API_KEY=xxx
GROQ_API_KEY=xxx
GEMINI_API_KEY=xxx
NEWS_API_KEY=xxx
JWT_SECRET=xxx
DATABASE_URL=postgresql://... (from Render PostgreSQL)
```

**Cost:** $0/month (FREE forever)

---

### Option 2: Railway.app (EXCELLENT!) 🚂

**Free Tier Specs:**
- ✅ **512MB RAM** (base)
- ✅ **$5 free credits/month** (can upgrade to 2GB with credits)
- ✅ **No sleep mode** - always on!
- ✅ Automatic deployments
- ✅ PostgreSQL included
- ✅ Free SSL

**Best Part:** $5/month credit = 2GB RAM instance!

**Setup:**

```bash
# 1. Install Railway CLI
npm i -g @railway/cli
# Or: curl -fsSL https://railway.app/install.sh | sh

# 2. Login
railway login

# 3. Create project
cd FactCheckAI/backend
railway init

# 4. Add PostgreSQL
railway add postgresql

# 5. Set environment variables
railway variables set DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector
railway variables set FORCE_TRANSFORMER_LOAD=true
railway variables set HF_TOKEN=xxx
# ... (add all other env vars)

# 6. Deploy
railway up

# 7. Get URL
railway domain
```

**Cost with Free Credits:**
- 512MB: FREE (just API calls)
- 2GB: $7/month - $5 credit = **$2/month**

---

### Option 3: Fly.io (Good for Multiple Regions) 🌍

**Free Tier Specs:**
- ✅ **3 shared-cpu-1x instances** (256MB each)
- ✅ **3GB total memory** when combined
- ✅ Multiple regions
- ✅ Auto-scaling
- ✅ Free PostgreSQL (3GB storage)

**Unique Feature:** Deploy to multiple regions for global speed!

**Setup:**

```bash
# 1. Install Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Launch app
cd FactCheckAI/backend
fly launch --name factcheck-api

# 4. Create PostgreSQL
fly postgres create --name factcheck-db

# 5. Attach database
fly postgres attach factcheck-db

# 6. Set secrets
fly secrets set DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector
fly secrets set FORCE_TRANSFORMER_LOAD=true
fly secrets set HF_TOKEN=xxx
# ... (add all)

# 7. Deploy
fly deploy

# 8. Scale up memory (use free allowance)
fly scale memory 512
```

**Cost:** $0/month (within free tier)

---

### Option 4: Hugging Face Spaces (Best for ML!) 🤗

**Free Tier Specs:**
- ✅ **16GB RAM** (CPU)
- ✅ **FREE GPU** (T4, limited hours)
- ✅ Designed for ML models
- ✅ Automatic deployments from GitHub
- ✅ No sleep mode

**Perfect for your fine-tuned models!**

**Setup:**

```bash
# 1. Create Space on HuggingFace
# Go to https://huggingface.co/spaces
# New Space → Name: factcheck-api → Gradio SDK

# 2. Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/factcheck-api
cd factcheck-api

# 3. Copy backend files
cp -r ../FactCheckAI/backend/* .

# 4. Create app.py
cat > app.py << 'EOF'
import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
EOF

# 5. Create requirements.txt (use your backend/requirements.txt)
cp requirements.txt requirements.txt

# 6. Add secrets in Space settings
# Go to Settings → Variables
# Add all your API keys

# 7. Push to deploy
git add .
git commit -m "Deploy FactCheckAI"
git push
```

**Cost:** $0/month (FREE forever)

---

### Option 5: Google Cloud (Best with GitHub Student Pack) ☁️

**Student Benefits:**
- ✅ **$300 credit** (12 months)
- ✅ Always Free tier after credits expire
- ✅ **E2-micro instance** (1GB RAM) - ENOUGH for DeBERTa!
- ✅ Cloud Run (2GB RAM container)
- ✅ Professional infrastructure

**Setup:**

```bash
# 1. Claim $300 credit
# Go to https://cloud.google.com/edu
# Sign up with your student email

# 2. Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# 3. Login
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 4. Deploy to Cloud Run (2GB RAM!)
cd FactCheckAI/backend
gcloud run deploy factcheck-api \
  --source . \
  --memory 2Gi \
  --cpu 1 \
  --region us-central1 \
  --allow-unauthenticated

# 5. Set environment variables
gcloud run services update factcheck-api \
  --set-env-vars DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector \
  --set-env-vars FORCE_TRANSFORMER_LOAD=true \
  --set-env-vars HF_TOKEN=xxx
```

**Cost:**
- First 12 months: FREE ($300 credit)
- After: Cloud Run free tier = 2 million requests/month FREE
- E2-micro: FREE forever (1 instance)

---

### Option 6: DigitalOcean with GitHub Student Pack 💎

**Student Benefits:**
- ✅ **$200 credit** (12 months)
- ✅ Droplet starting at **$4/month for 512MB**
- ✅ **$12/month for 2GB** (PERFECT for transformers!)
- ✅ Best performance/price ratio

**Recommendation:** Use **$12/month 2GB droplet**

**Cost Calculation:**
- $200 credit ÷ $12/month = **16 months FREE**
- **Plus** $15/month PostgreSQL = $27/month total
- $200 ÷ $27 = **7 months FREE** (with database)

**Alternative:** Use SQLite instead of PostgreSQL → 16 months FREE!

```bash
# In .env
DATABASE_URL=sqlite:///./factchecker.db
```

---

### Option 7: Oracle Cloud (Best RAM/Free!) 🔥

**Always Free Tier:**
- ✅ **4 ARM-based Ampere A1 cores**
- ✅ **24GB RAM** total (!!!)
- ✅ **200GB storage**
- ✅ **Forever FREE**
- ✅ No credit card required after trial

**Best specs of all free tiers!**

**Setup:**

```bash
# 1. Create Oracle Cloud account
# https://www.oracle.com/cloud/free/

# 2. Create Compute Instance
# - Shape: VM.Standard.A1.Flex
# - OCPU: 2
# - Memory: 12GB (you get 24GB total across instances)
# - Image: Ubuntu 22.04

# 3. SSH and install
ssh ubuntu@instance-ip
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx

# 4. Clone and setup
git clone https://github.com/YOUR_USERNAME/FactCheckAI.git
cd FactCheckAI/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Create .env with transformer config
echo "DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector" >> .env
echo "FORCE_TRANSFORMER_LOAD=true" >> .env
# ... add all keys

# 6. Run with systemd (see DEPLOYMENT_GITHUB_STUDENT.md)
```

**Cost:** $0/month (FREE FOREVER!)

---

## 📊 Comparison Table

| Platform | RAM | Cost | Sleep? | Best For |
|----------|-----|------|--------|----------|
| **Render** | 512MB | FREE | Yes (15min) | Quick deploy |
| **Railway** | 2GB | $2/month | No | Production ready |
| **Fly.io** | 512MB-1GB | FREE | No | Global CDN |
| **HuggingFace** | 16GB | FREE | No | ML-focused |
| **Google Cloud** | 2GB | FREE (12mo) | No | Enterprise grade |
| **DigitalOcean** | 2GB | FREE (16mo) | No | Full control |
| **Oracle Cloud** | 24GB | FREE forever | No | **BEST SPECS** |

## 🏆 WINNER: Oracle Cloud Always Free

**Why Oracle Cloud wins:**
- 24GB RAM (can run ALL transformers)
- 4 CPU cores
- Forever free (no expiration)
- No sleep mode
- Full root access

**Only downside:** Slightly complex setup (30 min vs 5 min)

---

## 🚀 Quick Start: Railway (Recommended for Beginners)

**Why Railway:**
- ✅ Easiest setup (5 minutes)
- ✅ 2GB RAM with free credits
- ✅ No sleep mode
- ✅ GitHub auto-deploy
- ✅ Built-in PostgreSQL

**Steps:**

1. **Sign up:** https://railway.app/
2. **New Project** → Deploy from GitHub
3. **Connect repo:** FactCheckAI
4. **Add PostgreSQL:** Railway automatically provisions
5. **Add variables:**
   ```
   DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector
   FORCE_TRANSFORMER_LOAD=true
   HF_TOKEN=your_huggingface_token
   ```
6. **Deploy!** - Railway handles everything

**Result:** Production-ready API with transformer models in 5 minutes! 🎉

---

## 💡 Optimization Tips for 512MB Deployments

If you must use 512MB (Render/Fly.io):

1. **Use DistilBERT** (smaller, faster):
   ```bash
   DEBERTA_MODEL=Bharat2004/out  # 268MB instead of 738MB
   ```

2. **Enable model quantization**:
   ```python
   # In ml.py, add:
   _roberta_pipe = pipeline(
       "text-classification",
       model=ROBERTA_MODEL,
       tokenizer=ROBERTA_MODEL,
       device=-1,  # CPU only
       framework="pt",
       model_kwargs={"torch_dtype": "float16"}  # Half precision
   )
   ```

3. **Lazy loading** (already implemented):
   - Model only loads on first request
   - TF-IDF used for health checks

4. **Add swap space** (Render):
   ```bash
   # In render.yaml
   services:
     - type: web
       name: factcheck-api
       env: python
       buildCommand: |
         pip install -r requirements.txt
         fallocate -l 1G /tmp/swapfile
         chmod 600 /tmp/swapfile
         mkswap /tmp/swapfile
         swapon /tmp/swapfile
   ```

---

## 🎓 Recommended Path

1. **Start with Railway** ($2/month, 2GB, easy)
2. **Scale to Oracle Cloud** (24GB, free forever, best performance)
3. **Use DigitalOcean Student Credit** as backup (16 months free)

---

## 📧 Need Help?

- GitHub Issues: https://github.com/YOUR_USERNAME/FactCheckAI/issues
- Email: bc833498@gmail.com

**Pro tip:** All these platforms have free tiers - try multiple and see which works best! 🚀
