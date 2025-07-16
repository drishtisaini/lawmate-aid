import streamlit as st
import datetime
import os
from docxtpl import DocxTemplate

# Make sure your template path is correct relative to where you run your app (lawmate_app folder)
# The template path should be 'templates/legal_notice_template.docx'
# Ensure 'generated_docs' folder is created in the same level as main_app.py
def generate_legal_notice(user_data):
    template_path = "templates/legal_notice_template.docx"
    doc = DocxTemplate(template_path)
    doc.render(user_data)

    output_dir = "generated_docs"
    os.makedirs(output_dir, exist_ok=True) # Ensures the folder exists
    output_path = os.path.join(output_dir, f"{user_data['sender_name'].replace(' ', '_')}_legal_notice.docx")
    doc.save(output_path)
    return output_path

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