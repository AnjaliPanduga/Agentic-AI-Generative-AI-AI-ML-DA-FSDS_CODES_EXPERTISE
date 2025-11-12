import streamlit as st
import random

# 🌈 App Config
st.set_page_config(page_title="MoodGlow ✨", page_icon="🌈", layout="centered")

# 🌸 App Title
st.markdown(
    "<h1 style='text-align:center; color:white;'>🌈 MoodGlow ✨</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align:center; color:white;'>Let your mood shine with a glowing quote!</p>", unsafe_allow_html=True)

# 🎭 Mood options
moods = ["😊 Happy", "😔 Sad", "💪 Motivated", "😴 Tired", "😡 Angry"]

# 🌈 Gradient backgrounds for each mood
gradients = {
    "😊 Happy": "linear-gradient(to right, #FFD700, #FF8C00)",
    "😔 Sad": "linear-gradient(to right, #83a4d4, #b6fbff)",
    "💪 Motivated": "linear-gradient(to right, #00b09b, #96c93d)",
    "😴 Tired": "linear-gradient(to right, #8360c3, #2ebf91)",
    "😡 Angry": "linear-gradient(to right, #e52d27, #b31217)"
}

# 💭 Quotes for each mood
quotes = {
    "😊 Happy": [
        "Happiness is contagious — spread it everywhere you go!",
        "Smile! It makes you and the world brighter 😊",
        "Enjoy the little things — they make life big!"
    ],
    "😔 Sad": [
        "It’s okay to feel down — better days are coming 💖",
        "Tough times don’t last, but tough people do.",
        "Even the darkest night will end and the sun will rise 🌅"
    ],
    "💪 Motivated": [
        "Push yourself, because no one else is going to do it for you 💪",
        "Dream it. Believe it. Build it.",
        "Don’t stop when you’re tired — stop when you’re done!"
    ],
    "😴 Tired": [
        "Take a break — rest is also productive 😴",
        "Recharge now, shine later 🌟",
        "Even machines need to power down to perform better."
    ],
    "😡 Angry": [
        "Breathe in peace, breathe out stress 🌬️",
        "Don’t let anger control your actions — stay calm.",
        "You’re stronger than your anger ❤️"
    ]
}

# 🎯 Mood selection
mood = st.selectbox("How are you feeling today?", moods)

# 🌟 Animated background with gradient
page_bg = f"""
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
h1, h3, p, label {{
    color: white;
    text-align: center;
    font-family: 'Trebuchet MS', sans-serif;
}}
div.stButton > button {{
    background-color: black;
    color: black;
    border-radius: 12px;
    font-size: 18px;
    padding: 8px 20px;
    transition: 0.3s;
}}
div.stButton > button:hover {{
    background-color: #f0f0f0;
    transform: scale(1.05);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 🔁 Button to generate new quote
if st.button("✨ Inspire Me ✨"):
    st.markdown(f"<h3 style='text-align:center;'>{random.choice(quotes[mood])}</h3>", unsafe_allow_html=True)
else:
    st.markdown(f"<h3 style='text-align:center;'>{random.choice(quotes[mood])}</h3>", unsafe_allow_html=True)
