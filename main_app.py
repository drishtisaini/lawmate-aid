import streamlit as st

# Page settings (these apply to the whole app)
st.set_page_config(page_title="LawMate: AI Legal Assistant", layout="centered", page_icon="⚖️")

# Sidebar (this will appear on all pages by default)
st.sidebar.title("About LawMate")
st.sidebar.info(
    "LawMate is an AI-powered legal FAQ assistant for basic Indian legal awareness.\n\n"
    "It helps you generate legal notices and find answers to common legal questions quickly.\n\n"
    "**Disclaimer:** This tool provides general legal information and is not a substitute for professional legal advice."
)

# Main content for the starting page
st.title("Welcome to LawMate: Your AI Legal Assistant ⚖️")
st.write("Navigate through the sections using the sidebar or the buttons below.")

st.markdown("---")

st.subheader("Quick Access:")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Generate Legal Notices")
    st.write("Create professional legal documents quickly.")
    if st.button("Go to Document Generator 📝", use_container_width=True):
        # This is where st.switch_page() comes in!
        st.switch_page("pages/1_document_generator.py")

with col2:
    st.markdown("#### Search Legal FAQs")
    st.write("Find answers to common legal questions.")
    if st.button("Go to FAQ Search 💬", use_container_width=True):
        # This is where st.switch_page() comes in!
        st.switch_page("pages/2_faq_search.py")

st.markdown("---")
st.info("Remember: This tool provides general information and is not a substitute for professional legal advice.")