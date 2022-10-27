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

def nothing(x):
    pass

cv2.namedWindow('tune')
cv2.createTrackbar('x', 'tune', 0, 1280, nothing)
cv2.createTrackbar('x1', 'tune', 0, 1280, nothing)
cv2.createTrackbar('y', 'tune', 0, 720, nothing)
cv2.createTrackbar('y1', 'tune', 0, 720, nothing)

with open('templateDO7.yaml', 'r') as file:
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
        self.companyNameFoundFromPO = False
        self.companyNameFromPO = ''
        self.companyNameFoundFromYaml = False
        self.companyNameFromYaml = ''
        self.companyNameRegex =''
        self.itemDetails = [] # item_id, quantity, part_number
        self.itemDetected = [] # item_id, quantity, part_number
        self.itemQuantityToBeDetected = [] # item_id, quantity, part_number
        self.partNumberRegex = []
        self.startSearchItem = False
        self.startSearchQuantity = False
        self.do_date = ''
        self.dateFound = False
        self.companyNameMatched = False

    def searchCompanyFromYaml(self, text):
        self.companyID = 0 # my own index, not same with the database company id
        for i in companyYaml['companies']:
            comStr = re.search(i[1], text)
            if comStr != None:
                print("Company id ", i[0])
                print("Company is ", i[2])
                self.companyNameFromYaml = i[2]
                self.companyNameFoundFromYaml = True
                echoStr = 'Company Detected: '+self.companyNameFromYaml
                secondGnome.echo(echoStr)
                print(comStr.group())
                #self.register(self.companyName)
                #self.cvBoardInitialize(board)
            else:
                self.companyID += 1

    def searchCompanyFromPO(self, text):
        poLike = re.search('T-P[0,O]-(\d{8})',text)
        if poLike != None:
            query = 'select id, supplier_id from purchase_orders where po_number=\''+poLike.group(1)+'\''
            myCursor.execute(query)
            descr = myCursor.description
            qResults = myCursor.fetchall()
            if qResults:
                mySqlTable(qResults, descr)
                self.poId = qResults[0][0]
                self.companyID = qResults[0][1]
                query = 'select name from suppliers where id='+str(self.companyID)
                myCursor.execute(query)
                descr = myCursor.description
                qResults = myCursor.fetchall()
                
                if qResults:
                    mySqlTable(qResults, descr)
                    self.companyNameFromPO = qResults[0][0]
                    echoStr = "company Name From PO num = "+self.companyNameFromPO
                    secondGnome.echo(echoStr)
                    self.companyNameFoundFromPO = True
                    self.po_number = poLike.group(1)
            else:
                secondGnome.echo("no PO record")

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
                                companyYaml[self.companyNameFromYaml]['date_format']).date()
                        self.resStr[i] = self.realDate.strftime('%Y-%m-%d')
                    elif self.field[i] == 'do_num':
                        self.resStr[i] = companyYaml[self.companyNameFromYaml]['do_prefix'] + find.group(1)
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
        self.companyNameFoundFromYaml = False
        self.companyNameFromYaml = ''
        self.companyNameFoundFromPO = False
        self.companyNameFromPO = ''
        self.itemDetails.clear()
        self.itemDetected.clear()
        self.itemQuantityToBeDetected.clear()
        self.partNumberRegex.clear()
        self.startSearchItem = False
        self.startSearchQuantity = False
        self.do_date = ''
        self.dateFound = False
        self.companyNameMatched = False

    def checkDatabase(self):
        self.queried = True
        Q1 = "select id, grn_number, po_number, supplier_id\
        from goodsreceiptsnotes where supplier_do_number='"
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
                secondGnome.echo('Record Found')
                self.goodsreceiptsnotesExist = True
                self.grn_id = qResults[0][0]
                # check if there is record of DO based on do number
                """
                if self.resStr[0] == qResults[0][1]:
                    #self.loadItemDetails()
                    #self.startSearchItem = True
                """
        else:
            secondGnome.echo('No record found !!!')
            self.goodsreceiptsnotesExist = False
            """
            secondGnome.echo('Press key i to insert, key p to skip')
            key = cv2.waitKey(0)
            if key == ord('i'):
                self.insertDatabase()
                self.startSearchItem = True
            else:
                self.next()
                board = np.zeros((360,900,3), np.uint8)
            """
        secondGnome.echo('Loading item details based on PO ...')
        self.loadItemDetails()
        self.startSearchItem = True

    def insertDatabase(self):

        if self.goodsreceiptsnotesExist == False:
            myCursor.execute("select id, grn_number from goodsreceiptsnotes order by grn_number desc limit 1")
            qResults = myCursor.fetchall()
            self.grn_id = qResults[0][0]+1
            self.grn_number = str(int(qResults[0][1])+1)
            secondGnome.echo("inserting goodsreceiptsnotes")
            val = (self.grn_number, self.do_date, self.resStr[0],\
                    self.poId, self.companyID)
            secondGnome.echo(str(val))
            Q3 = "insert into\
            goodsreceiptsnotes(grn_number, supplier_do_date, supplier_do_number,\
                                po_number, supplier_id)\
            VALUES (%s,%s,%s,%s,%s)"
            myCursor.execute(Q3, val)
            db.commit()
        else: 
           secondGnome.echo("goodsreceiptsnotes record exist")

        # itemDetails[0] = purchase_order_items.id
        # itemDetails[1] = purchase_order_items.item_id
        # itemDetails[2] = purchase_order_items.quantity
        # itemDetails[3] = inventories.part_number
        print("self.itemDetected")
        print(self.itemDetected)
        for item in self.itemDetected:
            query = "select grn_id from goodrecieptsnoteitems where po_item_id='"+str(item[0])+"'"
            #secondGnome.echo(query)
            myCursor.execute(query)
            exist = myCursor.fetchall()
            #print(exist)
            if not exist:
                secondGnome.echo("inserting goodrecieptsnoteitems")
                Q6 = "insert into goodrecieptsnoteitems(grn_id, po_item_id, item_id, ordered_quantity)\
                VALUES(%s,%s,%s,%s)"
                val1 = (self.grn_id, item[0], item[1], item[2])
                secondGnome.echo(str(val1))
                myCursor.execute(Q6, val1)
                db.commit()
            else:
                echoStr = item[3]+"with item_id="+str(item[1])+", po_item_id="+str(item[0])+" exist in goodrecieptsnoteitems"
                secondGnome.echo(echoStr)
        
        """
        Q2 = "select id from purchase_orders where po_number='"
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
                Q3 = "insert into\
                goodsreceiptsnotes(supplier_do_date, supplier_do_number, po_number, supplier_id)\
                VALUES (%s,%s,%s,%s)"
                myCursor.execute(Q3, val)
                db.commit()
        else:
            secondGnome.echo('No po_number id record found')
        """

    def loadItemDetails(self):
        # itemDetails[0] = purchase_order_items.id
        # itemDetails[1] = purchase_order_items.item_id
        # itemDetails[2] = purchase_order_items.quantity
        # itemDetails[3] = inventories.part_number
        Q4 = "drop temporary table if exists tempPO;"
        Q5 = "create temporary table tempPO select poi.id, poi.item_id, poi.quantity, i.part_number\
        from purchase_order_items poi inner join inventories i on poi.item_id=i.id \
        where poi.po_id=(select id from purchase_orders where po_number='"+self.po_number+"');"
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
        # itemDetails[0] = purchase_order_items.id
        # itemDetails[1] = purchase_order_items.item_id
        # itemDetails[2] = purchase_order_items.quantity
        # itemDetails[3] = inventories.part_number
        for index, item_detail in enumerate(self.itemDetails):
            match = re.search(genRegexCapitalInsensitive(self.itemDetails[index][3]), text)
            #secondGnome.echo(genRegexCapitalInsensitive(self.itemDetails[index][2]))
            if match != None:
                self.itemDetected.append(item_detail)
                echoStr = 'Found item with id '+str(item_detail[1])\
                    +' \''+item_detail[3]+'\''
                #echoStr = 'Found item with id '+str(detail[index][0])
                secondGnome.echo(echoStr)
            #score = fuzz.ratio(item_detail[2], text)
            #if score > conf:
                #record.append(index)
            else:
                record.append(index) ## remaining 
        #if len(record
        #for i in record:
            #self.itemDetected.append(self.itemDetails[i])
            #print("Detected")
            #print(self.itemDetected)

        temp = self.itemDetails.copy()
        self.itemDetails.clear()
        for i in record:
            self.itemDetails.append(temp[i])

    def getQuantity(self, img):
        data = pytesseract.image_to_data(img, output_type='dict')
        stringLoc = []
        quantityY = []
        quantityX = 0
        quantityW = 0
        for i in range(0, len(data['text'])):
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            text = data['text'][i]
            text = "".join(text).strip()
            for ele in companyYaml['quantity_format']:
                match = re.search(ele[0], text)
                if match != None:
                    #secondGnome.echo("found x")
                    #secondGnome.echo(match.group())
                    print(text)
                    quantityX = x - 20
                    quantityW = w + 50
                    print("x = ", quantityX)
                    print("w = ", quantityW)
                    break

            if text.isspace() == False:
                if len(stringLoc)==0:
                    stringLoc.append([text,[x,y,w,h]])
                else:
                    inserted = False
                    for i in stringLoc:
                        if y >= i[1][1]-3 and y<=i[1][1]+3:
                            i[0] = i[0]+" "+text
                            i[1][2] += w
                            inserted = True
                            break
                    if inserted == False:
                        stringLoc.append([text,[x,y,w,h]])

        # itemDetails[0] = purchase_order_items.id
        # itemDetails[1] = purchase_order_items.item_id
        # itemDetails[2] = purchase_order_items.quantity
        # itemDetails[3] = inventories.part_number
        
        # stringLoc = [text, (x,y,w,h)]
        # Find Y
        for item_index, i in enumerate(self.itemDetected):
            for j in stringLoc:
                if self.itemQuantityToBeDetected[item_index] == True:
                    match = re.search(genRegexCapitalInsensitive(i[3]), j[0])
                    if match != None:
                        # [y, h] of item
                        #secondGnome.echo("found y")
                        if len(quantityY) == 0:
                            quantityY.append( [j[1][1]-20, j[1][3]+50, item_index] )
                        else:
                            # sort in ascending order by y
                            inserted = False
                            for index, k in enumerate(quantityY):
                                if (j[1][1]-20) < k[0]:
                                    quantityY.insert(index, [j[1][1]-20, j[1][3]+50, item_index] )
                                    inserted = True
                                    break
                            if inserted == False:
                                quantityY.append( [j[1][1]-20, j[1][3]+50, item_index] )
                        break

        # Find X
        """
        for i in stringLoc:
            print(i[0])
            match = re.search('QTY', i[0])
            if match != None:
                secondGnome.echo("found x")
                quantityX = i[1][0] - 10
                quantityW = i[1][2] + 10
        """
        
        if quantityX != 0 and len(quantityY) != 0:
            #secondGnome.echo("draw box")
            for i in quantityY:
                print("quantityY")
                print(i)
                    # [y, h] of item
                cv2.rectangle(img,
                      (quantityX, i[0]),
                      (quantityX + quantityW, i[0] + i[1]),
                      (0, 0, 255), 2)
                cropped = img[i[0]:i[0]+i[1], quantityX:quantityX+quantityW]
           #     cv2.imwrite("cropped.jpg", cropped)
                if cropped.shape[0] and cropped.shape[1]:
                    cv2.imshow("cropped", cv2.resize(cropped,(640,480)))
                    cv2.moveWindow("cropped", 0, 4000)
                #quantityY.append( [j[1][1]-20, j[1][3]+50, item_index] )
                    cropped = cv2.resize(cropped, (int(3.0*cropped.shape[1]),int(3.0*cropped.shape[0])))
                    text = pytesseract.image_to_string(cropped)
                    #secondGnome.echo(text)
                    match = re.search('\s*(\d*,*\d*,*\d*,*\d*,*\d*,*\d*.\d{2,4})\s*.*', text)
                    if match!=None:
                        qty = match.group(1)
                        echoStr = self.itemDetected[i[2]][3]+" | "+qty
                        secondGnome.echo(echoStr)
                        self.itemQuantityToBeDetected[i[2]] = False
    

    def cvBoardInitialize(self, cvMat):
        
        cvMat = cv2.putText(cvMat, self.companyNameFromYaml, (50, 50), font, 
                       fontScale, color, thickness, cv2.LINE_AA)
        cvMat = cv2.putText(cvMat, "T-PO-"+self.po_number, (50, 85), font, 
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


echoOnce = False
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
        

    if d_o.companyNameMatched == False:
        ocr_text = pytesseract.image_to_string(frame)
        if d_o.companyNameFoundFromPO == False:
            d_o.searchCompanyFromPO(ocr_text)
        if d_o.companyNameFoundFromYaml == False:
            d_o.searchCompanyFromYaml(ocr_text)

        if d_o.companyNameFoundFromYaml == True and d_o.companyNameFoundFromPO == True:
            if d_o.companyNameFromYaml == d_o.companyNameFromPO:
                d_o.register(d_o.companyNameFromYaml)
                d_o.cvBoardInitialize(board)
                d_o.companyNameMatched = True
                secondGnome.echo("Company Found From PO number matched with DO")
            else:
                secondGnome.echo("Company Found from PO number not matched with DO")
                d_o.companyNameFoundFromYaml = False
                d_o.companyNameFoundFromPO = False
                d_o.companyNameFromPO = ''
                d_o.companyFromYaml = ''
    else:
        if (d_o.numFieldFound != d_o.numField and d_o.numField != 0) \
                or d_o.dateFound == False\
                or d_o.startSearchItem == True:
            #ocr_text = pytesseract.image_to_string(warped)
            ocr_text = pytesseract.image_to_string(frame)

            if d_o.startSearchItem == True:
                d_o.searchItem(ocr_text)
                if len(d_o.itemDetails) == 0:
                    d_o.startSearchItem = False
                    for item in d_o.itemDetected:
                        d_o.itemQuantityToBeDetected.append(True)
                    d_o.startSearchQuantity = True
            elif d_o.dateFound == False:
                d_o.searchDate(ocr_text)
            else: 
                d_o.search(ocr_text)
        else:
            if echoOnce == False:
                echoOnce = True
                secondGnome.echo("Everything ready, Press i to insert to Database")
        
        if d_o.startSearchQuantity:
            d_o.getQuantity(frame)

    cv2.imshow("Result", board)
    cv2.moveWindow("Result", 650, 0)
    
    if d_o.queried == False and (d_o.numFieldFound == d_o.numField and d_o.numField != 0) and d_o.dateFound == True:
        secondGnome.echo("checkDatabase")
        d_o.checkDatabase()
    
    #cv2.imshow("Warped", cv2.resize(warped, (int(0.75 * warped.shape[1]), int(0.75 * warped.shape[0]))))
    #cv2.moveWindow("Warped", 0, 450)
    x = cv2.getTrackbarPos('x', 'tune')
    x1 = cv2.getTrackbarPos('x1', 'tune')
    y = cv2.getTrackbarPos('y', 'tune')
    y1 = cv2.getTrackbarPos('y1', 'tune')
    cropped = frame[y:y1,x:x1]
    if cropped.shape[0] != 0 and cropped.shape[1] != 0:
        cv2.imshow("cropped", cv2.resize(cropped, (int(3.0*cropped.shape[1]), int(3.0*cropped.shape[0]))))

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
        secondGnome.send('clear')
    elif pressed_key == ord('i'):
        d_o.insertDatabase()
    elif pressed_key == ord('c'):
        test_text = pytesseract.image_to_string(cropped)
        secondGnome.echo(test_text)

cv2.destroyAllWindows()
secondGnome.kill()
