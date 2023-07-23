import sys
import os
from math import log2
import time
from PyQt6.QtWidgets import ( QApplication, QDialog,)
from PyQt6 import QtCore, QtGui, QtWidgets
from math import log2
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi

# Set DPI Awareness
os.environ["QT_FONT_DPI"] = "96"

class Main(QDialog):

    hide = True

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/main.ui", self)

        self.setWindowTitle("Main")
        self.setWindowIcon(QIcon("./assets/icons/Logo.png"))

        # ------------------------------------------------------------------
        self.btn_advancedUserHome.clicked.connect(self.openAdvancedUserHome)
        # ------------------------------------------------------------------
        self.btn_password.clicked.connect(self.PasswordEvaluationHome)
        self.btn_malware.clicked.connect(self.openMalwareHome)
        self.btn_digest.clicked.connect(self.openDigestHome)

        # ------------------------------------------------------------------
        self.btn_networkUserHome.clicked.connect(self.openNetworkUserHome)
        # ------------------------------------------------------------------
        self.btn_vulner.clicked.connect(self.openVulnerabilityHome)
        self.btn_https.clicked.connect(self.openHttpsHome)


    def openAdvancedUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_advancedUser)

    def PasswordEvaluationHome(self):
        self.stackedWidget.setCurrentWidget(self.page_password)
    
    def openMalwareHome(self):
        self.stackedWidget.setCurrentWidget(self.page_malware)

    def openDigestHome(self):
        self.stackedWidget.setCurrentWidget(self.page_digest)

    def openNetworkUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_networkUser_home)

    def openVulnerabilityHome(self):
        self.stackedWidget.setCurrentWidget(self.page_vulner)
    
    def openHttpsHome(self):
        self.stackedWidget.setCurrentWidget(self.page_https)

    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    