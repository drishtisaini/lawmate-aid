🧑‍⚖ LawMate - Your Legal Assistant Chatbot
LawMate is an AI-powered legal assistant designed to help users generate legal notices and get answers to common legal questions. It leverages NLP, customizable templates, and TTS (Text-to-Speech) for an intuitive and accessible legal support experience.

🚀 Features
💬 AI Chatbot Interface: Friendly legal chatbot for FAQs and guidance

📄 Auto Legal Notice Generation: Generates formatted legal notices (e.g., property, employment, etc.) using templates

🧩 Modular Codebase: Easy to extend with new templates and legal topics

📂 Project Structure
bash
Copy
Edit
lawmate-aid/
│
├──main_ app.py                  # Streamlit app entry point
├── chatbot_app.py               # Chatbot interface
├── document_gen/
│   ├── generator.py             # Legal notice generator logic
│   └── .streamlit/config.toml   # Theme configuration
├── templates/                   # DOCX templates for legal notices
├── generated_docs/              # Output folder for generated notices
├── law_faqs.json                # Predefined legal FAQs
├── lawt.html                    # Landing or static HTML page
├── law.webp                     # App logo/image
├── README.md                    # You're here!
└── requirements.txt             # Python dependencies
└──pages
            └──document generator
              └──faqs 
⚙ Installation
bash
Copy
Edit
git clone https://github.com/drishtisaini/lawmate-aid.git

Launching methods:-
cd lawmate-aid
pip install -r requirements.txt
▶ Running the App
bash
Copy
Edit
streamlit run app.py
Or for chatbot directly:

bash
Copy
Edit
streamlit run chatbot_app.py
🧠 Tech Stack
HTML for frontend 
Streamlit for the web interface
Python for backend logic
DocxTemplate for generating DOCX documents
JSON for storing legal FAQs

###🌐live demo
Try it now :[https://chhavic4004.github.io/lawmate_new/]

🛡 Disclaimer
LawMate is intended for educational and assistance purposes only. It is not a substitute for professional legal advice. Consult a certified lawyer for real-world legal matters.
