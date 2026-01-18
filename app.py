import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- INITIAL SETUP ---
# Replace with your actual API Key
os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- CRAZY UI STYLING ---
st.set_page_config(page_title="PostMortem AI", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .main { background-color: #060a0f; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .stAlert { background-color: rgba(0, 242, 255, 0.1); border: 1px solid #00f2ff; color: #00f2ff; }
    .stButton>button { 
        background: linear-gradient(45deg, #00f2ff, #0066ff); 
        color: white; border-radius: 5px; border: none;
        box-shadow: 0px 0px 15px #00f2ff; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0px 0px 25px #00f2ff; }
    .sdg-box {
        padding: 15px; border-radius: 10px; border-left: 5px solid #00f2ff;
        background: rgba(255, 255, 255, 0.05); margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_input=True)

# --- APP LAYOUT ---
st.title("🦾 POSTMORTEM AI")
st.write("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("📸 Digital Autopsy")
    img_file = st.file_uploader("Upload Image of Broken Product", type=['jpg', 'png', 'jpeg'])
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Scanning Product Anatomy...", use_container_width=True)
        
        if st.button("🚀 INITIATE ANALYSIS"):
            with st.spinner("Decoding failure patterns..."):
                # AI PROMPT
                prompt = """
                Act as a master repair engineer and environmentalist. 
                Analyze this image and provide:
                1. Identification: What is this product?
                2. Autopsy: Likely cause of failure.
                3. Action: Can it be fixed? If not, what parts (copper, battery, etc.) can be harvested?
                4. SDG Impact: How much CO2 is saved by not buying a new one?
                Format as a professional report.
                """
                response = model.generate_content([prompt, img])
                st.session_state['report'] = response.text
                st.session_state['points'] = 150 # Simulated points

with col2:
    if 'report' in st.session_state:
        st.header("📋 AI Diagnostic Report")
        st.markdown(st.session_state['report'])
        
        st.write("---")
        st.header("🌍 SDG Impact Earned")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
                <div class="sdg-box">
                    <h3>+{st.session_state['points']} Karma</h3>
                    <p>SDG 12: Responsible Consumption</p>
                </div>
            """, unsafe_allow_input=True)
        with c2:
            st.markdown(f"""
                <div class="sdg-box">
                    <h3>0.5kg CO2 Saved</h3>
                    <p>SDG 13: Climate Action</p>
                </div>
            """, unsafe_allow_input=True)

        if st.button("SEND DATA TO MANUFACTURER (+50 Bonus Points)"):
            st.toast("Anonymized data sent to R&D. Design feedback loop closed!")
            st.balloons()
    else:
        st.info("Upload an image and hit 'Initiate Analysis' to see the magic.")
