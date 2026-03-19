import streamlit as st
import pickle
import base64

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('words.pkl', 'rb') as f:
    top_scam_words, top_ham_words = pickle.load(f)

def predict(message):
    vec = vectorizer.transform([message])
    return model.predict_proba(vec)[0][1]

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64_image("bg.jpg")

st.markdown(f"""
    <style>
    /* Full screen background including sidebar area */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Dark overlay over main content only */
    .block-container {{
        background: rgba(0,0,0,0.78);
        border-radius: 12px;
        padding: 2rem !important;
    }}
    /* Sidebar dark overlay */
    [data-testid="stSidebar"] {{
        background: rgba(0,0,0,0.85) !important;
    }}
    h1 {{
        white-space: nowrap;
        font-size: 2rem !important;
        color: white !important;
    }}
    .stMarkdown, .stText, p, label, .stRadio {{
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Game Settings")
difficulty = st.sidebar.radio("Select Difficulty", ["Easy", "Medium", "Hard"])
thresholds = {"Easy": 0.7, "Medium": 0.5, "Hard": 0.3}
threshold = thresholds[difficulty]
st.sidebar.markdown(f"**Beat this threshold: {threshold}**")
st.sidebar.markdown("---")

# About toggle using session state
if "show_about" not in st.session_state:
    st.session_state.show_about = False

if st.sidebar.button("📋 About This Project"):
    st.session_state.show_about = not st.session_state.show_about

if st.session_state.show_about:
    st.sidebar.info("""
    **Scamouflage**
    
    A scam detection system trained on 2248 synthetic messages using TF-IDF and Logistic Regression.
    
    Your goal: fool the detector by writing a scam message that scores below the threshold.
    
    - F1 Score: 0.94
    - ROC-AUC: 0.99
    - Dataset: Synthetic phishing & scam messages
    
    Built to demonstrate adversarial robustness of text classifiers.
    """)

# Main
st.title("Scamouflage — Can You Fool The Detector?")
st.markdown(f"Get scam probability **below {threshold}** in 1 attempt")
st.markdown("---")

# Session state
if "attempt" not in st.session_state:
    st.session_state.attempt = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "prob" not in st.session_state:
    st.session_state.prob = None
if "won" not in st.session_state:
    st.session_state.won = False

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Probability bar
if st.session_state.prob is not None:
    st.progress(st.session_state.prob)
    st.markdown(f"### Scam Probability: {st.session_state.prob:.2f}")

# Game logic
if not st.session_state.game_over:
    user_input = st.chat_input("Type your scam message here...")
    if user_input:
        prob = predict(user_input)
        st.session_state.prob = prob
        st.session_state.attempt += 1
        st.session_state.messages.append({"role": "user", "content": user_input})

        if prob < threshold:
            st.session_state.messages.append({"role": "assistant", "content": f"Scam Probability: {prob:.2f} — 🎉 YOU WIN! You fooled the detector!"})
            st.session_state.game_over = True
            st.session_state.won = True
        else:
            st.session_state.messages.append({"role": "assistant", "content": f"Scam Probability: {prob:.2f} — ❌ GAME OVER! The detector caught you."})
            st.session_state.game_over = True
            st.session_state.won = False
        st.rerun()
else:
    if st.session_state.won:
        st.success("🎉 You fooled the detector! Hit Reset to play again.")
    else:
        st.error("❌ Game Over! The detector caught you. Hit Reset to try again.")
    
    if st.button("🔄 Reset Game"):
        st.session_state.attempt = 0
        st.session_state.messages = []
        st.session_state.game_over = False
        st.session_state.prob = None
        st.session_state.won = False
        st.rerun()
