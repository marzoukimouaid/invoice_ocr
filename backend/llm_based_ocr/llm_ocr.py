import ollama
import re
import json



IMG_PATH = 'img.png'
BASE_MODEL = 'llava:latest'
CUSTOM_MODEL = 'ocrLLM'


def create_custom_model():
    system_prompt = """"
            SYSTEM You are a an experct at OCR and extracting data from image.
            Your job is help the user extract data from images to json
            """
    ollama.create(
        model=CUSTOM_MODEL,
        from_=BASE_MODEL,
        system=system_prompt,
        parameters={
            'temperature': 0
        }
        )


def llm_ocr(img):
    model_names = [i['model'] for i in ollama.list()['models']]
    if CUSTOM_MODEL not in model_names:
        create_custom_model()

    response = ollama.chat(
        model=CUSTOM_MODEL,
        messages=[{
            'role': 'user',
            'content':
                'given this image your task is to extract all the details of this invoice that are useful in json format.'
                'include only the json data in your response so that your response is automatically parsable.'
                'dont include any extra text'

            ,
            'images': [img]
        }]
    )

    cleaned_response = response['message']['content'].strip()
    match = re.search(r"```json\s*(\{.*?\})\s*```", cleaned_response, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
    else:
        print("No valid JSON block found.")






