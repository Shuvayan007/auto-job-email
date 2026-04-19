import os
import streamlit as st
from dotenv import load_dotenv


def load_config():
    config = {}

    # --------- TRY STREAMLIT SECRETS (CLOUD) ---------
    try:
        if "AZURE_OPENAI_API_KEY" in st.secrets:
            config["api_key"] = st.secrets.get("AZURE_OPENAI_API_KEY")
            config["endpoint"] = st.secrets.get("AZURE_OPENAI_ENDPOINT")
            config["deployment"] = st.secrets.get("AZURE_DEPLOYMENT_NAME")

            # Gmail
            config["gmail_email"] = st.secrets.get("GMAIL_EMAIL")
            config["gmail_app_password"] = st.secrets.get("GMAIL_APP_PASSWORD")

            return config
    except Exception:
        pass  # fall back to .env

    # --------- FALLBACK TO .env (LOCAL) ---------
    load_dotenv()

    config["api_key"] = os.getenv("AZURE_OPENAI_API_KEY")
    config["endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT")
    config["deployment"] = os.getenv("AZURE_DEPLOYMENT_NAME")

    # Gmail
    config["gmail_email"] = os.getenv("GMAIL_EMAIL")
    config["gmail_app_password"] = os.getenv("GMAIL_APP_PASSWORD")

    return config