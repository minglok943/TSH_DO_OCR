#!/usr/bin/env python3

import time
import sys
import math
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtTest

from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

import cv2
from DO_Processing import DO

import res1

class loginWindow(QMainWindow):
    def __init__(self):
        super(loginWindow, self).__init__()
        uic.loadUi('login2.ui', self)        #load the .ui file made from Qt designer -- you can also use pyside-uic -o outpit.py input.ui on terminal to see your .ui file converted to python objects.

     #   self.label.setPixmap(QPixmap('tsh.png').scaled(self.logoLabel.size(), Qt.KeepAspectRatio))
        self.logoLabel.setPixmap(QPixmap('logo.PNG').scaled(self.logoLabel.size(), Qt.KeepAspectRatio))
        self.loginButton.clicked.connect(self.loginCheck)
        self.passwordEdit.editingFinished.connect(self.focusOnLoginButton)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        self.loginButton.setShortcut('Return')
        self.errorEdit.hide()
        self.DO_check_login = DO(debugEnable=False, showQuantityCrop=False, insertConfirm=True)

    def loginCheck(self):
        userID = self.userEdit.text()
        password = self.passwordEdit.text()
        query = "select * from users where staff_id=%s and password=%s"
        val = (userID, password)
        self.DO_check_login.myCursor.execute(query, val)
        res = self.DO_check_login.myCursor.fetchall()
        if res:
            self.MyWindow = MyWindow()
            self.MyWindow.show()
            self.close()
        else:
            self.errorEdit.show()
            QtTest.QTest.qWait(888)
            self.errorEdit.hide()
            self.passwordEdit.setText('')
            if self.userEdit.text() != "":
                self.passwordEdit.setFocus()
        
    def focusOnLoginButton(self):
        self.loginButton.setFocus()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

        #def userIdKeyIn(self):
         #   self.userIdEdit.setText('')


class detailWindow(QMainWindow):
    def __init__(self, Worker, exist):

        #Qt Stuff..
        super(detailWindow, self).__init__()
        uic.loadUi('detail3.ui', self)        #load the .ui file made from Qt designer -- you can also use pyside-uic -o outpit.py input.ui on terminal to see your .ui file converted to python objects.

        # move to center of screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        self.exist = exist
        self.Worker1 = Worker
        self.d_o = Worker.d_o
        self.vbox = QVBoxLayout()
        length = 1+len(self.d_o.grnItemStringList)+len(self.d_o.siStringList)\
                +len(self.d_o.silStringList)+len(self.d_o.sitStringList)
        self.hboxList = []
        for i in range(0, math.ceil(length/3)):
            self.hboxList.append(QHBoxLayout())

        member = 0
        index = 0
        pilWidth = 381
        pilHeight = 281

        plain = QPlainTextEdit()
        font = QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        plain.setFont(font)

        plain.setGeometry(QRect(60, 50, pilWidth, pilHeight))

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(plain.sizePolicy().hasHeightForWidth())
        plain.setSizePolicy(sizePolicy)
        plain.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        plain.setMinimumSize(QSize(pilWidth, pilHeight))

        plain.setStyleSheet("border-width: 2px;\n"
                            "border-radius: 20px;\n"
                            "background-color: rgb(80, 200, 120);")

        plain.setPlainText(self.d_o.grnString)
        self.hboxList[index].addWidget(plain)
        member += 1
        #self.plainTextEdit_4.setPlainText(self.d_o.grnString)
        
        for i in range(member,member+len(self.d_o.grnItemStringList)):
            plain = QPlainTextEdit()
            font = QFont()
            font.setFamily("Ubuntu Mono")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            plain.setFont(font)

            plain.setGeometry(QRect(60, 50, pilWidth, pilHeight))

            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(plain.sizePolicy().hasHeightForWidth())
            plain.setSizePolicy(sizePolicy)
            plain.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            plain.setMinimumSize(QSize(pilWidth, pilHeight))

            plain.setStyleSheet("border-width: 2px;\n"
                                "border-radius: 20px;\n"
                                "background-color: rgb(114, 159, 207);")

            plain.setPlainText(self.d_o.grnItemStringList[i-member])
            if i%3 == 0 and i!=0:
                index = index + 1
            self.hboxList[index].addWidget(plain)
        
        member += len(self.d_o.grnItemStringList)

        # stock_inventories
        for i in range(member,member+len(self.d_o.siStringList)):
            plain = QPlainTextEdit()
            font = QFont()
            font.setFamily("Ubuntu Mono")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            plain.setFont(font)

            plain.setGeometry(QRect(60, 50, pilWidth, pilHeight))

            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(plain.sizePolicy().hasHeightForWidth())
            plain.setSizePolicy(sizePolicy)
            plain.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            plain.setMinimumSize(QSize(pilWidth, pilHeight))

            plain.setStyleSheet("border-width: 2px;\n"
                                "border-radius: 20px;\n"
                                "background-color: rgb(245, 121, 0);")

            plain.setPlainText(self.d_o.siStringList[i-member])
            if i%3 == 0 and i!=0:
                index = index + 1
            self.hboxList[index].addWidget(plain)
        
        member += len(self.d_o.siStringList)

        # stock_inventory_locations
        for i in range(member,member+len(self.d_o.silStringList)):
            plain = QPlainTextEdit()
            font = QFont()
            font.setFamily("Ubuntu Mono")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            plain.setFont(font)

            plain.setGeometry(QRect(60, 50, pilWidth, pilHeight))

            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(plain.sizePolicy().hasHeightForWidth())
            plain.setSizePolicy(sizePolicy)
            plain.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            plain.setMinimumSize(QSize(pilWidth, pilHeight))

            plain.setStyleSheet("border-width: 2px;\n"
                                "border-radius: 20px;\n"
                                "background-color: rgb(173, 127, 168);")

            plain.setPlainText(self.d_o.silStringList[i-member])
            if i%3 == 0 and i!=0:
                index = index + 1
            self.hboxList[index].addWidget(plain)
        
        member += len(self.d_o.silStringList)

        # stock_inventory_transactions
        for i in range(member,member+len(self.d_o.sitStringList)):
            plain = QPlainTextEdit()
            font = QFont()
            font.setFamily("Ubuntu Mono")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            plain.setFont(font)

            plain.setGeometry(QRect(60, 50, pilWidth, pilHeight))

            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(plain.sizePolicy().hasHeightForWidth())
            plain.setSizePolicy(sizePolicy)
            plain.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            plain.setMinimumSize(QSize(pilWidth, pilHeight))

            plain.setStyleSheet("border-width: 2px;\n"
                                "border-radius: 20px;\n"
                                "background-color: rgb(252, 233, 79);")

            plain.setPlainText(self.d_o.sitStringList[i-member])
            if i%3 == 0 and i!=0:
                index = index + 1
            self.hboxList[index].addWidget(plain)
        
        member += len(self.d_o.sitStringList)

        for hbox in self.hboxList:
            self.vbox.addLayout(hbox)
        self.scrollAreaWidgetContents.setLayout(self.vbox)

        self.confirmButton.clicked.connect(self.on_click_confirm)
        self.cancelButton.clicked.connect(self.on_click_cancel)
        
        if self.exist == True:
            self.confirmButton.hide()
            self.cancelButton.setText("Quit")
        #else:
            #self.statusText.hide()

    def on_click_confirm(self):
        self.d_o.confirm()
        self.close()

    def on_click_cancel(self):
        self.close()
        if self.exist == True:
            self.d_o.next()
            self.Worker1.statusPo = False
            self.Worker1.statusCmp = False
            self.Worker1.statusDoDate = False
            self.Worker1.statusDoNumber = False
            self.Worker1.statusItem = False
            self.Worker1.lastItemDetectedCount = 0
            self.Worker1.lastQuantityDetectedCount = 0
            self.Worker1.statusQuantity.clear()
            self.Worker1.lastDebugString = ''
            self.Worker1.statusDoExist = False

    def closeEvent(self,event):
        if self.exist == True:
            self.d_o.next()
            self.Worker1.statusPo = False
            self.Worker1.statusCmp = False
            self.Worker1.statusDoDate = False
            self.Worker1.statusDoNumber = False
            self.Worker1.statusItem = False
            self.Worker1.lastItemDetectedCount = 0
            self.Worker1.lastQuantityDetectedCount = 0
            self.Worker1.statusQuantity.clear()
            self.Worker1.lastDebugString = ''
            self.Worker1.statusDoExist = False



class MyWindow(QWidget):
    def __init__(self):

        #Qt Stuff..
        super(MyWindow, self).__init__()
        uic.loadUi('DO.ui', self)        #load the .ui file made from Qt designer -- you can also use pyside-uic -o outpit.py input.ui on terminal to see your .ui file converted to python objects.

        # move to center of screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.itemComboList = [self.comboBox0, self.comboBox1, self.comboBox2, self.comboBox3,
                          self.comboBox4, self.comboBox5, self.comboBox6, self.comboBox7,
                          self.comboBox8, self.comboBox9, self.comboBox10, self.comboBox11
                        ]
        self.orderedEditList = [self.orderedEdit0, self.orderedEdit1, self.orderedEdit2, self.orderedEdit3,
                          self.orderedEdit4, self.orderedEdit5, self.orderedEdit6, self.orderedEdit7,
                          self.orderedEdit8, self.orderedEdit9, self.orderedEdit10, self.orderedEdit11
                        ]
        self.receivedEditList = [self.receivedEdit0, self.receivedEdit1, self.receivedEdit2, self.receivedEdit3,
                          self.receivedEdit4, self.receivedEdit5, self.receivedEdit6, self.receivedEdit7,
                          self.receivedEdit8, self.receivedEdit9, self.receivedEdit10, self.receivedEdit11
                        ]
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker1.poNumberUpdate.connect(self.update_po_number)
        self.Worker1.companyNameUpdate.connect(self.update_company_name)
        self.Worker1.doDateUpdate.connect(self.update_do_date)
        self.Worker1.doNumberUpdate.connect(self.update_do_number)
        self.Worker1.itemAdd.connect(self.add_item)
        self.Worker1.itemAddDetected.connect(self.add_detected_item)
        self.Worker1.itemQuantityUpdate.connect(self.add_quantity)
        self.Worker1.infoUpdate.connect(self.update_info)
        self.Worker1.doExist.connect(self.showExist)
        self.Worker1.fpsSig.connect(self.showFps)

        
         
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.poRetakeButton.clicked.connect(self.on_click_PO)
        self.companyNameRetakeButton.clicked.connect(self.on_click_companyName)
        self.doDateRetakeButton.clicked.connect(self.on_click_do_date)
        self.doNumberRetakeButton.clicked.connect(self.on_click_do_number)

        self.insertButton.clicked.connect(self.on_click_insert)
        self.insertButton.setShortcut('Ctrl+\\')

        self.nextButton.clicked.connect(self.on_click_next)
        self.nextButton.setShortcut('Ctrl+Return')

        self.tPOLineEdit.editingFinished.connect(self.po_key_in)
        self.companyNameLineEdit.editingFinished.connect(self.companyName_key_in)
        self.dO_dateLineEdit.editingFinished.connect(self.doDate_key_in)
        self.dO_numberLineEdit.editingFinished.connect(self.doNumber_key_in)
        self.receivedEditList[0].editingFinished.connect(self.quantity_key_in_0)
        self.receivedEditList[1].editingFinished.connect(self.quantity_key_in_1)
        self.receivedEditList[2].editingFinished.connect(self.quantity_key_in_2)
        self.receivedEditList[3].editingFinished.connect(self.quantity_key_in_3)
        self.receivedEditList[4].editingFinished.connect(self.quantity_key_in_4)
        self.receivedEditList[5].editingFinished.connect(self.quantity_key_in_5)
        self.receivedEditList[6].editingFinished.connect(self.quantity_key_in_6)
        self.receivedEditList[7].editingFinished.connect(self.quantity_key_in_7)
        self.receivedEditList[8].editingFinished.connect(self.quantity_key_in_8)
        self.receivedEditList[9].editingFinished.connect(self.quantity_key_in_9)
        self.receivedEditList[10].editingFinished.connect(self.quantity_key_in_10)
        self.receivedEditList[11].editingFinished.connect(self.quantity_key_in_11)

        self.logoLabel.setPixmap(QPixmap('logo.PNG').scaled(self.logoLabel.size(), Qt.KeepAspectRatio))
        self.infoTextBrowser.setReadOnly(True)

        self.tPOLineEdit.setFocus()

    def po_key_in(self):
        print(self.tPOLineEdit.text())

    def companyName_key_in(self):
        print(self.companyNameLineEdit.text())

    def doDate_key_in(self):
        print(self.dO_dateLineEdit.text())

    def doNumber_key_in(self):
        print(self.dO_numberLineEdit.text())

    def quantity_key_in_0(self):
        index = 0
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_1(self):
        index = 1
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_2(self):
        index = 2
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_3(self):
        index = 3
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_4(self):
        index = 4
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_5(self):
        index = 5
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_6(self):
        index = 6
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_7(self):
        index = 7
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_8(self):
        index = 8
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_9(self):
        index = 9
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_10(self):
        index = 10
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())

    def quantity_key_in_11(self):
        index = 11
        qty = self.receivedEditList[index].text()
        if qty != '':
            self.Worker1.d_o.itemQuantityToBeDetected[index][0] = False
            if qty.isdigit():
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = qty+'.00'
                self.receivedEditList[index].setText(qty+'.00')
            else:
                self.Worker1.d_o.itemQuantityToBeDetected[index][1] = self.receivedEditList[0].text()
            print(self.receivedEditList[index].text())


    @pyqtSlot()
    def on_click_PO(self):
        print('retake PO')
        self.tPOLineEdit.setText('')
        self.Worker1.d_o.po_number = ''
        self.Worker1.d_o.companyNameFoundFromPO = False

        """
        self.cb = QComboBox()
        self.ord = QLineEdit()
        self.rec = QLinedit()
        self.itemComboVLayout.addWidget(self.cb)
        self.orderedVLayout.addWidget(self.ord)
        self.receivedVLayout.addWidget(self.rec)
        self.itemVLayout.addStretch(1)
        """

    def on_click_companyName(self):
        print('retake companyName')
        self.companyNameLineEdit.setText('')
        self.Worker1.d_o.companyNameFoundFromYaml = False
    
    def on_click_do_date(self):
        print('retake do date')
        self.dO_dateLineEdit.setText('')
        self.Worker1.d_o.dateFound = False
    
    def on_click_do_number(self):
        print('retake do number')
        self.dO_numberLineEdit.setText('')
        self.Worker1.d_o.numFieldFound = 0
    
    def on_click_insert(self):
        self.Worker1.d_o.insertDatabase()
        if self.Worker1.d_o.insertConfirm == True:
            self.detWin = detailWindow(self.Worker1, exist=False)
            self.detWin.show()

    def on_click_next(self):
        self.tPOLineEdit.setText('')
        self.companyNameLineEdit.setText('')
        self.dO_dateLineEdit.setText('')
        self.dO_numberLineEdit.setText('')
        for i in range(0, len(self.Worker1.d_o.itemDetected)):
            self.itemComboList[i].clear()
            self.orderedEditList[i].setText('')
            self.receivedEditList[i].setText('')
        self.Worker1.d_o.next()
        self.Worker1.statusPo = False
        self.Worker1.statusCmp = False
        self.Worker1.statusDoDate = False
        self.Worker1.statusDoNumber = False
        self.Worker1.statusItem = False
        self.Worker1.lastItemDetectedCount = 0
        self.Worker1.lastQuantityDetectedCount = 0
        self.Worker1.statusQuantity.clear()
        self.Worker1.lastDebugString = ''
        self.Worker1.statusDoExist = False

    def ImageUpdateSlot(self, Image):
        self.feedLabel.setPixmap(QPixmap.fromImage(Image))

    def update_po_number(self, text):
        self.tPOLineEdit.setText(text)
        self.companyNameLineEdit.setFocus()

    def update_company_name(self, text):
        self.companyNameLineEdit.setText(text)
        self.dO_dateLineEdit.setFocus()

    def update_do_date(self, text):
        self.dO_dateLineEdit.setText(text)
        self.dO_numberLineEdit.setFocus()

    def update_do_number(self, text):
        self.dO_numberLineEdit.setText(text)
        self.receivedEditList[0].setFocus()

    def add_item(self, itemDetails):
        for i in range(0, len(itemDetails)):
            for item in itemDetails:
                # itemDetails[0] = purchase_order_items.id        (int)
                # itemDetails[1] = purchase_order_items.item_id   (int)
                # itemDetails[2] = purchase_order_items.quantity  (float)
                # itemDetails[3] = inventories.part_number        (str)
                self.itemComboList[i].addItem(item[3])
            self.itemComboList[i].addItem('Press to select ...')
            self.itemComboList[i].setCurrentText('Press to select ...')
            self.itemComboList[i].currentIndexChanged.connect(self.onItemIndexChanged)

    def add_detected_item(self, itemDetected):
        #print(itemDetected)
        for index, item in enumerate(itemDetected):
            self.itemComboList[index].setCurrentText(item[3])
            self.orderedEditList[index].setText(str(item[2]))

    def add_quantity(self, index, quantity):
        self.receivedEditList[index].setText(quantity)

    def update_info(self, info):
        self.infoTextBrowser.setText(info)

        self.scrollbar = self.infoTextBrowser.verticalScrollBar()
        try:
            time.sleep(0.1) #needed for the refresh
            self.scrollbar.setValue(10000) #try input different high value

        except:
            pass #when it is not available

    def showExist(self):
        self.detWin = detailWindow(self.Worker1, exist=True)
        self.detWin.show()
        self.tPOLineEdit.setText('')
        self.companyNameLineEdit.setText('')
        self.dO_dateLineEdit.setText('')
        self.dO_numberLineEdit.setText('')
        for i in range(0, len(self.Worker1.d_o.itemDetected)):
            self.itemComboList[i].clear()
            self.orderedEditList[i].setText('')
            self.receivedEditList[i].setText('')

    def showFps(self, fps):
        self.fpsLabel.setText(str(fps))

    def onItemIndexChanged(self, id):
        #print("currentIndex:", id)
        self.orderedEditList[id].setText(str(self.Worker1.d_o.itemDetails[id][2]))
        self.Worker1.d_o.itemDetected.append(self.Worker1.d_o.itemDetails[id])
        self.Worker1.d_o.itemQuantityToBeDetected.append([True,0])
        del self.Worker1.d_o.itemDetails[id]

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
      
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    poNumberUpdate = pyqtSignal(str)
    statusPo = False
    companyNameUpdate = pyqtSignal(str)
    statusCmp = False
    doDateUpdate = pyqtSignal(str)
    statusDoDate = False
    doNumberUpdate = pyqtSignal(str)
    statusDoNumber = False
    itemAdd = pyqtSignal(list)
    statusItem = False
    itemAddDetected = pyqtSignal(list)
    lastItemDetectedCount = 0
    itemQuantityUpdate = pyqtSignal(int ,str)
    lastQuantityDetectedCount = 0
    statusQuantity = []
    infoUpdate = pyqtSignal(str)
    lastDebugString = ''
    doExist = pyqtSignal(bool)
    statusDoExist = False
    fpsSig = pyqtSignal(int)

    def run(self):
        self.ThreadActive = True
        WIDTH, HEIGHT = 1280, 720
        Capture = cv2.VideoCapture(0,cv2.CAP_V4L2)

        """
        WIDTH, HEIGHT = 640, 480
        Capture = cv2.VideoCapture(3,cv2.CAP_V4L2)
        """

        Capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        Capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        print("fps: ", Capture.get(cv2.CAP_PROP_FPS))
        self.d_o = DO(debugEnable=False, showQuantityCrop=False, insertConfirm=True)
        while self.ThreadActive:
            start = time.time()
            ret, frame = Capture.read()
            if ret:
                self.d_o.run(frame)
                
                if self.d_o.goodsreceiptsnotesExist == True and self.statusDoExist == False:
                    self.statusDoExist = True
                    self.doExist.emit(True)

                if self.lastDebugString != self.d_o.debugString:
                    self.infoUpdate.emit(self.d_o.debugString)
                    self.lastDebugString = self.d_o.debugString

                if self.d_o.po_number != '' and self.statusPo == False:
                    self.poNumberUpdate.emit(self.d_o.po_number)
                    self.statusPo = True
                
                if self.d_o.companyNameMatched == True and self.statusCmp == False:
                    self.companyNameUpdate.emit(self.d_o.companyNameFromPO)
                    self.statusCmp = True
                
                if self.d_o.do_date != '' and self.statusDoDate == False:
                    self.doDateUpdate.emit(self.d_o.do_date)
                    self.statusDoDate = True
                
                if len(self.d_o.resStr) != 0:
                    if self.d_o.resStr[0] != '' and self.statusDoNumber == False:
                        self.doNumberUpdate.emit(self.d_o.resStr[0])
                        self.statusDoNumber = True
                
                if len(self.d_o.itemDetails) != 0 and self.statusItem == False: 
                    self.itemAdd.emit(self.d_o.itemDetails)
                    self.statusItem = True

                if len(self.d_o.itemDetected) != 0:
                    if self.lastItemDetectedCount < len(self.d_o.itemDetected):
                        self.lastItemDetectedCount = len(self.d_o.itemDetected)
                        self.itemAddDetected.emit(self.d_o.itemDetected)
                
                if len(self.d_o.itemQuantityToBeDetected) != 0:
                    if self.lastQuantityDetectedCount < len(self.d_o.itemQuantityToBeDetected):
                        for i in range(0, len(self.d_o.itemQuantityToBeDetected)):
                            self.statusQuantity.append(False)
                        self.lastQuantityDetectedCount = len(self.d_o.itemQuantityToBeDetected)

                    for index, item in enumerate(self.d_o.itemQuantityToBeDetected):
                        if self.statusQuantity[index] == False:
                            # item[0] = True/False (boolean)
                            # item[1] = Quantity   (str)      Ex. 20.00
                            if item[0] == False:
                                self.itemQuantityUpdate.emit(index, item[1])
                                self.statusQuantity[index] = True

                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #FlippedImage = cv2.flip(Image, 1)
                #ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

                end = time.time()
                self.fpsSig.emit(int(1/(end-start)))
    def stop(self):
        self.ThreadActive = False
        self.quit()
        self.d_o.secondGnome.kill()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #myWindow = MyWindow()
    #myWindow.show()
    login = loginWindow()
    login.show()
    app.exec_()
