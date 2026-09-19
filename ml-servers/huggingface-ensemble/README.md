---
title: FactCheckAI ML Server
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.11.0
app_file: app_gradio.py
pinned: false
---

# 🤖 FactCheckAI ML Ensemble Server

Fine-tuned RoBERTa models for fake news detection. This Space serves as the ML inference backend for the FactCheckAI Chrome extension.

## Models

- **Model A**: `Bharat2004/factcheckai-model-a` - 96.3% accuracy on held-out split
- **Model B**: `Bharat2004/factcheckai-model-b` - 79.8% accuracy on mixed datasets
- **Ensemble**: Weighted average (0.6 × Model A + 0.4 × Model B)

## API Endpoints

### `GET /health`
Returns server status and loaded models.

### `POST /predict`
Classifies a claim as real or fake.

**Request:**
```json
{
  "text": "Your claim here",
  "use_cache": true
}
```

**Response:**
```json
{
  "fake_probability": 0.8234,
  "confidence": 0.6468,
  "verdict": "fake",
  "model_a_score": 0.8521,
  "model_b_score": 0.7734,
  "ensemble_weights": {"model_A": 0.6, "model_B": 0.4},
  "model_sources": ["model_A", "model_B"],
  "cached": false,
  "inference_ms": 245
}
```

## Environment Variables

Set these in your Space Secrets:

- `ML_API_KEY` - Bearer token for authentication (optional)
- `MODEL_A_REPO` - HuggingFace model repo (default: `Bharat2004/factcheckai-model-a`)
- `MODEL_B_REPO` - HuggingFace model repo (default: `Bharat2004/factcheckai-model-b`)
- `HF_TOKEN` - HuggingFace token for private/gated models (optional)
- `WEIGHT_A` - Model A weight (default: 0.6)
- `WEIGHT_B` - Model B weight (default: 0.4)

## Local Development

```bash
pip install -r requirements.txt
python app_gradio.py
```

Open http://localhost:7860

## Integration

This Space is designed to be called by the FactCheckAI backend:

```python
import requests

response = requests.post(
    "https://YOUR-USERNAME-factcheckai-ml-server.hf.space/predict",
    json={"text": "Your claim here"},
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
print(response.json())
```

## License

Apache 2.0 - See [LICENSE](https://github.com/BharatChandra-sys/FactCheckAI/blob/main/LICENSE)

## Links

- [GitHub Repository](https://github.com/BharatChandra-sys/FactCheckAI)
- [Chrome Extension](https://chromewebstore.google.com/detail/factcheckai)
- [Backend API](https://factcheckai-backend.onrender.com)
