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

import yaml
from fuzzywuzzy import fuzz

from dateutil.parser import parse

from regexGen import *

with open('templateDO4.yaml', 'r') as file:
    companyYaml = yaml.safe_load(file)

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
Q1 = "select supplier_do_date, supplier_do_number, po_number, supplier_id\
        from goodsreceiptsnotes where supplier_do_number='"

Q2 = "select id from purchase_orders where po_number='"

Q3 = "insert into\
        goodsreceiptsnotes(supplier_do_date, supplier_do_number, po_number, supplier_id)\
        VALUES (%s,%s,%s,%s)"

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

secondGnome = Term(width=105,height=31)

board = np.zeros((360,900,3), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (255, 255, 0)
thickness = 2
offset = 35

class DO:
    def __init__(self):
        self.field = []
        self.rePattern = []
        self.queried = False
        self.numFieldFound = 0
        self.fieldFound = []
        self.resStr = []
        self.numField = 0
        self.companyNameFound = False
        self.companyName = ''
        self.companyNameRegex =''
        self.itemDetails = [] # item_id, quantity, part_number
        self.itemDetected = [] # item_id, quantity, part_number
        self.partNumberRegex = []
        self.startSearchItem = False
        self.do_date = ''
        self.dateFound = False

    def searchCompany(self, text):
        self.companyID = 0 
        poLike = re.search('T-P[0,O]-(\d{8})',text)
        if poLike != None:
            query = 'select supplier_id from purchase_orders where po_number=\''+poLike.group(1)+'\''
            myCursor.execute(query)
            descr = myCursor.description
            qResults = myCursor.fetchall()
            if qResults:
                mySqlTable(qResults, descr)
                self.companyID = qResults[0][0]
                query = 'select name from suppliers where id='+str(self.companyID)
                myCursor.execute(query)
                descr = myCursor.description
                qResults = myCursor.fetchall()
                
                if qResults:
                    mySqlTable(qResults, descr)
                    self.companyName = qResults[0][0]
                    self.companyNameRegex = genRegex(self.companyName)

                    comMatch = re.search(self.companyNameRegex, text)
                    if comMatch != None:
                        self.po_number = poLike.group(1)
                        print("Company id ", self.companyID)
                        print("Company is ", self.companyName)
                        self.companyNameFound = True
                        echoStr = 'Company Detected: '+self.companyName
                        secondGnome.echo(echoStr)
                        self.register(self.companyName)
                        self.cvBoardInitialize(board)

    def register(self, compName):
        for key, rePattern in companyYaml[compName]['regex'].items():
            self.field.append(key)
            self.rePattern.append(rePattern)
            self.fieldFound.append(0)
            self.numField += 1
            self.resStr.append('')

    def search(self, text):
        for i in range(0, len(self.fieldFound)):
            if self.fieldFound[i] == 0: # not found
                find = re.search(self.rePattern[i], text)
                if find != None:
                    if self.field[i] == 'date':
                        dateStr = find.group(1).replace(" ", "")
                        self.realDate = datetime.strptime(dateStr, \
                                companyYaml[self.companyName]['date_format']).date()
                        self.resStr[i] = self.realDate.strftime('%Y-%m-%d')
                    elif self.field[i] == 'do_num':
                        self.resStr[i] = companyYaml[self.companyName]['do_prefix'] + find.group(1)
                    else:
                        self.resStr[i] = find.group(1)

                    self.fieldFound[i] = 1
                    self.numFieldFound += 1
                    echoStr = self.field[i] + ': ' + self.resStr[i]
                    secondGnome.echo(echoStr)
                    self.cvBoardShowRes(board, i)

    def searchDate(self, text):
        for i in companyYaml['date_format']:
            dateMatch = re.findall(i[0], text)
            if dateMatch != None:
                for j in dateMatch:
                    datestr = j
                    datestr = datestr.replace(" ", "")
                    try:
                        realDate = datetime.strptime(datestr, i[1]).date()
                        self.do_date = realDate.strftime('%Y-%m-%d')
                        echoStr = "do_date = "+self.do_date
                        secondGnome.echo(echoStr)
                    except ValueError:
                        pass
                if self.do_date != '':
                    self.dateFound = True

    
    def next(self):
        self.po_number = ''
        self.field.clear()
        self.rePattern.clear()
        self.queried = False
        self.numFieldFound = 0
        self.fieldFound.clear()
        self.resStr.clear()
        self.numField = 0
        self.companyNameFound = False
        self.companyName = ''
        self.itemDetails.clear()
        self.itemDetected.clear()
        self.partNumberRegex.clear()
        self.startSearchItem = False
        self.do_date = ''
        self.dateFound = False

    def checkDatabase(self):
        self.queried = True
        query = Q1+self.resStr[0]+'\''
        secondGnome.echo(query)
        myCursor.execute(query)
        descr = myCursor.description
        qResults = myCursor.fetchall()
        
        if qResults:
            mySqlTable(qResults, descr)
            if len(qResults) > 1:
                secondGnome.echo('more than one record')
            else:
                # check if there is record of DO based on do number
                if self.resStr[0] == qResults[0][1]:
                    secondGnome.echo('Record Found')
                    secondGnome.echo('Loading item details based on PO ...')
                    self.loadItemDetails()
                    self.startSearchItem = True
        else:
            secondGnome.echo('No record found !!!')
            secondGnome.echo('Press key i to insert, key p to skip')
            key = cv2.waitKey(0)
            if key == ord('i'):
                self.insertDatabase()
                self.startSearchItem = True
            else:
                self.next()
                board = np.zeros((360,900,3), np.uint8) 

    def insertDatabase(self):
        query = Q2+self.po_number+'\'' # query po_number id 
        secondGnome.echo(query)
        myCursor.execute(query)
        descr = myCursor.description
        qResults = myCursor.fetchall()
        
        if qResults:
            mySqlTable(qResults, descr)
            if len(qResults) > 1:
                secondGnome.echo('more than one record') 
            else:
                po_id = qResults[0][0]
                    #supplier_do_date, supplier_do_number, po_number, supplier_id
                val = (self.do_date, self.resStr[0],\
                        po_id, self.companyID)
                print(val)
                myCursor.execute(Q3, val)
                db.commit()
        else:
            secondGnome.echo('No po_number id record found')

    def loadItemDetails(self):
        Q4 = "drop temporary table if exists tempPO;"
        Q5 = "create temporary table tempPO select poi.item_id, poi.quantity, i.part_number\
        from purchase_order_items poi inner join inventories i on poi.item_id=i.id \
        where poi.po_id=(select id from purchase_orders where po_number='"+self.po_number+"');"
        ## resStr[0] = date, [1]=do_num, [2]=po_number
        Q6 = "select * from tempPO;"
        myCursor.execute(Q4)
        myCursor.execute(Q5)
        myCursor.execute(Q6)
        descr = myCursor.description
        res = myCursor.fetchall()

        if res:
            mySqlTable(res, descr)
            for row in res:
                self.itemDetails.append(row)
          #  print("Load")
           # print(self.itemDetails)
        else:
            secondGnome.echo("No PO record or No part_number record !!!")

    def searchItem(self, text):
        record = []
        for index, item_detail in enumerate(self.itemDetails):
            match = re.search(genRegexCapitalInsensitive(self.itemDetails[index][2]), text)
            #secondGnome.echo(genRegexCapitalInsensitive(self.itemDetails[index][2]))
            if match != None:
                echoStr = 'Found item with id '+str(item_detail[0])\
                    +' \''+item_detail[2]+'\''
                #echoStr = 'Found item with id '+str(detail[index][0])
                secondGnome.echo(echoStr)
            #score = fuzz.ratio(item_detail[2], text)
            #if score > conf:
                #record.append(index)
            else:
                record.append(index) ## remaining 
        #if len(record
        for i in record:
            self.itemDetected.append(self.itemDetails[i])
            #print("Detected")
            #print(self.itemDetected)

        temp = self.itemDetails.copy()
        self.itemDetails.clear()
        for i in record:
            self.itemDetails.append(temp[i])

    def cvBoardInitialize(self, cvMat):
        
        cvMat = cv2.putText(cvMat, self.companyName, (50, 50), font, 
                       fontScale, color, thickness, cv2.LINE_AA)
        cvMat = cv2.putText(cvMat, self.po_number, (50, 85), font, 
               fontScale, color, thickness, cv2.LINE_AA)

        for i in range(0, self.numField):
            cvMat = cv2.putText(cvMat, self.field[i]+'  :  ', (50, 120+offset*i), font, 
                       fontScale, color, thickness, cv2.LINE_AA)

    def cvBoardShowRes(self, cvMat, i):
            cvMat = cv2.putText(cvMat, self.resStr[i], (450, 120+offset*i), font, 
                       fontScale, color, thickness, cv2.LINE_AA)
##################################################################################################

count = 0
scale = 0.5

d_o = DO()


WIDTH, HEIGHT = 1280, 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


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


while True:

    _, frame = cap.read()
    #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    frame_copy = frame.copy()
    scan_detection(frame_copy)

    cv2.imshow("input", cv2.resize(frame, (640, 360)))
    #cv2.imshow("input", frame)
    cv2.moveWindow("input", 0, 0)

    warped = four_point_transform(frame_copy, document_contour.reshape(4, 2))

    pressed_key = cv2.waitKey(1) & 0xFF
        
   # allFound = jobFound+salesFound+termsFound+dateFound+totalFound+invoiceNoFound
    if (d_o.numFieldFound != d_o.numField and d_o.numField != 0) \
            or d_o.companyNameFound == False\
            or d_o.dateFound == False\
            or d_o.startSearchItem == True:
        #ocr_text = pytesseract.image_to_string(warped)
        ocr_text = pytesseract.image_to_string(frame)
        if d_o.companyNameFound == False:
            d_o.searchCompany(ocr_text)
        elif d_o.startSearchItem == True:
            d_o.searchItem(ocr_text)
            if len(d_o.itemDetails) == 0:
                d_o.startSearchItem = False
        elif d_o.dateFound == False:
            d_o.searchDate(ocr_text)
        else: 
            d_o.search(ocr_text)

    cv2.imshow("Result", board)
    cv2.moveWindow("Result", 650, 0)
    
    if d_o.queried == False and (d_o.numFieldFound == d_o.numField and d_o.numField != 0) and d_o.dateFound == True:
        d_o.checkDatabase()
    
    #cv2.imshow("Warped", cv2.resize(warped, (int(0.75 * warped.shape[1]), int(0.75 * warped.shape[0]))))
    #cv2.moveWindow("Warped", 0, 450)

    if pressed_key == 27:
        break

    elif pressed_key == ord('s'):
        cv2.imwrite("output/scanned_" + str(count) + ".jpg", warped)
        count += 1

        cv2.imshow("input", cv2.resize(frame, (int(scale * WIDTH), int(scale * HEIGHT))))
        cv2.waitKey(500)

    elif pressed_key == ord('n'):
        d_o.next()
        board = np.zeros((360,900,3), np.uint8)

cv2.destroyAllWindows()
secondGnome.kill()
