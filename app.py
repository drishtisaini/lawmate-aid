# LawMate: Clean, Demo-Ready Streamlit App

import streamlit as st
import json
import random

# Page configuration
st.set_page_config(page_title="LawMate :AI Legal Assistant", page_icon="⚖️")

# Sidebar About section
st.sidebar.title("About LawMate")
st.sidebar.info(
    "LawMate is a AI-powered legal FAQ assistant for basic Indian legal awareness.\n"
    "It helps you find answers to common legal questions quickly.\n\n"
    "**Disclaimer:** This tool provides general legal information and is not a substitute for professional legal advice."
)

# ---------- Load legal_faqs.json [ frequently asked questions] ----------
def load_faqs(file_path='data/legal_faqs.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            faqs = json.load(f)
        return faqs
    except Exception as e:
        st.error(f"Error loading FAQs: {e}")
        return []

# ---------- Display a random FAQ ----------
def show_random_faq(faqs):
    if faqs:
        faq = random.choice(faqs)
        st.info(f"**Category:** {faq['category'].capitalize()}\n\n**Q:** {faq['question']}\n\n**A:** {faq['answer']}")
    else:
        st.warning("No FAQs available.")

# ---------- FAQ search UI with Keyword Chips (No Category Filter) ----------
def faq_search_ui(faqs):
    st.subheader("🔍 Search Legal FAQs")

    # Popular keyword suggestion chips
    st.markdown("**Popular Keywords:**")
    keywords = ["rent", "consumer", "women", "cyber", "workplace", "RTI", "property"]
    cols = st.columns(len(keywords))
    keyword_clicked = ""
    for i, word in enumerate(keywords):
        if cols[i].button(word):
            keyword_clicked = word

    # Search bar
    if keyword_clicked:
        query = keyword_clicked
        st.info(f"Showing results for **{query}**")
    else:
        query = st.text_input("Enter a keyword (e.g., rent, consumer, workplace):")

    # Filter logic without category filter
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

# ---------- Main integration ----------
def main():
    st.title("⚖️ LawMate: Legal FAQ Explorer")
    faqs = load_faqs()

    st.markdown("---")
    if st.button("Show Random FAQ"):
        show_random_faq(faqs)
    
    st.markdown("---")
    faq_search_ui(faqs)

    st.markdown("---")
    legal_samples_ui()

if __name__ == "__main__":
    main()