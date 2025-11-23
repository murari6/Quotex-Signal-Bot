import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageEnhance
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Quotex Bot Pro", page_icon="📈", layout="wide")

st.title("📈 Quotex AI Bot Pro (with Journal)")
st.caption("Analyze -> Trade -> Record Win/Loss")

# --- 2. INITIALIZE SESSION STATE (The Memory) ---
if 'history' not in st.session_state:
    st.session_state['history'] = [] # Stores all past trades

if 'last_signal' not in st.session_state:
    st.session_state['last_signal'] = None # Stores the current active signal

# --- 3. SIDEBAR & SETTINGS ---
with st.sidebar:
    st.header("🔐 Authorization")
    api_key = st.text_input("Paste Google API Key", type="password")
    
    st.divider()
    
    st.header("⚙️ Trade Settings")
    expiry = st.selectbox("Expiry Time", ["1 Minute", "2 Minutes", "5 Minutes", "15 Minutes"])
    
    # Show Stats
    if len(st.session_state['history']) > 0:
        st.divider()
        st.header("📊 Performance")
        df = pd.DataFrame(st.session_state['history'])
        wins = df[df['Result'] == 'WIN'].shape[0]
        total = df.shape[0]
        win_rate = (wins / total) * 100
        st.write(f"**Win Rate:** {win_rate:.1f}%")
        st.write(f"**Total Trades:** {total}")

# --- 4. FUNCTIONS ---
def enhance_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(1.5)

def analyze_market(api_key, image, expiry_time):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = (
        f"Act as a strict Binary Options Analyst. User wants {expiry_time} expiry. "
        f"Analyze: Trend, Key Levels, Candle Patterns. "
        f"DECISION RULE: Need 2+ confirmations. "
        f"OUTPUT FORMAT (JSON ONLY): "
        f"SIGNAL: [CALL / PUT / NO TRADE] "
        f"CONFIDENCE: [High/Medium/Low] "
        f"REASON: [Strict reason]"
    )
    response = model.generate_content([prompt, image])
    return response.text

# --- 5. MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📂 1. Upload Chart", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        raw_image = Image.open(uploaded_file)
        enhanced_image = enhance_image(raw_image)
        st.image(enhanced_image, caption="Enhanced Analysis View", use_container_width=True)

with col2:
    st.subheader("🤖 2. Signal Panel")
    
    # BUTTON: Generate Signal
    if uploaded_file and api_key:
        if st.button("⚡ ANALYZE CHART", type="primary", use_container_width=True):
            with st.spinner("Thinking..."):
                try:
                    result_text = analyze_market(api_key, enhanced_image, expiry)
                    # Save signal to session state so it doesn't disappear
                    st.session_state['last_signal'] = {
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "expiry": expiry,
                        "raw_result": result_text
                    }
                except Exception as e:
                    st.error(f"Error: {e}")

    # DISPLAY: Show the Signal if it exists
    if st.session_state['last_signal']:
        signal_data = st.session_state['last_signal']
        
        st.info("Analysis Result:")
        st.code(signal_data['raw_result'], language="yaml")
        
        st.divider()
        st.subheader("📝 3. Trade Result")
        
        # Form for Win/Loss/Note
        with st.form("result_form"):
            outcome = st.radio("Was this a Win or Loss?", ["WIN 🟢", "LOSS 🔴", "NO TRADE ⚪"], horizontal=True)
            note = st.text_input("Add a Note (e.g., 'Bad entry', 'Strong trend')")
            
            submitted = st.form_submit_button("💾 SAVE TO HISTORY")
            
            if submitted:
                # Add to history list
                st.session_state['history'].append({
                    "Time": signal_data['time'],
                    "Expiry": signal_data['expiry'],
                    "Result": outcome,
                    "Note": note,
                    "Signal_Raw": signal_data['raw_result'][:50] + "..." # Save snippet
                })
                # Clear the current signal to reset the form
                st.session_state['last_signal'] = None
                st.rerun() # Refresh page to show updated table

# --- 6. TRADE HISTORY TABLE (Bottom) ---
st.divider()
st.subheader("📜 Trade History Journal")

if len(st.session_state['history']) > 0:
    # Create a pretty dataframe
    history_df = pd.DataFrame(st.session_state['history'])
    st.dataframe(history_df, use_container_width=True)
else:
    st.text("No trades recorded yet.")
