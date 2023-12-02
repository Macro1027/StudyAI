import streamlit as st
import requests

model = "pplx-70b-online"
url = "https://api.perplexity.ai/chat/completions"
PPX_API_KEY = st.secrets["PPX_API_KEY"]

def get_content(content):
    payload = {
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": content
        }
    ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {PPX_API_KEY}"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

