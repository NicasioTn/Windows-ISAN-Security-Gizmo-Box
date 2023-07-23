import sys
import os
import time
from math import log2
import json

from PyQt6.QtWidgets import ( QApplication, QDialog, QLineEdit)
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.uic import loadUi


# Set DPI Awareness
# os.environ["QT_FONT_DPI"] = "96"

class Main(QDialog):
    
    nordpass_common_passwords = []
    hint_btn = []

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/main.ui", self)

        # initialize 
        self.setWindowTitle("ISAN Security Gizmo Box v1.0")
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
        if self.lineEdit_inputPwd.text() == '':
            self.checkLength.setIcon(self.warning_icon)
            self.checkDigits.setIcon(self.warning_icon)
            self.checkUpper.setIcon(self.warning_icon)
            self.checkLower.setIcon(self.warning_icon)
            self.checkSpecial.setIcon(self.warning_icon)

        # Load the list of weak passwords
        with open('./data/nordpass_wordlist.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        for item in json_object:
            self.nordpass_common_passwords.append(str(item['Password']))

        self.tbtn_eyePwd.clicked.connect(self.btn_hidePwd)
        self.lineEdit_inputPwd.textChanged.connect(self.getPassword)

        # --------------------- Message Digest ------------------------------
        
        # Load the list of hints from the JSON file
        with open('./data/hint.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        for item in json_object:
            self.hint_btn.append(str(item['tool_description'])) 
        
        self.btn_openDigest.clicked.connect(self.openFileDialog)
        self.btn_clearDigest.clicked.connect(self.clearMessageDigest)
        self.btn_saveDigest.clicked.connect(self.saveQRCode)

        # --------------------- Malware Scan --------------------------------    
        # --------------------- Vulnerability -------------------------------
        # --------------------- HTTPS Testing -------------------------------


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
        password = PasswordEvaluation.update(self)
        entropy = PasswordEvaluation.calculate_entropy(self, password)

        self.label_outEntropyPwd.setText(f'{entropy:.0f} bits')

        if entropy == 0:
            self.label_outEntropyPwd.setText(f'-- Bits')
            self.label_outStrengthPwd.setText('')
        elif entropy > 999:
            self.label_outEntropyPwd.setText(f'~NaN Bits')
        else:
            self.label_outEntropyPwd.setText(f'~{entropy:.0f} Bits')
        
        length = len(password)        
        if length < 8:
            self.label_outStrengthPwd.setText('So very, very bad Password')
            if length == 0:
                self.label_outStrengthPwd.setText('')
        else : 
            if entropy < 50 :
                self.label_outStrengthPwd.setText('Weak password')
            elif entropy < 80 :
                self.label_outStrengthPwd.setText('Medium strength')
            else:
                self.label_outStrengthPwd.setText('Good password')
        
        # Show length of password
        self.label_lengthOfPassword.setText(f'{length} Chars')
        # Show time to crack
        self.label_outTimeCrackPwd.setText(f'{PasswordEvaluation.time_to_Crack(self, password)}')
        # Check if password is in the list of weak passwords
        PasswordEvaluation.check_common_password(self, password, self.nordpass_common_passwords)
        
    def openFileDialog(self):
        MessageDigest.open_file_dialog(self)
    
    def clearMessageDigest(self):
        MessageDigest.clear(self)
    
    def saveQRCode(self):
        MessageDigest.saveQRCode(self)
        

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

    def check_common_password(self, password, nordpass_common_passwords):
        if password == '':
            self.label_outEntropyPwd.setText('')
            self.label_outChkNordpass.setText('Start typing to see the entropy score')
            self.label_outStrengthPwd.setText('')
        else:
            if password in self.nordpass_common_passwords:
                print(self.nordpass_common_passwords.index(password))
                self.label_outChkNordpass.setText('Found in the top 200 most common passwords by NordPass')
            else:
                self.label_outChkNordpass.setText('Not found in the list')

    def update(self):
        self.checkLength.setChecked(False)
        self.checkDigits.setChecked(False)
        self.checkUpper.setChecked(False)
        self.checkLower.setChecked(False)
        self.checkSpecial.setChecked(False)
        
        # Get password real time
        password = self.lineEdit_inputPwd.text()

        for char in password:
            if char.isdigit():
                self.checkDigits.setChecked(True)
                self.checkDigits.setIcon(self.check_icon)
            elif char.isupper():
                self.checkUpper.setChecked(True)
                self.checkUpper.setIcon(self.check_icon)
            elif char.islower():
                self.checkLower.setChecked(True)
                self.checkLower.setIcon(self.check_icon)
            else:
                self.checkSpecial.setChecked(True)
                self.checkSpecial.setIcon(self.check_icon)
                
            if len(self.lineEdit_inputPwd.text()) >= 8:
                self.checkLength.setChecked(True)
                self.checkLength.setIcon(self.check_icon)
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
        entropy = log2(possible_characters**len(password))
        return entropy
    
    def time_to_Crack(self, password):
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

        combinations = possible_characters ** len(password)
        KPS_2020 = 17042497.3 # 17 Million
        seconds = combinations / KPS_2020
        seconds = f'{seconds:.0f}'
        seconds = int(seconds)

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        weeks, days = divmod(days, 7)
        months, weeks = divmod(weeks, 4)
        years, months = divmod(months, 12)

        time_parts = []
        if years > 0:
            time_parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months > 0:
            time_parts.append(f"{months} month{'s' if months != 1 else ''}")
        if weeks > 0:
            time_parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
        if days > 0:
            time_parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            time_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            time_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds > 0:
            time_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

        return ", ".join(time_parts)
    
import hashlib
import qrcode
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog

class MessageDigest(QDialog):

    state_browse_file = False

    def __init__(self):
        super(MessageDigest, self).__init__()

    def clear (self):
        self.lineEdit_inputDigest.clear()

    def qrCodeGenerator(self, hash):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(hash)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("./data/MessageDigest-QRCode.png")
        ## Run on Kali Linux
        '''
        img.save("/home/kali/Gizmo/SaveQR/MessageDigest-QRCode.png")
        '''
        self.ShowImage_QR() # show image

    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            # self,
            # "Select a File", 
            # "D:\\icons\\avatar\\", 
            # "Images (*.png *.jpg)"
            self,
            "Select a File", 
            "D:\\icons\\avatar\\", 
            "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            path = Path(filename)
            self.lineEdit_inputDigest.setText(str(path))
            if path.exists(): # check if file exists 
                print("File exists")
            print(f"\"{path}\"") 
            
            # self.state_browse_file = True # browsed file 
            # if(self.state_browse_file == True):
            #     #hashfile = self.hash_file(path, self.state)
            #     self.setPath(path)

    # def setPath(self, path):
    #     self.path = path
    
    # def getPath(self):
    #     return self.path
    
    def saveQRCode(self):
        pathfile, ok = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Images (*.png *.jpg)")
        
        # Check if a filename was provided
        if pathfile: # show place to save
            print("Save at: ", pathfile)
            # Save QR-Code with pixmap at pathfile
            if not self.label_outQRCode.pixmap().isNull():
                # Save the pixmap to the specified file path
                self.label_outQRCode.pixmap().save(pathfile, 'PNG')
                # Set the text of the save button to "SAVED!" to indicate successful save
                self.btn_saveDigest.setText("SAVED!")
            else:
                print("Error: QR-Code is Not Generated")
        else:
            print("Error: No file name specified")
    
    def ShowImage_QR(self):
        imagePath = "./data/MessageDigest-QRCode.png"
        ## Run on Kali Linux
        '''
        imagePath = "/home/kali/Gizmo/SaveQR/MessageDigest-QRCode.png"
        '''
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaledToWidth(200)
        pixmap = pixmap.scaledToHeight(200)
        self.output_QR_Label.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    #window.setFixedHeight(700)
    #window.setFixedWidth(1200)
    #window.setMinimumSize(1200, 700)
    #window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    