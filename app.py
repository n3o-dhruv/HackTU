import time
import streamlit as st
from PIL import Image
from google import genai
import os

st.set_page_config(page_title="PostMortem AI", layout="wide")

# ---- API SETUP ----
client = None
api_key = st.secrets.get("GOOGLE_API_KEY", None) or os.getenv("GOOGLE_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("❌ GOOGLE_API_KEY not found in secrets")

# ---- UI ----
st.title("🦾 POSTMORTEM AI")
st.write("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("📸 Scan Product")
    img_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if img_file:
        img = Image.open(img_file).convert("RGB")
        st.image(img, caption="Scanning Anatomy...", use_container_width=True)

        if st.button("🚀 INITIATE AUTOPSY"):
            if not client:
                st.error("API client not initialized.")
            else:
                with st.spinner("AI is analyzing failure points..."):
                    prompt = """
You are PostMortem AI.
1) Identify product
2) Diagnose failure reasons
3) Provide 3-step repair guide
4) Safety warnings
Return structured headings + bullet points.
"""

                    try:
                        # ✅ safer model (more likely available on free quota)
                        response = client.models.generate_content(
                            model="gemini-1.5-flash-latest",
                            contents=[prompt, img],
                        )
                        st.session_state["report"] = response.text

                    except Exception as e:
                        msg = str(e)

                        # ✅ handle 429 gracefully
                        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                            st.error("⚠️ Quota/Rate limit exceeded. Wait 20 sec and try again.")
                            time.sleep(20)
                            st.warning("Retrying once...")

                            try:
                                response = client.models.generate_content(
                                    model="gemini-1.5-flash-latest",
                                    contents=[prompt, img],
                                )
                                st.session_state["report"] = response.text
                            except Exception as e2:
                                st.error(f"Still blocked by quota/rate limit: {e2}")
                        else:
                            st.error(f"AI Error: {e}")

with col2:
    if "report" in st.session_state:
        st.header("📋 Diagnostic Report")
        st.write(st.session_state["report"])
    else:
        st.info("Awaiting scan...")
