from . import preprocessing
import pytesseract
import re
import spacy


def tesseract_ocr(img):
    return text_to_json(image_to_text(img))


def image_to_text(filename):
    img = preprocessing.open_image(filename)
    img = preprocessing.preprocess_image(img)

    conf = r'--oem 3 --psm 11'
    ocr_result = pytesseract.image_to_string(img, config=conf)

    return ocr_result


def text_to_json(ocr_result):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(ocr_result)

    invoice_number = None
    invoice_date = None
    amount = None

    full_text = doc.text

    inv_match = re.search(r"(?:INV[-\s]?|#)?(\w{3,}-?\d+)", full_text, re.IGNORECASE)
    if inv_match:
        invoice_number = inv_match.group(1)

    date_match = re.search(r"\b(20\d{2}[-/\.](0?[1-9]|1[0-2])[-/\.](0?[1-9]|[12][0-9]|3[01]))\b", full_text)
    if date_match:
        invoice_date = date_match.group(1)

    amount_matches = re.findall(r"\b\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{2})\b", full_text)
    if amount_matches:
        # Clean and convert last (or largest) match
        cleaned_amount = amount_matches[-1].replace(',', '').replace(' ', '')
        try:
            amount = float(cleaned_amount)
        except:
            pass

    return {
        "invoice_number": invoice_number or "",
        "invoice_date": invoice_date or "",
        "amount": amount or 0.0
    }






