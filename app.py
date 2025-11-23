import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="Quotex Gemini Bot", page_icon="⚡")

st.title("⚡ Quotex Bot (Gemini 1.5 Flash)")
st.caption("Upload Chart -> Select Expiry -> Gemini Analysis")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    # Get this key from: https://aistudio.google.com/app/apikey
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    
    st.divider()
    
    expiry_time = st.selectbox(
        "Select Expiry Time",
        ["1 Minute", "2 Minutes", "5 Minutes", "15 Minutes", "1 Hour"]
    )

# --- LOGIC ---
def get_gemini_signal(api_key, image, expiry):
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Use Gemini 1.5 Flash (Fast & Good with Images)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = (
        f"You are an expert Binary Options trader using Price Action technical analysis. "
        f"The user wants to take a trade with an expiry time of {expiry}. "
        f"Analyze the chart image deeply. Look for: "
        f"1. Trend Direction (Uptrend/Downtrend/Ranging). "
        f"2. Key Support & Resistance levels. "
        f"3. Candlestick patterns (Hammer, Engulfing, Doji). "
        f"Based on this, provide a trading signal."
        f"\n\nRETURN STRICT JSON FORMAT:"
        f"\nSIGNAL: CALL (UP) or PUT (DOWN)"
        f"\nCONFIDENCE: (High/Medium/Low)"
        f"\nREASON: (Brief logic)"
    )
    
    # Gemini takes the prompt and the image directly
    response = model.generate_content([prompt, image])
    return response.text

# --- MAIN INTERFACE ---
if not api_key:
    st.warning("⚠️ Please enter your Google API Key in the sidebar.")
    st.markdown("[Get a Free API Key Here](https://aistudio.google.com/app/apikey)")
else:
    uploaded_file = st.file_uploader("Upload Quotex Screenshot", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        # Convert to PIL Image for Gemini
        image = Image.open(uploaded_file)
        st.image(image, caption="Chart Preview", use_container_width=True)
        
        if st.button("🚀 ANALYZE WITH GEMINI", type="primary"):
            with st.spinner("Gemini Flash is thinking..."):
                try:
                    result = get_gemini_signal(api_key, image, expiry_time)
                    
                    st.success("Signal Generated!")
                    st.markdown("### ⚡ Gemini Signal")
                    st.write(result)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
