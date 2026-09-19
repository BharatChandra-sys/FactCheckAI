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
- **Model C**: `Bharat2004/deberta-fakenews-detector` - DeBERTa fallback
- **Ensemble**: Weighted average (0.6/0.4)

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
- `ML_API_KEY` - Bearer token for authentication (optional)
- `HF_TOKEN` - HuggingFace token for private models
- `MODEL_A_REPO`, `MODEL_B_REPO`, `MODEL_C_REPO` - Model repos
- `WEIGHT_A`, `WEIGHT_B`, `WEIGHT_C` - Ensemble weights

## License
Apache 2.0