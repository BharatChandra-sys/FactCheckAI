"""
ML Server 2 - Ensemble on HuggingFace Spaces
Runs multiple models and returns ensemble prediction
"""

import gradio as gr
from transformers import pipeline
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ML_API_KEY = os.getenv("ML_API_KEY", "change-me-in-production")

# Load multiple models
logger.info("Loading models...")
model1 = pipeline("text-classification", model="Bharat2004/out", device=-1)
model2 = pipeline("text-classification", model="Bharat2004/deberta-factchecker", device=-1)
logger.info("Models loaded")


def predict_ensemble(text: str, api_key: str):
    """Run ensemble prediction"""
    
    # Auth check
    if api_key != ML_API_KEY:
        return {"error": "Invalid API key"}
    
    # Run both models
    r1 = model1(text[:1500])[0]
    r2 = model2(text[:1500])[0]
    
    # Parse results
    def get_fake_prob(result):
        label = result["label"].upper()
        score = float(result["score"])
        if label in ("LABEL_1", "FAKE"):
            return score
        else:
            return 1.0 - score
    
    fake1 = get_fake_prob(r1)
    fake2 = get_fake_prob(r2)
    
    # Weighted ensemble (DistilBERT: 0.4, DeBERTa: 0.6)
    ensemble_score = (fake1 * 0.4) + (fake2 * 0.6)
    
    logger.info(f"Ensemble: {ensemble_score:.3f} (model1={fake1:.3f}, model2={fake2:.3f})")
    
    return {
        "fake_probability": round(ensemble_score, 3),
        "models": ["distilbert", "deberta"],
        "individual_scores": [
            {"model": "distilbert", "fake_prob": round(fake1, 3)},
            {"model": "deberta", "fake_prob": round(fake2, 3)}
        ],
        "server": "ml-server-2-huggingface"
    }


# Create Gradio interface (provides both UI and API)
demo = gr.Interface(
    fn=predict_ensemble,
    inputs=[
        gr.Textbox(label="Text to analyze", lines=5),
        gr.Textbox(label="API Key", type="password")
    ],
    outputs=gr.JSON(label="Prediction"),
    title="ML Server 2 - Ensemble",
    description="Runs DistilBERT + DeBERTa ensemble for fact-checking",
    examples=[
        ["The Earth is flat", ML_API_KEY],
        ["The sky is blue", ML_API_KEY]
    ]
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
