from PIL import Image
import pytesseract
import traceback
import cv2
from pytesseract import Output
from .models import File, PanInfo
from django.conf import settings
import os
import time
import re
import datetime
import platform


def process_image_data(data):
    pan_info = PanInfo()

    if is_data_valid(data):
        lines = data.split('\n')
        lines = [line for line in lines if len(line.strip()) > 0]
        for index, line in enumerate(lines):
            try:
                # print(line)
                if 'Permanent Account Number Card' in line:
                    pan_info.pan_number = extract_alpha_numeric(lines[index+1])
                if 'Name' in line and "Father's Name" not in line:
                    pan_info.full_name = extract_alpha(lines[index+1])
                if "Father's Name" in line:
                    pan_info.fathers_name = extract_alpha(lines[index+1])
                if 'Date of Birth' in line:
                    pan_info.date_of_birth = process_date(extract_numeric(lines[index+1]))
            except:
                traceback.print_exc()
    else:
        return None
    return pan_info


def process_date(text):
    # [0-9]{8}, '07101995'
    if len(text) == 8:
        matches = re.findall(r'[0-9]{8}', text)
        if len(matches) == 1:
            return datetime.datetime(int(matches[0][4:]), int(matches[0][2:4]), int(matches[0][0:2])).date()

    # [0-9]{2}\/[0-9]{2}\/[0-9]{4}, '07/10/1995'
    if len(text) == 10:
        matches = re.findall(r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}', text)
        if len(matches) == 1:
            return datetime.datetime(int(matches[0][6:]), int(matches[0][3:5]), int(matches[0][0:2])).date()
    return None


def is_data_valid(data):
    value_count = 0
    if 'INCOME TAX DEPARTMENT' in data:
        value_count += 1
    if 'Permanent Account Number Card' in data:
        value_count += 1
    if 'Name' in data:
        value_count += 1
    if "Father's Name" in data:
        value_count += 1
    if 'Date of Birth' in data:
        value_count += 1
    if 'Signature' in data:
        value_count += 1
    if value_count >= 4:
        return True
    else:
        return False


def extract_alpha_numeric(text):
    extracted_text = ''
    for ch in text:
        if ch.isalnum() or ch is ' ':
            extracted_text += ch
    return extracted_text.strip()


def extract_alpha(text):
    extracted_text = ''
    for ch in text:
        if ch.isalpha() or ch is ' ':
            extracted_text += ch
    return extracted_text.strip()


def extract_numeric(text):
    extracted_text = ''
    for ch in text:
        if ch.isnumeric():
            extracted_text += ch
    return extracted_text.strip()


def extract_pan_number(text):
    regex = r"[A-Z0-9]{10}"
    text = extract_alpha_numeric(text)
    re.findall(regex, text)


def extract_face(imagePath):
    print('settings.HAARCASCADE_LOCATION', settings.HAARCASCADE_LOCATION)
    face_cascade = cv2.CascadeClassifier(settings.HAARCASCADE_LOCATION)

    try:
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print("Found {0} faces!".format(len(faces)))
        if len(faces) != 1:
            return None

        for (x, y, w, h) in faces:
            print(y-x, w, h)
            factor = int(w/2.7)
            # cv2.rectangle(image, (x-factor, y-factor), (x + w + factor, y + h + factor), (255, 0, 0), 2)
            crop_image = image[y-factor:y + h + factor, x-factor:x + w + factor]
            # cv2.imshow("Faces found", crop_image)
            # cv2.waitKey(0)
            file_name = str(int(time.time() * 1000)) + ".jpg"
            cv2.imwrite(os.getcwd() + "/media/" + file_name, crop_image)
            return file_name
        return None
    except:
        traceback.print_exc()
        return None


def extract_signature(imagePath, signature_positions):

    try:
        image = cv2.imread(imagePath)

        sig_factor = signature_positions['width']
        x1 = signature_positions['left']-sig_factor
        y1 = signature_positions['top']-sig_factor
        x2 = signature_positions['left'] + signature_positions['width']
        y2 = signature_positions['top'] + signature_positions['height'] - int(sig_factor/3)
        # cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        crop_image = image[y1:y2, x1:x2]
        # cv2.imshow("Faces found", crop_image)
        # cv2.waitKey(0)
        file_name = str(int(time.time() * 1000)) + ".jpg"
        cv2.imwrite(os.getcwd() + "/media/" + file_name, crop_image)
        return file_name
    except:
        traceback.print_exc()
        return None


def extract_data(img_file):
    if 'linux' in str(platform.platform()):
        img_file = os.getcwd() + img_file
    else:
        img_file = os.getcwd() + img_file.replace('/', '\\')
    print('img_file', img_file)
    pan_info = PanInfo()
    # Get Json Text Data
    try:
        pan_info = process_image_data(pytesseract.image_to_string(Image.open(img_file)))
        print('process_image_data', pan_info)
    except:
        traceback.print_exc()

    # Get Picture
    try:
        pan_info.photo.name = extract_face(img_file)
        print('extract_face', pan_info.photo)
    except:
        traceback.print_exc()

    # Get Signature
    try:
        df = pytesseract.image_to_data(Image.open(img_file), output_type=Output.DATAFRAME)
        row = df[df.text == 'Signature'].iloc[0]
        signature_positions = {
            'left': row['left'],
            'top': row['top'],
            'width': row['width'],
            'height': row['height']
        }
        pan_info.scanned_signature.name = extract_signature(img_file, signature_positions)
        print('pan_info.scanned_signature', pan_info.scanned_signature)
    except:
        traceback.print_exc()

    return pan_info
