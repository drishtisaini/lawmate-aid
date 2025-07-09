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

# ---------- sample legal document ---------------
def legal_samples_ui():
    st.subheader("📄 Sample Legal Documents for Learning")

    options = ["RTI Application", "Consumer Complaint", "Tenancy Notice","Harassment Complaint"]
    choice = st.selectbox("Choose a sample to view:", options)

    if choice == "RTI Application":
        st.markdown("### 📝 RTI Application Sample")
        st.code("""
To,
The Public Information Officer,
[Department Name],
[Office Address]

Subject: Request for information under the Right to Information Act, 2005

Sir/Madam,

I hereby request the following information under Section 6(1) of the RTI Act:

1. [Specify information required]
2. [Specify additional points if needed]

I have paid the application fee of Rs. 10 via [mode of payment].

Kindly provide the information within 30 days as stipulated under the RTI Act.

Thank you.

Sincerely,
[Your Name]
[Your Contact Details]
[Date]
        """, language='text')

    elif choice == "Consumer Complaint":
        st.markdown("### 📝 Consumer Complaint Sample")
        st.code("""
To,
The Consumer Dispute Redressal Forum,
[Forum Address]

Subject: Complaint against defective product/service

Sir/Madam,

I wish to lodge a complaint regarding [details of product/service], which I purchased on [date] from [seller details]. The product/service has the following issues: [list issues].

Despite contacting the seller for resolution, the issue remains unresolved.

I request your office to kindly take necessary action and provide appropriate relief.

Thank you.

Sincerely,
[Your Name]
[Your Contact Details]
[Date]
        """, language='text')

    elif choice == "Harassment Complaint":
        st.markdown("### 📝 Police Complaint for Harassment Sample")
        st.code("""To,
The Station House Officer,
[Police Station Name],
[Station Address]

Subject: Complaint against harassment

Sir/Madam,

I wish to file a complaint regarding harassment faced by me from [mention the person/situation briefly] on [date and location].

I request you to kindly register my complaint and take necessary action.

Thank you.

Sincerely,
[Your Name]
[Your Contact Details]
[Date]
    """, language='text')


    elif choice == "Tenancy Notice":
        st.markdown("### 📝 Tenancy Notice Sample")
        st.code("""
To,
[Landlord Name],
[Landlord Address]

Subject: Notice regarding tenancy

Sir/Madam,

I am writing to inform you regarding [rent increase / eviction / maintenance issues] as per our rental agreement dated [date].

[Describe your concern clearly].

Kindly take necessary action within [time period].

Thank you.

Sincerely,
[Your Name]
[Your Address]
[Date]
        """, language='text')

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
        st.markdown("---")
        legal_samples_ui()

if __name__ == "__main__":
    main()
