# Flagship Gradio Application Entrypoint for Render, Hugging Face Spaces & Cloud Deployment
import os
import sys

# Ensure unbuffered standard output so logs appear immediately in Render console
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"

from gradio_app import demo

if __name__ == "__main__":
    # Render assigns the PORT environment variable dynamically (defaults to 10000 on Render)
    port = int(os.environ.get("PORT", os.environ.get("GRADIO_SERVER_PORT", 10000)))
    server_name = "0.0.0.0"
    
    print(f"🚀 Launching Planetary Climate Sentinel on {server_name}:{port} for Render cloud deployment...", flush=True)
    demo.launch(
        server_name=server_name,
        server_port=port,
        share=False,
        inbrowser=False
    )
