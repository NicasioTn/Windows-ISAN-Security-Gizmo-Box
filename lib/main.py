import sys
import os
import time
from math import log2
import json

from PyQt6.QtWidgets import ( QApplication, QDialog, QLineEdit)
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.uic import loadUi
import requests


# Set DPI Awareness
# os.environ["QT_FONT_DPI"] = "96"

class Main(QDialog):

    algorithm = ''
    nordpass_common_passwords = []
    hint_btn = []
    state_detect = 0
    path = ''

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/mainUI.ui", self)

        # initialize 
        self.setWindowTitle("ISAN Security Gizmo Box v1.0")
        self.setWindowIcon(QIcon("./assets/icons/Logo.png"))
        self.hide_icon = QIcon("./assets/icons/icon_closedeye.png")
        self.unhide_icon = QIcon("./assets/icons/icon_openeye.png")
        self.warning_icon = QIcon("./assets/icons/warning.png")
        self.check_icon = QIcon("./assets/icons/Checked.png")

        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_iconEye.setIcon(self.hide_icon)

        # -------------------- Home ---------------------------------------
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_home))
        self.btn_advanceUser.clicked.connect(self.openAdvancedUserHome)
        self.btn_networkUser.clicked.connect(self.openNetworkUserHome)

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
        # Load the list of weak passwords
        with open('./data/nordpass_wordlist.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        for item in json_object:
            self.nordpass_common_passwords.append(str(item['Password']))

        if self.lineEdit_password.text() == '':
            self.chk_length.setIcon(self.warning_icon)
            self.chk_digits.setIcon(self.warning_icon)
            self.chk_upper.setIcon(self.warning_icon)
            self.chk_lower.setIcon(self.warning_icon)
            self.chk_special.setIcon(self.warning_icon)
            self.label_outputEntropy.setText('')

        self.btn_iconEye.clicked.connect(self.btn_hidePwd)
        self.lineEdit_password.textChanged.connect(self.getPassword)
        self.btn_dicAttack.clicked.connect(self.Passowrd_Dictionary_Attack)
        ### --------------------- Dictionary Attack -------------------------
        self.btn_openDic.clicked.connect(lambda: PasswordEvaluation.open_file_wordlist(self))
        self.btn_clearDic.clicked.connect(lambda: PasswordEvaluation.clear(self))
        self.btn_rockyou.clicked.connect(lambda: self.lineEdit_inputFileDic.setText("rockyou.txt"))
        self.btn_crackstation.clicked.connect(lambda: self.lineEdit_inputFileDic.setText("crackstation.txt"))

        # --------------------- Message Digest ------------------------------
        # Load the list of hints from the JSON file
        with open('./data/hint.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        # Load the API key from the config file and display it in the textbox
        with open('./data/api.conf', 'r') as config_file:
            self.lineAPIKey = config_file.read()
            if self.lineAPIKey != '':
                self.lineEdit_digest_2.setText(self.lineAPIKey)
            config_file.close()
        
        for item in json_object:
            self.hint_btn.append(str(item['tool_description'])) 
        
        self.btn_openDigest.clicked.connect(self.openFileDialog)
        self.btn_clearDigest.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_saveQR.clicked.connect(lambda: MessageDigest.saveQRCode(self))
        self.btn_lineAPI.clicked.connect(self.showBtnLine)
        self.btn_sendDigest.clicked.connect(lambda: MessageDigest.processLineKey(self))
        self.btn_copy.clicked.connect(lambda: MessageDigest.copyOutput(self))

        # --------------------- Malware Scan --------------------------------
        self.btn_scanMalware.clicked.connect(MalwareScanning.scanMalware)
        self.btn_openMalware.clicked.connect(MalwareScanning.openFileScanning)
        self.btn_clearMalware.clicked.connect(MalwareScanning.clear)

        # --------------------- Vulnerability -------------------------------
        # --------------------- HTTPS Testing -------------------------------


    def openAdvancedUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_advanceUser)

    def PasswordEvaluationHome(self):
        self.stackedWidget.setCurrentWidget(self.page_password)
        self.btn_dicAttack.setVisible(False)
        self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
    
    def Passowrd_Dictionary_Attack(self):
        self.lineEdit_passwordDic.setText(self.lineEdit_password.text())
        self.stackedWidget.setCurrentWidget(self.page_dictionary)

    def openMalwareHome(self):
        self.stackedWidget.setCurrentWidget(self.page_malware)

    def openDigestHome(self):
        self.stackedWidget.setCurrentWidget(self.page_messageDigest)

        self.lineEdit_digest_2.setVisible(False)
        self.btn_sendDigest.setVisible(False)
        self.lineEdit_digest.textChanged.connect(lambda: self.checkFile_Text())
        
    def checkFile_Text(self):
        if os.path.exists(self.lineEdit_digest.text()) == True: # check if file exists
            print("File")
            self.state_detect = 1
            self.btn_md5.clicked.connect(lambda: MessageDigest.fileExtract(self, "md5", self.getPath()))
            self.btn_sha1.clicked.connect(lambda: MessageDigest.fileExtract(self, "sha1", self.getPath()))
            self.dropdown_sha2.activated.connect(lambda: MessageDigest.fileExtract(self, "sha2_" + self.dropdown_sha2.currentText(), self.getPath()))
            self.dropdown_sha3.activated.connect(lambda: MessageDigest.fileExtract(self, "sha3_" + self.dropdown_sha3.currentText(), self.getPath()))
        else:
            self.state_detect = 0
            print("Plaintext")
            self.btn_md5.clicked.connect(lambda: MessageDigest.hash(self, "md5"))
            self.btn_sha1.clicked.connect(lambda: MessageDigest.hash(self, "sha1"))
            self.dropdown_sha2.activated.connect(lambda: self.getdropdown_sha2())
            self.dropdown_sha3.activated.connect(lambda: self.getdropdown_sha3())

        # show Image QR Code
        self.btn_md5.clicked.connect(self.ShowImage_QR)
        self.btn_sha1.clicked.connect(self.ShowImage_QR)
        self.dropdown_sha2.activated.connect(self.ShowImage_QR)
        self.dropdown_sha3.activated.connect(self.ShowImage_QR)

    def openNetworkUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_networklUser)

    def openVulnerabilityHome(self):
        self.stackedWidget.setCurrentWidget(self.page_vulner)
    
    def openHttpsHome(self):
        self.stackedWidget.setCurrentWidget(self.page_https)
    
    def btn_hidePwd(self):
        PasswordEvaluation.show_hide_password(self)

    def getPassword(self):
        password = PasswordEvaluation.update(self)
        entropy = PasswordEvaluation.calculate_entropy(self, password)

        self.label_outputEntropy.setText(f'{entropy:.0f} bits')

        if entropy == 0:
            self.label_outputEntropy.setText(f'-- Bits')
            self.label_outputPasswordStrength.setText('')
        elif entropy > 999:
            self.label_outputEntropy.setText(f'~NaN Bits')
        else:
            self.label_outputEntropy.setText(f'~{entropy:.0f} Bits')
        
        length = len(password)        
        if length < 8:
            self.label_outputPasswordStrength.setText('So very, very bad Password')
            if length == 0:
                self.label_outputPasswordStrength.setText('')
        else : 
            if entropy < 50 :
                self.label_outputPasswordStrength.setText('Weak password')
            elif entropy < 80 :
                self.label_outputPasswordStrength.setText('Medium strength')
            else:
                self.label_outputPasswordStrength.setText('Good password')
        
        # Show length of password
        self.label_lengthOfPassword.setText(f'{length} Chars')
        # Show time to crack
        self.label_outputTimeToCrack.setText(f'{PasswordEvaluation.time_to_Crack(self, password)}')
        # Check if password is in the list of weak passwords
        PasswordEvaluation.check_common_password(self, password, self.nordpass_common_passwords)
    
    def getdropdown_sha2(self):
        MessageDigest.hash(self, "sha2_" + self.dropdown_sha2.currentText())
        self.algorithm = 'SHA2-' + self.dropdown_sha2.currentText()
        self.dropdown_sha3.setCurrentIndex(0) 

    def getdropdown_sha3(self):
        MessageDigest.hash(self, "sha3_" + self.dropdown_sha3.currentText())
        self.algorithm = 'SHA3-' + self.dropdown_sha3.currentText()
        self.dropdown_sha2.setCurrentIndex(0)


    def openFileDialog(self):
        path = MessageDigest.open_file_dialog(self)
        #print(type(path)) # <class 'pathlib.WindowsPath'>

        # try except to check if file exists
        try:
            if path.exists() == True: # check if file exists
                print(f"File exists at: {path.exists()}" + " ++")
        except AttributeError as e:
            print(f"Empty file or Not found")

        self.setPath(path)
    
    def setPath(self, path):
        self.path = path

    def getPath(self):
        return self.path

    def ShowImage_QR(self):
        if self.lineEdit_outputTextDigest.text() != '':
            MessageDigest.qrCodeGenerator(self, self.lineEdit_outputTextDigest.text())
            MessageDigest.ShowImage_QR(self)

    def showBtnLine(self):
        self.lineEdit_digest_2.setVisible(True)
        self.btn_sendDigest.setVisible(True)

from PyQt6.QtCore import QFileInfo

class PasswordEvaluation(QDialog):

    hide = True
    
    def __init__(self):
        super(PasswordEvaluation, self).__init__()

    def clear(self):
        self.lineEdit_inputFileDic.setText('')

    def show_hide_password(self):
        if self.hide == True:
            self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password) 
            self.hide = False
            self.btn_iconEye.setIcon(self.hide_icon)
            
        else:
            self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Normal) 
            self.hide = True
            self.btn_iconEye.setIcon(self.unhide_icon)

    def check_common_password(self, password, nordpass_common_passwords):
        if password == '':
            self.label_outputEntropy.setText('')
            self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
            self.label_outputPasswordStrength.setText('')
            self.btn_dicAttack.setVisible(False)
        else:
            if password in self.nordpass_common_passwords:
                print(self.nordpass_common_passwords.index(password))
                self.label_outputSearchNordPass.setText('Found in the top 200 most common passwords by NordPass')
                self.btn_dicAttack.setVisible(False)
            else:
                self.label_outputSearchNordPass.setText('Not found in the list')
                self.btn_dicAttack.setVisible(True) if self.label_outputSearchNordPass.text() == '' or self.label_outputSearchNordPass.text() == 'Not found in the list' else self.btn_dicAttack.setVisible(False)

    def update(self):
        self.chk_length.setChecked(False)
        self.chk_digits.setChecked(False)
        self.chk_upper.setChecked(False)
        self.chk_lower.setChecked(False)
        self.chk_special.setChecked(False)
        
        # Get password real time
        password = self.lineEdit_password.text()

        for char in password:
            if char.isdigit():
                self.chk_digits.setChecked(True)
                self.chk_digits.setIcon(self.check_icon)
            elif char.isupper():
                self.chk_upper.setChecked(True)
                self.chk_upper.setIcon(self.check_icon)
            elif char.islower():
                self.chk_lower.setChecked(True)
                self.chk_lower.setIcon(self.check_icon)
            else:
                self.chk_special.setChecked(True)
                self.chk_special.setIcon(self.check_icon)
                
            if len(self.lineEdit_password.text()) >= 8:
                self.chk_length.setChecked(True)
                self.chk_length.setIcon(self.check_icon)
        return password

    def calculate_entropy(self, password):
        
        if password == '':
            self.chk_length.setIcon(self.warning_icon)
            self.chk_digits.setIcon(self.warning_icon)
            self.chk_upper.setIcon(self.warning_icon)
            self.chk_lower.setIcon(self.warning_icon)
            self.chk_special.setIcon(self.warning_icon)
            return 0
    
        possible_characters = 0
        if self.chk_digits.isChecked(): # 0-9
            possible_characters += 10
        if self.chk_upper.isChecked(): # A-Z
            possible_characters += 26
        if self.chk_lower.isChecked(): # a-z
            possible_characters += 26
        if self.chk_special.isChecked(): # !@#$%^&*()_+-=
            possible_characters += 32
        # Calculate the entropy using the formula log2(possible_characters^password_length)
        entropy = log2(possible_characters**len(password))
        return entropy
    
    def time_to_Crack(self, password):
        try:
            if password == '':
                self.chk_length.setIcon(self.warning_icon)
                self.chk_digits.setIcon(self.warning_icon)
                self.chk_upper.setIcon(self.warning_icon)
                self.chk_lower.setIcon(self.warning_icon)
                self.chk_special.setIcon(self.warning_icon)
                return 0
        
            possible_characters = 0
            if self.chk_digits.isChecked(): # 0-9
                possible_characters += 10
            if self.chk_upper.isChecked(): # A-Z
                possible_characters += 26
            if self.chk_lower.isChecked(): # a-z
                possible_characters += 26
            if self.chk_special.isChecked(): # !@#$%^&*()_+-=
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
            if years > 10:
                time_parts = ['more than 10 years']
            return ", ".join(time_parts)
        
        except OverflowError as e:
            print(f"Error: {e}")
        except UnboundLocalError as e:
            print(f"Error: {e}")
    
    def open_file_wordlist(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
           "Open Wordlist File", 
            "D:\\icons\\avatar\\", 
            "Text Files (*.txt)",
        )
        file_name = QFileInfo(filepath).fileName()
        if filepath:
            # Process the selected filename
            print("Selected file:", filepath)
            
            if filepath:
                path = Path(filepath)
                #self.lineEdit_inputFileDic.setText(str(path)) # show path file
                self.lineEdit_inputFileDic.setText(file_name) # show file name
                if path.exists() != True: # check if file exists 
                    print(f"File exists at: {path.exists()}")
                print(f"Get file at: {path}") 

                return path

import hashlib
import qrcode
import pyperclip
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog

class MessageDigest(QDialog):

    def __init__(self):
        super(MessageDigest, self).__init__()
        
    def saveAPIKey(self):
        self.lineAPIKey = self.lineEdit_digest_2.text()
        print(self.lineAPIKey)

        with open("./data/api.conf", "w") as config_file:
            config_file.write(self.lineAPIKey)
            config_file.close()

    def clear (self):
        self.lineEdit_digest.setText('')
        self.label_QRCode.clear()
        self.dropdown_sha2.setCurrentIndex(0)
        self.dropdown_sha3.setCurrentIndex(0)
        self.lineEdit_digest_2.setVisible(False)
        self.btn_sendDigest.setVisible(False)
        self.lineEdit_digest_2.setText('')
        self.lineEdit_outputTextDigest.setText('')
        self.lineEdit_outputTextDigest.setStyleSheet("border: 1px solid black;")
        self.lineEdit_outputTextDigest.setPlaceholderText('')

    def hash(self, type):
        #print(self.dropdown_sha2.currentText())
        if type == "md5":
            self.lineEdit_outputTextDigest.setText(MessageDigest.md5(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'MD5'
        elif type == "sha1":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha1(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA-1'
        elif type == "sha2_224 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha224(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA2-224'
        elif type == "sha2_256 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha256(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA2-256'
        elif type == "sha2_384 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha384(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA2-384'
        elif type == "sha2_512 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha512(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA2-512'
        elif type == "sha3_224 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha3_224(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA3-224'
        elif type == "sha3_256 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha3_256(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA3-256'
        elif type == "sha3_384 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha3_384(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA3-384'
        elif type == "sha3_512 BIT":
            self.lineEdit_outputTextDigest.setText(MessageDigest.sha3_512(self, self.lineEdit_digest.text()))if self.lineEdit_digest.text() != '' else self.lineEdit_outputTextDigest.setText('')
            self.algorithm = 'SHA3-512'
        
        # reset copy button
        self.btn_copy.setText('Copy')

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
        return img
        
    def ShowImage_QR(self):
        imagePath = "./data/MessageDigest-QRCode.png"
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaledToWidth(200)
        pixmap = pixmap.scaledToHeight(200)
        self.label_QRCode.setPixmap(pixmap)
        
    
    def fileExtract(self, type, path):
        print(type)
        if type == "md5":
            MessageDigest.fileHash(self, "md5", path)
        elif type == "sha1":
            MessageDigest.fileHash(self, "sha1", path)
        elif type == "sha2_224 BIT":
            MessageDigest.fileHash(self, "sha224", path)
        elif type == "sha2_256 BIT":
            MessageDigest.fileHash(self, "sha256", path)
        elif type == "sha2_384 BIT":
            MessageDigest.fileHash(self, "sha384", path)
        elif type == "sha2_512 BIT":
            MessageDigest.fileHash(self, "sha512", path)
        elif type == "sha3_224 BIT":
            MessageDigest.fileHash(self, "sha3_224", path)
        elif type == "sha3_256 BIT":
            MessageDigest.fileHash(self, "sha3_256", path)
        elif type == "sha3_384 BIT":
            MessageDigest.fileHash(self, "sha3_384", path)
        elif type == "sha3_512 BIT":
            MessageDigest.fileHash(self, "sha3_512", path)

        # Show Image QR Code
        self.btn_md5.clicked.connect(self.ShowImage_QR)
        self.btn_sha1.clicked.connect(self.ShowImage_QR)
        self.dropdown_sha2.activated.connect(self.ShowImage_QR)
        self.dropdown_sha3.activated.connect(self.ShowImage_QR)

    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            # self,
            # "Select a File", 
            # "D:\\icons\\avatar\\", 
            # "Images (*.png *.jpg)"
            self,
            "Select a File", 
            "D:\\icons\\avatar\\", 
            "Text Files (*.txt);;All Files (*)" # filter file type text but can select all file
        )
        if filename:
            path = Path(filename)
            self.lineEdit_digest.setText(str(path))
            if path.exists() != True: # check if file exists 
                print(f"File exists at: {path.exists()}")
            print(f"Get file at: {path}") 

            return path
    
    # File Hashing -----------------------------------------------
    def fileHash(self, type, path):
        if type == "md5":
            init_hash = hashlib.md5()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha1":
            init_hash = hashlib.sha1()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha224":
            init_hash = hashlib.sha224()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha256":
            init_hash = hashlib.sha256()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha384":
            init_hash = hashlib.sha384()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha512":
            init_hash = hashlib.sha512()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}")
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha3_224":
            init_hash = hashlib.sha3_224()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}") 
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha3_256":
            init_hash = hashlib.sha3_256()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}") 
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha3_384":
            init_hash = hashlib.sha3_384()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}") 
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

        elif type == "sha3_512":
            init_hash = hashlib.sha3_512()
            file = path
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash {type}: {file_hashed}") 
            self.lineEdit_outputTextDigest.setText(f'{file_hashed}')

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
            if not self.label_QRCode.pixmap().isNull():
                # Save the pixmap to the specified file path
                self.label_QRCode.pixmap().save(pathfile, 'PNG')
                # Set the text of the save button to "SAVED!" to indicate successful save
                self.btn_saveQR.setText("SAVED!")
            else:
                print("Error: QR-Code is Not Generated")
        else:
            print("Error: No file name specified")
    
    # Type of Hashing ------------------------------------------
    def md5(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def sha1(self, data):
        return hashlib.sha1(data.encode('utf-8')).hexdigest()

    def sha224(self, data):
        return hashlib.sha224(data.encode('utf-8')).hexdigest()

    def sha256(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def sha384(self, data):
        return hashlib.sha384(data.encode('utf-8')).hexdigest()

    def sha512(self, data):
        return hashlib.sha512(data.encode('utf-8')).hexdigest()

    def sha3_224(self, data):
        return hashlib.sha3_224(data.encode('utf-8')).hexdigest()

    def sha3_256(self, data):
        return hashlib.sha3_256(data.encode('utf-8')).hexdigest()

    def sha3_384(self, data):
        return hashlib.sha3_384(data.encode('utf-8')).hexdigest()

    def sha3_512(self, data):
        return hashlib.sha3_512(data.encode('utf-8')).hexdigest()
    
    def processLineKey(self):
        api_key = '6tA0qnCW3qp6jtAMEVyL2T3CIINiEusqZ3nJH5kuzKL'
        message = self.lineEdit_outputTextDigest.text() + "\nHash Algorithms:" + self.algorithm
        token = self.lineEdit_digest_2.text()
        try:
            if token != '':
                getQR = "./data/MessageDigest-QRCode.png"
                url = "https://notify-api.line.me/api/notify"

                headers = {"Authorization": "Bearer " + token}
                payload = {"message": message}

                with open(getQR, "rb") as image_file:
                    files = {"imageFile": image_file}
                    response = requests.post(url, headers=headers, params=payload, files=files)
                
                if response.status_code == 200:
                    MessageDigest.saveAPIKey(self) # save api key to file api.conf
                    print("Image sent successfully!")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid green;")
                elif response.status_code == 400:
                    print("Bad request!")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid red;")
                elif response.status_code == 401:
                    print("Invalid access token!")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid orange;")
                elif response.status_code == 500:
                    print("Server error!")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid yellow;")
                else:
                    print("Process over time.")
                    self.lineEdit_digest_2.setStyleSheet("border: 1px solid grey;")
            else:
                self.lineEdit_digest_2.setStyleSheet("border: 1px solid red;")
        except UnicodeEncodeError as e:
            print("Cannot send message to LINE")
            

    def copyOutput(self):
        clipboard = self.lineEdit_outputTextDigest.text()
        if clipboard == '':
            self.lineEdit_outputTextDigest.setPlaceholderText("Empty")
            self.lineEdit_outputTextDigest.setStyleSheet("border: 1px solid red;")
        else:
            self.lineEdit_outputTextDigest.setStyleSheet("border: 1px solid green;")
            self.btn_copy.setText("Copied!")
            pyperclip.copy(clipboard)

class MalwareScanning():
    api_key = 'e8cf03a48915da2f70adfb45ae906ce940e837c47ba572bb30a8f1b8573df8e8'

    def __init__(self):
        super(MalwareScanning, self).__init__()
    
    def scanMalware(self):
        print("Scan Malware")
        #pass

    def openFileScanning(self):
        print("Open File")
        #pass
    
    def clear(self):
        print("Clear")
        #pass

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    #window.setFixedHeight(700)
    #window.setFixedWidth(1200)
    #window.setMinimumSize(1200, 700)
    #window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    