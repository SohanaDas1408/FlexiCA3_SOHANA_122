# Flagship Gradio Application Entrypoint for Render, Hugging Face Spaces & Cloud Deployment
import os
import sys

# Ensure unbuffered standard output so logs appear immediately in Render console
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"

from gradio_app import demo

if __name__ == "__main__":
    # Render assigns the PORT environment variable dynamically (e.g. 10000). Locally defaults to 7860.
    port_env = os.environ.get("PORT") or os.environ.get("GRADIO_SERVER_PORT")
    port = int(port_env) if port_env else 7860
    server_name = "0.0.0.0"
    
    print(f"🚀 Launching Planetary Climate Sentinel on {server_name}:{port} for cloud deployment...", flush=True)
    try:
        demo.launch(
            server_name=server_name,
            server_port=port,
            share=False,
            inbrowser=False
        )
    except OSError:
        demo.launch(server_name=server_name, share=False, inbrowser=False)
