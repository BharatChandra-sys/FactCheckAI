"""
FactCheckAI ML Server — Gradio Interface
"""
import os
import json
import time
import hashlib
import gradio as gr
import spaces
import torch

ML_API_KEY   = os.getenv("ML_API_KEY", "").strip() or None  # None if empty/whitespace
print(f"DEBUG: ML_API_KEY configured: {ML_API_KEY is not None}, value_length: {len(ML_API_KEY) if ML_API_KEY else 0}")
MODEL_A_REPO = os.getenv("MODEL_A_REPO", "Bharat2004/factcheckai-model-a")
MODEL_B_REPO = os.getenv("MODEL_B_REPO", "Bharat2004/factcheckai-model-b")
MODEL_C_REPO = os.getenv("MODEL_C_REPO", "Bharat2004/deberta-fakenews-detector")
HF_TOKEN     = os.getenv("HF_TOKEN", "")
WEIGHT_A     = float(os.getenv("WEIGHT_A", "0.6"))
WEIGHT_B     = float(os.getenv("WEIGHT_B", "0.4"))
WEIGHT_C     = float(os.getenv("WEIGHT_C", "0.0"))
DEVICE       = "cpu"

_models: dict = {}
_load_errors: dict = {}
_startup_time = time.time()
_pred_cache: dict = {}
_CACHE_MAX = 2000


def _cache_key(text: str) -> str:
    return hashlib.sha256(text[:500].lower().strip().encode()).hexdigest()[:16]


def _load_model(name: str, repo: str):
    if not repo:
        return
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        tok = AutoTokenizer.from_pretrained(repo, token=HF_TOKEN or None)
        mdl = AutoModelForSequenceClassification.from_pretrained(repo, token=HF_TOKEN or None)
        mdl.eval()
        _models[name] = (mdl, tok)
        print(f"model_{name} loaded")
    except Exception as e:
        _load_errors[name] = str(e)
        print(f"model_{name} load FAILED: {e}")


_load_model("A", MODEL_A_REPO)
_load_model("B", MODEL_B_REPO)
if MODEL_C_REPO:
    _load_model("C", MODEL_C_REPO)
print(f"Startup complete. Loaded models: {list(_models.keys())}")


def _infer_single(model, tokenizer, text: str) -> float:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True).to(DEVICE)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]
    return float(probs[1])


@spaces.GPU
def predict(text, api_key=""):
    if not _models:
        return {"error": "No models loaded"}
    # Only check API key if ML_API_KEY is configured (not None)
    if ML_API_KEY is not None and api_key != ML_API_KEY:
        return {"error": "Invalid API key"}
    text = text.strip()[:2000]
    if not text:
        return {"error": "text cannot be empty"}
    ck = _cache_key(text)
    if ck in _pred_cache:
        cached = dict(_pred_cache[ck])
        cached["cached"] = True
        return cached

    t0 = time.perf_counter()
    scores = {}
    for name in ["A", "B", "C"]:
        if name in _models:
            try:
                scores[name] = _infer_single(*_models[name], text)
            except Exception as e:
                print(f"model_{name} inference error: {e}")

    sa, sb, sc = scores.get("A"), scores.get("B"), scores.get("C")
    if sa is not None and sb is not None and sc is not None:
        fake_prob = WEIGHT_A * sa + WEIGHT_B * sb + WEIGHT_C * sc
        sources = ["model_A", "model_B", "model_C"]
        weights = {"model_A": WEIGHT_A, "model_B": WEIGHT_B, "model_C": WEIGHT_C}
    elif sa is not None and sb is not None:
        fake_prob = WEIGHT_A * sa + WEIGHT_B * sb
        sources = ["model_A", "model_B"]
        weights = {"model_A": WEIGHT_A, "model_B": WEIGHT_B}
    elif sa is not None:
        fake_prob = sa
        sources = ["model_A"]
        weights = {"model_A": 1.0}
    elif sb is not None:
        fake_prob = sb
        sources = ["model_B"]
        weights = {"model_B": 1.0}
    elif sc is not None:
        fake_prob = sc
        sources = ["model_C"]
        weights = {"model_C": 1.0}
    else:
        return {"error": "All models failed inference"}

    confidence = abs(fake_prob - 0.5) * 2
    verdict = "fake" if fake_prob >= 0.5 else "real"
    ms = int((time.perf_counter() - t0) * 1000)

    result = {
        "fake_probability": round(fake_prob, 4),
        "confidence": round(confidence, 4),
        "verdict": verdict,
        "model_a_score": round(sa, 4) if sa is not None else None,
        "model_b_score": round(sb, 4) if sb is not None else None,
        "model_c_score": round(sc, 4) if sc is not None else None,
        "ensemble_weights": weights,
        "model_sources": sources,
        "cached": False,
        "inference_ms": ms,
    }
    if len(_pred_cache) >= _CACHE_MAX:
        oldest = next(iter(_pred_cache))
        del _pred_cache[oldest]
    _pred_cache[_cache_key(text)] = result
    return result


def health():
    return {
        "status": "healthy" if _models else "degraded",
        "loaded_models": list(_models.keys()),
        "load_errors": _load_errors,
        "device": DEVICE,
        "uptime_s": int(time.time() - _startup_time),
        "cache_size": len(_pred_cache),
    }


# ─── Gradio Interface ─────────────────────────────────────────────────────


with gr.Blocks(title="FactCheckAI ML Server") as demo:
    gr.Markdown("""
    # FactCheckAI ML Ensemble Server
    
    Fine-tuned RoBERTa models for fake news detection.
    
    - **Model A**: 96.3% accuracy (daniB2112 dataset)
    - **Model B**: 79.8% accuracy (mixed datasets)
    - **Model C**: DeBERTa fallback
    - **Ensemble**: Weighted average (0.6/0.4)
    
    ### API Endpoints:
    - `GET /health` - Server status
    - `POST /predict` - Classify claim
    """)
    
    with gr.Tab("Predict"):
        text_input = gr.Textbox(
            label="Enter claim to verify",
            placeholder="Type or paste a claim here...",
            lines=3
        )
        api_key_input = gr.Textbox(
            label="API Key (optional)",
            type="password",
            placeholder="Leave empty if no auth configured"
        )
        predict_btn = gr.Button("Classify", variant="primary")
        output = gr.JSON(label="Result")
        
        predict_btn.click(
            fn=predict,
            inputs=[text_input, api_key_input],
            outputs=output
        )
        
        gr.Examples(
            examples=[
                ["COVID-19 vaccines contain microchips to track people"],
                ["The Earth's climate is changing due to human activity"],
                ["5G towers spread coronavirus through radio waves"]
            ],
            inputs=text_input
        )
    
    with gr.Tab("Health Check"):
        health_btn = gr.Button("Check Server Health")
        health_output = gr.JSON(label="Server Status")
        
        health_btn.click(
            fn=health,
            outputs=health_output
        )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )