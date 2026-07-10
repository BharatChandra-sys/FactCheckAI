# Deployment Guide with GitHub Student Developer Pack

This guide shows how to deploy FactCheckAI using free credits and services available through the [GitHub Student Developer Pack](https://education.github.com/pack).

## 🎓 GitHub Student Benefits for FactCheckAI

### Top Recommendations (With Transformers)

#### 🏆 **Oracle Cloud Always Free** (BEST - 24GB RAM!)
- **Best for**: Maximum performance, all transformer models
- **Free tier**: 24GB RAM, 4 cores, **FOREVER FREE**
- **Setup time**: 30 minutes

#### 🚂 **Railway** (EASIEST - 2GB RAM)
- **Best for**: Quick deployment, beginners
- **Free tier**: $5 credit/month = 2GB RAM instance
- **Setup time**: 5 minutes

#### ☁️ **Google Cloud** (STUDENT - $300 credit)
- **Best for**: 2GB RAM, professional infrastructure  
- **Free tier**: $300 credit for 12 months
- **Setup time**: 15 minutes

### Traditional Options

#### 1. **DigitalOcean** ($200 credit for 1 year)
- **Best for**: Full control, 2GB+ RAM
- **Free tier**: $200 credit (~16 months with 2GB droplet)
- **Setup time**: 30 minutes

#### 2. **Heroku** (Free with GitHub Student Pack)
- **Best for**: Quick deployment, PostgreSQL included
- **Free tier**: 1 free dyno (512MB - TF-IDF only)
- **Setup time**: 5 minutes

### 3. **MongoDB Atlas** (Free $50 credit)
- **Best for**: Document storage (if you want to switch from PostgreSQL)
- **Free tier**: Shared cluster + $50 credit
- **Setup time**: 5 minutes

### 4. **Azure** ($100 credit for students)
- **Best for**: Enterprise-grade hosting
- **Free tier**: $100 credit + 12 months free services
- **Setup time**: 15 minutes

## 📦 Recommended: Railway (Fastest & Easiest)

Railway offers the best balance of ease and performance for transformer models.

### Why Railway?
- ✅ **5 minute setup** (vs 30+ for others)
- ✅ **2GB RAM** with free $5/month credits
- ✅ **No sleep mode** (always responsive)
- ✅ **Auto-deploy** from GitHub
- ✅ **PostgreSQL included** for free
- ✅ **Can run DeBERTa** transformer models
- ✅ **$2/month** after using $5 credit

### Step 1: Create Railway Account

1. Go to https://railway.app/
2. Sign up with GitHub
3. Verify your account

### Step 2: Deploy from GitHub

1. **New Project** → **Deploy from GitHub repo**
2. Select your FactCheckAI repository
3. Railway automatically detects Python
4. Click **Deploy Now**

### Step 3: Add PostgreSQL

1. In your project, click **New** → **Database** → **PostgreSQL**
2. Railway provisions a database automatically
3. Connection string is auto-added to your app

### Step 4: Configure Environment Variables

Click on your service → **Variables** tab → Add these:

```bash
# Transformer model (use your fine-tuned model!)
DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector
FORCE_TRANSFORMER_LOAD=true
HF_TOKEN=your_huggingface_token

# AI API Keys
CEREBRAS_API_KEY=your_key
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
NEWS_API_KEY=your_key

# JWT Secret (generate: openssl rand -hex 32)
JWT_SECRET=your_secret_here

# Google OAuth
GOOGLE_CLIENT_ID=your_client_id

# Email
SMTP_USER=your_email@gmail.com
BREVO_API_KEY=your_brevo_key

# DATABASE_URL is automatically set by Railway!
```

### Step 5: Deploy!

Railway automatically:
- ✅ Installs dependencies from requirements.txt
- ✅ Runs database migrations
- ✅ Starts uvicorn server
- ✅ Provides HTTPS domain
- ✅ Monitors health

**Your API is live!** Get the URL from the Railway dashboard.

### Step 6: Update Extension

Update `extension/popup/config.js`:

```javascript
const API = "https://factcheck-api.up.railway.app";
```

### Cost Breakdown (Railway)

- **Month 1-12**: $2/month ($5 credit - $7 actual = $2 out of pocket)
- **After 12 months**: $7/month for 2GB instance

**Total first year: $24** (much cheaper than alternatives!)

---

## 📦 Alternative: Oracle Cloud (Most RAM!)

For maximum performance (24GB RAM!), use Oracle Cloud Always Free:

### Step 1: Create Oracle Cloud Account

1. Go to https://oracle.com/cloud/free
2. Sign up (requires credit card but won't charge)
3. Complete verification

### Step 2: Create Compute Instance

1. **Compute** → **Instances** → **Create Instance**
2. Name: `factcheck-api`
3. Image: **Ubuntu 22.04**
4. Shape: Click **Change Shape**
   - **VM.Standard.A1.Flex** (ARM processor)
   - OCPU: **2** 
   - Memory: **12 GB** (you get 24GB total!)
5. Add SSH key
6. Click **Create**

### Step 3: Configure Firewall

```bash
# SSH into instance
ssh ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Configure firewall
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

### Step 4: Install Dependencies

```bash
# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx

# Clone repository
git clone https://github.com/YOUR_USERNAME/FactCheckAI.git
cd FactCheckAI/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies (including transformers!)
pip install -r requirements.txt
```

### Step 5: Configure Environment

```bash
# Create .env file
nano .env
```

Add all your API keys (same as Railway above, but use SQLite):

```bash
DATABASE_URL=sqlite:///./factchecker.db
DEBERTA_MODEL=Bharat2004/deberta-fakenews-detector
FORCE_TRANSFORMER_LOAD=true
# ... all other keys
```

### Step 6: Setup Systemd Service

(Follow the systemd setup from the DigitalOcean section below)

---

## 📦 Original: DigitalOcean Deployment

DigitalOcean offers the best balance of performance and ease of use.

### Step 1: Claim Your GitHub Student Pack

1. Go to https://education.github.com/pack
2. Verify your student status (use your .edu email or student ID)
3. Once approved, claim the **DigitalOcean $200 credit**

### Step 2: Create a DigitalOcean Account

1. Sign up at https://www.digitalocean.com/
2. Apply your GitHub Student promo code
3. Verify $200 credit is added to your account

### Step 3: Create a Droplet

1. Click **Create** → **Droplets**
2. Choose these settings:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($6/month - 1GB RAM, 25GB SSD)
   - **Datacenter**: Choose nearest region
   - **Authentication**: SSH key (recommended) or Password
   - **Hostname**: `factcheck-api`

3. Click **Create Droplet**

### Step 4: Setup PostgreSQL Database

1. Click **Create** → **Databases**
2. Choose:
   - **Engine**: PostgreSQL 15
   - **Plan**: Basic ($15/month - 1GB RAM)
   - **Datacenter**: Same as droplet
   - **Database name**: `factcheck-db`

3. Click **Create Database**
4. Copy the **Connection String** (looks like `postgresql://user:pass@host:port/db`)

### Step 5: SSH into Droplet and Deploy

```bash
# SSH into your droplet
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y

# Install Python 3.11
apt install -y python3.11 python3.11-venv python3-pip git nginx

# Clone repository
git clone https://github.com/YOUR_USERNAME/FactCheckAI.git
cd FactCheckAI/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
```

Add these environment variables:

```bash
# Database (use DigitalOcean connection string)
DATABASE_URL=postgresql://user:pass@host:port/factcheck-db

# AI API Keys (get free tier keys)
CEREBRAS_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
NEWS_API_KEY=your_key_here

# JWT Secret (generate with: openssl rand -hex 32)
JWT_SECRET=your_secret_here

# Google OAuth (create at console.cloud.google.com)
GOOGLE_CLIENT_ID=your_client_id

# Email (use Brevo free tier)
SMTP_USER=your_email@gmail.com
BREVO_API_KEY=your_brevo_key

# Production settings
ENABLE_DOCS=false
RATE_LIMIT_ENABLED=true
```

Save and exit (Ctrl+X, Y, Enter)

### Step 6: Setup Systemd Service

```bash
# Create service file
nano /etc/systemd/system/factcheck.service
```

Add this content:

```ini
[Unit]
Description=FactCheckAI API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/FactCheckAI/backend
Environment="PATH=/root/FactCheckAI/backend/venv/bin"
ExecStart=/root/FactCheckAI/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and enable:

```bash
systemctl daemon-reload
systemctl enable factcheck
systemctl start factcheck
systemctl status factcheck
```

### Step 7: Setup Nginx Reverse Proxy

```bash
# Create Nginx config
nano /etc/nginx/sites-available/factcheck
```

Add this content:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Or use droplet IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:

```bash
ln -s /etc/nginx/sites-available/factcheck /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 8: Setup SSL with Let's Encrypt (Optional)

```bash
# Install certbot
apt install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### Step 9: Update Extension Config

Update `extension/popup/config.js`:

```javascript
const API = "https://your-domain.com";  // Or http://your-droplet-ip
```

### Step 10: Test Deployment

```bash
# Test health endpoint
curl http://your-droplet-ip/health

# Should return:
# {"status":"ok","version":"2.6.1",...}
```

## 💰 Cost Breakdown (with GitHub Student Pack)

| Service | Regular Cost | With Student Pack | Duration |
|---------|--------------|-------------------|----------|
| DigitalOcean Droplet | $6/month | **FREE** ($200 credit) | ~33 months |
| PostgreSQL Database | $15/month | **FREE** ($200 credit) | Included |
| Domain Name | $12/year | **FREE** (from Namecheap via pack) | 1 year |
| SSL Certificate | Free (Let's Encrypt) | **FREE** | Forever |

**Total: $0 for the first year!** 🎉

## 🚀 Alternative: Quick Deploy with Heroku

If you want even faster deployment (no server setup):

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
cd backend
heroku create factcheck-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set CEREBRAS_API_KEY=xxx
heroku config:set GROQ_API_KEY=xxx
heroku config:set GEMINI_API_KEY=xxx
# ... (add all other env vars)

# Deploy
git push heroku main

# Open app
heroku open
```

## 📊 Monitoring & Scaling

### DigitalOcean Monitoring

1. Enable monitoring in DigitalOcean dashboard
2. Set up alerts for:
   - CPU usage > 80%
   - Memory usage > 90%
   - Disk usage > 85%

### Log Management

```bash
# View logs
journalctl -u factcheck -f

# View Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Scaling Up

When you need more resources:

```bash
# Resize droplet (takes ~2 minutes)
# Go to Droplets → Your Droplet → Resize
# Choose larger plan

# Update workers in systemd service
nano /etc/systemd/system/factcheck.service
# Change: --workers 2 to --workers 4

systemctl daemon-reload
systemctl restart factcheck
```

## 🔒 Security Best Practices

1. **Firewall Setup**:
```bash
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw enable
```

2. **Disable Root Login** (after setting up SSH key):
```bash
nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
systemctl restart sshd
```

3. **Automatic Updates**:
```bash
apt install -y unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
```

4. **Backup Database**:
```bash
# DigitalOcean auto-backups (enable in dashboard)
# Manual backup:
pg_dump $DATABASE_URL > backup.sql
```

## 🎯 Credit Usage Tracking

Keep track of your remaining credits:

| Month | DigitalOcean Usage | Remaining Credit |
|-------|-------------------|------------------|
| Month 1 | $21 | $179 |
| Month 2 | $21 | $158 |
| ... | ... | ... |

Set a reminder to:
1. Monitor usage monthly
2. Apply for free tier hosting before credits run out
3. Consider Render.com free tier as backup

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check logs
journalctl -u factcheck -n 50

# Common issues:
# - Missing .env file
# - Database connection failed
# - Port already in use
```

### Extension can't connect
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check Nginx config
nginx -t

# Check firewall
ufw status
```

### Database connection errors
```bash
# Test database connection
psql $DATABASE_URL

# Check connection string format
# Should be: postgresql://user:pass@host:port/db
```

## 📚 Additional Resources

- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)
- [GitHub Student Pack](https://education.github.com/pack)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)
- [Nginx Configuration](https://nginx.org/en/docs/)

## 🎓 More Free Services for Students

Also available in GitHub Student Pack:
- **Namecheap**: Free domain for 1 year
- **Mailgun**: 20,000 free emails/month
- **Twilio**: $50 credit for SMS/calls
- **Stripe**: Waived transaction fees on first $1000
- **DataDog**: 2-year free Pro plan for monitoring

---

**Need help?** Open an issue on GitHub or email: bc833498@gmail.com
