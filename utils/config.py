import os
import streamlit as st
from dotenv import load_dotenv

def load_config():
    # Try Streamlit secrets first (Cloud)
    try:
        if "AZURE_OPENAI_API_KEY" in st.secrets:
            return {
                "api_key": st.secrets["AZURE_OPENAI_API_KEY"],
                "endpoint": st.secrets["AZURE_OPENAI_ENDPOINT"],
                "deployment": st.secrets["AZURE_DEPLOYMENT_NAME"]
            }
    except:
        # Fallback to .env (Local)
        load_dotenv()

        return {
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "deployment": os.getenv("AZURE_DEPLOYMENT_NAME")
        }