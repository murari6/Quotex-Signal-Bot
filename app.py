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
        f"The user wants to enter a trade with {expiry} expiry. "
        f"Analyze this chart image specifically for: "
        f"1. Immediate Trend (Micro-trend). "
        f"2. Candlestick Psychology (Wicks, Body size). "
        f"3. Support/Resistance proximity. "
        f"Provide a strict signal."
        f"\n\nOUTPUT FORMAT (JSON ONLY):"
        f"\nSIGNAL: [CALL / PUT]"
        f"\nCONFIDENCE: [0-100%]"
        f"\nREASON: [One sentence strict reason]"
    )
    
    # Generate response
    response = model.generate_content([prompt, image])
    return response.text

# --- MAIN INTERFACE ---
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📂 Upload Screenshot", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        # Show image
        image = Image.open(uploaded_file)
        st.image(image, caption="Market Context", use_container_width=True)

with col2:
    st.subheader("Signal Panel")
    if uploaded_file and api_key:
        if st.button("⚡ PREDICT SIGNAL", type="primary", use_container_width=True):
            with st.spinner("Gemini 2.5 is thinking..."):
                try:
                    # Call the AI
                    result = analyze_market(api_key, image, expiry)
                    
                    # Display result
                    st.info("Analysis Result:")
                    st.code(result, language="yaml")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    elif not uploaded_file:
        st.info("👈 Upload a chart to begin.")
    elif not api_key:
        st.warning("👈 Please paste your API Key in the sidebar.")
