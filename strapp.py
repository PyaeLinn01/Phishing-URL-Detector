import streamlit as st
import numpy as np
import pickle
from feature import FeatureExtraction

# Load model
with open("pickle/retrain.pkl", "rb") as file:
    model = pickle.load(file)

# Language dictionary
english_texts = {
    "title": "🛡️ Phishing URL Detector",
    "desc": "Enter a URL to find out if it's safe or potentially malicious",
    "input": "🔗 Enter a URL",
    "placeholder": "https://example.com",
    "button": "🚀 Check Now",
    "safe": "✅ VALID URL",
    "unsafe": "❌ UNSAFE URL",
    "conf": "Confidence",
    "safe_visit": "✅ It is safe to visit: ",
    "unsafe_visit": "❌ This is not safe to visit that link!!!",
    "error": "An error occurred during processing.",
    "empty": "⚠️ Please enter a valid URL."
}

myanmar_texts = {
    "title": "🛡️ သင်သွားလိုသည့်လင့်ခ်ကို လုံခြုံမှုရှိမရှိ စစ်​ဆေးနိုင်သည့် ကိရိယာ",
    "desc": "သွားလိုသည့် လင့်ခ်ကို ​ကူးယူပြီး ​​အောက်​​ဖော်ပြပါ ​နေရာ​တွေထည့်ပြီး စစ်​ဆေးလို့ရပါသည်",
    "input": "🔗 လင့်ခ်ကို ထည့်ပါ",
    "placeholder": "https://example.com",
    "button": "🚀 စစ်ဆေးရန်",
    "safe": "✅ လုံခြုံသော လင့်ခ်",
    "unsafe": "❌ အန္တရာယ်ရှိသော လင့်ခ်ဖြစ်ပါသည်",
    "conf": "ဖြစ်နိုင်​​​ခြေ",
    "safe_visit": "✅ လုံခြုံသည့် လင့်ခ်ဖြစ်သည် - ",
    "unsafe_visit": "❌ ဤလင့်ခ်ကို သွားရန်မသင့်ပါ!",
    "error": "လုပ်ဆောင်ချိန်တွင် ပြဿနာတစ်ခု ဖြစ်ပွားခဲ့သည်။",
    "empty": "⚠️ ကျေးဇူးပြု၍ သင်ဧ။်လင့်ခ်ကို ထည့်ပါ။"
}

# Page setup
st.set_page_config(page_title="Phishing URL Detector", layout="centered", page_icon="🔍")

# Language selection
lang = st.sidebar.radio("🌐 Language / ဘာသာစကား", ["English", "မြန်မာ"])

texts = english_texts if lang == "English" else myanmar_texts

# Title
st.markdown(f"<h1 style='text-align:center;'>{texts['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>{texts['desc']}</p>", unsafe_allow_html=True)

# Input
url = st.text_input(texts["input"], placeholder=texts["placeholder"])

if st.button(texts["button"]):
    if url:
        try:
            extractor = FeatureExtraction(url)
            features = np.array(extractor.getFeaturesList()).reshape(1, 30)

            prediction = model.predict(features)[0]
            proba_safe = model.predict_proba(features)[0][1]
            proba_phishing = model.predict_proba(features)[0][0]

            if prediction == 1:
                # Safe
                st.markdown(f"""
                    <div style="background-color:#d4edda;padding:40px 20px;border-radius:10px;text-align:center;">
                        <h1 style="color:#155724;font-size:48px;">{texts['safe']}</h1>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**{texts['conf']}:** {proba_safe*100:.2f}%")
                st.markdown(f'<span style="color:#008000;">{texts["safe_visit"]}<a href="{url}" target="_blank">{url}</a></span>', unsafe_allow_html=True)
            else:
                # Unsafe
                st.markdown(f"""
                    <div style="background-color:#f8d7da;padding:40px 20px;border-radius:10px;text-align:center;">
                        <h1 style="color:#721c24;font-size:48px;">{texts['unsafe']}</h1>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**{texts['conf']}:** {proba_phishing*100:.2f}%")
                st.markdown(f'<span style="color:#FF0000;">{texts["unsafe_visit"]}</span>', unsafe_allow_html=True)

        except Exception as e:
            st.error(texts["error"])
            st.code(str(e))
    else:
        st.warning(texts["empty"])

