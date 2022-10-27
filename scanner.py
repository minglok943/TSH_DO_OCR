import cv2
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract
from pytesseract import Output
import re
from datetime import datetime
from datetime import date

import time
import mysql.connector as mysql
from secondTerminal import Term


def mySqlTable(results, description):
    #results = cursor.fetchall()
    widths = []
    columns = []
    tavnit='|'
    seperator='+'
    for cd in description:
        widths.append(len(cd[0]))
        columns.append(cd[0])
    for w in widths:
        tavnit += " %-"+"%ss |" % (w)
        seperator += '-'*w + '--+'
    print(seperator)
    secondGnome.echo(seperator)
    tmp = tavnit % tuple(columns)
    print(tmp)
    secondGnome.echo(tmp)
    print(seperator)
    secondGnome.echo(seperator)
    for row in results:
        tmp = tavnit % row
        print(tmp)
        secondGnome.echo(tmp)
    print(seperator)
    secondGnome.echo(seperator)

db = mysql.connect(
        host="localhost",
        user="lokcharming",
        passwd="asdfasdf",
        database="ERP"
        )

myCursor = db.cursor()
Q1 = "select invoice_date, invoice_number, so_number, jo_number, term, final_total_amount\
        from invoices where invoice_number='"
#invoice_number = '09220634'
#f = Q1+invoice_number+"'"
#print(f)
#myCursor.execute(f)
#for x in myCursor:
#    print(type(x[0]))
#    print(x[0])
#    print(x)
    
#results = myCursor.fetchall()
#print(results)

#mySqlTable(myCursor)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

secondGnome = Term(width=105,height=31)

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
queried = 0
numData = 6

invDateStr = None  #actually is datetime.date type
totalStr = ''
subStr = ''
invNoStr = ''
jobNumStr = ''
salesNumStr = ''
termStr = ''

board = np.zeros((360,900,3), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (255, 255, 0)
thickness = 2
offset = 35

def boardInitialize(board):
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
    #board = cv2.putText(board, 'Sub Amount:', (50, 50+offset*5), font, 
    #                   fontScale, color, thickness, cv2.LINE_AA)
    board = cv2.putText(board, 'Total Amount:', (50, 50+offset*5), font, 
                       fontScale, color, thickness, cv2.LINE_AA)

WIDTH, HEIGHT = 1280, 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
boardInitialize(board)

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
    #lowThres = cv2.getTrackbarPos('low', 'tune')
    #highThres = cv2.getTrackbarPos('high', 'tune')
    #processed = image_processing(warped, lowThres, highThres)
    #processed = processed[10:processed.shape[0] - 10, 10:processed.shape[1] - 10]
    #cv2.imshow("Processed", cv2.resize(processed, (int(scale * processed.shape[1]),
     #                                              int(scale * processed.shape[0]))))
    #cv2.imshow("Processed", processed)
    cv2.moveWindow("Processed", 1450, 0)
    pressed_key = cv2.waitKey(1) & 0xFF
        
    allFound = jobFound+salesFound+termsFound+dateFound+totalFound+invoiceNoFound
    if allFound != numData:
        ocr_text = pytesseract.image_to_string(warped)
        #print(ocr_text)
        d = pytesseract.image_to_data(warped, output_type=Output.DICT)
    
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                jobOrder = re.search(r'\w{2}(\d{8})', d['text'][i])
                salesOrder = re.search(r'\w{2}(\d{8})', d['text'][i])
                match = re.search(r'\d{4}-\d{2}-\d{2}', d['text'][i])
                total_amount = re.search(r'(\d*,\d*.\d{2,4})', d['text'][i])
                sub_amount = re.search(r'(\d*,\d*.\d{2,4})', d['text'][i])
                invoiceNo = re.search(r'(TCM-\d{8})', d['text'][i])
                if jobOrder != None or salesOrder != None or match != None or total_amount != None\
                    or sub_amount != None or invoiceNo != None:
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    warped = cv2.rectangle(warped, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Result", board)
    cv2.moveWindow("Result", 650, 0)
    
#    allFound = jobFound+salesFound+termsFound+dateFound+totalFound+subFound+invoiceNoFound
    if allFound == numData and queried == 0:
        queried = 1
        query = Q1+invNoStr+'\''
        secondGnome.echo(query)
        myCursor.execute(query)
        descr = myCursor.description
        qResults = myCursor.fetchall()
        
        if qResults:
            mySqlTable(qResults, descr)
            if len(qResults) > 1:
                print("more than one record")
                board = cv2.putText(board, "More than one record!", (50, 50+offset*6), font, 
                   fontScale, (125, 255, 0), thickness, cv2.LINE_AA)
            else:
                check = 0
                record = []
                check += (qResults[0][0]==invDateStr)
                print('1', check)
                if qResults[0][0]!=invDateStr:
                    board = cv2.putText(board, "Error!", (750, 50+offset*0), font, 
                                    fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
                    record.append(0)
                    dateFound = 0

                check += (qResults[0][1]==invNoStr)
                print('2', check)
                if qResults[0][1]!=invNoStr:
                    board = cv2.putText(board, "Error!", (750, 50+offset*1), font, 
                                    fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
                    record.append(1)
                    invoiceNoFound = 0

                check += (qResults[0][2]==salesNumStr)
                print('3', check)
                if qResults[0][2]!=salesNumStr:
                    record.append(3)
                    salesFound = 0
                    board = cv2.putText(board, "Error!", (750, 50+offset*3), font, 
                                    fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
                
                check += (qResults[0][3]==jobNumStr)
                print('4', check)
                if qResults[0][3]!=jobNumStr:
                    record.append(2)
                    jobFound = 0
                    board = cv2.putText(board, "Error!", (750, 50+offset*2), font, 
                                    fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
                check += (qResults[0][4]==termStr)
                print('5', check)
                
                if qResults[0][4]!=termStr:
                    record.append(4)
                    termsFound = 0
                    board = cv2.putText(board, "Error!", (750, 50+offset*4), font, 
                                    fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
                
                #check += (qResults[0][5]==subStr)
                check += (str(qResults[0][5])==totalStr)
                print('6', check)
                if (str(qResults[0][5])!=totalStr):
                    record.append(5)
                    totalFound = 0
                    board = cv2.putText(board, "Error!", (750, 50+offset*5), font, 
                                    fontScale, (0, 0, 255), thickness, cv2.LINE_AA)

                if check == numData:
                    print("Record Matched")
                    board = cv2.line(board, (0,65+offset*6-6), (900,65+offset*6-6), (0,0,0), 33) 
                    board = cv2.putText(board, "Record Matched !", (250, 65+offset*6), font, 
                                    fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
                else:
                    print("Not matched")
                    print('q{} i{}', qResults[0][0], invDateStr)
                    #print('q', type(qResults[0][0], type(invDateStr))
                    print('q{} i{}', qResults[0][1], invNoStr)
                    print('q{} i{}', qResults[0][2], salesNumStr)
                    print('q{} i{}', qResults[0][3], jobNumStr)
                    print('q{} i{}', qResults[0][4], termStr)
                    print('q{} i{}', qResults[0][5], totalStr)
                    print(type(qResults[0][5]), type(totalStr))
                    board = cv2.putText(board, "Record Not Matched! Scan again", (150, 65+offset*6), font, 
                                    fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
                    cv2.imshow("Result", board)
                    cv2.waitKey(2000)
                    queried = 0
                    for i in record:
                        board = cv2.line(board, (450,50+offset*i-6), (900,50+offset*i-6), (0,0,0), 33) 


                
        else:
            print("No record found")
            board = cv2.putText(board, "No record found!", (200, 65+offset*6), font, 
                   fontScale, (0,0,255), thickness, cv2.LINE_AA)
        

    if jobFound == 0:
        jobOrder = re.search(r'JOB\s+ORDER\s+NUMBER:*\s+\w{2}(\d{8})', ocr_text)
        if jobOrder != None:
            jobString = "JO"
            jobString += jobOrder.group(1)
            jobNumStr = jobOrder.group(1)
            jobNumStr = jobNumStr.replace(" ", "")
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
            salesNumStr = salesOrder.group(1)
            salesNumStr = salesNumStr.replace(" ", "")
            #print('Sales Order Number is SO', salesOrder.group(1))
            #print(salesOrderString)
            salesFound = 1
            board = cv2.putText(board, salesString, (450, 50+offset*3), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if termsFound == 0:
        terms = re.search(r'TERMS:*\s+(\d{1,3}\s+Days)', ocr_text)
        if terms != None:
            termStr = terms.group(1)
            print('Terms is ', terms.group(1))
            termsFound = 1
            board = cv2.putText(board, terms.group(1), (450, 50+offset*4), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if dateFound == 0:
        match = re.search(r'\d{4}-\d{2}-\d{2}', ocr_text)
        if match != None:
            date_str = match.group()
            date_str = date_str.replace(" ", "")
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            invDateStr = date
            print('date is', date)
            dateFound = 1
            board = cv2.putText(board, match.group(), (450, 50), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)
    
    if totalFound == 0:
        total_amount = re.search(r'TOTAL\s+AMOUNT\s*.*\s+(\d*,*\d*,*\d*,*\d*,*\d*,*\d*.\d{2,4})', ocr_text)
        if total_amount != None:
            totalAmountString = "SGD "
            totalAmountString += total_amount.group(1)
            totalStr = total_amount.group(1)
            totalStr = totalStr.replace(" ", "")
            totalStr = totalStr.replace(",","")
            print('total amount is', total_amount.group(1))
            totalFound = 1
            board = cv2.putText(board, totalAmountString, (450, 50+offset*5), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if subFound == 0:
        sub_amount = re.search(r'SUB\s+AMOUNT\s+\|\s+(\d*,*\d*,*\d*,*\d*,*\d*,*\d*.\d{2,4})', ocr_text)
        if sub_amount != None:
            subAmountString = "SGD "
            subAmountString += sub_amount.group(1)
            subStr = sub_amount.group(1)
            subStr = subStr.replace(" ", "")
            print('sub amount is', sub_amount.group(1))
            subFound = 1
            #board = cv2.putText(board, subAmountString, (450, 50+offset*5), font, 
             #               fontScale, (255,0,0), thickness, cv2.LINE_AA)

    if invoiceNoFound == 0:
        #invoiceNo = re.search(r'DELIVERY\s+ORDER\s+NUMBER\s+:\s+(\w{1,3}-\d{1,8})', ocr_text)
        invoiceNo = re.search(r'DELIVERY\s+ORDER\s+NUMBER:*\s+(TCM-)(\d{8})', ocr_text)
        if invoiceNo != None:
            invNoStr = invoiceNo.group(2)
            invNoStr = invNoStr.replace(" ", "")
            print('Invoice Number is', invoiceNo.group(1)+invoiceNo.group(2))
            invoiceNoFound = 1
            board = cv2.putText(board, invoiceNo.group(1)+invoiceNo.group(2), (450, 50+offset), font, 
                            fontScale, (255,0,0), thickness, cv2.LINE_AA)
    
    cv2.imshow("Warped", cv2.resize(warped, (int(0.75 * warped.shape[1]), int(0.75 * warped.shape[0]))))
    #cv2.imshow("Warped", warped)
    cv2.moveWindow("Warped", 0, 450)

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
    
    elif pressed_key == ord('n'):
        invoiceNoFound = 0
        jobFound = 0
        salesFound = 0
        termsFound = 0
        totalFound = 0
        dateFound = 0
        queried = 0
        board = np.zeros((360,900,3), np.uint8)
        boardInitialize(board)

cv2.destroyAllWindows()
secondGnome.kill()
