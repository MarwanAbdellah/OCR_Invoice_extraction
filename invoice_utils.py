from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import json
import base64
import matplotlib.pyplot as plt
from PIL import Image
import os

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

# Image encoder
def read_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to read image: {e}")

# Define output structure
class InvoiceItem(BaseModel):
    item_name: str = Field(..., description="Name of the item")
    quantity: int = Field(..., description="Quantity of the item")
    taxes: Optional[float] = Field(..., description="Taxes applied to the item")
    total_price: float = Field(..., description="Total price for the item")

class InvoiceData(BaseModel):
    buyer_name: str = Field(..., description="Name of the buyer")
    invoice_date : str = Field(..., description="Date of the invoice")
    items: List[InvoiceItem] = Field(..., description="List of items in the invoice")

parser = PydanticOutputParser(pydantic_object=InvoiceData)

# Dummy few-shot setup (to be customized or loaded externally)
few_shot_prompt = FewShotChatMessagePromptTemplate.from_examples(
    examples=[],  # Add few-shot examples here if needed
    example_prompt=None,  # Define if using
    input_variables=[]
)

def process_invoice(image_path=None, invoice_text=None):
    messages = [
        SystemMessage(
            content=f"Extract the data from this invoice. Follow this output format: {parser.get_format_instructions()}"
        )
    ]

    few_shot_prompt_messages = few_shot_prompt.invoke({}).to_messages()
    messages.extend(few_shot_prompt_messages)

    if image_path:
        image_data = read_image_base64(image_path)
        if not image_data:
            raise ValueError("Image could not be read or encoded.")

        messages.append(HumanMessage(
            content=[{
                "type": "image",
                "source_type": "base64",
                "data": image_data,
                "mime_type": "image/jpeg",
            }]))

    if invoice_text:
        messages.append(HumanMessage(content=invoice_text))

    output = llm.invoke(messages)
    return output

def format_invoice_data(output):
    try:
        raw_json_string = output.content.strip("```json\n").strip()
        invoice_data = json.loads(raw_json_string)

        formatted_output = f"""Buyer: {invoice_data['buyer_name']}
Invoice Date: {invoice_data['invoice_date']}

Items:"""

        for item in invoice_data['items']:
            qty = item.get("quantity", 1) or 1
            tax = item.get("taxes")
            tax_display = f"{tax * 100:.2f}%" if tax is not None else "N/A"
            unit_price = item['total_price'] / qty

            formatted_output += f"""
- Item: {item['item_name']}
  Quantity: {qty}
  Unit Price: ${unit_price:.2f}
  Tax: {tax_display}
  Total Price: ${item['total_price']:.2f}
"""

        return formatted_output

    except Exception as e:
        return f"Error processing output: {str(e)}"

def plot_tax_per_item(formatted_output):
    try:
        lines = formatted_output.strip().split('\n')
        items = []
        current_item = {}

        for line in lines:
            line = line.strip()
            if line.startswith('- Item:'):
                if current_item:
                    items.append(current_item)
                current_item = {}
                current_item['item_name'] = line.split('Item:')[1].strip()
            elif 'Tax:' in line and '%' in line:
                tax_value = float(line.split('Tax:')[1].strip().replace('%', ''))
                current_item['taxes'] = tax_value

        if current_item:
            items.append(current_item)

        names = []
        taxes = []

        for item in items:
            name = item.get("item_name", "Unknown")
            tax = item.get("taxes")
            if isinstance(tax, (int, float)):
                names.append(name)
                taxes.append(tax)
            else:
                print(f"Skipping item without valid tax: {name}")

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(names, taxes, color="skyblue")
        ax.set_xlabel("Item")
        ax.set_ylabel("Tax Percentage")
        ax.set_title("Tax per Invoice Item")
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45)
        fig.tight_layout()

        return fig

    except Exception as e:
        raise ValueError(f"Error processing data: {str(e)}\nMake sure the formatted output contains valid item and tax information.")
