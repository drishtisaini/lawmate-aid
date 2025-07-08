import warnings
import logging

# Suppress warnings and verbose logs
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("langchain").setLevel(logging.ERROR)

import streamlit as st
from extract_fields import extract_fields_from_text
from generate_document import render_template

def generate_complaint_from_message(message: str) -> str:
    try:
        if not message or len(message.strip()) == 0:
            return "❗ No input message provided."

        # Step 1: Extract fields from the message
        fields = extract_fields_from_text(message)

        # Step 2: Fallbacks for missing or invalid fields
        name = fields.get("name")
        if not name or not isinstance(name, str) or name.lower().startswith("not provided"):
            fields["name"] = "________"

        fields["product"] = fields.get("product", "________")
        fields["retailer"] = fields.get("retailer", "________")
        fields["date"] = fields.get("date", "________")
        fields["amount"] = fields.get("amount", "________")

        # Step 3: Add complaint type from session
        fields["complaint_type"] = st.session_state.get("complaint_type", "General Complaint")

        # Optional: Show fields in UI for debugging
        st.write("📋 Extracted Fields:", fields)

        # Step 4: Generate the complaint draft
        document = render_template(fields)
        return document

    except Exception as e:
        return f"⚠️ Error generating complaint: {str(e)}"

# ✅ For testing independently
if __name__ == "__main__":
    test_msg = "My name is Avni. I bought a washing machine from Vijay Sales for ₹15000 on 3rd July 2024. It stopped working within 2 days."
    result = generate_complaint_from_message(test_msg)
    print("\n📄 Complaint Draft:\n")
    print(result)








# def generate_complaint_from_message(message: str, complaint_type: str = "Consumer Complaint") -> str:
#     try:
#         print(f"📂 Complaint Type: {complaint_type}")
#         fields = extract_fields_from_text(message)

#         if fields.get("name", "").lower().startswith("not provided"):
#             fields["name"] = "________"

#         fields["complaint_type"] = complaint_type  # Pass to template if needed
#         document_text = render_template(fields)
#         return document_text

#     except Exception as e:
#         return f"⚠️ Error generating complaint: {str(e)}"


#     # existing field extraction logic...


# import warnings
# import logging

# # 🔇 Suppress deprecation warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# # 🔇 Suppress LangChain log spam
# logging.getLogger("langchain").setLevel(logging.ERROR)


# from extract_fields import extract_fields_from_text
# from generate_document import render_template

# def generate_complaint_from_message(message: str) -> str:
#     try:
#         print("🔍 Extracting fields from user message...")
#         fields = extract_fields_from_text(message)

#         # If name wasn't mentioned, prompt for it later
#         if fields.get("name", "").lower().startswith("not provided"):
#             fields["name"] = "________"

#         print("📝 Generating document using extracted fields...")
#         document_text = render_template(fields)
#         return document_text

#     except Exception as e:
#         return f"⚠️ Error generating complaint: {str(e)}"

# # Example usage
# if __name__ == "__main__":
#     msg = "My name is Avni. I bought a washing machine from Vijay Sales for ₹15000 on 3rd July 2024. It's defective."
#     doc = generate_complaint_from_message(msg)
#     print("\n📄 Complaint Draft:\n")
#     print(doc)
