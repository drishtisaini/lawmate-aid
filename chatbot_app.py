import streamlit as st
import requests
import speech_recognition as sr

# 🔑 Your API Key
API_KEY = "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"
MODEL = "mistralai/mixtral-8x7b-instruct"

# ✅ Allowed legal topics
ALLOWED_TOPICS = [
    "rent", "tenant", "landlord", "rental",
    "consumer", "refund", "complaint",
    "women", "dowry", "harassment",
    "workplace", "salary", "employee", "rights", "labour"
]

# ✅ Topic validation
def is_question_valid(question):
    return any(keyword in question.lower() for keyword in ALLOWED_TOPICS)

# 🎙 Voice capture
def capture_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("❌ Could not understand your voice.")
        except sr.RequestError:
            st.error("❌ Speech service error.")
    return ""

# ✅ Page setup
st.set_page_config(page_title="LawMate Legal Chatbot", layout="wide")

# ✅ Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # (role, message)
if "question_titles" not in st.session_state:
    st.session_state.question_titles = []  # Saved questions
if "temp_voice" not in st.session_state:
    st.session_state.temp_voice = ""
if "mic_status" not in st.session_state:
    st.session_state.mic_status = "🎙 Start Listening"

# 🧱 Sidebar: Saved questions with clickable links
with st.sidebar:
    st.title("📁 Saved Questions")
    if st.session_state.question_titles:
        for idx, title in enumerate(st.session_state.question_titles):
            st.markdown(f"<a href='#{idx}' style='text-decoration: none;'>👉 {title}</a>", unsafe_allow_html=True)
    else:
        st.info("No questions yet.")

# 🧾 Title & Prompt
st.title("💬 LawMate Legal Chatbot")
st.markdown("Ask about Indian law: 🏠 Rental | 🛍 Consumer | 🏢 Workplace | 👩 Women's Rights")

# 🎙 Voice and Input UI
col1, col2 = st.columns([6, 2])
with col2:
    if st.button(st.session_state.mic_status):
        st.session_state.mic_status = "🔴 Listening..."
        with st.spinner("🎧 Listening for your voice..."):
            voice_text = capture_voice()
            if voice_text:
                st.session_state.temp_voice = voice_text
                st.session_state.mic_status = "✅ Voice Captured"
            else:
                st.session_state.mic_status = "🎙 Start Listening"

    if st.session_state.temp_voice:
        st.success(f"🎤 Transcribed: {st.session_state.temp_voice}")
        st.info("Auto-submitting...")

with col1:
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("🧑‍⚖ Type or Speak Your Question:", value=st.session_state.temp_voice)
        submitted = st.form_submit_button("Send")

# 🤖 Process chat
def process_input(question):
    if not is_question_valid(question):
        ai_reply = "⚠ I only answer Indian legal questions related to rental, workplace, consumer, and women's rights."
        st.session_state.chat_history.append(("user", question))
        st.session_state.chat_history.append(("assistant", ai_reply))
        return

    with st.spinner("🤖 Thinking..."):
        try:
            messages = [{"role": "system", "content":
                "You are LawMate, a chatbot that only helps with Indian legal topics on rental, consumer complaints, workplace issues, and women's rights."
            }]
            for role, msg in st.session_state.chat_history:
                messages.append({"role": role, "content": msg})
            messages.append({"role": "user", "content": question})

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "HTTP-Referer": "http://localhost:8502",
                    "Content-Type": "application/json"
                },
                json={"model": MODEL, "messages": messages}
            )

            data = response.json()
            if "choices" in data:
                ai_reply = data["choices"][0]["message"]["content"].strip()
                st.session_state.chat_history.append(("user", question))
                st.session_state.chat_history.append(("assistant", ai_reply))

                # Save short title
                summary = " ".join(question.strip().split()[:6]) + "..."
                st.session_state.question_titles.append(summary)
            else:
                st.error("⚠ API returned an error.")
                st.error(data.get("error", "No error message."))
        except Exception as e:
            st.error(f"❌ Exception: {e}")

# ✅ Manual input
if submitted and user_input:
    st.session_state.mic_status = "🎙 Start Listening"
    process_input(user_input)
    st.session_state.temp_voice = ""

# ✅ Auto-submit voice input
if not submitted and st.session_state.mic_status == "✅ Voice Captured":
    voice_input = st.session_state.temp_voice.strip()
    if voice_input:
        st.info(f"🔁 Auto-submitting voice: {voice_input}")
        st.session_state.mic_status = "🎙 Start Listening"
        process_input(voice_input)
        st.session_state.temp_voice = ""
    else:
        st.warning("⚠ Captured voice was empty.")
        st.session_state.mic_status = "🎙 Start Listening"

# 💬 Conversation Display with Anchor IDs
st.markdown("---")
st.subheader("🧾 Conversation")

message_index = 0
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(
            f"""
            <div id="{message_index}" style='text-align: right; padding: 10px; margin: 10px 0;'>
                <div style='display: inline-block; background-color: #d1ffd6; color: #000; padding: 12px 16px; border-radius: 12px; max-width: 80%; font-size: 16px; font-family: Arial;'>
                    👤 {msg}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div id="{message_index}" style='text-align: left; padding: 10px; margin: 10px 0;'>
                <div style='display: inline-block; background-color: #f4f4f4; color: #111; padding: 12px 16px; border-radius: 12px; max-width: 80%; font-size: 16px; font-family: Arial;'>
                    🤖 {msg}
                </div>
            </div>
            """, unsafe_allow_html=True)
        message_index += 1
