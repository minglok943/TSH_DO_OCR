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
    def __init__(self, debugEnable, showQuantityCrop, insertConfirm):
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
        self.debugString = ''

        self.showQuantityCrop = showQuantityCrop
        self.insertConfirm = insertConfirm

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
        self.doNumFound = False
        self.do_date = ''
        self.dateFound = False
        self.companyNameMatched = False
        self.echoOnce = False
        self.goodsreceiptsnotesExist = False

        self.grnItemList = []
        self.grnItemStringList = []
        self.userName = 'Chia Ming Lok'
        self.grn = {
            "id": 'NULL',
            "grn_number": 'NULL',
            "po_number": 'NULL',
            "supplier_id": 'NULL',
            "supplier_do_number": 'NULL',
            "supplier_inv_number": 'NULL',
            "supplier_inv_date": 'NULL',
            "currency_rate": 'NULL',
            "recieve_by": 'NULL',
            "status": 'NULL',
            "created_at": 'NULL',
            "updated_at": 'NULL',
            "deleted_at": 'NULL',
            "k1_id": 'NULL'
        }

        self.grnItem ={
            "id": 'NULL',
            "grn_id": 'NULL',
            "po_item_id": 'NULL',
            "wo_number": 'NULL',
            "item_id": 'NULL',
            "ordered_quantity": 'NULL',
            "recieving_quantity": 'NULL',
            "status": 'NULL',
            "created_at": 'NULL',
            "updated_at": 'NULL',
            "deleted_at": 'NULL',
            "supinvunitprice": 'NULL',
            "supinvtotal": 'NULL'
        }



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
                    self.debugString += "Company Found From PO number matched with DO\n"
                    if self.debugEnable == True:
                        self.secondGnome.echo("Company Found From PO number matched with DO")
                else:
                    self.debugString += "Company Found From PO number not matched with DO\n"
                    if self.debugEnable == True:
                        self.secondGnome.echo("Company Found from PO number not matched with DO")
                    self.companyNameFoundFromYaml = False
                    self.companyNameFoundFromPO = False
                    self.companyNameFromPO = ''
                    self.companyFromYaml = ''
        else:
            if (self.numFieldFound != self.numField and self.numField != 0) \
                    or self.dateFound == False:
                #ocr_text = pytesseract.image_to_string(warped)
                ocr_text = pytesseract.image_to_string(frame)
                
                if self.dateFound == False:
                    self.searchDate(ocr_text)
                else: 
                    self.search(ocr_text)
            else:
                if self.echoOnce == False:
                    self.echoOnce = True
                    #self.startSearchQuantity = True
                    self.debugString += "Start Search Quantity\n"
                    if self.debugEnable == True:
                        self.secondGnome.echo("Start Search Quantity")
            
            if self.startSearchQuantity:
                self.getQuantity(frame)
        if self.queried == False and (self.numFieldFound == self.numField and self.numField != 0) and self.dateFound == True:
            self.debugString += "Checking Database...\n"
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
                self.debugString += echoStr
                self.debugString += "\n"
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
                self.mySqlTable(qResults, descr)
                self.poId = qResults[0][0]
                self.companyID = qResults[0][1]
                query = 'select name from suppliers where id='+str(self.companyID)
                self.myCursor.execute(query)
                descr = self.myCursor.description
                qResults = self.myCursor.fetchall()
                
                if qResults:
                    self.mySqlTable(qResults, descr)
                    self.companyNameFromPO = qResults[0][0]
                    echoStr = "company Name From PO num = "+self.companyNameFromPO
                    self.debugString += echoStr 
                    self.debugString += "\n"
                    if self.debugEnable == True:
                        self.secondGnome.echo(echoStr)
                    self.companyNameFoundFromPO = True
                    self.po_number = poLike.group(1)
            else:
                self.debugString += "no PO record\n"
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
                    if self.field[i] == 'do_num':
                        self.resStr[i] = self.companyYaml[self.companyNameFromYaml]['do_prefix'] + find.group(1)
                        self.doNumFound = True
                    else:
                        self.resStr[i] = find.group(1)

                    self.fieldFound[i] = 1
                    self.numFieldFound += 1
                    echoStr = self.field[i] + ': ' + self.resStr[i]
                    self.debugString += echoStr
                    self.debugString += "\n"
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
                        self.debugString += echoStr
                        self.debugString += "\n"
                        if self.debugEnable == True:
                            self.secondGnome.echo(echoStr)
                    except ValueError:
                        pass
                if self.do_date != '':
                    self.dateFound = True

    
    def next(self):
        self.debugString = ''
        self.po_number = ''
        self.field.clear()
        self.rePattern.clear()
        self.queried = False
        self.numFieldFound = 0
        self.fieldFound.clear()
        self.resStr.clear()
        self.numField = 0
        self.doNumFound = False
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
        self.grnItemList.clear()
        self.grnItemStringList.clear()
        self.goodsreceiptsnotesExist = False

    def checkDatabase(self):
        self.queried = True
        Q1 = "select id, grn_number, po_number, supplier_id, \
                supplier_do_date, recieve_by, created_at, updated_at\
                from goodsreceiptsnotes where supplier_do_number='"
        query = Q1+self.resStr[0]+'\''
        self.debugString += query
        self.debugString += "\n"
        if self.debugEnable == True:
            self.secondGnome.echo(query)
        self.myCursor.execute(query)
        descr = self.myCursor.description
        qResults = self.myCursor.fetchall()
        
        if qResults:
            self.mySqlTable(qResults, descr)
            if len(qResults) > 1:
                self.debugString += "more than one record\n"
                if self.debugEnable == True:
                    self.secondGnome.echo('more than one record')
            else:
                self.debugString += "Record Found\n"
                if self.debugEnable == True:
                    self.secondGnome.echo('Record Found')
                self.goodsreceiptsnotesExist = True
                self.grn_id = qResults[0][0]
                self.grn_number = qResults[0][1]
                self.grn["id"] = self.grn_id
                self.grn["grn_number"] = self.grn_number
                self.grn["po_number"] = qResults[0][2]
                self.grn["supplier_id"] = qResults[0][3]
                self.grn["supplier_do_number"] = self.resStr[0]
                self.grn["supplier_do_date"] = qResults[0][4]
                self.grn["recieve_by"] = qResults[0][5]
                self.grn["created_at"] = qResults[0][6]
                self.grn["updated_at"] = qResults[0][7]

                self.grnString = ''
                for key, value in self.grn.items():
                    self.grnString += '{:^19}: {}\n'.format(key, value)
                self.grnString = self.grnString[:self.grnString.rfind('\n')]

                query = "select id, po_item_id, item_id, ordered_quantity, recieving_quantity,\
                        created_at, updated_at from goodrecieptsnoteitems where grn_id='"+str(self.grn_id)+"'"
                #secondGnome.echo(query)
                self.myCursor.execute(query)
                exist = self.myCursor.fetchall()
                if exist:
                    for result in exist:
                        grnItemString = ''
                        self.grnItem["id"] = result[0]
                        self.grnItem["grn_id"] = self.grn_id
                        self.grnItem["po_item_id"] = result[1]
                        self.grnItem["item_id"] = result[2]
                        self.grnItem["ordered_quantity"] = result[3]
                        self.grnItem["recieving_quantity"] = result[4]
                        self.grnItem["created_at"] = result[5]
                        self.grnItem["updated_at"] = result[6]
                        self.grnItemList.append(self.grnItem)
                        for key, value in self.grnItem.items():
                            grnItemString += '{:^19}: {}\n'.format(key, value)
                        grnItemString = grnItemString[:grnItemString.rfind('\n')]
                        self.grnItemStringList.append(grnItemString)
                # check if there is record of DO based on do number
                """
                """
        else:
            self.debugString += "No record found\n"
            if self.debugEnable == True:
                self.secondGnome.echo('No record found !!!')
            self.debugString += "Loading item details base on PO ...\n"
            if self.debugEnable == True:
                self.secondGnome.echo('Loading item details based on PO ...')
            self.loadItemDetails()
            self.startSearchQuantity = True
            self.goodsreceiptsnotesExist = False

        """
        self.debugString += "Loading item details base on PO ...\n"
        if self.debugEnable == True:
            self.secondGnome.echo('Loading item details based on PO ...')
        self.loadItemDetails()
        self.startSearchItem = True
        """

    def insertDatabase(self):

        if self.goodsreceiptsnotesExist == False:
            self.myCursor.execute("select id, grn_number from goodsreceiptsnotes order by grn_number desc limit 1")
            qResults = self.myCursor.fetchall()
            self.grn_id = qResults[0][0]+1
            self.grn_number = str(int(qResults[0][1])+1)
            self.debugString += "inserting goodsreceiptsnotes\n"
            if self.debugEnable == True:
                self.secondGnome.echo("inserting goodsreceiptsnotes")
            nowDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            val = (self.grn_id, self.grn_number, self.do_date, self.resStr[0],\
                    self.poId, self.companyID, nowDateTime, nowDateTime)
            self.debugString += "INSERT INTO goodsreceiptsnotes(id, grn_number, supplier_do_date, supplier_do_number, \
                    po_number, supplier_id, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)\n"
            self.debugString += str(val)
            self.debugString += '\n'
            if self.debugEnable == True:
                self.secondGnome.echo(str(val))
            Q3 = "insert into\
            goodsreceiptsnotes(id, grn_number, supplier_do_date, supplier_do_number,\
                                po_number, supplier_id, created_at, updated_at)\
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            self.myCursor.execute(Q3, val)
            if self.insertConfirm == False:
                self.db.commit()
            #self.myCursor.execute("select id, grn_number from goodsreceiptsnotes order by grn_number desc limit 1")
            #qResults = self.myCursor.fetchall()
            #self.grn_id = qResults[0][0]
            self.grn["id"] = self.grn_id
            #else:
            #self.grn["id"] = "AUTO_INCREMENT"
            self.grn["grn_number"] = self.grn_number
            self.grn["po_number"] = self.poId
            self.grn["supplier_id"] = self.companyID
            self.grn["supplier_do_number"] = self.resStr[0]
            self.grn["supplier_do_date"] = self.do_date
            self.grn["recieve_by"] = self.userName
            self.grn["created_at"] = nowDateTime
            self.grn["updated_at"] = nowDateTime
            
            self.grnString = ''
            for key, value in self.grn.items():
                self.grnString += '{:^19}: {}\n'.format(key, value)
            self.grnString = self.grnString[:self.grnString.rfind('\n')]

        else: 
            self.debugString += 'goodsreceiptsnotes record exist\n'
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
                    if index == 0:
                        self.myCursor.execute("select id from goodrecieptsnoteitems order by id desc limit 1")
                        qResults = self.myCursor.fetchall()
                        self.grn_item_id = qResults[0][0]+1
                    else:
                        self.grn_item_id += 1
                    self.debugString += "inserting goodrecieptsnoteitems\n"
                    if self.debugEnable == True:
                        self.secondGnome.echo("inserting goodrecieptsnoteitems")
                    nowDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #if self.insertConfirm == False:
                    Q6 = "insert into goodrecieptsnoteitems(id, grn_id, po_item_id, item_id,\
                            ordered_quantity,recieving_quantity, created_at, updated_at)\
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                    val1 = (self.grn_item_id, self.grn_id, item[0], item[1], item[2], self.itemQuantityToBeDetected[index][1], nowDateTime, nowDateTime)
                    self.debugString += Q6
                    self.debugString += '\n'
                    self.debugString += str(val1)
                    self.debugString += '\n'
                    if self.debugEnable == True:
                        self.secondGnome.echo(str(val1))
                    self.myCursor.execute(Q6, val1)
                    if self.insertConfirm == False:
                        self.db.commit()
                    #self.myCursor.execute("select id from goodrecieptsnoteitems order by id desc limit 1")
                    #qResults = self.myCursor.fetchall()
                    #self.grn_item_id = qResults[0][0]
                    self.grnItem["id"] = self.grn_item_id
                    #else:
                    #    self.grnItem["id"] = "AUTO_INCREMENT"
                    
                    grnItemString = ''
                    self.grnItem["grn_id"] = self.grn_id
                    self.grnItem["po_item_id"] = item[0]
                    self.grnItem["item_id"] = item[1]
                    self.grnItem["ordered_quantity"] = item[2]
                    self.grnItem["recieving_quantity"] = self.itemQuantityToBeDetected[index][1]
                    self.grnItem["created_at"] = nowDateTime
                    self.grnItem["updated_at"] = nowDateTime
                    self.grnItemList.append(self.grnItem)
                    for key, value in self.grnItem.items():
                        grnItemString += '{:^19}: {}\n'.format(key, value)
                    grnItemString = grnItemString[:grnItemString.rfind('\n')]
                    self.grnItemStringList.append(grnItemString)
                else:
                    echoStr = item[3]+"with item_id="+str(item[1])+", po_item_id="+str(item[0])+" exist in goodrecieptsnoteitems"
                    self.debugString += echoStr
                    self.debugString += '\n'
                    if self.debugEnable == True:
                        self.secondGnome.echo(echoStr)
        

    def confirm(self):
        if self.insertConfirm == True:
            """
            # insert goodsreceiptsnotes
            nowDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            val = (self.grn_number, self.do_date, self.resStr[0],\
                    self.poId, self.companyID, nowDateTime, nowDateTime)
            self.debugString += "INSERT INTO goodsreceiptsnotes(grn_number, supplier_do_date, supplier_do_number, \
                    po_number, supplier_id, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)\n"
            self.debugString += str(val)
            self.debugString += '\n'
            if self.debugEnable == True:
                self.secondGnome.echo(str(val))
            Q3 = "insert into\
            goodsreceiptsnotes(grn_number, supplier_do_date, supplier_do_number,\
                                po_number, supplier_id, created_at, updated_at)\
            VALUES (%s,%s,%s,%s,%s,%s,%s)"
            self.myCursor.execute(Q3, val)
            self.db.commit()
            self.myCursor.execute("select id, grn_number from goodsreceiptsnotes order by grn_number desc limit 1")
            qResults = self.myCursor.fetchall()
            self.grn_id = qResults[0][0]
            self.grn["id"] = self.grn_id

            # insert goodrecieptsnoteitems
            for item in self.grnItemList:
                if self.debugEnable == True:
                    self.secondGnome.echo("inserting goodrecieptsnoteitems")
                nowDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Q6 = "insert into goodrecieptsnoteitems(grn_id, po_item_id, item_id,\
                        ordered_quantity,recieving_quantity, created_at, updated_at)\
                VALUES(%s,%s,%s,%s,%s,%s,%s)"
                val1 = (self.grn_id, item["po_item_id"], item["item_id"], item["ordered_quantity"], item["recieving_quantity"], nowDateTime, nowDateTime)
                self.debugString += Q6
                self.debugString += '\n'
                self.debugString += str(val1)
                self.debugString += '\n'
                if self.debugEnable == True:
                    self.secondGnome.echo(str(val1))
                self.myCursor.execute(Q6, val1)
                self.db.commit()
                self.myCursor.execute("select id from goodrecieptsnoteitems order by id desc limit 1")
                qResults = self.myCursor.fetchall()
                self.grn_item_id = qResults[0][0]
                self.grnItem["id"] = self.grn_item_id
            """
            self.db.commit()

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
            self.mySqlTable(res, descr)
            for row in res:
                self.itemDetails.append(row)
          #  print("Load")
           # print(self.itemDetails)
        else:
            self.debugString += 'No PO record or No part_number record\n'
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
                self.debugString += echoStr
                self.debugString += '\n'
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
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
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
                        cv2.rectangle(img, (j[1][0], j[1][1]), (j[1][0]+j[1][2], j[1][1]+j[1][3]), (0, 0, 255), 2)
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
                        # eliminate possible error eg. 50.04 -> 50.00
                        qty = str(int(float(qty)))+'.00'
                        echoStr = self.itemDetected[i[2]][3]+" | "+qty
                        self.debugString += echoStr
                        self.debugString += '\n'
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
        self.debugString += seperator
        self.debugString += '\n'
        if self.debugEnable == True:
            self.secondGnome.echo(seperator)
        tmp = tavnit % tuple(columns)
        #print(tmp)
        self.debugString += tmp
        self.debugString += '\n'
        if self.debugEnable == True:
            self.secondGnome.echo(tmp)
        #print(seperator)
        self.debugString += seperator
        self.debugString += '\n'
        if self.debugEnable == True:
            self.secondGnome.echo(seperator)
        for row in results:
            tmp = tavnit % row
            #print(tmp)
            self.debugString += tmp
            self.debugString += '\n'
            if self.debugEnable == True:
                self.secondGnome.echo(tmp)
        #print(seperator)
        self.debugString += seperator
        self.debugString += '\n'
        if self.debugEnable == True:
            self.secondGnome.echo(seperator)
##################################################################################################

