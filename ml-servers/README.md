# ML Servers - Hybrid Deployment

Separate ML inference servers that can be deployed independently for free.

## 📁 Structure

```
ml-servers/
├── oracle-deberta/          # ML Server 1 - DeBERTa on Oracle Cloud
│   ├── main.py             # FastAPI server
│   ├── requirements.txt    # Dependencies
│   └── .env.example       # Config template
│
├── huggingface-ensemble/   # ML Server 2 - Ensemble on HuggingFace
│   ├── app.py             # Gradio server (auto-deploys)
│   └── requirements.txt   # Dependencies
│
└── README.md              # This file
```

## 🚀 Quick Deploy

### ML Server 1 (Oracle Cloud - DeBERTa)

```bash
# 1. SSH into Oracle Cloud instance
ssh ubuntu@your-oracle-ip

# 2. Clone and setup
git clone https://github.com/YOUR_USERNAME/FactCheckAI.git
cd FactCheckAI/ml-servers/oracle-deberta

# 3. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env
nano .env  # Add your ML_API_KEY

# 6. Run server
uvicorn main:app --host 0.0.0.0 --port 8001
```

### ML Server 2 (HuggingFace Spaces)

```bash
# 1. Create new Space on huggingface.co
#    - Name: ml-server-2
#    - SDK: Gradio
#    - Hardware: CPU (free)

# 2. Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/ml-server-2
cd ml-server-2

# 3. Copy files
cp /path/to/FactCheckAI/ml-servers/huggingface-ensemble/* .

# 4. Add ML_API_KEY to Space settings
#    Settings → Variables → Add secret
#    Name: ML_API_KEY
#    Value: your_key_here

# 5. Push to deploy
git add .
git commit -m "Deploy ML server"
git push
```

## 🔧 Configuration

### Generate API Key

```bash
# Generate secure random key
openssl rand -hex 32
```

Use this key in:
1. ML Server 1 `.env` file
2. ML Server 2 HuggingFace secrets
3. Main API `ML_API_KEY` environment variable

### Test Servers

```bash
# Test ML Server 1
curl -X POST http://your-oracle-ip:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth is flat", "api_key": "your_key"}'

# Test ML Server 2
curl -X POST https://your-username-ml-server-2.hf.space/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["The Earth is flat", "your_key"]}'
```

## 📊 Models Used

### ML Server 1 (DeBERTa)
- **Model**: `Bharat2004/deberta-fakenews-detector`
- **Size**: 738 MB
- **Accuracy**: 96.63%
- **RAM needed**: 2GB minimum
- **Best for**: High accuracy predictions

### ML Server 2 (Ensemble)
- **Model 1**: `Bharat2004/out` (DistilBERT)
- **Model 2**: `Bharat2004/deberta-factchecker`
- **Total Size**: ~1GB
- **RAM needed**: 3GB minimum
- **Best for**: Balanced speed + accuracy

## 🔒 Security

1. **API Key Authentication**: All requests require valid API key
2. **Firewall**: Restrict Oracle Cloud to only accept Railway IP
3. **HTTPS**: HuggingFace auto-provides HTTPS
4. **Rate Limiting**: Add to main API (Railway)

## 📈 Performance

### Expected Latency

| Server | Model | Inference Time |
|--------|-------|---------------|
| ML Server 1 | DeBERTa | ~300ms |
| ML Server 2 | Ensemble | ~500ms |
| Fallback | TF-IDF | ~50ms |

### Load Handling

- **Oracle Cloud**: Can handle ~100 requests/second
- **HuggingFace**: Can handle ~50 requests/second
- **Main API caches results**: Instant for repeated claims

## 🛠️ Systemd Service (Oracle Cloud)

Create `/etc/systemd/system/ml-server.service`:

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

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ml-server
sudo systemctl start ml-server
sudo systemctl status ml-server
```

## 🔍 Monitoring

### Health Checks

```bash
# Check ML Server 1
curl http://oracle-ip:8001/health

# Check ML Server 2
curl https://your-space.hf.space/api/health
```

### Logs

```bash
# Oracle Cloud logs
sudo journalctl -u ml-server -f

# HuggingFace logs
# View in Space → Logs tab
```

## 💡 Tips

1. **Model Updates**: Just restart the server after model changes
2. **Multiple Instances**: Deploy to multiple Oracle instances for redundancy
3. **Caching**: Main API caches results for 24 hours
4. **Fallback**: Main API falls back to TF-IDF if ML servers are down

## 📚 Resources

- [Oracle Cloud Always Free](https://oracle.com/cloud/free)
- [HuggingFace Spaces](https://huggingface.co/spaces)
- [Your Fine-Tuned Models](https://huggingface.co/Bharat2004)

---

**Cost**: $0/month for both ML servers! 🎉
