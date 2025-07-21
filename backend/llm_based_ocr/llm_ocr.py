import ollama
import re
import json


BASE_MODEL = 'llama3.2-vision:latest'
CUSTOM_MODEL = 'ocrLLM'


def create_custom_model():
    system_prompt = """You are an expert in extracting structured data from images, especially invoices and receipts. Your goal is to return only the relevant information in clean, valid JSON format, without extra explanation or markdown."""

    ollama.create(
        model=CUSTOM_MODEL,
        from_=BASE_MODEL,
        system=system_prompt,

        )


def llm_ocr(img):
    model_names = [i['model'] for i in ollama.list()['models']]
    content = """
        From this invoice image, extract only the following fields:
    
    - invoice_number: the invoice number (string or alphanumeric identifier)
    - invoice_date: the date of the invoice in format YYYY-MM-DD
    - amount: the total amount to be paid as a number (no currency symbols)
    
    Return the output as raw JSON without markdown or explanation, like this:
    
    {
      "invoice_number": "INV-00123",
      "invoice_date": "2023-12-15",
      "amount": 1450.75
    }
    """

    if CUSTOM_MODEL not in model_names:
        create_custom_model()

    response = ollama.chat(
        model=BASE_MODEL,
        messages=[{
            'role': 'user',
            'content': content
            ,
            'images': [img]
        }]
    )

    cleaned_response = response['message']['content'].strip()
    match = re.search(r"```json\s*(\{.*?\})\s*```", cleaned_response, re.DOTALL)
    print(cleaned_response)
    try:
        return json.loads(cleaned_response)
    except:
        return json.loads("Error during extraction")
    # if match:
    #     json_str = match.group(1)
    #     try:
    #         return json.loads(json_str)
    #     except json.JSONDecodeError as e:
    #         print("JSON decode error:", e)
    # else:
    #     print("No valid JSON block found.")






