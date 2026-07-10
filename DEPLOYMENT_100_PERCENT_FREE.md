# 100% FREE Deployment - Complete Guide

Deploy FactCheckAI with **$0/month cost** using only free tiers!

## 🎯 Final Architecture (100% FREE!)

```
┌─────────────────────────────────────────────────────────┐
│  Main API Server (Oracle Cloud FREE - 12GB RAM)        │
│  - FastAPI backend                                      │
│  - TF-IDF model (50MB)                                  │
│  - Auth, rate limiting, caching                         │
│  Cost: $0 FOREVER                                       │
└────────────┬────────────────────────────────────────────┘
             │
             ├─────────────────────┬─────────────────────┐
             ▼                     ▼                     ▼
┌──────────────────────┐  ┌─────────────────┐  ┌────────────────────┐
│ PostgreSQL           │  │ ML Server 1     │  │ ML Server 2        │
│ (Render FREE)        │  │ (Oracle #2 FREE)│  │ (HuggingFace FREE) │
│ - 256MB RAM          │  │ - 12GB RAM      │  │ - 16GB RAM         │
│ - 1GB storage        │  │ - DeBERTa       │  │ - Ensemble         │
│ Cost: $0             │  │ Cost: $0        │  │ Cost: $0           │
└──────────────────────┘  └─────────────────┘  └────────────────────┘
```

**Total: $0/month for 40GB RAM + PostgreSQL!** 🎉

---

## 📋 Prerequisites

1. **GitHub Account** (for code hosting)
2. **Oracle Cloud Account** (24GB free tier)
3. **Render Account** (free PostgreSQL)
4. **HuggingFace Account** (16GB free tier)
5. **Student email** (optional, for extra credits)

---

## 🚀 Step-by-Step Deployment

### Phase 1: Setup Render PostgreSQL (5 minutes)

#### Step 1.1: Create Render Account

1. Go to https://render.com
2. Click **Get Started for Free**
3. Sign up with GitHub
4. Verify your email

#### Step 1.2: Create PostgreSQL Database

1. Click **New** → **PostgreSQL**
2. Configure:
   - **Name**: `factcheck-db`
   - **Database**: `factcheck`
   - **User**: `factcheck_user` (auto-generated)
   - **Region**: `Oregon (US West)` (or nearest to you)
   - **PostgreSQL Version**: `16`
   - **Plan**: **Free** (256 MB RAM, 1 GB storage)
3. Click **Create Database**
4. **Wait 2-3 minutes** for database to provision

#### Step 1.3: Get Database Connection String

1. Once database is ready, click on it
2. Scroll to **Connections**
3. Copy **Internal Database URL** (looks like this):
   ```
   postgresql://factcheck_user:LONG_PASSWORD@dpg-xxx-xxx.oregon-postgres.render.com/factcheck
   ```
4. **Save this URL** - you'll need it later

**✅ PostgreSQL is ready!** Cost: $0/month

---

### Phase 2: Deploy ML Server 2 on HuggingFace (10 minutes)

#### Step 2.1: Create HuggingFace Account

1. Go to https://huggingface.co
2. Sign up with email
3. Verify your account

#### Step 2.2: Create New Space

1. Click your profile → **New Space**
2. Configure:
   - **Space name**: `ml-server-2`
   - **License**: `MIT`
   - **SDK**: `Gradio`
   - **Hardware**: `CPU basic` (FREE - 16GB RAM)
   - **Visibility**: `Public` (required for free tier)
3. Click **Create Space**

#### Step 2.3: Clone and Setup

```bash
# On your local machine
cd ~/Desktop  # or wherever you work

# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/ml-server-2
cd ml-server-2

# Copy ML server files
cp /path/to/FactCheckAI/ml-servers/huggingface-ensemble/* .

# Should have:
# - app.py
# - requirements.txt
```

#### Step 2.4: Add API Key Secret

1. In HuggingFace, go to your Space
2. Click **Settings** tab
3. Scroll to **Repository secrets**
4. Click **New secret**
5. Add:
   - **Name**: `ML_API_KEY`
   - **Value**: Generate with: `openssl rand -hex 32`
   - Click **Save**

**Copy this key** - you'll need it for other servers!

#### Step 2.5: Deploy

```bash
# In ml-server-2 folder
git add .
git commit -m "Deploy ML ensemble server"
git push
```

Wait 3-5 minutes. HuggingFace will:
- Install dependencies
- Load models
- Start Gradio server

#### Step 2.6: Test ML Server 2

1. Your space URL: `https://YOUR_USERNAME-ml-server-2.hf.space`
2. Test in browser - you should see Gradio interface
3. Test API:
```bash
curl -X POST https://YOUR_USERNAME-ml-server-2.hf.space/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["The Earth is flat", "YOUR_ML_API_KEY"]}'
```

**✅ ML Server 2 is live!** Cost: $0/month

---

### Phase 3: Deploy ML Server 1 on Oracle Cloud (30 minutes)

#### Step 3.1: Create Oracle Cloud Account

1. Go to https://oracle.com/cloud/free
2. Click **Start for free**
3. Fill in details:
   - Email
   - Country
   - Cloud Account Name (unique)
4. Add **credit/debit card** (won't be charged!)
5. Verify phone number
6. Complete sign-up

**Important**: Even after 30-day trial ends, Always Free resources stay FREE!

#### Step 3.2: Create First Compute Instance (ML Server 1)

1. Click **Create a VM instance**
2. Configure:
   - **Name**: `ml-server-1`
   - **Placement**: Leave defaults
   - **Image**: `Canonical Ubuntu 22.04`
   - **Shape**: Click **Change Shape**
     - Series: `Ampere`
     - Shape name: `VM.Standard.A1.Flex`
     - OCPU: `2`
     - Memory: `12 GB`
   - **Networking**: Leave defaults (creates VCN automatically)
   - **Add SSH keys**: 
     - Generate key pair (download both public and private)
     - OR paste your existing public key
3. Click **Create**

Wait 2-3 minutes for instance to start.

#### Step 3.3: Configure Firewall

1. In instance page, click **Subnet** link
2. Click your subnet name
3. Click **Default Security List**
4. Click **Add Ingress Rules**
5. Add rule for port 8001:
   - **Source CIDR**: `0.0.0.0/0`
   - **Destination Port**: `8001`
   - **Description**: `ML Server 1`
6. Click **Add Ingress Rules**

#### Step 3.4: SSH and Setup ML Server 1

```bash
# SSH into instance (use your private key)
ssh -i ~/Downloads/your-key.key ubuntu@instance-public-ip

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

# Install dependencies (this takes 5-10 minutes)
pip install -r requirements.txt

# Create .env file
nano .env
```

In nano, add:
```bash
ML_API_KEY=YOUR_ML_API_KEY_FROM_STEP_2.4
DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector
```

Save (Ctrl+X, Y, Enter)

```bash
# Test run
uvicorn main:app --host 0.0.0.0 --port 8001
```

Open new terminal and test:
```bash
curl http://instance-public-ip:8001/health
```

Should return: `{"status":"ok","model":"Bharat2004/deberta-fakenews-detector"}`

Press Ctrl+C to stop.

#### Step 3.5: Setup Systemd Service (ML Server 1)

```bash
# Create service file
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

Should show "active (running)"

**✅ ML Server 1 is live!** Cost: $0/month forever

---

### Phase 4: Deploy Main API on Oracle Cloud (30 minutes)

#### Step 4.1: Create Second Compute Instance (Main API)

Repeat Step 3.2 but with:
- **Name**: `main-api`
- **Memory**: `12 GB` (we have 24GB total free)

#### Step 4.2: Configure Firewall for Main API

Repeat Step 3.3 but add rules for:
- **Port 80**: HTTP
- **Port 443**: HTTPS

#### Step 4.3: SSH and Setup Main API

```bash
ssh -i ~/Downloads/your-key.key ubuntu@main-api-public-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx certbot python3-certbot-nginx

# Clone repository
git clone https://github.com/YOUR_USERNAME/FactCheckAI.git
cd FactCheckAI/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies (5-10 minutes)
pip install -r requirements.txt

# Create .env file
nano .env
```

Paste (replace with your actual values):
```bash
# Database (from Phase 1)
DATABASE_URL=postgresql://factcheck_user:PASSWORD@dpg-xxx.oregon-postgres.render.com/factcheck

# ML Servers
ML_SERVER_1_URL=http://ml-server-1-ip:8001
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
FORCE_TRANSFORMER_LOAD=false

# Razorpay (optional)
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
```

Save (Ctrl+X, Y, Enter)

#### Step 4.4: Setup Systemd Service (Main API)

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

Save and enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable factcheck-api
sudo systemctl start factcheck-api
sudo systemctl status factcheck-api
```

#### Step 4.5: Setup Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/factcheck
```

Paste:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Or use instance IP

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

Save and enable:
```bash
sudo ln -s /etc/nginx/sites-available/factcheck /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 4.6: Setup SSL (Optional but Recommended)

**Option 1: With Domain**
```bash
# Point your domain to instance IP first
sudo certbot --nginx -d your-domain.com
```

**Option 2: Self-signed (for testing)**
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt
```

#### Step 4.7: Test Main API

```bash
# Test locally
curl http://localhost:8000/health

# Test externally
curl http://main-api-public-ip/health
```

Should return full health check with model info!

**✅ Main API is live!** Cost: $0/month forever

---

### Phase 5: Update Extension (5 minutes)

#### Step 5.1: Update Extension Config

```bash
# On your local machine
cd /path/to/FactCheckAI/extension/popup

# Edit config.js
nano config.js
```

Change:
```javascript
const API = "http://main-api-public-ip";  
// Or with domain: const API = "https://your-domain.com";
```

Save.

#### Step 5.2: Reload Extension in Chrome

1. Go to `chrome://extensions`
2. Find "FactCheckAI"
3. Click refresh icon 🔄
4. Open extension popup

#### Step 5.3: Test End-to-End

1. Sign up / Login
2. Enter a claim: "The Earth is flat"
3. Click "Fact Check"
4. Should get response with verdict!

**✅ Extension is working!**

---

## 📊 Final Architecture Summary

| Component | Server | RAM | Storage | Cost |
|-----------|--------|-----|---------|------|
| **Main API** | Oracle #1 | 12GB | 50GB | $0 |
| **ML Server 1** | Oracle #2 | 12GB | 50GB | $0 |
| **ML Server 2** | HuggingFace | 16GB | 10GB | $0 |
| **PostgreSQL** | Render | 256MB | 1GB | $0 |
| **TOTAL** | 4 servers | **40GB** | **111GB** | **$0** |

---

## 🔧 Maintenance & Monitoring

### Check All Services

```bash
# Main API
curl http://main-api-ip/health

# ML Server 1
curl http://ml-server-1-ip:8001/health

# ML Server 2
curl https://YOUR_USERNAME-ml-server-2.hf.space/api/health

# PostgreSQL
# Check in Render dashboard
```

### View Logs

```bash
# Main API logs
ssh ubuntu@main-api-ip
sudo journalctl -u factcheck-api -f

# ML Server 1 logs
ssh ubuntu@ml-server-1-ip
sudo journalctl -u ml-server-1 -f

# ML Server 2 logs
# View in HuggingFace Space → Logs tab
```

### Update Code

```bash
# SSH into each instance
cd FactCheckAI
git pull
# Restart services
sudo systemctl restart factcheck-api
sudo systemctl restart ml-server-1
```

---

## 🚨 Troubleshooting

### Main API won't start

```bash
# Check logs
sudo journalctl -u factcheck-api -n 50

# Common issues:
# - Database connection failed → check DATABASE_URL
# - Port already in use → check with: sudo lsof -i :8000
# - Missing .env file → create it!
```

### ML Server connection failed

```bash
# Test ML Server 1
curl -X POST http://ml-server-1-ip:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"test","api_key":"YOUR_KEY"}'

# Check firewall
sudo iptables -L -n
```

### Database connection issues

1. Check Render dashboard - database should be "Available"
2. Test connection:
```bash
psql "postgresql://user:pass@host/db"
```
3. Check firewall allows outbound connections

---

## 📈 Performance Optimization

### Enable Caching (Redis - Optional)

Use Render's free Redis:
```bash
# In Render dashboard
# New → Redis → Free tier
# Copy REDIS_URL
# Add to .env
```

### Add CDN (Cloudflare - Free)

1. Sign up at cloudflare.com
2. Add your domain
3. Change nameservers
4. Enable caching rules

### Scale Up (If Needed)

With Oracle Always Free, you can:
- Create **2 more instances** (12GB each)
- Load balance between them
- Still $0/month!

---

## 🎯 Next Steps

1. **Get a domain** (Namecheap via GitHub Student Pack)
2. **Setup monitoring** (UptimeRobot - free)
3. **Add analytics** (Google Analytics - free)
4. **Backup database** (automated in Render)
5. **Scale as needed** (add more Oracle instances)

---

## 💰 Total Cost Analysis

### Setup Costs
- Oracle Cloud: $0 (no credit card charged)
- Render: $0 (no credit card required)
- HuggingFace: $0 (no credit card required)
- **Total Setup: $0**

### Monthly Costs
- Oracle Cloud Always Free: $0
- Render Free Tier: $0
- HuggingFace Free Tier: $0
- **Total Monthly: $0**

### Annual Costs
- **Total Annual: $0**

**You're running a production ML system with 40GB RAM for FREE!** 🎉

---

## 📚 Resources

- [Oracle Cloud Always Free](https://oracle.com/cloud/free)
- [Render Free Tier](https://render.com/docs/free)
- [HuggingFace Spaces](https://huggingface.co/docs/hub/spaces)
- [GitHub Student Pack](https://education.github.com/pack)

---

**Need help?** Open an issue or email bc833498@gmail.com

**This is production-ready and scales to thousands of users!** 🚀
