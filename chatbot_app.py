import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import streamlit as st
from generate_complaint import generate_complaint_from_message
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# 🔐 API setup
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["OPENAI_API_KEY"] = "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"  # Replace with real key

# 🤖 LLM setup
llm = ChatOpenAI(model_name="mistralai/mixtral-8x7b-instruct", temperature=0.6)

# 📄 Streamlit setup
st.set_page_config(page_title="LawMate AI Chatbot", layout="centered")
st.title("⚖️ LawMate - AI Legal Assistant")

# 🗂 Complaint Type
complaint_types = [
    "Consumer Complaint", "Rent Dispute",
    "FIR / Police Complaint", "Workplace Harassment", "Refund Request"
]
selected_type = st.selectbox("Choose Complaint Type", complaint_types)
st.session_state["complaint_type"] = selected_type

# 💾 Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""
if "response_done" not in st.session_state:
    st.session_state.response_done = False
if "draft_done" not in st.session_state:
    st.session_state.draft_done = False

# 🧾 Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🧠 Chat Input
if prompt := st.chat_input("Ask a legal question..."):
    st.session_state.last_prompt = prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        st.session_state.messages.append({"role": "assistant", "content": response.content})
        st.session_state.response_done = True
        st.session_state.draft_done = False
    except Exception as e:
        st.error(f"❌ Error from assistant: {e}")
        st.stop()

# ✅ Show assistant reply if response is done
if st.session_state.response_done:
    with st.chat_message("assistant"):
        st.markdown(st.session_state.messages[-1]["content"])

        # 📄 Button to trigger complaint generation
        if st.button("📄 Generate Complaint Draft") and not st.session_state.draft_done:
            with st.spinner("Generating complaint draft..."):
                try:
                    draft = generate_complaint_from_message(st.session_state.last_prompt)
                    st.session_state["draft_text"] = draft
                    st.session_state.draft_done = True
                except Exception as e:
                    st.error(f"❌ Error generating draft: {e}")
                    st.stop()

# ✅ Show complaint draft if ready
if st.session_state.get("draft_done", False):
    with st.chat_message("assistant"):
        st.success("✅ Complaint draft generated!")
        st.markdown("### 📄 Complaint Draft:")
        st.code(st.session_state["draft_text"], language="markdown")
        st.download_button(
            label="📥 Download Draft as .txt",
            data=st.session_state["draft_text"],
            file_name="complaint_draft.txt",
            mime="text/plain"
        )














# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# import os
# import streamlit as st
# from generate_complaint import generate_complaint_from_message
# from langchain_openai import ChatOpenAI  # ✅ Updated import

# from langchain.schema import HumanMessage

# # 🔐 Set proxy OpenAI endpoint
# os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_API_KEY"] = "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"

# # 🔗 Initialize LLM
# llm = ChatOpenAI(
#     model_name="mistralai/mixtral-8x7b-instruct",
#     temperature=0.6
# )

# # 🌐 Streamlit UI setup
# st.set_page_config(page_title="LawMate AI Chatbot", layout="centered")
# st.title("⚖️ LawMate - AI Legal Assistant")

# # 🔄 Session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 🧾 Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # 🗣 User input
# if prompt := st.chat_input("Ask a legal question..."):
#     # Save user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Generate assistant reply
#     with st.chat_message("assistant"):
#         try:
#             response = llm.invoke([HumanMessage(content=prompt)])
#             st.markdown(response.content)

#             # ✅ Generate Legal Draft (only shown after response)
#             if st.button("📄 Generate Complaint Draft"):
#                 with st.spinner("Generating draft..."):
#                     draft = generate_complaint_from_message(prompt)
#                     st.success("✅ Draft generated!")
#                     st.markdown("### 📄 Complaint Draft:")
#                     st.code(draft, language="markdown")


#         except Exception as e:
#             st.error(f"❌ Error occurred: {e}")

#     st.session_state.messages.append({"role": "assistant", "content": response.content})









# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# import os
# import streamlit as st
# from generate_complaint import generate_complaint_from_message
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage

# # 🛡️ Set up OpenRouter LLM endpoint
# os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_API_KEY"] = "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"  # Replace with your actual OpenRouter key

# # 🤖 Load the language model
# llm = ChatOpenAI(
#     model_name="mistralai/mixtral-8x7b-instruct",
#     temperature=0.6
# )

# # 🖥️ Setup Streamlit UI
# st.set_page_config(page_title="LawMate AI Chatbot", layout="centered")
# st.title("⚖️ LawMate - AI Legal Assistant")

# # 🔄 Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 💬 Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # ✍️ Handle user input
# if prompt := st.chat_input("Ask a legal question..."):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         try:
#             response = llm.invoke([HumanMessage(content=prompt)])
#             st.markdown(response.content)
#         except Exception as e:
#             response = None
#             st.error(f"❌ Error: {e}")

#     if response:
#         st.session_state.messages.append({"role": "assistant", "content": response.content})
#         st.session_state.last_prompt = prompt  # ✅ Save last prompt for later draft generation

# # 📄 Enable draft generation after successful interaction
# if "last_prompt" in st.session_state:
#     if st.button("📄 Generate Complaint Draft"):
#         with st.spinner("Generating draft..."):
#             try:
#                 draft = generate_complaint_from_message(st.session_state.last_prompt)
#                 st.success("✅ Draft generated!")
#                 st.markdown("### 📄 Complaint Draft:")
#                 st.code(draft, language="markdown")
#             except Exception as e:
#                 st.error(f"⚠️ Error generating complaint: {e}")












# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# import os
# import streamlit as st
# from generate_complaint import generate_complaint_from_message
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage

# # 🔐 API setup
# os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_API_KEY"] = "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"  # Replace with valid key

# # 🤖 Initialize LangChain LLM
# llm = ChatOpenAI(
#     model_name="mistralai/mixtral-8x7b-instruct",
#     temperature=0.6
# )

# # 🌐 Streamlit page config
# st.set_page_config(page_title="LawMate AI Chatbot", layout="centered")
# st.title("⚖️ LawMate - AI Legal Assistant")

# # 🔄 Maintain session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "last_prompt" not in st.session_state:
#     st.session_state.last_prompt = ""

# if "show_generate_button" not in st.session_state:
#     st.session_state.show_generate_button = False

# # 📜 Show chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # 🧠 Get user input
# if prompt := st.chat_input("Ask a legal question..."):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.session_state.last_prompt = prompt
#     st.session_state.show_generate_button = False

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # 🤖 Assistant response
#     with st.chat_message("assistant"):
#         try:
#             response = llm.invoke([HumanMessage(content=prompt)])
#             st.markdown(response.content)
#             st.session_state.show_generate_button = True
#         except Exception as e:
#             st.error(f"❌ Error: {e}")
#             response = None

#     if response:
#         st.session_state.messages.append({"role": "assistant", "content": response.content})

# # 📝 Draft Generator Button
# if st.session_state.show_generate_button and st.session_state.last_prompt:
#     if st.button("\ud83d\udcc4 Generate Complaint Draft"):
#         with st.spinner("Generating complaint draft..."):
#             try:
#                 draft = generate_complaint_from_message(st.session_state.last_prompt)
#                 st.success("\u2705 Draft generated!")
#                 st.markdown("### \ud83d\udcc4 Complaint Draft:")
#                 st.code(draft, language="markdown")
#             except Exception as e:
#                 st.error(f"\u274c Error while generating draft: {e}")





# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# import os
# import streamlit as st
# from generate_complaint import generate_complaint_from_message
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage

# # Set proxy endpoint
# os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_API_KEY"] = "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"  # 🔁 Replace with your actual key

# # Initialize model
# llm = ChatOpenAI(
#     model_name="mistralai/mixtral-8x7b-instruct",
#     temperature=0.6
# )

# # Streamlit page config
# st.set_page_config(page_title="LawMate AI Chatbot", layout="centered")
# st.title("⚖️ LawMate - AI Legal Assistant")

# # Setup session state for chat
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "last_prompt" not in st.session_state:
#     st.session_state.last_prompt = ""

# # Display past messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Capture new input
# if prompt := st.chat_input("Ask a legal question..."):
#     st.session_state.last_prompt = prompt
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         try:
#             response = llm.invoke([HumanMessage(content=prompt)])
#             st.markdown(response.content)
#             st.session_state.messages.append({"role": "assistant", "content": response.content})
#         except Exception as e:
#             st.error(f"❌ Chat Error: {e}")

# # Complaint Draft Generation (shown always for now)
# if st.session_state.last_prompt:
#     if st.button("📄 Generate Complaint Draft"):
#         with st.spinner("Generating complaint draft..."):
#             try:
#                 draft = generate_complaint_from_message(st.session_state.last_prompt)
#                 st.success("✅ Complaint draft generated:")
#                 st.code(draft, language="markdown")
#             except Exception as e:
#                 st.error(f"❌ Draft generation failed: {e}")





# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# import os
# import streamlit as st
# from generate_complaint import generate_complaint_from_message
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage

# # API Setup
# os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_API_KEY"] = "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"  # Replace with your actual key

# # Initialize the LLM
# llm = ChatOpenAI(
#     model_name="mistralai/mixtral-8x7b-instruct",
#     temperature=0.6
# )

# # Streamlit config
# st.set_page_config(page_title="LawMate AI Chatbot", layout="centered")
# st.title("⚖️ LawMate - AI Legal Assistant")



# # Session state setup
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "last_prompt" not in st.session_state:
#     st.session_state.last_prompt = ""
# if "show_draft_button" not in st.session_state:
#     st.session_state.show_draft_button = False
# if "draft_generated" not in st.session_state:
#     st.session_state.draft_generated = False

# # Display previous messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Handle new prompt
# if prompt := st.chat_input("Ask a legal question..."):
#     st.session_state.last_prompt = prompt
#     st.session_state.show_draft_button = False
#     st.session_state.draft_generated = False

#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         try:
#             response = llm.invoke([HumanMessage(content=prompt)])
#             st.markdown(response.content)
#             st.session_state.messages.append({"role": "assistant", "content": response.content})
#             st.session_state.show_draft_button = True
#         except Exception as e:
#             st.error(f"❌ Chat Error: {e}")

# # Complaint Draft Button (if assistant already replied)
# if st.session_state.show_draft_button and not st.session_state.draft_generated:
#     if st.button("📄 Generate Complaint Draft"):
#         with st.spinner("Generating complaint draft..."):
#             try:
#                 draft = generate_complaint_from_message(st.session_state.last_prompt)
#                 st.session_state.draft_generated = True
#                 st.session_state.messages.append({"role": "assistant", "content": draft})
#                 with st.chat_message("assistant"):
#                     st.success("✅ Complaint draft generated!")
#                     st.markdown(draft)
#             except Exception as e:
#                 st.error(f"❌ Error generating draft: {e}")






# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# import os
# import streamlit as st
# from generate_complaint import generate_complaint_from_message
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage

# # 🔐 Set OpenRouter credentials
# os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_API_KEY"] = "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"  # Replace with your OpenRouter key

# # 🔗 Initialize LLM
# llm = ChatOpenAI(
#     model_name="mistralai/mixtral-8x7b-instruct",
#     temperature=0.6
# )

# # 🌐 Streamlit UI config
# st.set_page_config(page_title="LawMate AI Chatbot", layout="centered")
# st.title("⚖️ LawMate - AI Legal Assistant")

# # 🗂 Complaint Type Selector
# complaint_types = [
#     "Consumer Complaint",
#     "Rent Dispute",
#     "FIR / Police Complaint",
#     "Workplace Harassment",
#     "Refund Request"
# ]

# selected_type = st.selectbox("Choose Complaint Type", complaint_types)
# st.session_state["complaint_type"] = selected_type  # ✅ Store in session state

# # 🔄 Session state for chat
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 🧾 Display previous messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # 🧠 Main chat interaction
# if prompt := st.chat_input("Ask a legal question..."):
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         try:
#             response = llm.invoke([HumanMessage(content=prompt)])
#             st.markdown(response.content)

#             # ✅ Complaint Draft Generation
#             if st.button("📄 Generate Complaint Draft"):
#                 with st.spinner("Generating draft..."):
#                     try:
#                         draft = generate_complaint_from_message(prompt)
#                         st.success("✅ Draft generated!")
#                         st.markdown("### 📄 Complaint Draft:")
#                         st.code(draft, language="markdown")
#                     except Exception as e:
#                         st.error(f"❌ Error generating draft: {e}")

#         except Exception as e:
#             st.error(f"❌ Error: {e}")

#     st.session_state.messages.append({"role": "assistant", "content": response.content})



