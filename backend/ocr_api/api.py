import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pdf2image import convert_from_bytes
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from tesseract_based_ocr.tesseract_ocr import tesseract_ocr
from llm_based_ocr.llm_ocr import llm_ocr
import uuid


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGEDIR = os.path.join(BASE_DIR, '..', 'images')
os.makedirs(IMAGEDIR, exist_ok=True)

app = FastAPI()

# Used to allow the React app in local, Change accordingly when deploying
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/tesseract/extract")
async def extract_data_tesseract(file: UploadFile = File(...)):
    contents = await file.read()
    file_ext = file.filename.split('.')[-1].lower()
    result = {}

    if file_ext == 'pdf':

        images = convert_from_bytes(contents)
        for i, img in enumerate(images):
            image_path = os.path.join(IMAGEDIR, f"{uuid.uuid4()}.jpg")
            img.save(image_path, "JPEG")
            ocr_result = tesseract_ocr(image_path)
            result[f"page{i}"] = ocr_result
            os.remove(image_path)

    else:
        image_path = os.path.join(IMAGEDIR, f"{uuid.uuid4()}.jpg")
        with open(image_path, "wb") as f:
            f.write(contents)
        result = tesseract_ocr(image_path)
        os.remove(image_path)

    return result


@app.post("/llm/extract")
async def extract_data_llm(file: UploadFile = File(...), instructions: str = Form(None)):
    contents = await file.read()
    file_ext = file.filename.split('.')[-1].lower()
    result = {}

    if file_ext == 'pdf':
        images = convert_from_bytes(contents)
        for i, img in enumerate(images):
            image_path = os.path.join(IMAGEDIR, f"{uuid.uuid4()}.jpg")
            img.save(image_path, "JPEG")
            ocr_result = llm_ocr(image_path, instructions)
            result[f"page{i}"] = ocr_result
            os.remove(image_path)

    else:
        image_path = os.path.join(IMAGEDIR, f"{uuid.uuid4()}.jpg")
        with open(image_path, "wb") as f:
            f.write(contents)
        result = llm_ocr(image_path, instructions)
        os.remove(image_path)

    return result


