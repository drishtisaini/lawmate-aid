import streamlit as st
import json
import datetime
import random
import os
from docxtpl import DocxTemplate

# Page settings
st.set_page_config(page_title="LawMate: AI Legal Assistant", layout="centered", page_icon="⚖️")

# Sidebar
st.sidebar.title("About LawMate")
st.sidebar.info(
    "LawMate is an AI-powered legal FAQ assistant for basic Indian legal awareness.\n\n"
    "It helps you generate legal notices and find answers to common legal questions quickly.\n\n"
    "**Disclaimer:** This tool provides general legal information and is not a substitute for professional legal advice."
)

# Load FAQs from JSON
def load_faqs(file_path='law_faqs.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading FAQs: {e}")
        return []

# Show random FAQ
def show_random_faq(faqs):
    if faqs:
        faq = random.choice(faqs)
        st.info(f"**Category:** {faq['category'].capitalize()}\n\n**Q:** {faq['question']}\n\n**A:** {faq['answer']}")
    else:
        st.warning("No FAQs available.")

# FAQ Search UI
def faq_search_ui(faqs):
    st.subheader("🔍 Search Legal FAQs")

    st.markdown("**Popular Keywords:**")
    keywords = ["rent", "women", "cyber", "workplace", "RTI", "property"]
    cols = st.columns(len(keywords))
    keyword_clicked = ""

    for i, word in enumerate(keywords):
        if cols[i].button(word):
            keyword_clicked = word

    query = keyword_clicked or st.text_input("Enter a keyword (e.g., rent, consumer, workplace):")

    if query:
        results = [faq for faq in faqs if query.lower() in faq['question'].lower() or query.lower() in faq['answer'].lower()]
        if results:
            for i, faq in enumerate(results, 1):
                with st.expander(f"{i}. {faq['question']}"):
                    st.write(f"**Category:** {faq['category'].capitalize()}\n\n{faq['answer']}")
        else:
            st.warning("No matching FAQs found.")

# Document Generator (Drishti)
def generate_legal_notice(user_data):
    template_path = "templates/legal_notice_template.docx"
    doc = DocxTemplate(template_path)
    doc.render(user_data)

    output_dir = "generated_docs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{user_data['sender_name'].replace(' ', '_')}_legal_notice.docx")
    doc.save(output_path)

    return output_path

# ----------------- MAIN APP -------------------

def main():
     
    tab1, tab2 = st.tabs(["📄 Generate Legal Document", "💬 Search Legal FAQs"])

    with tab1:
        st.header("📄 Generate Legal Notice")
        with st.form("notice_form"):
            sender_name = st.text_input("Your Full Name")
            sender_address = st.text_area("Your Address")
            recipient_name = st.text_input("Recipient's Name")
            recipient_address = st.text_area("Recipient's Address")
            subject = st.text_input("Subject of the Notice")
            issue_description = st.text_area("Describe the Issue")
            notice_period = st.number_input("Notice Period (days)", min_value=1, max_value=60, value=15)
            date = st.date_input("Date", value=datetime.date.today())
            submitted = st.form_submit_button("Generate Document")

        if submitted:
            user_data = {
                "sender_name": sender_name,
                "sender_address": sender_address,
                "recipient_name": recipient_name,
                "recipient_address": recipient_address,
                "subject": subject,
                "issue_description": issue_description,
                "notice_period": notice_period,
                "date": date.strftime("%B %d, %Y")
            }
            file_path = generate_legal_notice(user_data)
            st.success("✅ Legal notice created successfully!")
            with open(file_path, "rb") as file:
                st.download_button(
                    label="📥 Download Your Legal Notice",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

    with tab2:
        st.header("💬 Legal FAQs")
        faqs = load_faqs()
        st.markdown("---")
        if st.button("🎲 Show Random FAQ"):
            show_random_faq(faqs)
        st.markdown("---")
        faq_search_ui(faqs)

if __name__ == "__main__":
    main()
