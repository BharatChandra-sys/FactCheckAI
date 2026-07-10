# 100% FREE Deployment - NO CREDIT CARD NEEDED! 🎓

Deploy FactCheckAI using **only** GitHub Student Developer Pack (no credit card required!)

---

## 🎯 Your Situation

✅ You have: GitHub Student Developer Pack  
✅ You have: Models on HuggingFace  
✅ You have: $200 DigitalOcean credit  
✅ You have: $100 Azure credit  
❌ You don't have: Credit card (so no Oracle Cloud)

**Solution: Use HuggingFace + Azure + DigitalOcean!**

---

## 🏗️ New Architecture (NO Credit Card Needed!)

```
┌─────────────────────────────────────────────────────────┐
│  Main API Server (Azure FREE - 1GB RAM)                 │
│  - FastAPI backend                                       │
│  - TF-IDF model (50MB)                                   │
│  - Auth, rate limiting, caching                          │
│  Cost: $0 (FREE tier for 12 months)                     │
└────────────┬────────────────────────────────────────────┘
             │
             ├─────────────────────┬─────────────────────┐
             ▼                     ▼                     ▼
┌──────────────────────┐  ┌─────────────────┐  ┌────────────────────┐
│ PostgreSQL           │  │ ML Server 1     │  │ ML Server 2        │
│ (Azure FREE)         │  │ (HF Space #1)   │  │ (HF Space #2)      │
│ - 250MB storage      │  │ - 16GB RAM      │  │ - 16GB RAM         │
│ Cost: $0             │  │ - DeBERTa       │  │ - Ensemble         │
│                      │  │ - FREE          │  │ - FREE             │
└──────────────────────┘  └─────────────────┘  └────────────────────┘

Total: $0/month for 12 months! No credit card! 🎉
```

---

## 🚀 Step-by-Step Deployment

### Phase 1: Setup PostgreSQL on Azure (10 minutes)

#### Option A: Azure Database for PostgreSQL (Easiest)

```bash
# 1. Go to portal.azure.com
# 2. Click "Create a resource"
# 3. Search "Azure Database for PostgreSQL"
# 4. Select "Flexible server"
# 5. Configure:
#    - Resource group: factcheck-rg (create new)
#    - Server name: factcheck-db
#    - Region: East US
#    - Version: 14
#    - Compute + storage: Burstable, B1ms (1 vCore, 2 GiB memory)
#    - Set admin username: factcheck_admin
#    - Set password: (create strong password)
# 6. Networking tab:
#    - Allow public access from any Azure service: Yes
#    - Add current IP address: Yes
# 7. Review + Create
# 8. Wait 5-10 minutes for deployment
```

**Connection string format:**
```
postgresql://factcheck_admin:YOUR_PASSWORD@factcheck-db.postgres.database.azure.com:5432/postgres?sslmode=require
```

#### Option B: Use Render (Free, No Azure credit used)

If you want to save Azure credit:

```bash
# 1. Go to render.com
# 2. Sign up with GitHub (NO CREDIT CARD!)
# 3. New → PostgreSQL
# 4. Name: factcheck-db
# 5. Region: Oregon
# 6. Plan: Free (256MB RAM, 1GB storage)
# 7. Create
# 8. Copy "Internal Database URL"
```

**Recommended**: Use Render for database (free), save Azure for API server!

---

### Phase 2: Deploy ML Server 1 on HuggingFace (10 minutes)

You already have models on HuggingFace! Let's create the first ML server.

#### Step 2.1: Create Space for DeBERTa

```bash
# 1. Go to huggingface.co
# 2. Click your profile → New Space
# 3. Configure:
#    - Name: factcheck-ml-server-1
#    - License: MIT
#    - SDK: Gradio
#    - Hardware: CPU basic (FREE - 16GB RAM)
#    - Visibility: Public
# 4. Create Space
```

#### Step 2.2: Create the Server Code

Click "Files" → "Add file" → Create these files:

**File 1: `app.py`**
```python
import gradio as gr
from transformers import pipeline
import os

ML_API_KEY = os.getenv("ML_API_KEY", "change-me")

# Load your DeBERTa model from HuggingFace
model = pipeline(
    "text-classification",
    model="Bharat2004/deberta-fakenews-detector",
    device=-1
)

def predict(text: str, api_key: str):
    if api_key != ML_API_KEY:
        return {"error": "Invalid API key"}
    
    result = model(text[:1500])[0]
    label = result["label"].upper()
    score = float(result["score"])
    
    # Convert to fake probability
    if label in ("LABEL_1", "FAKE"):
        fake_prob = score
    else:
        fake_prob = 1.0 - score
    
    return {
        "fake_probability": round(fake_prob, 3),
        "model": "deberta",
        "confidence": score,
        "server": "ml-server-1-hf"
    }

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Textbox(label="Text", lines=5),
        gr.Textbox(label="API Key", type="password")
    ],
    outputs=gr.JSON(),
    title="ML Server 1 - DeBERTa",
    examples=[["The Earth is flat", ML_API_KEY]]
)

demo.launch()
```

**File 2: `requirements.txt`**
```
gradio==4.44.0
transformers==4.45.0
torch==2.5.0
```

#### Step 2.3: Add API Key Secret

1. Go to Space → Settings tab
2. Scroll to "Repository secrets"
3. Click "New secret"
4. Add:
   - Name: `ML_API_KEY`
   - Value: Run this command to generate: `python -c "import secrets; print(secrets.token_hex(32))"`
5. **Save this key** - you'll need it later!

#### Step 2.4: Wait for Deployment

Space will auto-build (3-5 minutes). Watch the "Logs" tab.

When done, your server will be at:
```
https://huggingface.co/spaces/YOUR_USERNAME/factcheck-ml-server-1
```

✅ **ML Server 1 ready!**

---

### Phase 3: Deploy ML Server 2 on HuggingFace (10 minutes)

Same process for ensemble model.

#### Step 3.1: Create Second Space

```bash
# 1. New Space
# 2. Name: factcheck-ml-server-2
# 3. SDK: Gradio
# 4. Hardware: CPU basic (FREE)
# 5. Visibility: Public
```

#### Step 3.2: Create Server Code

**File 1: `app.py`**
```python
import gradio as gr
from transformers import pipeline
import os

ML_API_KEY = os.getenv("ML_API_KEY", "change-me")

# Load your models
model1 = pipeline("text-classification", model="Bharat2004/out", device=-1)
model2 = pipeline("text-classification", model="Bharat2004/deberta-factchecker", device=-1)

def predict(text: str, api_key: str):
    if api_key != ML_API_KEY:
        return {"error": "Invalid API key"}
    
    # Run both models
    r1 = model1(text[:1500])[0]
    r2 = model2(text[:1500])[0]
    
    def get_fake_prob(result):
        label = result["label"].upper()
        score = float(result["score"])
        return score if label in ("LABEL_1", "FAKE") else 1.0 - score
    
    fake1 = get_fake_prob(r1)
    fake2 = get_fake_prob(r2)
    
    # Weighted ensemble
    ensemble = (fake1 * 0.4) + (fake2 * 0.6)
    
    return {
        "fake_probability": round(ensemble, 3),
        "models": ["distilbert", "deberta"],
        "individual": [fake1, fake2],
        "server": "ml-server-2-hf"
    }

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Textbox(label="Text", lines=5),
        gr.Textbox(label="API Key", type="password")
    ],
    outputs=gr.JSON(),
    title="ML Server 2 - Ensemble",
    examples=[["Modi is PM of India", ML_API_KEY]]
)

demo.launch()
```

**File 2: `requirements.txt`**
```
gradio==4.44.0
transformers==4.45.0
torch==2.5.0
```

#### Step 3.3: Add Same API Key

Use the **same API key** as ML Server 1 in the secrets!

✅ **ML Server 2 ready!**

---

### Phase 4: Deploy Main API on Azure (30 minutes)

#### Option A: Azure App Service (Recommended)

```bash
# 1. Go to portal.azure.com
# 2. Create a resource → Web App
# 3. Configure:
#    - Resource group: factcheck-rg (same as before)
#    - Name: factcheck-api
#    - Publish: Code
#    - Runtime: Python 3.11
#    - OS: Linux
#    - Region: East US
#    - Plan: Free F1 (1GB RAM) - FREE TIER!
# 4. Review + Create
# 5. Wait for deployment
```

#### Step 4.1: Setup Deployment from GitHub

```bash
# 1. In Azure portal, go to your Web App
# 2. Deployment Center → GitHub
# 3. Authorize Azure to access GitHub
# 4. Select:
#    - Organization: YOUR_USERNAME
#    - Repository: FactCheckAI
#    - Branch: main
# 5. Save
```

#### Step 4.2: Configure Environment Variables

```bash
# In Azure portal, go to:
# Configuration → Application settings → New application setting

# Add these (one by one):
```

**Required Settings:**
```bash
DATABASE_URL=postgresql://user:pass@host/db
ML_SERVER_1_URL=https://huggingface.co/spaces/YOUR_USERNAME/factcheck-ml-server-1
ML_SERVER_2_URL=https://huggingface.co/spaces/YOUR_USERNAME/factcheck-ml-server-2
ML_API_KEY=your_api_key_from_phase_2

# AI Keys
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
CEREBRAS_API_KEY=your_cerebras_key
NEWS_API_KEY=your_news_key
TAVILY_API_KEY=your_tavily_key
SERPAPI_KEY=your_serpapi_key
GOOGLE_FACTCHECK_API_KEY=your_google_key

# Auth
JWT_SECRET=run: python -c "import secrets; print(secrets.token_hex(32))"
GOOGLE_CLIENT_ID=your_google_client_id

# Email
SMTP_USER=your_email@gmail.com
BREVO_API_KEY=your_brevo_key

# Settings
ENABLE_DOCS=false
RATE_LIMIT_ENABLED=true
```

#### Step 4.3: Create Startup File

In your repository, create `backend/startup.sh`:

```bash
#!/bin/bash
cd /home/site/wwwroot/backend
python -m pip install --upgrade pip
pip install -r requirements.txt
gunicorn --bind=0.0.0.0:8000 --workers=2 --timeout=600 app.main:app
```

Make it executable:
```bash
git update-index --chmod=+x backend/startup.sh
git commit -m "Make startup script executable"
git push
```

#### Step 4.4: Configure Startup Command

In Azure:
```bash
# Configuration → General settings → Startup Command:
/home/site/wwwroot/backend/startup.sh
```

Save and restart the app.

#### Step 4.5: Test Main API

After ~5 minutes, your API will be at:
```
https://factcheck-api.azurewebsites.net
```

Test:
```bash
curl https://factcheck-api.azurewebsites.net/health
```

✅ **Main API ready!**

---

### Phase 5: Update Extension (5 minutes)

Edit `extension/popup/config.js`:

```javascript
const API = "https://factcheck-api.azurewebsites.net";
```

Reload extension in Chrome:
1. Go to `chrome://extensions`
2. Find FactCheckAI
3. Click refresh 🔄

✅ **Extension ready!**

---

## 📊 Cost Breakdown

### With GitHub Student Pack

| Service | Provider | RAM | Cost | Duration |
|---------|----------|-----|------|----------|
| Main API | Azure | 1GB | $0 | 12 months free |
| PostgreSQL | Render | 256MB | $0 | Forever |
| ML Server 1 | HuggingFace | 16GB | $0 | Forever |
| ML Server 2 | HuggingFace | 16GB | $0 | Forever |
| **TOTAL** | 4 servers | 33GB | **$0** | **12 months** |

After 12 months, you still have:
- HuggingFace: Forever free
- Render: Forever free
- Azure: Use your remaining credit or switch to DigitalOcean

---

## 🎯 Alternative: Use DigitalOcean Instead of Azure

If you prefer DigitalOcean:

### Deploy on DigitalOcean App Platform

```bash
# 1. Go to cloud.digitalocean.com
# 2. Apps → Create App
# 3. Connect GitHub repository
# 4. Select FactCheckAI repo
# 5. Configure:
#    - Build command: pip install -r backend/requirements.txt
#    - Run command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
#    - Environment: Add all variables from Phase 4
# 6. Choose plan: Basic ($5/month)
# 7. Deploy
```

**Cost**: $5/month, but you have $200 credit = **40 months free!**

---

## 🎓 What About Oracle Cloud?

**Problem**: Oracle requires credit card verification (even for free tier)

**Solutions if you get a credit card later:**
1. Get a prepaid card with $1-2
2. Use a virtual card (Privacy.com in some countries)
3. Ask a parent/friend to verify (they won't be charged)

**But for now**: Azure + HuggingFace works perfectly!

---

## 🔧 Troubleshooting

### Azure App Service Issues

**Issue**: App won't start
```bash
# Check logs in Azure portal:
# Monitoring → Log stream

# Common fix: Update startup.sh path
```

**Issue**: Database connection fails
```bash
# Fix: Add Azure's outbound IP to database firewall
# In PostgreSQL settings → Networking → Add Azure IPs
```

### HuggingFace Space Issues

**Issue**: Space stuck "Building"
```bash
# Fix: Check requirements.txt for errors
# Common: Wrong version numbers
```

**Issue**: API returns error
```bash
# Fix: Check Space logs tab
# Common: Wrong API key or model not found
```

---

## 🚀 After Deployment

### Test Everything

```bash
# 1. Test ML Server 1
curl -X POST https://huggingface.co/spaces/YOUR_USERNAME/factcheck-ml-server-1/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["Test claim", "YOUR_API_KEY"]}'

# 2. Test ML Server 2
curl -X POST https://huggingface.co/spaces/YOUR_USERNAME/factcheck-ml-server-2/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["Test claim", "YOUR_API_KEY"]}'

# 3. Test Main API
curl https://factcheck-api.azurewebsites.net/health

# 4. Test Extension
# Open extension → Enter claim → Fact Check!
```

---

## 💡 Pro Tips

### Save Azure Credit

- Use Render for PostgreSQL (free forever)
- Use HuggingFace for ML servers (free forever)
- Use Azure only for Main API (most important)

### Optimize Performance

- Enable caching in backend
- Use CDN (Cloudflare - free)
- Monitor Azure metrics

### When Azure Free Tier Ends (After 12 months)

**Option 1**: Switch to DigitalOcean
- Still have ~$150 credit left
- Same setup process
- 30+ more months free

**Option 2**: Get credit card and use Oracle
- 24GB RAM free forever
- Better performance
- No time limit

---

## 📚 Summary

### What You Deployed

✅ Main API on Azure (1GB RAM, 12 months free)
✅ PostgreSQL on Render (free forever)
✅ ML Server 1 on HuggingFace (16GB, free forever)
✅ ML Server 2 on HuggingFace (16GB, free forever)
✅ Extension connected and working

### Total Cost

- **First 12 months**: $0
- **After 12 months**: Switch to DigitalOcean ($0 for 30+ more months)
- **Total free time**: 42+ months! 🎉

### No Credit Card Needed!

All services used:
- ✅ Azure (student email only)
- ✅ HuggingFace (email only)
- ✅ Render (GitHub only)
- ✅ GitHub (email only)

**You did it without a credit card!** 🎊

---

## 📞 Need Help?

If stuck:
1. Check Azure logs (Monitoring → Log stream)
2. Check HuggingFace Space logs
3. Test each service individually
4. Email: bc833498@gmail.com

---

**Deployment guide for students without credit cards!** 🎓✨

