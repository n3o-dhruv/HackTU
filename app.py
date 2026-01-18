import streamlit as st
from PIL import Image
from google import genai
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="PostMortem AI", layout="wide")

# ---------------- UI STYLING ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    .main { background-color: #060a0f; color: #00f2ff; font-family: 'Orbitron', sans-serif; }

    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #0066ff);
        color: white;
        border-radius: 8px;
        border: none;
        box-shadow: 0px 0px 15px #00f2ff;
        font-family: 'Orbitron', sans-serif;
        padding: 10px 18px;
        font-weight: 700;
    }

    h1, h2, h3 { color: #00f2ff !important; }

    .report-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #00f2ff;
        background: rgba(0, 242, 255, 0.06);
        margin-top: 20px;
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🦾 POSTMORTEM AI")
st.subheader("Product Autopsy & SDG Resurrection")
st.write("---")

# ---------------- API SETUP ----------------
client = None
try:
    api_key = st.secrets.get("GOOGLE_API_KEY", None)

    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("❌ GOOGLE_API_KEY not found. Streamlit Secrets me add karo.")
    else:
        client = genai.Client(api_key=api_key)

except Exception as e:
    st.error(f"Setup Error: {e}")

# ---------------- APP LAYOUT ----------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("📸 Scan Product")
    img_file = st.file_uploader("Upload Image of Broken Item", type=['jpg', 'png', 'jpeg'])

    if img_file:
        img = Image.open(img_file).convert("RGB")
        st.image(img, caption="Scanning Anatomy...", use_container_width=True)

        if st.button("🚀 INITIATE AUTOPSY"):
            if not client:
                st.error("Client initialize nahi hua. API key check kar.")
            else:
                with st.spinner("AI is analyzing failure points..."):
                    try:
                        prompt = """
You are PostMortem AI.
Task:
1) Identify the product in the image.
2) Diagnose possible failure causes (physical, electrical, wear & tear).
3) Provide a clear 3-step repair guide (simple, DIY).
4) Provide safety warnings if needed.
Return response in structured format with headings and bullet points.
"""

                        # ✅ FIXED MODEL: gemini-2.0-flash (stable + available)
                        response = client.models.generate_content(
                            model="gemini-2.0-flash",
                            contents=[prompt, img]
                        )

                        st.session_state["report"] = response.text

                    except Exception as e:
                        st.error(f"AI Error: {e}")

with col2:
    if "report" in st.session_state:
        st.header("📋 Diagnostic Report")
        st.markdown(
            f'<div class="report-box">{st.session_state["report"]}</div>',
            unsafe_allow_html=True
        )

        st.divider()
        st.success("✅ Analysis Complete! Contribution to SDG 12 recorded.")

        if st.button("Send Data to Manufacturer"):
            st.toast("📡 Data sent to R&D!")
            st.balloons()
    else:
        st.info("Awaiting product scan. Upload an image to start.")
