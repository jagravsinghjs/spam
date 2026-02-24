import streamlit as st
import pickle
import numpy as np

# Load model and vectorizer
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('words.pkl', 'rb') as f:
    top_spam_words, top_ham_words = pickle.load(f)

def predict_proba_single(message):
    vec = vectorizer.transform([message])
    return model.predict_proba(vec)[0][1]

# Page config
st.set_page_config(page_title="SMS Spam Detector Game", layout="wide")

# Sidebar
st.sidebar.title("Game Settings")
difficulty = st.sidebar.radio("Difficulty", ["Easy", "Medium", "Hard"])
thresholds = {"Easy": 0.7, "Medium": 0.5, "Hard": 0.3}
threshold = thresholds[difficulty]
st.sidebar.markdown(f"**Threshold:** {threshold}")
st.sidebar.markdown("---")
st.sidebar.markdown("**Top Spam Words:**")
st.sidebar.write(list(top_spam_words[:10]))

# Main title
st.title("SMS Spam Detector — Can You Fool It?")
st.markdown(f"Your goal is to get spam probability **below {threshold}** within 3 attempts.")
st.markdown("---")

# Session state init
if "attempt" not in st.session_state:
    st.session_state.attempt = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "prob" not in st.session_state:
    st.session_state.prob = None

# Reset button
if st.sidebar.button("Reset Game"):
    st.session_state.attempt = 0
    st.session_state.messages = []
    st.session_state.game_over = False
    st.session_state.prob = None
    st.rerun()

# Chat history display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Probability bar
if st.session_state.prob is not None:
    st.markdown("**Spam Probability:**")
    st.progress(st.session_state.prob)
    st.markdown(f"### {st.session_state.prob:.2f}")

# Input
if not st.session_state.game_over:
    if st.session_state.attempt == 0:
        placeholder = "Enter a spam message to start..."
    else:
        placeholder = f"Attempt {st.session_state.attempt + 1} of 3 — modify your message..."

    user_input = st.chat_input(placeholder)

    if user_input:
        prob = predict_proba_single(user_input)
        st.session_state.prob = prob
        st.session_state.attempt += 1

        st.session_state.messages.append({"role": "user", "content": user_input})

        if prob < threshold:
            st.session_state.messages.append({"role": "assistant", "content": f"Probability: {prob:.2f} — YOU WIN! You fooled the detector!"})
            st.session_state.game_over = True
        elif st.session_state.attempt >= 3:
            st.session_state.messages.append({"role": "assistant", "content": f"Probability: {prob:.2f} — GAME OVER! You failed to fool the detector."})
            st.session_state.game_over = True
        else:
            remaining = 3 - st.session_state.attempt
            st.session_state.messages.append({"role": "assistant", "content": f"Probability: {prob:.2f} — Still above {threshold}. {remaining} attempt(s) left."})

        st.rerun()
else:
    st.success("Game over! Hit Reset in the sidebar to play again.")
