import streamlit as st
import requests

# ✅ Your OpenRouter API Key
API_KEY = "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"

# ✅ Model name
MODEL = "mistralai/mixtral-8x7b-instruct"

# Topics we allow
ALLOWED_TOPICS = ["rent", "tenant", "landlord", "rental", "consumer", "refund", "complaint",
                  "women", "dowry", "harassment", "workplace", "salary", "employee", "rights", "labour"]

# Function to check if the input is related
def is_question_valid(user_question):
    lower_q = user_question.lower()
    return any(keyword in lower_q for keyword in ALLOWED_TOPICS)

# Streamlit setup
st.set_page_config(page_title="LawMate Chatbot (Topic Restricted)", layout="centered")
st.title("💬 LawMate Legal Chatbot (Free AI)")
st.markdown("Ask only about Indian law topics: 🏠 Rental | 🛍️ Consumer | 🏢 Workplace | 👩 Women's Rights")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
user_input = st.text_input("🧑‍⚖️ Type your legal question:")

if user_input:
    if not is_question_valid(user_input):
        ai_reply = "⚠️ I'm sorry. I'm only allowed to answer questions about rental, consumer, workplace, and women's rights issues in India. Please ask something related to those topics."
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", ai_reply))
    else:
        with st.spinner("🤖 Thinking..."):
            try:
                # System instruction
                messages = [{
                    "role": "system",
                    "content": (
                        "You are a legal chatbot named LawMate. You only help with rental issues, consumer complaints, "
                        "workplace rights, and women's rights in India. Stay focused on these topics only."
                    )
                }]

                # Add history
                for role, msg in st.session_state.chat_history:
                    messages.append({"role": role, "content": msg})

                # Add new question
                messages.append({"role": "user", "content": user_input})

                # Call OpenRouter API
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "HTTP-Referer": "https://chat.openai.com/",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": MODEL,
                        "messages": messages
                    },
                )

                data = response.json()

                if "choices" in data:
                    ai_reply = data["choices"][0]["message"]["content"].strip()
                    st.session_state.chat_history.append(("user", user_input))
                    st.session_state.chat_history.append(("assistant", ai_reply))
                else:
                    st.error("⚠️ OpenRouter returned an error.")
                    st.error(data.get("error", "No error message provided."))

            except Exception as e:
                st.error(f"❌ Exception: {e}")

# Show chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("🕘 Chat History")
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**👤 You:** {msg}")
        else:
            st.markdown(f"**🤖 LawMate AI:** {msg}")
