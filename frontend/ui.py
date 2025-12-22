import os
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Backend API URL
API_URL = os.getenv(
    "API_URL",
    "http://localhost:8080/generate"  # default for local dev
)

st.set_page_config(
    page_title="AI Image Generator",
    layout="centered"
)

st.title("AI Image Generator")

# Inputs
prompt = st.text_input(
    "Prompt",
    placeholder="A cinematic portrait of a cyberpunk samurai, 35mm, ultra-detailed"
)

negative_prompt = st.text_input(
    "Negative Prompt (optional)",
    placeholder="blurry, low quality, watermark"
)

generate = st.button("Generate Image")

if generate:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            try:
                res = requests.post(
                    API_URL,
                    json={
                        "prompt": prompt,
                        "negative_prompt": negative_prompt or None
                    },
                    timeout=1800
                )

                if res.status_code != 200:
                    st.error(f"Backend error ({res.status_code}): {res.text}")
                else:
                    image = Image.open(BytesIO(res.content))
                    st.image(image, use_container_width=True)

            except requests.exceptions.Timeout:
                st.error("⏱Request timed out. The model may be busy.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach backend. Is FastAPI running?")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
