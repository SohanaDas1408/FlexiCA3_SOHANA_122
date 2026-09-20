# Flagship Gradio Application Entrypoint for Render, Hugging Face Spaces & Cloud Deployment
import os
from gradio_app import demo

if __name__ == "__main__":
    # Render and cloud platforms dynamically assign a PORT environment variable (default: 7860 or 10000)
    port = int(os.environ.get("PORT", os.environ.get("GRADIO_SERVER_PORT", 7860)))
    server_name = os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0")
    
    print(f"🚀 Launching Planetary Climate Sentinel on {server_name}:{port} for cloud deployment...")
    demo.launch(
        server_name=server_name,
        server_port=port,
        share=False,
        inbrowser=False
    )
