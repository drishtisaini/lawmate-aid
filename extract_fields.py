# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# import os
# from langchain_openai import ChatOpenAI

# from langchain.prompts import PromptTemplate
# from langchain.output_parsers import ResponseSchema, StructuredOutputParser
# from langchain.schema import HumanMessage

# # Load API setup
# os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
# os.environ["OPENAI_API_KEY"] = "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"  # Replace with actual key

# # 1. Define the fields you want to extract
# fields = [
#     ResponseSchema(name="name", description="Name of the person filing the complaint"),
#     ResponseSchema(name="product", description="Product involved in the complaint"),
#     ResponseSchema(name="retailer", description="Store or website from which the product was bought"),
#     ResponseSchema(name="date", description="Date of purchase"),
#     ResponseSchema(name="amount", description="Price paid in INR")
# ]

# # 2. Create the OutputParser
# parser = StructuredOutputParser.from_response_schemas(fields)
# format_instructions = parser.get_format_instructions()

# # 3. Create the prompt
# prompt_template = PromptTemplate(
#     template="Extract the following information from this message:\n{format_instructions}\nMessage: {user_input}",
#     input_variables=["user_input"],
#     partial_variables={"format_instructions": format_instructions}
# )

# # 4. LangChain model
# model = ChatOpenAI(
#     model_name="mistralai/mixtral-8x7b-instruct",
#     temperature=0.3
# )

# # 5. Function to extract structured data
# def extract_fields_from_text(user_input):
#     prompt = prompt_template.format(user_input=user_input)
#     response = model.invoke([HumanMessage(content=prompt)])
#     return parser.parse(response.content)

# # Example run
# if __name__ == "__main__":
#     message = "I bought a defective printer from Croma for ₹8500 on 12th June 2024."
#     fields = extract_fields_from_text(message)
#     print("\n🧾 Extracted Data:\n", fields)


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.schema import HumanMessage

# 🔐 API config
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["OPENAI_API_KEY"] = "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"  # Replace before running

# 1. Define fields to extract
fields = [
    ResponseSchema(name="name", description="Name of the person filing the complaint"),
    ResponseSchema(name="product", description="Product involved in the complaint"),
    ResponseSchema(name="retailer", description="Store or website from which the product was bought"),
    ResponseSchema(name="date", description="Date of purchase"),
    ResponseSchema(name="amount", description="Price paid in INR"),
    ResponseSchema(name="complaint_type", description="Type of complaint: Refund, Replacement, Repair, Service, or Other")
]

# 2. Output parser
parser = StructuredOutputParser.from_response_schemas(fields)
format_instructions = parser.get_format_instructions()

# 3. Prompt
prompt_template = PromptTemplate(
    template="""
Extract the following fields from this user complaint message:
{format_instructions}
Message: {user_input}
""",
    input_variables=["user_input"],
    partial_variables={"format_instructions": format_instructions}
)

# 4. Model
model = ChatOpenAI(
    model_name="mistralai/mixtral-8x7b-instruct",
    temperature=0.3
)

# 5. Function

def extract_fields_from_text(user_input):
    prompt = prompt_template.format(user_input=user_input)
    response = model.invoke([HumanMessage(content=prompt)])
    return parser.parse(response.content)

# 🧪 Test locally
if __name__ == "__main__":
    test_message = "My name is Avni. I bought a washing machine from Vijay Sales on July 3rd for ₹15000. It's not working and I want a replacement."
    data = extract_fields_from_text(test_message)
    print("\n🧾 Extracted Data:\n", data)

