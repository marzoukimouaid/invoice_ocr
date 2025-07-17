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
    sents = nlp(ocr_result)
    data_list = []
    for sent in sents:
        tokens = sent.text.split(" ")
        for i in range(len(tokens)):
            var = tokens[i]
            data = {}

            if re.match(r"#(\d+)", str(var)):
                data.update({"Invoice Number": str(var)})
            elif re.match(r'^(0[1-9]|[12][0-9]|3[01]).(0[1-9]|1[012]).(19|20)\d\d$', str(var)):
                data.update({"Date of Invoice": str(var)})
            elif re.match(r'\d{1,6}', str(var)):
                data.update({"Amount": str(var)})

            if data != {}:
                data_list.append(data)

    return data_list






