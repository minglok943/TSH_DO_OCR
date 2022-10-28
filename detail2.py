# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detail2.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(921, 785)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 0, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(186, 189, 182);")
        self.label.setObjectName("label")
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(20, 30, 381, 281))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_4.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.plainTextEdit_4.setFont(font)
        self.plainTextEdit_4.setStyleSheet("border-width: 2px;\n"
"border-radius: 20px;\n"
"background-color: rgb(80, 200, 120);")
        self.plainTextEdit_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit_4.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 320, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(186, 189, 182);\n"
"border-radius: 20px;")
        self.label_2.setObjectName("label_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(30, 350, 861, 391))
        self.scrollArea.setStyleSheet("border-radius: 40px;\n"
"background-color: rgb(233, 185, 110);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 861, 391))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.confirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmButton.setGeometry(QtCore.QRect(660, 30, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.confirmButton.setFont(font)
        self.confirmButton.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(115, 210, 22);")
        self.confirmButton.setObjectName("confirmButton")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(660, 120, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.cancelButton.setFont(font)
        self.cancelButton.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(204, 0, 0);")
        self.cancelButton.setObjectName("cancelButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 921, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "goodsreceiptsnotes"))
        self.plainTextEdit_4.setPlainText(_translate("MainWindow", "                 id: 1\n"
"         grn_number: 21100001\n"
"          po_number: 2\n"
"        supplier_id: 19\n"
" supplier_do_number: NST13217\n"
"   supplier_do_date: 2021-10-25\n"
"supplier_inv_number: NST13217\n"
"  supplier_inv_date: NULL\n"
"      currency_rate: NULL\n"
"         recieve_by: DINDA  AULIVIA SYNTIANY\n"
"             status: 13\n"
"         created_at: 2021-10-25 17:14:29\n"
"         updated_at: 2021-10-25 17:16:44\n"
"         deleted_at: NULL\n"
"              k1_id: NULL"))
        self.label_2.setText(_translate("MainWindow", "goodreceiptsnoteitems"))
        self.confirmButton.setText(_translate("MainWindow", "Confirm"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
