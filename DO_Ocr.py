#!/usr/bin/env python3

import time
import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *

import cv2
from DO_Processing import DO

class MyWindow(QWidget):
    def __init__(self):

        #Qt Stuff..
        super(MyWindow, self).__init__()
        uic.loadUi('DO.ui', self)        #load the .ui file made from Qt designer -- you can also use pyside-uic -o outpit.py input.ui on terminal to see your .ui file converted to python objects.

        #initialise your rviz widget
        #self.map_widget = MyViz()
        #add the widget to a layout present in the main window.(This will depend on the name of your layout defined by you in the designer file)
        #self.gridLayout.addWidget(self.map_widget)

        """
        self.tableWidget.setColumnWidth(0,400)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,100)
        """

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
         
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.poRetakeButton.clicked.connect(self.on_click_PO)
        self.companyNameRetakeButton.clicked.connect(self.on_click_companyName)
        self.doDateRetakeButton.clicked.connect(self.on_click_do_date)
        self.doNumberRetakeButton.clicked.connect(self.on_click_do_number)
        self.insertButton.clicked.connect(self.on_click_insert)
        self.nextButton.clicked.connect(self.on_click_next)

        self.tPOLineEdit.editingFinished.connect(self.po_key_in)
        self.companyNameLineEdit.editingFinished.connect(self.companyName_key_in)
        self.dO_dateLineEdit.editingFinished.connect(self.doDate_key_in)
        self.dO_numberLineEdit.editingFinished.connect(self.doNumber_key_in)

        self.logoLabel.setPixmap(QPixmap('logo.PNG').scaled(self.logoLabel.size(), Qt.KeepAspectRatio))
        self.infoTextBrowser.setReadOnly(True)

    def po_key_in(self):
        print(self.tPOLineEdit.text())

    def companyName_key_in(self, text):
        print(self.companyNameLineEdit.text())

    def doDate_key_in(self):
        print(self.dO_dateLineEdit.text())

    def doNumber_key_in(self):
        print(self.dO_numberLineEdit.text())

    @pyqtSlot()
    def on_click_PO(self):
        print('retake PO')

        """
        self.tPOLineEdit.setText('')
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
    
    def on_click_do_date(self):
        print('retake do date')
        self.dO_dateLineEdit.setText('')
    
    def on_click_do_number(self):
        print('retake do number')
        self.dO_numberLineEdit.setText('')
    
    def on_click_insert(self):
        self.Worker1.d_o.insertDatabase()

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

    def ImageUpdateSlot(self, Image):
        self.feedLabel.setPixmap(QPixmap.fromImage(Image))

    def update_po_number(self, text):
        self.tPOLineEdit.setText(text)

    def update_company_name(self, text):
        self.companyNameLineEdit.setText(text)

    def update_do_date(self, text):
        self.dO_dateLineEdit.setText(text)

    def update_do_number(self, text):
        self.dO_numberLineEdit.setText(text)

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
        """
        horScrollBar = self.infoTextBrowser.horizontalScrollBar()
        verScrollBar = self.infoTextBrowser.verticalScrollBar()
        scrollIsAtEnd = verScrollBar.maximum() - verScrollBar.value() <= 10

        if scrollIsAtEnd:
            verScrollBar.setValue(verScrollBar.maximum()) # Scrolls to the bottom
            horScrollBar.setValue(0) # scroll to the left
        """

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

    def run(self):
        self.ThreadActive = True
        WIDTH, HEIGHT = 1280, 720

        Capture = cv2.VideoCapture(0,cv2.CAP_V4L2)
        Capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.d_o = DO(debugEnable=False, showQuantityCrop=False)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                self.d_o.run(frame)
                
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
    def stop(self):
        self.ThreadActive = False
        self.quit()
        self.d_o.secondGnome.kill()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
