# 100% Free Deployment Checklist ✅

Complete step-by-step checklist for deploying FactCheckAI with **$0/month cost**.

---

## 📋 Before You Start

### Required Accounts (All Free!)
- [ ] GitHub account
- [ ] Oracle Cloud account (24GB free tier)
- [ ] Render account (free PostgreSQL)
- [ ] HuggingFace account (16GB free tier)

### Estimated Time
- **Total**: ~1.5 hours
- **Phase 1** (PostgreSQL): 5 minutes
- **Phase 2** (ML Server 2): 10 minutes
- **Phase 3** (ML Server 1): 30 minutes
- **Phase 4** (Main API): 30 minutes
- **Phase 5** (Extension): 5 minutes
- **Testing**: 10 minutes

---

## Phase 1: PostgreSQL Database (5 min) ✅

### 1.1 Create Render Account
- [ ] Go to https://render.com
- [ ] Sign up with GitHub
- [ ] Verify email

### 1.2 Create Database
- [ ] Click **New** → **PostgreSQL**
- [ ] Name: `factcheck-db`
- [ ] Region: Oregon (or nearest)
- [ ] Plan: **Free** (256MB RAM, 1GB storage)
- [ ] Click **Create Database**
- [ ] Wait 2-3 minutes

### 1.3 Get Connection String
- [ ] Open database in Render dashboard
- [ ] Scroll to **Connections**
- [ ] Copy **Internal Database URL**
- [ ] Save in notes (format: `postgresql://user:pass@host/db`)

**Status**: PostgreSQL ready! ($0/month)

---

## Phase 2: ML Server 2 - HuggingFace (10 min) ✅

### 2.1 Create HuggingFace Account
- [ ] Go to https://huggingface.co
- [ ] Sign up with email
- [ ] Verify account

### 2.2 Create Space
- [ ] Click profile → **New Space**
- [ ] Name: `ml-server-2`
- [ ] SDK: **Gradio**
- [ ] Hardware: **CPU basic** (FREE - 16GB)
- [ ] Visibility: **Public**
- [ ] Click **Create Space**

### 2.3 Clone and Setup
```bash
# On your computer
git clone https://huggingface.co/spaces/YOUR_USERNAME/ml-server-2
cd ml-server-2

# Copy files
cp /path/to/FactCheckAI/ml-servers/huggingface-ensemble/app.py .
cp /path/to/FactCheckAI/ml-servers/huggingface-ensemble/requirements.txt .
```

- [ ] Files copied to space directory

### 2.4 Generate and Add API Key
```bash
# Generate key
openssl rand -hex 32
```

- [ ] Copy the generated key
- [ ] Go to HuggingFace Space → **Settings**
- [ ] Scroll to **Repository secrets**
- [ ] Click **New secret**
  - Name: `ML_API_KEY`
  - Value: (paste generated key)
- [ ] Click **Save**
- [ ] **Save this key in notes** - you'll need it for other servers!

### 2.5 Deploy to HuggingFace
```bash
# In ml-server-2 directory
git add .
git commit -m "Deploy ML ensemble server"
git push
```

- [ ] Pushed to HuggingFace
- [ ] Wait 3-5 minutes for build
- [ ] Space shows "Running" status

### 2.6 Test ML Server 2
```bash
curl -X POST https://YOUR_USERNAME-ml-server-2.hf.space/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["The Earth is flat", "YOUR_ML_API_KEY"]}'
```

- [ ] Returns prediction with `fake_probability`

**Status**: ML Server 2 ready! ($0/month)

---

## Phase 3: ML Server 1 - Oracle Cloud (30 min) ✅

### 3.1 Create Oracle Cloud Account
- [ ] Go to https://oracle.com/cloud/free
- [ ] Click **Start for free**
- [ ] Fill in email, country, account name
- [ ] Add credit/debit card (won't be charged!)
- [ ] Verify phone number
- [ ] Complete sign-up

### 3.2 Create First VM Instance
- [ ] Click **Create a VM instance**
- [ ] Name: `ml-server-1`
- [ ] Image: **Canonical Ubuntu 22.04**
- [ ] Click **Change Shape**
  - [ ] Series: **Ampere**
  - [ ] Shape: **VM.Standard.A1.Flex**
  - [ ] OCPU: **2**
  - [ ] Memory: **12 GB**
- [ ] SSH keys: Generate and download OR paste existing
- [ ] Click **Create**
- [ ] Wait 2-3 minutes
- [ ] Copy **Public IP** to notes

### 3.3 Configure Firewall
- [ ] In instance page, click **Subnet** link
- [ ] Click subnet name
- [ ] Click **Default Security List**
- [ ] Click **Add Ingress Rules**
  - [ ] Source CIDR: `0.0.0.0/0`
  - [ ] Destination Port: `8001`
  - [ ] Description: `ML Server 1`
- [ ] Click **Add Ingress Rules**

### 3.4 SSH and Install
```bash
# SSH into instance
ssh -i ~/Downloads/your-key.key ubuntu@INSTANCE_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip git

# Clone repository
git clone https://github.com/YOUR_USERNAME/FactCheckAI.git
cd FactCheckAI/ml-servers/oracle-deberta

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies (5-10 minutes)
pip install -r requirements.txt
```

- [ ] Python installed
- [ ] Repository cloned
- [ ] Dependencies installed

### 3.5 Configure ML Server 1
```bash
# Create .env file
nano .env
```

Add:
```bash
ML_API_KEY=YOUR_ML_API_KEY_FROM_PHASE_2.4
DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector
```

- [ ] .env file created with correct API key
- [ ] Save (Ctrl+X, Y, Enter)

### 3.6 Test ML Server 1
```bash
# Test run
uvicorn main:app --host 0.0.0.0 --port 8001
```

Open new terminal:
```bash
curl http://INSTANCE_IP:8001/health
```

- [ ] Returns `{"status":"ok","model":"Bharat2004/deberta-fakenews-detector"}`
- [ ] Press Ctrl+C to stop test

### 3.7 Setup Systemd Service
```bash
sudo nano /etc/systemd/system/ml-server-1.service
```

Paste:
```ini
[Unit]
Description=ML Server 1 - DeBERTa
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/FactCheckAI/ml-servers/oracle-deberta
Environment="PATH=/home/ubuntu/FactCheckAI/ml-servers/oracle-deberta/venv/bin"
ExecStart=/home/ubuntu/FactCheckAI/ml-servers/oracle-deberta/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ml-server-1
sudo systemctl start ml-server-1
sudo systemctl status ml-server-1
```

- [ ] Service shows "active (running)"

**Status**: ML Server 1 ready! ($0/month)

---

## Phase 4: Main API - Oracle Cloud (30 min) ✅

### 4.1 Create Second VM Instance
- [ ] In Oracle Cloud, click **Create a VM instance**
- [ ] Name: `main-api`
- [ ] Image: **Canonical Ubuntu 22.04**
- [ ] Shape: **VM.Standard.A1.Flex** (2 OCPU, 12GB RAM)
- [ ] SSH keys: Use same as before OR generate new
- [ ] Click **Create**
- [ ] Wait 2-3 minutes
- [ ] Copy **Public IP** to notes

### 4.2 Configure Firewall
- [ ] In instance page, click **Subnet** link
- [ ] Click **Default Security List**
- [ ] Click **Add Ingress Rules** (do this twice):
  
  **Rule 1 - HTTP:**
  - [ ] Source CIDR: `0.0.0.0/0`
  - [ ] Destination Port: `80`
  - [ ] Description: `HTTP`
  
  **Rule 2 - HTTPS:**
  - [ ] Source CIDR: `0.0.0.0/0`
  - [ ] Destination Port: `443`
  - [ ] Description: `HTTPS`

### 4.3 SSH and Install
```bash
ssh -i ~/Downloads/your-key.key ubuntu@MAIN_API_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx

# Clone repository
git clone https://github.com/YOUR_USERNAME/FactCheckAI.git
cd FactCheckAI/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies (5-10 minutes)
pip install -r requirements.txt
```

- [ ] Dependencies installed

### 4.4 Configure Main API
```bash
nano .env
```

Add (replace with your actual values):
```bash
# Database (from Phase 1)
DATABASE_URL=postgresql://user:pass@host.render.com/db

# ML Servers
ML_SERVER_1_URL=http://ML_SERVER_1_IP:8001
ML_SERVER_2_URL=https://YOUR_USERNAME-ml-server-2.hf.space
ML_API_KEY=YOUR_ML_API_KEY

# AI API Keys
CEREBRAS_API_KEY=your_key
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
NEWS_API_KEY=your_key
TAVILY_API_KEY=your_key
SERPAPI_KEY=your_key
GOOGLE_FACTCHECK_API_KEY=your_key

# Auth
JWT_SECRET=$(openssl rand -hex 32)
GOOGLE_CLIENT_ID=your_google_client_id

# Email
SMTP_USER=your_email@gmail.com
BREVO_API_KEY=your_brevo_key

# Settings
ENABLE_DOCS=false
RATE_LIMIT_ENABLED=true
```

- [ ] .env file created with all values
- [ ] Save (Ctrl+X, Y, Enter)

### 4.5 Setup Systemd Service
```bash
sudo nano /etc/systemd/system/factcheck-api.service
```

Paste:
```ini
[Unit]
Description=FactCheckAI Main API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/FactCheckAI/backend
Environment="PATH=/home/ubuntu/FactCheckAI/backend/venv/bin"
ExecStart=/home/ubuntu/FactCheckAI/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable factcheck-api
sudo systemctl start factcheck-api
sudo systemctl status factcheck-api
```

- [ ] Service shows "active (running)"

### 4.6 Setup Nginx
```bash
sudo nano /etc/nginx/sites-available/factcheck
```

Paste:
```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/factcheck /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

- [ ] Nginx configured and running

### 4.7 Test Main API
```bash
curl http://localhost:8000/health
```

From your computer:
```bash
curl http://MAIN_API_IP/health
```

- [ ] Returns full health check with model info

**Status**: Main API ready! ($0/month)

---

## Phase 5: Update Extension (5 min) ✅

### 5.1 Update Config
```bash
# On your computer
cd /path/to/FactCheckAI/extension/popup
nano config.js
```

Change:
```javascript
const API = "http://MAIN_API_IP";
```

- [ ] Config updated with correct API URL
- [ ] Save file

### 5.2 Reload Extension
- [ ] Open Chrome
- [ ] Go to `chrome://extensions`
- [ ] Find "FactCheckAI"
- [ ] Click refresh icon 🔄

### 5.3 Test Extension
- [ ] Open extension popup
- [ ] Sign up / Login
- [ ] Enter claim: "The Earth is flat"
- [ ] Click "Fact Check"
- [ ] Verify: Gets response with verdict!

**Status**: Extension working! 🎉

---

## Final Verification ✅

### All Services Running
- [ ] PostgreSQL: Check Render dashboard (green status)
- [ ] ML Server 2: Check HuggingFace space (green status)
- [ ] ML Server 1: `curl http://ML_SERVER_1_IP:8001/health`
- [ ] Main API: `curl http://MAIN_API_IP/health`
- [ ] Extension: Open and test fact-checking

### Health Check Summary
```bash
# Check all services at once
curl http://MAIN_API_IP/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "models": {
    "ml_server_1": "connected",
    "ml_server_2": "connected",
    "tfidf": "loaded"
  },
  "database": "connected"
}
```

---

## 📊 Final Cost Summary

| Component | Server | RAM | Cost |
|-----------|--------|-----|------|
| Main API | Oracle #1 | 12GB | $0 |
| ML Server 1 | Oracle #2 | 12GB | $0 |
| ML Server 2 | HuggingFace | 16GB | $0 |
| PostgreSQL | Render | 256MB | $0 |
| **TOTAL** | 4 servers | **40GB** | **$0** |

**Monthly**: $0
**Yearly**: $0
**Forever**: $0 🎉

---

## 🚨 Troubleshooting

### If ML Server 1 fails to start:
```bash
ssh ubuntu@ML_SERVER_1_IP
sudo journalctl -u ml-server-1 -n 50
```

Common issues:
- Out of memory → Reduce batch size in code
- Model download failed → Check internet connection
- Port in use → Check with `sudo lsof -i :8001`

### If Main API can't connect to ML servers:
```bash
# Test ML Server 1
curl http://ML_SERVER_1_IP:8001/health

# Test ML Server 2
curl https://YOUR_USERNAME-ml-server-2.hf.space/api/health
```

Check:
- Firewall rules (port 8001 open?)
- API key matches in all .env files
- Services are running

### If Extension shows errors:
- Check browser console (F12)
- Verify API URL in config.js
- Test API directly: `curl http://MAIN_API_IP/health`

---

## 🎯 Next Steps

- [ ] Get a domain name (Namecheap via GitHub Student Pack)
- [ ] Setup SSL with Let's Encrypt (free)
- [ ] Add monitoring with UptimeRobot (free)
- [ ] Configure automated backups (Render does this automatically)
- [ ] Add analytics (Google Analytics - free)

---

## 📚 Resources

- **Full Guide**: `DEPLOYMENT_100_PERCENT_FREE.md`
- **Oracle Cloud**: https://oracle.com/cloud/free
- **Render**: https://render.com
- **HuggingFace**: https://huggingface.co/spaces

---

**Congratulations! You're running a production-grade ML system for FREE!** 🚀

Total setup time: ~1.5 hours
Total cost: $0/month
Total RAM: 40GB
Total awesomeness: 100% 🎉

