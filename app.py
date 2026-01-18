import streamlit as st
from PIL import Image
import time

# --- UI CONFIGURATION ---
st.set_page_config(page_title="PostMortem AI", layout="wide")

# Custom CSS for the "Clinical Neon" Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ffcc; }
    .stButton>button { 
        background-color: #00ffcc; color: black; 
        border-radius: 20px; border: none;
        font-weight: bold; width: 100%;
    }
    .sdg-card {
        background: rgba(0, 255, 204, 0.1);
        padding: 20px; border-radius: 15px;
        border: 1px solid #00ffcc;
    }
    h1, h2, h3 { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_input=True)

# --- SIDEBAR: USER STATS ---
st.sidebar.title("👤 User Profile")
st.sidebar.markdown("### **Karma Points: 1,250**")
st.sidebar.progress(75)
st.sidebar.write("Goal: SDG 12 - Responsible Consumption")

# --- MAIN INTERFACE ---
st.title("📟 PostMortem AI")
st.subheader("Digital Product Autopsy & Resurrection")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🔍 Scan Broken Product")
    uploaded_file = st.file_uploader("Upload photo or video of failure", type=['png', 'jpg', 'jpeg', 'mp4'])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Scanning for structural weaknesses...", use_container_width=True)
        
        if st.button("RUN AUTOPSY"):
            with st.spinner('AI analyzing failure points...'):
                time.sleep(2) # Simulating AI processing
                st.success("Analysis Complete!")
                st.session_state['analyzed'] = True

with col2:
    if 'analyzed' in st.session_state:
        st.markdown("### 📋 Autopsy Report")
        
        # Simulated Data Findings
        st.error("Detected: Capacitor Leakage (Model: XRT-500)")
        st.info("Repairability Score: 65%")
        
        tab1, tab2, tab3 = st.tabs(["🔧 Repair", "♻️ Harvest", "📈 Manufacturer Data"])
        
        with tab1:
            st.write("Manual Found: 'Toaster Power Circuitry'")
            st.markdown("- Step 1: Unscrew bottom plate\n- Step 2: Desolder C14 capacitor")
            if st.button("Claim +50 SDG Points for Repair"):
                st.balloons()
        
        with tab2:
            st.write("Valuable Components Detected:")
            st.markdown("* **Copper Wiring** (99% Pure)\n* **Heating Element** (Salvageable)")
            st.button("Locate Nearest Repair Cafe")

        with tab3:
            st.warning("⚠️ Manufacturer View (Locked)")
            st.write("Common failure detected in 14% of units. Sending anonymized data to R&D.")

# --- FOOTER: SDG TRACKER ---
st.divider()
st.markdown("### 🌍 Your Environmental Impact (SDG Tracker)")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="sdg-card"><b>SDG 12</b><br>12kg Waste Prevented</div>', unsafe_allow_input=True)
with c2:
    st.markdown('<div class="sdg-card"><b>SDG 13</b><br>45kg CO2 Offset</div>', unsafe_allow_input=True)
with c3:
    st.markdown('<div class="sdg-card"><b>SDG 9</b><br>2 Design Improvements Sent</div>', unsafe_allow_input=True)
