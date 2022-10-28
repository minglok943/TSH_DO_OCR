# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detail.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1272, 830)
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(60, 50, 361, 271))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_4.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_4.setSizePolicy(sizePolicy)
        self.plainTextEdit_4.setStyleSheet("border-width: 2px;\n"
"border-radius: 20px;\n"
"background-color: rgb(80, 200, 120);")
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(70, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 340, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(430, 10, 831, 541))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 815, 539))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 0, 771, 811))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit_2.setStyleSheet("border-width: 2px;\n"
"border-radius: 20px;\n"
"background-color: rgb(114, 159, 207);")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.verticalLayout.addWidget(self.plainTextEdit_2)
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit_3.setStyleSheet("border-width: 2px;\n"
"border-radius: 20px;\n"
"background-color: rgb(114, 159, 207);")
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.verticalLayout.addWidget(self.plainTextEdit_3)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit.setStyleSheet("border-width: 2px;\n"
"border-radius: 20px;\n"
"background-color: rgb(114, 159, 207);")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plainTextEdit_5 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit_5.setStyleSheet("border-width: 2px;\n"
"border-radius: 20px;\n"
"background-color: rgb(114, 159, 207);")
        self.plainTextEdit_5.setObjectName("plainTextEdit_5")
        self.verticalLayout_2.addWidget(self.plainTextEdit_5)
        self.plainTextEdit_6 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit_6.setStyleSheet("border-width: 2px;\n"
"border-radius: 20px;\n"
"background-color: rgb(114, 159, 207);")
        self.plainTextEdit_6.setObjectName("plainTextEdit_6")
        self.verticalLayout_2.addWidget(self.plainTextEdit_6)
        self.plainTextEdit_7 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit_7.setStyleSheet("border-width: 2px;\n"
"border-radius: 20px;\n"
"background-color: rgb(114, 159, 207);")
        self.plainTextEdit_7.setObjectName("plainTextEdit_7")
        self.verticalLayout_2.addWidget(self.plainTextEdit_7)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.plainTextEdit_4.setPlainText(_translate("Form", "                 id: 1\n"
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
        self.label.setText(_translate("Form", "goodsreceiptsnotes"))
        self.label_2.setText(_translate("Form", "goodreceiptsnoteitems"))
        self.plainTextEdit_2.setPlainText(_translate("Form", "                id: 1\n"
"            grn_id: 1\n"
"        po_item_id: 2\n"
"         wo_number: null\n"
"           item_id: 7350\n"
"  ordered_quantity: 1000.0000\n"
"recieving_quantity: 1000.0000\n"
"            status: 14\n"
"        created_at: 2021-10-25 17:14:30\n"
"        updated_at: 2021-10-25 17:14:30\n"
"        deleted_at: NULL\n"
"   supinvunitprice: 0.0000\n"
"       supinvtotal: 0.0000"))
        self.plainTextEdit_3.setPlainText(_translate("Form", "                id: 1\n"
"            grn_id: 1\n"
"        po_item_id: 2\n"
"         wo_number: null\n"
"           item_id: 7350\n"
"  ordered_quantity: 1000.0000\n"
"recieving_quantity: 1000.0000\n"
"            status: 14\n"
"        created_at: 2021-10-25 17:14:30\n"
"        updated_at: 2021-10-25 17:14:30\n"
"        deleted_at: NULL\n"
"   supinvunitprice: 0.0000\n"
"       supinvtotal: 0.0000"))
        self.plainTextEdit.setPlainText(_translate("Form", "                id: 1\n"
"            grn_id: 1\n"
"        po_item_id: 2\n"
"         wo_number: null\n"
"           item_id: 7350\n"
"  ordered_quantity: 1000.0000\n"
"recieving_quantity: 1000.0000\n"
"            status: 14\n"
"        created_at: 2021-10-25 17:14:30\n"
"        updated_at: 2021-10-25 17:14:30\n"
"        deleted_at: NULL\n"
"   supinvunitprice: 0.0000\n"
"       supinvtotal: 0.0000"))
        self.plainTextEdit_5.setPlainText(_translate("Form", "                id: 1\n"
"            grn_id: 1\n"
"        po_item_id: 2\n"
"         wo_number: null\n"
"           item_id: 7350\n"
"  ordered_quantity: 1000.0000\n"
"recieving_quantity: 1000.0000\n"
"            status: 14\n"
"        created_at: 2021-10-25 17:14:30\n"
"        updated_at: 2021-10-25 17:14:30\n"
"        deleted_at: NULL\n"
"   supinvunitprice: 0.0000\n"
"       supinvtotal: 0.0000"))
        self.plainTextEdit_6.setPlainText(_translate("Form", "                id: 1\n"
"            grn_id: 1\n"
"        po_item_id: 2\n"
"         wo_number: null\n"
"           item_id: 7350\n"
"  ordered_quantity: 1000.0000\n"
"recieving_quantity: 1000.0000\n"
"            status: 14\n"
"        created_at: 2021-10-25 17:14:30\n"
"        updated_at: 2021-10-25 17:14:30\n"
"        deleted_at: NULL\n"
"   supinvunitprice: 0.0000\n"
"       supinvtotal: 0.0000"))
        self.plainTextEdit_7.setPlainText(_translate("Form", "                id: 1\n"
"            grn_id: 1\n"
"        po_item_id: 2\n"
"         wo_number: null\n"
"           item_id: 7350\n"
"  ordered_quantity: 1000.0000\n"
"recieving_quantity: 1000.0000\n"
"            status: 14\n"
"        created_at: 2021-10-25 17:14:30\n"
"        updated_at: 2021-10-25 17:14:30\n"
"        deleted_at: NULL\n"
"   supinvunitprice: 0.0000\n"
"       supinvtotal: 0.0000"))
