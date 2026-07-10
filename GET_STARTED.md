# Get Started with FactCheckAI 🚀

**One-page guide to get FactCheckAI running.**

---

## 🎯 What Do You Want?

### Option 1: Test Locally (10 minutes) 💻
**Perfect for**: Trying it out, development

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/FactCheckAI.git
cd FactCheckAI

# 2. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env - add your API keys (Groq, Gemini, etc.)
uvicorn app.main:app --reload

# 3. Load extension
# Open Chrome → chrome://extensions
# Enable "Developer mode"
# Click "Load unpacked" → Select FactCheckAI/extension folder

# 4. Test!
# Click extension icon → Enter claim → Fact Check!
```

**You get**: Basic fact-checking with TF-IDF model (~90% accuracy)

---

### Option 2: Deploy for Free (1.5 hours) ☁️
**Perfect for**: Production use, sharing with others

#### Requirements
- GitHub account
- Oracle Cloud account (24GB free)
- Render account (free PostgreSQL)
- HuggingFace account (16GB free)

#### Steps
1. **Setup PostgreSQL** (5 min)
   - Go to render.com → New → PostgreSQL (Free plan)
   - Copy database URL

2. **Deploy ML Server 2** (10 min)
   - Create HuggingFace Space
   - Copy ml-servers/huggingface-ensemble files
   - Generate API key: `openssl rand -hex 32`
   - Push to HuggingFace

3. **Deploy ML Server 1** (30 min)
   - Create Oracle Cloud VM (12GB)
   - Clone repo, install dependencies
   - Setup systemd service

4. **Deploy Main API** (30 min)
   - Create another Oracle VM (12GB)
   - Clone repo, install dependencies
   - Setup nginx, systemd service

5. **Update Extension** (5 min)
   - Edit extension/popup/config.js
   - Change API URL to your Main API
   - Reload extension

**You get**: Full production system with 98.5% accuracy, $0/month cost

**Full Guide**: [DEPLOYMENT_100_PERCENT_FREE.md](DEPLOYMENT_100_PERCENT_FREE.md)  
**Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

### Option 3: Quick Deploy with Railway (5 minutes) 🚂
**Perfect for**: Quick test, don't mind small cost

```bash
# 1. Fork repository on GitHub

# 2. Go to railway.app
# - Sign up with GitHub
# - New Project → Deploy from GitHub
# - Select your fork

# 3. Add PostgreSQL
# - New → PostgreSQL

# 4. Set environment variables
# Add your API keys (Groq, Gemini, etc.)

# 5. Deploy!
# Railway auto-builds and deploys

# 6. Update extension
# Edit extension/popup/config.js
# Change API URL to Railway URL
# Reload extension
```

**You get**: Production deployment, $2/month after free credits

**Guide**: [DEPLOYMENT_GITHUB_STUDENT.md](DEPLOYMENT_GITHUB_STUDENT.md)

---

## 📚 Need More Help?

### Documentation
- 📖 [Main README](README.md) - Full project overview
- 🚀 [Quick Start](QUICKSTART_FREE.md) - Detailed free deployment
- 📋 [Deployment Checklist](DEPLOYMENT_CHECKLIST.md) - Step-by-step
- 🏗️ [Architecture](ARCHITECTURE_DIAGRAM.md) - How it works
- 🎯 [Deployment Summary](DEPLOYMENT_SUMMARY.md) - Compare all options

### Key API Keys You'll Need

**Required** (for AI analysis):
- **Groq API Key**: Get from groq.com (free tier available)
- **Google Gemini Key**: Get from ai.google.dev (free tier)

**Optional** (improves accuracy):
- Cerebras API Key: cerebras.ai
- News API Key: newsapi.org (100 req/day free)
- Tavily API Key: tavily.com (1000 req/month free)
- SerpAPI Key: serpapi.com (100 searches/month free)
- Google Fact Check API: console.cloud.google.com

### Quick Troubleshooting

**Backend won't start:**
```bash
# Check Python version
python --version  # Need 3.11+

# Install dependencies
pip install -r requirements.txt

# Check .env file exists
ls .env  # Should exist in backend/
```

**Extension errors:**
```bash
# Check API URL in extension/popup/config.js
# Should match your backend URL
# Local: http://localhost:8000
# Railway: https://your-app.railway.app
# Oracle: http://your-ip
```

**ML server connection failed:**
```bash
# Check ML_API_KEY matches in:
# - backend/.env
# - ml-servers/oracle-deberta/.env
# - HuggingFace Space secrets
```

---

## 🎯 Next Steps After Setup

1. ✅ **Test Basic Fact-Checking**
   - Try: "The Earth is flat"
   - Try: "Water boils at 100°C"
   - Try: "Hitler is still alive"

2. ✅ **Create Account**
   - Sign up in extension
   - Get 30 free requests/day
   - History saved automatically

3. ✅ **Explore Features**
   - Chat with AI about claims
   - View source evidence
   - Check confidence scores
   - Review flagged claims

4. 🚀 **Deploy to Production** (if running locally)
   - Follow [free deployment guide](DEPLOYMENT_100_PERCENT_FREE.md)
   - Get custom domain (Namecheap via GitHub Student Pack)
   - Add SSL certificate (Let's Encrypt)

5. 📣 **Share with Others!**
   - Publish on Chrome Web Store
   - Share with friends
   - Get feedback

---

## 💡 Pro Tips

### For Best Accuracy
- Deploy full multi-server setup (all 3 ML models)
- Add all optional API keys
- Use production AI providers (not just free tiers)

### For Cost Optimization
- Use free multi-server setup (Oracle + Render + HuggingFace)
- Enable caching (Redis) to reduce API calls
- Set up rate limiting to prevent abuse

### For Development
- Use local setup with hot reload
- Test with SQLite (no PostgreSQL needed)
- Use TF-IDF model only (fast, good enough for testing)

---

## 🤝 Contributing

Want to improve FactCheckAI?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Areas that need help:**
- More language support
- Better UI/UX
- Additional ML models
- Performance optimizations
- Documentation improvements

---

## 📞 Support

**Need help?**
- 📧 Email: bc833498@gmail.com
- 💬 GitHub Issues: Create an issue
- 📖 Documentation: Read the guides
- 🔍 Search: Check existing issues

**Found a bug?**
- Create a GitHub issue with:
  - What you were doing
  - What happened (error message)
  - What you expected to happen
  - Screenshots if possible

---

## 🎉 Success!

You should now have:
- ✅ Backend running (locally or deployed)
- ✅ Extension loaded in Chrome
- ✅ Ability to fact-check claims
- ✅ User account with 30 free requests/day

**Now go fact-check the world!** 🌍✨

---

## 📊 Quick Facts

- **Accuracy**: 98.5% with full pipeline
- **Speed**: <500ms for most requests
- **Cost**: $0/month with free deployment
- **Capacity**: Handles thousands of users
- **Models**: DeBERTa (96.63%) + Ensemble (95.8%) + TF-IDF (90%)
- **AI Providers**: Groq, Gemini, Cerebras
- **Data Sources**: Tavily, SerpAPI, Google Fact Check

---

**Questions? Start with [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) to compare all options!**

