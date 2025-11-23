import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Quotex Bot 2.5", page_icon="⚡", layout="wide")

st.title("⚡ Quotex Signal Bot (Gemini 2.5)")
st.caption("Powered by Google Gemini 2.5 Flash | High-Speed Technical Analysis")

# --- SIDEBAR (Where you paste the key) ---
with st.sidebar:
    st.header("🔐 Authorization")
    
    # 1. THIS IS WHERE YOU PASTE THE KEY
    api_key = st.text_input(
        "Paste Google API Key Here", 
        type="password", 
        help="Get your key from aistudio.google.com"
    )
    
    if not api_key:
        st.error("⚠️ API Key Missing")
        st.markdown("[👉 Get Free Key Here](https://aistudio.google.com/app/apikey)")
    else:
        st.success("✅ Key Active")
    
    st.divider()
    
    st.header("⚙️ Trade Settings")
    expiry = st.selectbox(
        "Expiry Time", 
        ["1 Minute (Turbo)", "2 Minutes", "5 Minutes", "15 Minutes"]
    )

# --- GEMINI 2.5 LOGIC ---
def analyze_market(api_key, image, expiry):
    # Configure with the user's key
    genai.configure(api_key=api_key)
    
    # Using the LATEST Gemini 2.5 Flash model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = (
        f"Act as a professional Binary Options Analyst. "
        f"The user wants to enter a trade with {
