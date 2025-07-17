import cv2
import numpy as np
import pytesseract
import re


def open_image(im_name):
    return cv2.imread(im_name)

# Change these values according to your use case
def preprocess_image(image):
    # Turn image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Turn image to Black and White
    thresh, img_bw = cv2.threshold(gray, 200, 230, cv2.THRESH_BINARY)

    # Rotate Image
    rot_data = pytesseract.image_to_osd(img_bw);
    rot = re.search(r'(?<=Rotate: )\d+', rot_data).group(0)
    angle = float(rot)

    if angle > 0:
        angle = 360 - angle
    if (str(int(angle)) == '0'):
        rotated = img_bw
    elif (str(int(angle)) == '90'):
        rotated = cv2.rotate(img_bw, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif (str(int(angle)) == '180'):
        rotated = cv2.rotate(img_bw, cv2.ROTATE_180)
    elif (str(int(angle)) == '270'):
        rotated = cv2.rotate(img_bw, cv2.ROTATE_90_CLOCKWISE)

    image_blur = cv2.GaussianBlur(rotated, (3, 3), cv2.BORDER_DEFAULT)
    image_resized = cv2.resize(image_blur, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

    # Erode Image
    img_bw = cv2.bitwise_not(image_resized)
    kernel = np.ones((1, 1), np.uint8)
    eroded = cv2.erode(img_bw, kernel, iterations=1)

    # Dilate Image
    kernel = np.ones((1, 1), np.uint8)
    dilated = cv2.dilate(eroded, kernel, iterations=1)
    dilated = cv2.bitwise_not(dilated)

    # Remove any borders
    contours, heiarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = cntSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    cropped_img = dilated[y:y + h, x:x + w]

    # Add Borders
    color = [255, 255, 255]
    top, bottom, left, right = [50] * 4
    img_with_border = cv2.copyMakeBorder(cropped_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    return img_with_border



