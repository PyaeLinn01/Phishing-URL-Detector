import streamlit as st
import numpy as np
import pickle
from feature import FeatureExtraction

# Load the model
with open("pickle/retrain.pkl", "rb") as file:
    model = pickle.load(file)

# Page setup
st.set_page_config(page_title="🛡️ Phishing URL Detector", layout="centered", page_icon="🔍")

# Title
st.markdown("""
    <h1 style="text-align:center;">🛡️ Phishing URL Detector</h1>
    <p style="text-align:center;">Enter a URL to find out if it's safe or potentially malicious</p>
""", unsafe_allow_html=True)

# Input
url = st.text_input("🔗 Enter a URL", placeholder="https://example.com")

if st.button("🚀 Check Now"):
    if url:
        try:
            extractor = FeatureExtraction(url)
            features = np.array(extractor.getFeaturesList()).reshape(1, 30)

            prediction = model.predict(features)[0]
            proba_safe = model.predict_proba(features)[0][1]
            proba_phishing = model.predict_proba(features)[0][0]

            if prediction == 1:
                # Safe URL
                st.markdown("""
                    <div style="background-color:#d4edda;padding:40px 20px;border-radius:10px;text-align:center;">
                        <h1 style="color:#155724;font-size:48px;">✅ VALID URL</h1>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Confidence:** {proba_safe*100:.2f}%")
                st.markdown(f'<span style="color:#008000;">✅ It is safe to visit: <a href="{url}" target="_blank">{url}</a></span>', unsafe_allow_html=True)

            else:
                # Unsafe URL
                st.markdown("""
                    <div style="background-color:#f8d7da;padding:40px 20px;border-radius:10px;text-align:center;">
                        <h1 style="color:#721c24;font-size:48px;">❌ UNSAFE URL</h1>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Confidence:** {proba_phishing*100:.2f}%")
                st.markdown(f'<span style="color:#FF0000;">❌ This is not safe to visit that link!!!</span>', unsafe_allow_html=True)

        except Exception as e:
            st.error("An error occurred during processing.")
            st.code(str(e))
    else:
        st.warning("⚠️ Please enter a valid URL.")
