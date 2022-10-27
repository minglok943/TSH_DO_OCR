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

class DO:
    def __init__(self, debugEnable, showQuantityCrop):
        with open('templateDO7.yaml', 'r') as file:
            self.companyYaml = yaml.safe_load(file)

        self.db = mysql.connect(
                host="localhost",
                user="lokcharming",
                passwd="asdfasdf",
                database="ERP"
                )

        self.myCursor = self.db.cursor()
        
        self.board = np.zeros((360,900,3), np.uint8)

        self.debugEnable = debugEnable
        if self.debugEnable == True:
            self.secondGnome = Term(width=105,height=31)
        
        self.showQuantityCrop = showQuantityCrop
        self.po_number = ''
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
        self.echoOnce = False

    def run(self, frame):
        if self.companyNameMatched == False:
            ocr_text = pytesseract.image_to_string(frame)
            if self.companyNameFoundFromPO == False:
                self.searchCompanyFromPO(ocr_text)
            if self.companyNameFoundFromYaml == False:
                self.searchCompanyFromYaml(ocr_text)

            if self.companyNameFoundFromYaml == True and self.companyNameFoundFromPO == True:
                if self.companyNameFromYaml == self.companyNameFromPO:
                    self.register(self.companyNameFromYaml)
                    self.cvBoardInitialize()
                    self.companyNameMatched = True
                    if self.debugEnable == True:
                        self.secondGnome.echo("Company Found From PO number matched with DO")
                else:
                    if self.debugEnable == True:
                        self.secondGnome.echo("Company Found from PO number not matched with DO")
                    self.companyNameFoundFromYaml = False
                    self.companyNameFoundFromPO = False
                    self.companyNameFromPO = ''
                    self.companyFromYaml = ''
        else:
            if (self.numFieldFound != self.numField and self.numField != 0) \
                    or self.dateFound == False:
                
                """
                    or self.startSearchItem == True:
                """

                #ocr_text = pytesseract.image_to_string(warped)
                ocr_text = pytesseract.image_to_string(frame)
    
                """
                if self.startSearchItem == True:
                    self.searchItem(ocr_text)
                    if len(self.itemDetected) != 0:
                        self.startSearchQuantity = True
                        if len(self.itemQuantityToBeDetected) != len(self.itemDetected):
                            diff = len(self.itemDetected)-len(self.itemQuantityToBeDetected)
                            for i in range(0, diff):
                                self.itemQuantityToBeDetected.append([True,0])

                    if len(self.itemDetails) == 0:
                        self.startSearchItem = False
                    
                        for item in self.itemDetected:
                            #itemQuantityToBeDetected[0] = True/False
                            #itemQuantityToBeDetected[1] = quantity
                            self.itemQuantityToBeDetected.append([True,0])
                        self.startSearchQuantity = True
                """

                if self.dateFound == False:
                    self.searchDate(ocr_text)
                else: 
                    self.search(ocr_text)
            else:
                if self.echoOnce == False:
                    self.echoOnce = True
                    self.startSearchQuantity = True
                    if self.debugEnable == True:
                        self.secondGnome.echo("Start Search Quantity")
            
            if self.startSearchQuantity:
                self.getQuantity(frame)
        if self.queried == False and (self.numFieldFound == self.numField and self.numField != 0) and self.dateFound == True:
            if self.debugEnable == True:
                self.secondGnome.echo("checkDatabase")
            self.checkDatabase()

    def searchCompanyFromYaml(self, text):
        self.companyID = 0 # my own index, not same with the database company id
        for i in self.companyYaml['companies']:
            comStr = re.search(i[1], text)
            if comStr != None:
                #print("Company id ", i[0])
                #print("Company is ", i[2])
                self.companyNameFromYaml = i[2]
                self.companyNameFoundFromYaml = True
                echoStr = 'Company Detected: '+self.companyNameFromYaml
                if self.debugEnable == True:
                    self.secondGnome.echo(echoStr)
                #print(comStr.group())
                #self.register(self.companyName)
                #self.cvBoardInitialize(board)
            else:
                self.companyID += 1

    def searchCompanyFromPO(self, text):
        poLike = re.search('T-P[0,O]-(\d{8})',text)
        if poLike != None:
            query = 'select id, supplier_id from purchase_orders where po_number=\''+poLike.group(1)+'\''
            self.myCursor.execute(query)
            descr = self.myCursor.description
            qResults = self.myCursor.fetchall()
            if qResults:
                if self.debugEnable == True:
                    self.mySqlTable(qResults, descr)
                self.poId = qResults[0][0]
                self.companyID = qResults[0][1]
                query = 'select name from suppliers where id='+str(self.companyID)
                self.myCursor.execute(query)
                descr = self.myCursor.description
                qResults = self.myCursor.fetchall()
                
                if qResults:
                    if self.debugEnable == True:
                        self.mySqlTable(qResults, descr)
                    self.companyNameFromPO = qResults[0][0]
                    echoStr = "company Name From PO num = "+self.companyNameFromPO
                    if self.debugEnable == True:
                        self.secondGnome.echo(echoStr)
                    self.companyNameFoundFromPO = True
                    self.po_number = poLike.group(1)
            else:
                if self.debugEnable == True:
                    self.secondGnome.echo("no PO record")

    def register(self, compName):
        for key, rePattern in self.companyYaml[compName]['regex'].items():
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
                                self.companyYaml[self.companyNameFromYaml]['date_format']).date()
                        self.resStr[i] = self.realDate.strftime('%Y-%m-%d')
                    elif self.field[i] == 'do_num':
                        self.resStr[i] = self.companyYaml[self.companyNameFromYaml]['do_prefix'] + find.group(1)
                    else:
                        self.resStr[i] = find.group(1)

                    self.fieldFound[i] = 1
                    self.numFieldFound += 1
                    echoStr = self.field[i] + ': ' + self.resStr[i]
                    if self.debugEnable == True:
                        self.secondGnome.echo(echoStr)
                    self.cvBoardShowRes(i)

    def searchDate(self, text):
        for i in self.companyYaml['date_format']:
            dateMatch = re.findall(i[0], text)
            if dateMatch != None:
                for j in dateMatch:
                    datestr = j
                    datestr = datestr.replace(" ", "")
                    try:
                        realDate = datetime.strptime(datestr, i[1]).date()
                        self.do_date = realDate.strftime('%Y-%m-%d')
                        echoStr = "do_date = "+self.do_date
                        if self.debugEnable == True:
                            self.secondGnome.echo(echoStr)
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
        self.board = np.zeros((360,900,3), np.uint8)
        self.echoOnce = False
        if self.debugEnable == True:
            self.secondGnome.send('clear')

    def checkDatabase(self):
        self.queried = True
        Q1 = "select id, grn_number, po_number, supplier_id\
        from goodsreceiptsnotes where supplier_do_number='"
        query = Q1+self.resStr[0]+'\''
        if self.debugEnable == True:
            self.secondGnome.echo(query)
        self.myCursor.execute(query)
        descr = self.myCursor.description
        qResults = self.myCursor.fetchall()
        
        if qResults:
            if self.debugEnable == True:
                self.mySqlTable(qResults, descr)
            if len(qResults) > 1:
                if self.debugEnable == True:
                    self.secondGnome.echo('more than one record')
            else:
                if self.debugEnable == True:
                    self.secondGnome.echo('Record Found')
                self.goodsreceiptsnotesExist = True
                self.grn_id = qResults[0][0]
                # check if there is record of DO based on do number
                """
                if self.resStr[0] == qResults[0][1]:
                    #self.loadItemDetails()
                    #self.startSearchItem = True
                """
        else:
            if self.debugEnable == True:
                self.secondGnome.echo('No record found !!!')
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
        if self.debugEnable == True:
            self.secondGnome.echo('Loading item details based on PO ...')
        self.loadItemDetails()
        self.startSearchItem = True

    def insertDatabase(self):

        if self.goodsreceiptsnotesExist == False:
            self.myCursor.execute("select id, grn_number from goodsreceiptsnotes order by grn_number desc limit 1")
            qResults = self.myCursor.fetchall()
            self.grn_id = qResults[0][0]+1
            self.grn_number = str(int(qResults[0][1])+1)
            if self.debugEnable == True:
                self.secondGnome.echo("inserting goodsreceiptsnotes")
            val = (self.grn_number, self.do_date, self.resStr[0],\
                    self.poId, self.companyID)
            if self.debugEnable == True:
                self.secondGnome.echo(str(val))
            Q3 = "insert into\
            goodsreceiptsnotes(grn_number, supplier_do_date, supplier_do_number,\
                                po_number, supplier_id)\
            VALUES (%s,%s,%s,%s,%s)"
            self.myCursor.execute(Q3, val)
            db.commit()
        else: 
            if self.debugEnable == True:
                self.secondGnome.echo("goodsreceiptsnotes record exist")

        # itemDetails[0] = purchase_order_items.id
        # itemDetails[1] = purchase_order_items.item_id
        # itemDetails[2] = purchase_order_items.quantity
        # itemDetails[3] = inventories.part_number
        #print("self.itemDetected")
        #print(self.itemDetected)
        for index, item in enumerate(self.itemDetected):
            if self.itemQuantityToBeDetected[index][0] == False:
                query = "select grn_id from goodrecieptsnoteitems where po_item_id='"+str(item[0])+"'"
                #secondGnome.echo(query)
                self.myCursor.execute(query)
                exist = self.myCursor.fetchall()
                #print(exist)
                if not exist:
                    if self.debugEnable == True:
                        self.secondGnome.echo("inserting goodrecieptsnoteitems")
                    Q6 = "insert into goodrecieptsnoteitems(grn_id, po_item_id, item_id, ordered_quantity,recieving_quantity)\
                    VALUES(%s,%s,%s,%s,%s)"
                    val1 = (self.grn_id, item[0], item[1], item[2], self.itemQuantityToBeDetected[index][1])
                    if self.debugEnable == True:
                        self.secondGnome.echo(str(val1))
                    self.myCursor.execute(Q6, val1)
                    db.commit()
                else:
                    echoStr = item[3]+"with item_id="+str(item[1])+", po_item_id="+str(item[0])+" exist in goodrecieptsnoteitems"
                    if self.debugEnable == True:
                        self.secondGnome.echo(echoStr)
        
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
        self.myCursor.execute(Q4)
        self.myCursor.execute(Q5)
        self.myCursor.execute(Q6)
        descr = self.myCursor.description
        res = self.myCursor.fetchall()

        if res:
            if self.debugEnable == True:
                self.mySqlTable(res, descr)
            for row in res:
                self.itemDetails.append(row)
          #  print("Load")
           # print(self.itemDetails)
        else:
            if self.debugEnable == True:
                self.secondGnome.echo("No PO record or No part_number record !!!")

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
                if self.debugEnable == True:
                    self.secondGnome.echo(echoStr)
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

        # Sorting string according to y coordinate to stringLoc
        # stringLoc = [text, (x,y,w,h)]
        for i in range(0, len(data['text'])):
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            text = data['text'][i]
            text = "".join(text).strip()
            for ele in self.companyYaml['quantity_format']:
                match = re.search(ele[0], text)
                if match != None:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #self.secondGnome.echo("found x")
                    #secondGnome.echo(match.group())
                    #print(text)
                    quantityX = x - 20
                    quantityW = w + 50
                    #print("x = ", quantityX)
                    #print("w = ", quantityW)
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
        
        # Find ITEM #############################################################
        record = []
        # itemDetails[0] = purchase_order_items.id
        # itemDetails[1] = purchase_order_items.item_id
        # itemDetails[2] = purchase_order_items.quantity
        # itemDetails[3] = inventories.part_number
        for index, item_detail in enumerate(self.itemDetails):
            itemRegex = genRegexCapitalInsensitive(self.itemDetails[index][3])
            itemFound = False
            for j in stringLoc:
                match = re.search(itemRegex, j[0])
                if match != None:
                    itemFound = True
                    self.itemDetected.append(item_detail)
                    self.itemQuantityToBeDetected.append([True,0])
                    echoStr = 'Found item with id '+str(item_detail[1])\
                        +' \''+item_detail[3]+'\''
                    if self.debugEnable == True:
                        self.secondGnome.echo(echoStr)
                    break
            if itemFound == False:
                record.append(index) ## remaining 

        temp = self.itemDetails.copy()
        self.itemDetails.clear()
        for i in record:
            self.itemDetails.append(temp[i])
        ########################################################################

        # Find Y
        for item_index, i in enumerate(self.itemDetected):
            for j in stringLoc:
                if self.itemQuantityToBeDetected[item_index][0] == True:
                    match = re.search(genRegexCapitalInsensitive(i[3]), j[0])
                    if match != None:
                        # [y, h] of item
                        #self.secondGnome.echo("found y")
                        cv2.rectangle(img, (j[1][0], j[1][1]), (j[1][0]+j[1][2], j[1][1]+j[1][3]), (0, 255, 0), 2)
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
                #print("quantityY")
                #print(i)
                    # [y, h] of item
                cv2.rectangle(img,
                      (quantityX, i[0]),
                      (quantityX + quantityW, i[0] + i[1]),
                      (0, 255, 0), 2)
                cropped = img[i[0]:i[0]+i[1], quantityX:quantityX+quantityW]
           #     cv2.imwrite("cropped.jpg", cropped)
                if cropped.shape[0] and cropped.shape[1]:
                    if self.showQuantityCrop == True:
                        cv2.imshow("cropped", cv2.resize(cropped,(640,480)))
                        cv2.moveWindow("cropped", 0, 4000)
                #quantiteY.append( [j[1][1]-20, j[1][3]+50, item_index] )
                    cropped = cv2.resize(cropped, (int(3.0*cropped.shape[1]),int(3.0*cropped.shape[0])))
                    text = pytesseract.image_to_string(cropped)
                    #secondGnome.echo(text)
                    match = re.search('\s*(\d*,*\d*,*\d*,*\d*,*\d*,*\d*.\d{2,4})\s*.*', text)
                    if match!=None:
                        qty = match.group(1)
                        echoStr = self.itemDetected[i[2]][3]+" | "+qty
                        if self.debugEnable == True:
                            self.secondGnome.echo(echoStr)
                        self.itemQuantityToBeDetected[i[2]][0] = False
                        self.itemQuantityToBeDetected[i[2]][1] = qty

        if len(self.itemDetails) == 0:
            count = 0
            for boolean in self.itemQuantityToBeDetected:
                if boolean[0] == False:
                    count += 1
            if count == len(self.itemQuantityToBeDetected):
                self.startSearchQuantity = False

    def cvBoardInitialize(self):
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 255, 0)
        thickness = 2
        offset = 35

        self.board = cv2.putText(self.board, self.companyNameFromYaml, (50, 50), font, 
                       fontScale, color, thickness, cv2.LINE_AA)
        self.board = cv2.putText(self.board, "T-PO-"+self.po_number, (50, 85), font, 
               fontScale, color, thickness, cv2.LINE_AA)

        for i in range(0, self.numField):
            self.board = cv2.putText(self.board, self.field[i]+'  :  ', (50, 120+offset*i), font, 
                       fontScale, color, thickness, cv2.LINE_AA)

    def cvBoardShowRes(self, i):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 255, 0)
        thickness = 2
        offset = 35
        self.board = cv2.putText(self.board, self.resStr[i], (450, 120+offset*i), font, 
                       fontScale, color, thickness, cv2.LINE_AA)

    def mySqlTable(self, results, description):
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
        #print(seperator)
        self.secondGnome.echo(seperator)
        tmp = tavnit % tuple(columns)
        #print(tmp)
        self.secondGnome.echo(tmp)
        #print(seperator)
        self.secondGnome.echo(seperator)
        for row in results:
            tmp = tavnit % row
            #print(tmp)
            self.secondGnome.echo(tmp)
        #print(seperator)
        self.secondGnome.echo(seperator)
##################################################################################################

