import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageEnhance

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Quotex AI Bot 2.5", page_icon="🚀", layout="wide")

st.title("🚀 Quotex AI Signal Bot (Gemini 2.5)")
st.caption("Advanced Technical Analysis • Image Enhancement • Chain of Thought Logic")

# --- 2. SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("🔐 Authorization")
    api_key = st.text_input(
        "Paste Google API Key", 
        type="password",
        help="Get this from aistudio.google.com"
    )
    
    st.divider()
    
    st.header("⚙️ Trade Settings")
    # We define 'expiry' here so it can be used later
    expiry = st.selectbox(
        "Select Expiry Time", 
        ["1 Minute", "2 Minutes", "5 Minutes", "15 Minutes"]
    )
    
    st.info("ℹ️ Tip: Enable Bollinger Bands & RSI on your chart for better accuracy.")

# --- 3. THE AI BRAIN (Functions) ---
def enhance_image(image):
    """Increases contrast so AI sees wicks better."""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(1.5) # Increase contrast by 50%

def analyze_market(api_key, image, expiry_time):
    """Sends the image to Gemini 2.5 with the strict prompt."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # The Advanced Prompt
    prompt = (
        f"Act as a strict Price Action Scalper. "
        f"The user wants to trade with {expiry_time} expiry. "
        f"Analyze the chart using this 3-step confirmation process:"
        f"\n1. MARKET STRUCTURE: Identify if the trend is Up, Down, or Ranging. "
        f"\n2. KEY LEVELS: Look for Support/Resistance lines or round numbers. "
        f"\n3. CANDLE PATTERNS: Look for rejection wicks, engulfing bars, or dojis."
        f"\n\nDECISION RULE: Only generate a signal if at least 2 factors align. Otherwise, say 'NO TRADE'."
        f"\n\nOUTPUT FORMAT (JSON ONLY):"
        f"\nSIGNAL: [CALL / PUT / NO TRADE]"
        f"\nCONFIDENCE: [High / Medium / Low]"
        f"\nREASON: [List the factors that confirmed this trade]"
    )
    
    response = model.generate_content([prompt, image])
    return response.text

# --- 4. THE MAIN APP INTERFACE ---
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📂 Upload Quotex Screenshot", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        # Process the image
        raw_image = Image.open(uploaded_file)
        enhanced_image = enhance_image(raw_image)
        
        # Show the enhanced view
        st.image(enhanced_image, caption="AI Vision (Enhanced Contrast)", use_container_width=True)

with col2:
    st.subheader("🤖 Signal Panel")
    
    if uploaded_file and api_key:
        if st.button("⚡ ANALYZE CHART", type="primary", use_container_width=True):
            with st.spinner("Gemini 2.5 is analyzing market structure..."):
                try:
                    # Call the function defined above
                    result = analyze_market(api_key, enhanced_image, expiry)
                    
                    st.success("Analysis Complete")
                    st.code(result, language="yaml")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    
    elif not uploaded_file:
        st.info("👈 Upload a chart to start.")
    elif not api_key:
        st.warning("👈 Enter API Key in sidebar.")
