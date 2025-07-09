from docxtpl import DocxTemplate
import os

def generate_legal_notice(user_data):
    doc = DocxTemplate("templates/legal_notice_template.docx")
    doc.render(user_data)
    
    output_dir = "generated_docs"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{user_data['sender_name'].replace(' ', '_')}_legal_notice.docx"
    file_path = os.path.join(output_dir, filename)
    doc.save(file_path)
    return file_path
