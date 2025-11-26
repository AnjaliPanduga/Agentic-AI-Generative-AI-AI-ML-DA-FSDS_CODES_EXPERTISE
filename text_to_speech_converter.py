import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
import random
import time

st.set_page_config(page_title="Text To Speech Translator", page_icon="🎤", layout="wide")

# ---------------- QUOTES ----------------
quotes = [
    "🌟 Every language is a new world!",
    "🚀 Speak globally, dream big!",
    "💡 Technology makes communication limitless.",
    "🎯 Your voice can reach every country!",
    "🌍 Languages connect hearts."
]

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🎨 Theme")
    theme = st.radio("Select Theme",
                     ["Ocean Blue", "Mint Green", "Rose Red", "Lavender Purple", "Black"],
                     label_visibility="collapsed")

    if theme == "Ocean Blue": bg = "#C2E7FF"
    elif theme == "Mint Green": bg = "#C8FFD4"
    elif theme == "Rose Red": bg = "#FFC4C4"
    elif theme == "Lavender Purple": bg = "#E3C8FF"
    elif theme == "Black": bg = "#000000"

    st.markdown("----")
    st.caption("✨ VoiceX – Text to Speech in 18 Languages")
    st.caption("❤️ Made for creative minds")

# ---------------- BACKGROUND COLOR ----------------
st.markdown(
    f"""<style>[data-testid="stAppViewContainer"] {{background-color: {bg};}}</style>""",
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🎤 Text To Speech Converter </h1>", unsafe_allow_html=True)
st.subheader("🌏 Convert English to 18 languages — listen & download the audio")

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1, 2])
with col1:
    st.info(random.choice(quotes))
with col2:
    english_text = st.text_area("📝 Enter English Text", height=180, placeholder="Start typing here...")

# ---------------- LANGUAGE LIST ----------------
languages = {
    "English": "en", "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn",
    "Malayalam": "ml", "Gujarati": "gu", "Marathi": "mr", "Bengali": "bn",
    "Punjabi": "pa", "Urdu": "ur", "Odia": "or", "Assamese": "as", "Nepali": "ne",
    "Sinhala": "si", "Korean": "ko", "Japanese": "ja", "French": "fr"
}

selected_language = st.selectbox("🌐 Select Language", list(languages.keys()))

# ---------------- BUTTON ----------------
if st.button("🔥 Convert to Speech"):
    if english_text.strip() == "":
        st.warning("⚠ Please type something")
    else:
        with st.spinner("🔁 Translating text..."):
            translated = GoogleTranslator(source='auto', target=languages[selected_language]).translate(english_text)
            time.sleep(1)

        st.success("✨ Translation Completed!")
        st.write("### 📝 Converted Text:")
        st.write(translated)

        with st.spinner("🔊 Generating voice..."):
            tts = gTTS(translated, lang=languages[selected_language])
            tts.save("speech.mp3")
            time.sleep(1)

        st.audio("speech.mp3")
        with open("speech.mp3", "rb") as f:
            st.download_button("📥 Download Speech", f, file_name="speech.mp3")

# ---------------- FOOTER ----------------
st.markdown("<h4 style='text-align:center;'>💫 Voice bridges every emotion and every nation.</h4>", unsafe_allow_html=True)
