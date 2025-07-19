import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, File, UploadFile
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
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    # Save uploaded image
    file_path = os.path.join(IMAGEDIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Perform OCR
    result = tesseract_ocr(file_path)

    # Delete Image
    os.remove(file_path)
    return result


@app.post("/llm/extract")
async def extract_data_llm(file: UploadFile = File(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    # Save uploaded image
    file_path = os.path.join(IMAGEDIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Perform OCR
    result = llm_ocr(file_path)

    # Delete Image
    os.remove(file_path)
    return result


