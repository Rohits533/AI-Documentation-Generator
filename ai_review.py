import requests
import json

def explain_code(code, api_key):
    """Sends code to Groq and returns an AI explanation."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 1. Use a clean, single‑line prompt (no triple backticks)
    prompt = (
        "You are a senior developer. Explain the following Python code in simple, clear language. "
        "Focus on what the code does, not how it works.\n\n"
        f"{code}"
    )

    # 2. Use a valid model from Groq’s list
    payload = {
        "model": "llama-3.1-8b-instant",  # <-- THIS IS THE FIX
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"
