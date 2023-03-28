import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

st.title("Twitter Post Generator")

# TODO: import session state from home page and inject it into a prompt here