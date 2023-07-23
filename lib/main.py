import sys
import os
import time
from math import log2

from PyQt6.QtWidgets import ( QApplication, QDialog, QLineEdit)
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.uic import loadUi

# Set DPI Awareness
os.environ["QT_FONT_DPI"] = "96"

class Main(QDialog):

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/main.ui", self)

        self.setWindowTitle("Main")
        self.setWindowIcon(QIcon("./assets/icons/Logo.png"))
        self.hide_icon = QIcon("./assets/icons/icon_closedeye.png")
        self.unhide_icon = QIcon("./assets/icons/icon_openeye.png")
        self.warning_icon = QIcon("./assets/icons/warning.png")
        self.check_icon = QIcon("./assets/icons/Checked.png")

        self.lineEdit_inputPwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.tbtn_eyePwd.setIcon(self.hide_icon)

        # -------------------- Advance User ---------------------------------
        self.btn_advancedUserHome.clicked.connect(self.openAdvancedUserHome)
        # ------------------------------------------------------------------
        self.btn_password.clicked.connect(self.PasswordEvaluationHome)
        self.btn_malware.clicked.connect(self.openMalwareHome)
        self.btn_digest.clicked.connect(self.openDigestHome)

        # --------------------- Network User --------------------------------
        self.btn_networkUserHome.clicked.connect(self.openNetworkUserHome)
        # ------------------------------------------------------------------
        self.btn_vulner.clicked.connect(self.openVulnerabilityHome)
        self.btn_https.clicked.connect(self.openHttpsHome)

        # --------------------- Password Evaluation -------------------------
        self.tbtn_eyePwd.clicked.connect(self.btn_hidePwd)
        self.lineEdit_inputPwd.textChanged.connect(self.getPassword)

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

    def btn_hidePwd(self):
        PasswordEvaluation.show_hide_password(self)

    def getPassword(self):
        passoword = PasswordEvaluation.update(self)
        entropy = PasswordEvaluation.calculate_entropy(self, passoword)
        self.label_outEntropyPwd.setText(f'{entropy:.0f} bits')

        
    

class PasswordEvaluation(QDialog):

    hide = True
    
    def __init__(self):
        super(PasswordEvaluation, self).__init__()
        
    def show_hide_password(self):
        if self.hide == True:
            self.lineEdit_inputPwd.setEchoMode(QLineEdit.EchoMode.Password) 
            self.hide = False
            self.tbtn_eyePwd.setIcon(self.hide_icon)
            
        else:
            self.lineEdit_inputPwd.setEchoMode(QLineEdit.EchoMode.Normal) 
            self.hide = True
            self.tbtn_eyePwd.setIcon(self.unhide_icon)
            
    def update(self):
        # Get password real time
        password = self.lineEdit_inputPwd.text()
        return password

    def calculate_entropy(self, password):
        if password == '':
            self.checkLength.setIcon(self.warning_icon)
            self.checkDigits.setIcon(self.warning_icon)
            self.checkUpper.setIcon(self.warning_icon)
            self.checkLower.setIcon(self.warning_icon)
            self.checkSpecial.setIcon(self.warning_icon)
            return 0
    
        possible_characters = 0
        if self.checkDigits.isChecked(): # 0-9
            possible_characters += 10
        if self.checkUpper.isChecked(): # A-Z
            possible_characters += 26
        if self.checkLower.isChecked(): # a-z
            possible_characters += 26
        if self.checkSpecial.isChecked(): # !@#$%^&*()_+-=
            possible_characters += 32
        # Calculate the entropy using the formula log2(possible_characters^password_length)
        return log2(possible_characters**len(password))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    