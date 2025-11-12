import streamlit as st
import random

st.set_page_config(page_title="VibeBeats 🎶", page_icon="🎧", layout="centered")

# 🌈 Title
st.markdown("<h1 style='text-align:center; color:white;'>🎧 VibeBeats 🎶</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white;'>Let your mood set the beat!</p>", unsafe_allow_html=True)

# 🎭 Mood options
moods = ["😊 Happy", "😴 Calm", "💪 Energetic", "😔 Chill"]

# 🌈 Gradients for each mood
gradients = {
    "😊 Happy": "linear-gradient(to right, #FFD700, #FF8C00)",
    "😴 Calm": "linear-gradient(to right, #83a4d4, #b6fbff)",
    "💪 Energetic": "linear-gradient(to right, #ff512f, #dd2476)",
    "😔 Chill": "linear-gradient(to right, #654ea3, #eaafc8)"
}

# 🎵 Music URLs (YouTube links)
music_links = {
    "😊 Happy": "https://www.youtube.com/embed/ZbZSe6N_BXs",  # Happy - Pharrell Williams
    "😴 Calm": "https://www.youtube.com/embed/1ZYbU82GVz4",  # Relaxing music
    "💪 Energetic": "https://www.youtube.com/embed/d-diB65scQU",  # Power song
    "😔 Chill": "https://www.youtube.com/embed/2Vv-BfVoq4g"   # Ed Sheeran - Perfect
}

# 🧠 Select mood
mood = st.selectbox("Choose your mood:", moods)

# 🎨 Animated gradient background
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: {gradients[mood]};
    animation: gradient 10s ease infinite;
    background-size: 400% 400%;
}}
@keyframes gradient {{
    0% {{background-position: 0% 50%;}}
    50% {{background-position: 100% 50%;}}
    100% {{background-position: 0% 50%;}}
}}
h1, p, label {{
    color: white;
    text-align: center;
}}
div.stButton > button {{
    background-color: white;
    color: black;
    border-radius: 12px;
    font-size: 18px;
    padding: 6px 16px;
}}
</style>
""", unsafe_allow_html=True)

# ▶️ Show video player
st.markdown(f"<h3 style='text-align:center;'>Now playing: {mood} vibes 🎶</h3>", unsafe_allow_html=True)
st.video(music_links[mood])
