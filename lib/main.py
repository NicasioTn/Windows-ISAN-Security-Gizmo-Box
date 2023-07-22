import sys
import os
from math import log2
import time
from PyQt6.QtWidgets import ( QApplication, QDialog,)
from PyQt6 import QtCore, QtGui, QtWidgets
from math import log2
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi

os.environ["QT_FONT_DPI"] = "96"
class Main(QDialog):

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/main.ui", self)

        self.setWindowTitle("Main")
        self.setWindowIcon(QIcon("./assets/icons/Logo.png"))


        self.btn_advancedUserHome.clicked.connect(self.openAdvancedUserHome)
        self.btn_password.clicked.connect(self.PasswordEvaluationHome)

    def openAdvancedUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_advancedUser)

    def PasswordEvaluationHome(self):
        self.stackedWidget.setCurrentWidget(self.page_password)
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    