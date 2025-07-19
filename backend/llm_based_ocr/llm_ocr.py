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


def llm_ocr(img, instructions):
    model_names = [i['model'] for i in ollama.list()['models']]
    if instructions:
        content = f"Extract only the following data from the image: {instructions}. Return only valid JSON without markdown."
    else:
        content = """Extract all useful data from this invoice image and return it in valid JSON format. Do not include any explanation or markdown."""

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
    return json.loads(cleaned_response)
    # if match:
    #     json_str = match.group(1)
    #     try:
    #         return json.loads(json_str)
    #     except json.JSONDecodeError as e:
    #         print("JSON decode error:", e)
    # else:
    #     print("No valid JSON block found.")






