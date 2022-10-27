import cv2
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract

import re
from datetime import datetime

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

count = 0
scale = 0.5
dateFound = 0
totalFound = 0
subFound = 0
invoiceNoFound = 0
jobFound = 0
salesFound = 0
termsFound = 0

board = np.zeros((360,900,3), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0, 255, 0)
thickness = 2
offset = 35
board = cv2.putText(board, 'Date Issued:', (50, 50), font, 
                   fontScale, color, thickness, cv2.LINE_AA)

board = cv2.putText(board, 'Delivery Order Number:', (50, 50+offset), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
board = cv2.putText(board, 'Job Order Number:', (50, 50+offset*2), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
board = cv2.putText(board, 'Sales Order NUmber:', (50, 50+offset*3), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
board = cv2.putText(board, 'Terms:', (50, 50+offset*4), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
board = cv2.putText(board, 'Sub Amount:', (50, 50+offset*5), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
board = cv2.putText(board, 'Total Amount:', (50, 50+offset*6), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
WIDTH, HEIGHT = 1280, 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

def nothing(x):
    pass

cv2.namedWindow('tune')
cv2.createTrackbar('low', 'tune', 0, 255, nothing)
cv2.createTrackbar('high', 'tune', 0, 255, nothing)
lowThres = 128
highThres = 255

def image_processing(image, lowThres, highThres):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, lowThres, highThres, cv2.THRESH_BINARY)

    return threshold


def scan_detection(image):
    global document_contour

    document_contour = np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                document_contour = approx
                max_area = area

    cv2.drawContours(frame, [document_contour], -1, (0, 255, 0), 3)


def center_text(image, text):
    text_size = cv2.getTextSize(text, font, 2, 5)[0]
    text_x = (image.shape[1] - text_size[0]) // 2
    text_y = (image.shape[0] + text_size[1]) // 2
    cv2.putText(image, text, (text_x, text_y), font, 2, (255, 0, 255), 5, cv2.LINE_AA)


while True:

    _, frame = cap.read()
    #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    frame_copy = frame.copy()
    scan_detection(frame_copy)

    cv2.imshow("input", cv2.resize(frame, (640, 360)))
    #frame_crop = frame[250:1250, 10:800]
    #cv2.imshow("input", frame_crop)
    cv2.moveWindow("input", 0, 0)
    warped = four_point_transform(frame_copy, document_contour.reshape(4, 2))
    cv2.imshow("Warped", cv2.resize(warped, (int(scale * warped.shape[1]), int(scale * warped.shape[0]))))
    #cv2.imshow("Warped", warped)
    cv2.moveWindow("Warped", 0, 650)
    lowThres = cv2.getTrackbarPos('low', 'tune')
    highThres = cv2.getTrackbarPos('high', 'tune')
    processed = image_processing(warped, lowThres, highThres)
    processed = processed[10:processed.shape[0] - 10, 10:processed.shape[1] - 10]
    #cv2.imshow("Processed", cv2.resize(processed, (int(scale * processed.shape[1]),
     #                                              int(scale * processed.shape[0]))))
    #cv2.imshow("Processed", processed)
    cv2.moveWindow("Processed", 1450, 0)
    pressed_key = cv2.waitKey(1) & 0xFF
        
    ocr_text = pytesseract.image_to_string(warped)
    #print(ocr_text)
    
    cv2.imshow("Result", board)
    cv2.moveWindow("Result", 650, 0)
    if jobFound == 0:
        jobOrder = re.search(r'JOB\s+ORDER\s+NUMBER:*\s+\w{2}(\d{8})', ocr_text)
        if jobOrder != None:
            jobString = "JO"
            jobString += jobOrder.group(1)
            print('Job Order Number is', jobOrder.group(1))
            jobFound = 1
            board = cv2.putText(board, jobString, (450, 50+offset*2), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if salesFound == 0:
        salesOrder = re.search(r'SALES\s+ORDER\s+NUMBER:*\s+\w{2}(\d{8})', ocr_text)
        if salesOrder != None:
            salesOrderString = "Sales Order Number is SO"
            salesOrderString+=salesOrder.group(1)
            salesString = "SO"
            salesString += salesOrder.group(1)
            #print('Sales Order Number is SO', salesOrder.group(1))
            print(salesOrderString)
            salesFound = 1
            board = cv2.putText(board, salesString, (450, 50+offset*3), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if termsFound == 0:
        terms = re.search(r'TERMS:*\s+(\d{1,3}\s+Days)', ocr_text)
        if terms != None:
            print('Terms is ', terms.group(1))
            termsFound = 1
            board = cv2.putText(board, terms.group(1), (450, 50+offset*4), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if dateFound == 0:
        match = re.search(r'\d{4}-\d{2}-\d{2}', ocr_text)
        if match != None:
            #date = datetime.strptime(match.group(), '%Y-%m-%d').date()
            print('date is', match.group())
            dateFound = 1
            board = cv2.putText(board, match.group(), (450, 50), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)
    
    if totalFound == 0:
        total_amount = re.search(r'TOTAL\s+AMOUNT\s*.*\s+(\d*,\d*.\d{2,4})', ocr_text)
        if total_amount != None:
            totalAmountString = "SGD "
            totalAmountString += total_amount.group(1)
            print('total amount is', total_amount.group(1))
            totalFound = 1
            board = cv2.putText(board, totalAmountString, (450, 50+offset*6), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if subFound == 0:
        sub_amount = re.search(r'SUB\s+AMOUNT\s+\|\s+(\d*,\d*.\d{2,4})', ocr_text)
        if sub_amount != None:
            subAmountString = "SGD "
            subAmountString += sub_amount.group(1)
            print('sub amount is', sub_amount.group(1))
            subFound = 1
            board = cv2.putText(board, subAmountString, (450, 50+offset*5), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if invoiceNoFound == 0:
        #invoiceNo = re.search(r'DELIVERY\s+ORDER\s+NUMBER\s+:\s+(\w{1,3}-\d{1,8})', ocr_text)
        invoiceNo = re.search(r'DELIVERY\s+ORDER\s+NUMBER:*\s+(TCM-\d{8})', ocr_text)
        if invoiceNo != None:
            print('Invoice Number is', invoiceNo.group(1))
            invoiceNoFound = 1
            board = cv2.putText(board, invoiceNo.group(1), (450, 50+offset), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if pressed_key == 27:
        break

    elif pressed_key == ord('s'):
        #cv2.imwrite("output/scanned_" + str(count) + ".jpg", processed)
        cv2.imwrite("output/scanned_" + str(count) + ".jpg", warped)
        count += 1

        center_text(frame, "Scan Saved")
        cv2.imshow("input", cv2.resize(frame, (int(scale * WIDTH), int(scale * HEIGHT))))
        cv2.waitKey(500)

    elif pressed_key == ord('o'):
        file = open("output/recognized_" + str(count - 1) + ".txt", "w")
        ocr_text = pytesseract.image_to_string(warped)
        print(ocr_text)
        file.write(ocr_text)
        file.close()

        center_text(frame, "Text Saved")
        cv2.imshow("input", cv2.resize(frame, (int(scale * WIDTH), int(scale * HEIGHT))))
        cv2.waitKey(500)

cv2.destroyAllWindows()
