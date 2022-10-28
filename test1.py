from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vbox1 = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.hbox = QHBoxLayout()
        self.vbox.setSizeConstraint(QLayout.SetMaximumSize)
        self.vbox1.setSizeConstraint(QLayout.SetMaximumSize)

        length = 11
        for i in range(0,length):
            plain = QPlainTextEdit()
            plain.setGeometry(QRect(60, 50, 380, 231))

            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(plain.sizePolicy().hasHeightForWidth())
            plain.setSizePolicy(sizePolicy)
            plain.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            plain.setMinimumSize(QSize(380, 231))

            plain.setStyleSheet("border-width: 2px;\n"
                                "border-radius: 20px;\n"
                                "background-color: rgb(80, 200, 120);")
            plain.setPlainText("                id: 1\n"
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
"       supinvtotal: 0.0000")
            if i%2 == 0:
                self.vbox.addWidget(plain)
            else:
                self.vbox1.addWidget(plain)
        
        if length%2 == 1:
            plain = QPlainTextEdit()
            plain.setGeometry(QRect(60, 50, 380, 231))

            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(plain.sizePolicy().hasHeightForWidth())
            plain.setSizePolicy(sizePolicy)
            plain.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            plain.setMinimumSize(QSize(380, 231))

            plain.setStyleSheet("border-width: 2px;\n"
                                "border-radius: 20px;\n"
                                "background-color: rgb(80, 200, 120);")
            plain.setPlainText("                id: 1\n"
"            grn_id: \n"
"        po_item_id: \n"
"         wo_number: \n"
"           item_id: \n"
"  ordered_quantity: \n"
"recieving_quantity: \n"
"            status: \n"
"        created_at: \n"
"        updated_at: \n"
"        deleted_at: \n"
"   supinvunitprice: \n"
"       supinvtotal: ")
            self.vbox1.addWidget(plain)
            
        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.vbox1)
        self.widget.setLayout(self.hbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 800, 900)
        self.setWindowTitle('Scroll Area Demonstration')
        button = QPushButton('PyQt5 button', self)
        self.show()

        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

