"""
FactCheckAI ML Server — Gradio Interface
Wraps the FastAPI app for HuggingFace Spaces (Gradio SDK)
"""
import gradio as gr
import json
import uvicorn
import threading
import time

# Import FastAPI app
from app import app as fastapi_app

# Start FastAPI server in background thread
def start_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=7860, log_level="info")

threading.Thread(target=start_fastapi, daemon=True).start()
time.sleep(2)  # Wait for FastAPI to start

# Gradio prediction function
def predict(text, api_key=""):
    import requests
    try:
        response = requests.post(
            "http://localhost:7860/predict",
            json={"text": text, "use_cache": True},
            headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
            timeout=30
        )
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# Health check function
def health_check():
    import requests
    try:
        response = requests.get("http://localhost:7860/health", timeout=5)
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# Build Gradio interface
with gr.Blocks(title="FactCheckAI ML Server") as demo:
    gr.Markdown("""
    # 🤖 FactCheckAI ML Ensemble Server
    
    Fine-tuned RoBERTa models for fake news detection.
    
    - **Model A**: 96.3% accuracy (daniB2112 dataset)
    - **Model B**: 79.8% accuracy (mixed datasets)
    - **Ensemble**: Weighted average (0.6/0.4)
    
    ### Endpoints:
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
            fn=health_check,
            outputs=health_output
        )

# Launch
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
