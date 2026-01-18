import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- INITIAL SETUP ---
try:
    # Yeh aapke "Secrets" se key uthayega
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Secrets mein GOOGLE_API_KEY nahi mili!")

# --- CRAZY UI STYLING ---
st.set_page_config(page_title="PostMortem AI", layout="wide")

# FIXED ERROR: Changed unsafe_allow_input to unsafe_allow_html
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .main { background-color: #060a0f; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .stButton>button { 
        background: linear-gradient(45deg, #00f2ff, #0066ff); 
        color: white; border-radius: 5px; box-shadow: 0px 0px 15px #00f2ff;
    }
    h1, h2, h3 { color: #00f2ff !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦾 POSTMORTEM AI")
st.write("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("📸 Scan Product")
    img_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, use_container_width=True)
        if st.button("🚀 RUN AUTOPSY"):
            with st.spinner("AI analyzing..."):
                prompt = "Analyze this image: Identify the item, common failure points, and a quick repair guide."
                response = model.generate_content([prompt, img])
                st.session_state['report'] = response.text

with col2:
    if 'report' in st.session_state:
        st.header("📋 Diagnostic Report")
        st.write(st.session_state['report'])
        st.balloons()
