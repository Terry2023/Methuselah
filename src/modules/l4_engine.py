import requests
import json

# Native Ollama endpoint (More reliable on Windows than /v1/)
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

def call_engine(user_prompt, context_data):
    """L4: Fires direct to Ollama's native API."""
    sliders = context_data.get("sliders", {})
    context_text = context_data.get("text", "")
    
    # CRITICAL: This must match 'ollama list' exactly (e.g., 'qwen2.5:latest')
    MODEL_NAME = "qwen2.5:latest" 

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": f"Use these constraints: {context_text}"},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {
            "temperature": sliders.get('creativity', 0.3)
        }
    }
    
    try:
        # Diagnostic: Check the terminal running the GUI to see this:
        print(f"DEBUG: Pinging Ollama with model '{MODEL_NAME}'...")
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=90)
        
        if response.status_code == 404:
            return None, f"404: Ollama couldn't find model '{MODEL_NAME}'. Run 'ollama list' and verify."
        
        response.raise_for_status()
        return response.json()['message']['content'], None
        
    except Exception as e:
        return None, f"L4 Connection Failed: {str(e)}"