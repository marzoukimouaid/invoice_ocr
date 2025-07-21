import asyncio
import sys
import os
from typing import List

from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pdf2image import convert_from_bytes
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from tesseract_based_ocr.tesseract_ocr import tesseract_ocr
from llm_based_ocr.llm_ocr import llm_ocr
from sqlite.manage_db import get_session, DBinvoice, Invoice
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

    try:
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

    except Exception as e:
        return HTTPException(status_code=4400, detail="Something went wrong when extracting data")


@app.post("/llm/extract")
async def extract_data_llm(file: UploadFile = File(...)):
    contents = await file.read()
    file_ext = file.filename.split('.')[-1].lower()
    result = []

    try:
        if file_ext == 'pdf':
            images = await asyncio.to_thread(lambda: convert_from_bytes(contents, dpi=100))
            for i, img in enumerate(images):
                img = img.resize((img.width // 2, img.height // 2))
                image_path = os.path.join(IMAGEDIR, f"{uuid.uuid4()}.jpg")
                img.save(image_path, "JPEG")
                ocr_result = llm_ocr(image_path)
                result.append(ocr_result)
                os.remove(image_path)

        else:
            image_path = os.path.join(IMAGEDIR, f"{uuid.uuid4()}.jpg")
            with open(image_path, "wb") as f:
                f.write(contents)
            result = [llm_ocr(image_path)]
            os.remove(image_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong when extracting data")




@app.get("/invoices/", response_model=list[Invoice])
def read_invoices(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    heroes = session.query(DBinvoice).offset(skip).limit(limit).all()
    return heroes


@app.delete("/invoices/{invoice_id}", response_model=Invoice)
def delete_hero(invoice_id: int, session: Session = Depends(get_session)):
    hero = session.query(DBinvoice).filter(DBinvoice.id == invoice_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Invoice not found")

    session.delete(hero)
    session.commit()
    return hero


@app.post("/invoices/", response_model=List[Invoice])
def create_invoices(
    invoices: List[Invoice] = Body(...),
    session: Session = Depends(get_session)
):
    db_invoices = []

    try:
        for invoice in invoices:
            db_invoice = DBinvoice(
                invoice_number=invoice.invoice_number,
                invoice_date=invoice.invoice_date,
                amount=invoice.amount
            )
            session.add(db_invoice)
            db_invoices.append(db_invoice)

        session.commit()
        for db_invoice in db_invoices:
            session.refresh(db_invoice)

        return db_invoices
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="Invoice already exists or violates DB constraints.")

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"database error {e}")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Unexpected error {e}")






