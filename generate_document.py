# from jinja2 import Template

# def render_template(data: dict, template_path: str = "templates/consumer_template.txt") -> str:
#     with open(template_path, "r", encoding="utf-8") as file:
#         template = Template(file.read())
#     return template.render(**data)

# # Example usage
# if __name__ == "__main__":
#     filled_data = {
#         "name": "Avni",
#         "product": "Laptop",
#         "retailer": "Flipkart",
#         "date": "2nd January 2024",
#         "amount": "60000"
#     }

#     document = render_template(filled_data)
#     print("\n📄 Generated Document:\n")
#     print(document)

from jinja2 import Template

# ⬇️ Default consumer complaint template
DEFAULT_TEMPLATE = """
To,
The Consumer Dispute Redressal Commission

Subject: {{ complaint_type }} regarding {{ product }} purchased from {{ retailer }} on {{ date }} for ₹{{ amount }}

Dear Sir/Madam,

I, {{ name }}, purchased a {{ product }} from {{ retailer }} on {{ date }} for ₹{{ amount }}. I am filing this complaint due to a {{ complaint_type.lower() }} issue with the product/service. I have already attempted to resolve the issue with the seller but received no satisfactory resolution.

I request you to kindly intervene and take appropriate action under applicable consumer protection laws.

Sincerely,
{{ name }}
"""

# 🧩 Function to render from dictionary using either default or external template

def render_template(data: dict, template_path: str = None) -> str:
    try:
        if template_path:
            with open(template_path, "r", encoding="utf-8") as file:
                template = Template(file.read())
        else:
            template = Template(DEFAULT_TEMPLATE)
        return template.render(**data)
    except Exception as e:
        return f"Error rendering document: {str(e)}"

# 🧪 Test
if __name__ == "__main__":
    fields = {
        "name": "Avni",
        "product": "laptop",
        "retailer": "Flipkart",
        "date": "June 12, 2024",
        "amount": "45000",
        "complaint_type": "Refund Request"
    }
    print(render_template(fields))
