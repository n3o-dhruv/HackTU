import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- INITIAL SETUP ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # FIXED: Using a more stable model string
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- CRAZY UI STYLING ---
st.set_page_config(page_title="PostMortem AI", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .main { background-color: #060a0f; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .stButton>button { 
        background: linear-gradient(45deg, #00f2ff, #0066ff); 
        color: white; border-radius: 5px; box-shadow: 0px 0px 15px #00f2ff;
        font-family: 'Orbitron', sans-serif;
    }
    h1, h2, h3 { color: #00f2ff !important; }
    .report-text { background: rgba(0, 242, 255, 0.05); padding: 20px; border-radius: 10px; border: 1px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦾 POSTMORTEM AI")
st.subheader("Product Autopsy & SDG Resurrection")
st.write("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("📸 Scan Product")
    img_file = st.file_uploader("Upload Image of Broken Item", type=['jpg', 'png', 'jpeg'])
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Scanning Anatomy...", use_container_width=True)
        
        if st.button("🚀 RUN AUTOPSY"):
            with st.spinner("AI is examining failure points..."):
                try:
                    # Specific prompt for better results
                    prompt = "Identify this broken item. Explain likely cause of failure and give a step-by-step repair guide or harvesting advice for SDG impact."
                    response = model.generate_content([prompt, img])
                    st.session_state['report'] = response.text
                except Exception as e:
                    st.error(f"AI Error: {e}")

with col2:
    if 'report' in st.session_state:
        st.header("📋 Diagnostic Report")
        st.markdown(f'<div class="report-text">{st.session_state["report"]}</div>', unsafe_allow_html=True)
        
        st.divider()
        st.success("✅ Analysis Complete! You've earned +150 SDG Karma Points.")
        if st.button("Send Data to Manufacturer"):
            st.toast("Feedback sent to R&D team!")
            st.balloons()
    else:
        st.info("Upload an image and click 'Run Autopsy' to begin the digital dissection.")
