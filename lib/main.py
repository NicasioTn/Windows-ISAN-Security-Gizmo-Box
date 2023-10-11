import sys
import os
import json
import configparser

from PyQt6.QtWidgets import ( QApplication, QDialog, QLineEdit, QMainWindow )
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt

# Import all the classes from the lib folder
from PasswordEvaluation import *
from MessageDigest import *
from MalwareScanning import *
from VulnerabilityScanning import *
from HSTSTesting import *

class Main(QMainWindow):
    
    nordpass_common_passwords = []
    hint_btn = []
    api_url_scan = ''
    api_vt_key = ''
    api_file_scan = ''
    api_file_analysis = ''

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/mainWindow.ui", self)
         
        # Initialize the classes
        passwordEvaluation = PasswordEvaluation()
        passwordAttack = PasswordAttack()
        messageDigest = MessageDigest()
        malwareScanning = MalwareScanning()
        vulnerabilityScanning = VulnerabilityScanning()
        hstsTesting = HSTSTesting()

        # initialize Icon
        self.setWindowTitle("ISAN Security Gizmo Box v1.0")
        self.setWindowIcon(QIcon("./assets/icons/icons8-stan-marsh-96.png"))
        self.hide_icon = QIcon("./assets/icons/icon_closedeye.png")
        self.unhide_icon = QIcon("./assets/icons/icon_openeye.png")
        self.warning_icon = QIcon("./assets/icons/warning.png")
        self.check_icon = QIcon("./assets/icons/Checked.png")
        self.label_logo = QPixmap("./assets/icons/icons8-stan-marsh-96.png")
        self.image_main = QPixmap("./assets/images/main.png")

        # Event Back Button
        self.btn_backAdvancedUser.clicked.connect(self.openHomePage)
        self.btn_backPassword.clicked.connect(self.openAdvancedUserHome)
        self.btn_backDict.clicked.connect(self.PasswordEvaluationHome)
        self.btn_backMalware.clicked.connect(self.openAdvancedUserHome)
        self.btn_backMSDigest.clicked.connect(self.openAdvancedUserHome)
        self.btn_backNetworkUser.clicked.connect(self.openHomePage)
        self.btn_backVulner.clicked.connect(self.openNetworkUserHome)
        self.btn_backHsts.clicked.connect(self.openNetworkUserHome)

        # clear after back button
        self.btn_backPassword.clicked.connect(lambda: PasswordEvaluation.clear(self))
        self.btn_backDict.clicked.connect(lambda: PasswordAttack.clear(self))
        self.btn_backMalware.clicked.connect(lambda: MalwareScanning.clear(self))
        self.btn_backMSDigest.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_backVulner.clicked.connect(lambda: VulnerabilityScanning.clear(self))
        self.btn_backHsts.clicked.connect(lambda: HSTSTesting.clear(self))

        # --------------------- Get Started ---------------------------------
        self.btn_getStart.clicked.connect(self.openHomePage)

        # -------------------- Home ---------------------------------------
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.mainpage))
        self.btn_home.clicked.connect(lambda: PasswordEvaluation.clear(self))
        self.btn_home.clicked.connect(lambda: PasswordAttack.clear(self))
        self.btn_home.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_home.clicked.connect(lambda: MalwareScanning.clear(self))
        self.btn_home.clicked.connect(lambda: VulnerabilityScanning.clear(self))
        self.btn_home.clicked.connect(lambda: HSTSTesting.clear(self))

        self.btn_advancedUserHome.clicked.connect(self.openAdvancedUserHome)
        self.btn_networkUserHome.clicked.connect(self.openNetworkUserHome)

        # -------------------- Advance User ---------------------------------
        self.btn_advancedUserHome.clicked.connect(self.openAdvancedUserHome)
        # ------------------------------------------------------------------
        self.btn_password.clicked.connect(self.PasswordEvaluationHome)
        self.btn_malware.clicked.connect(self.openMalwareHome)
        self.btn_MSdigest.clicked.connect(self.openMessageDigestHome)

        # --------------------- Network User --------------------------------
        self.btn_networkUserHome.clicked.connect(self.openNetworkUserHome)
        # ------------------------------------------------------------------
        self.btn_vulner.clicked.connect(self.openVulnerabilityHome)
        self.btn_hsts.clicked.connect(self.openHttpsHome)

        # --------------------- Password Evaluation -------------------------

        # Initialize the password field
        self.btn_showPassword.setIcon(self.hide_icon)
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Load the list of weak passwords
        with open('./data/nordpass_wordlist.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        for item in json_object:
            self.nordpass_common_passwords.append(str(item['Password']))

        # Check if the password field is empty
        if self.lineEdit_password.text() == '':
            self.chk_length.setIcon(self.warning_icon)
            self.chk_numeric.setIcon(self.warning_icon)
            self.chk_upper.setIcon(self.warning_icon)
            self.chk_lower.setIcon(self.warning_icon)
            self.chk_special.setIcon(self.warning_icon)
            self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
            self.label_outputTimeToCrack.setText('0 Seconds')
            self.label_outputPasswordStrength.setText('no password')
            self.label_outputEntropy.setText('0 Bits')

        # Detect changes in the password field
        self.lineEdit_password.textChanged.connect(lambda: PasswordEvaluation.getPassword(self))
        
        # Event Button Page Password Evaluation
        self.btn_showPassword.clicked.connect(lambda: PasswordEvaluation.show_hide_password(self))
        self.btn_dictAttack.clicked.connect(self.Passowrd_Dictionary_Attack)
        self.btn_infoEntropy.clicked.connect(lambda: PasswordEvaluation.infoEntropy(self))

        ### --------------------- Dictionary Attack -------------------------

        # Event Button Page Dictionary Attack
        self.btn_browseDict.clicked.connect(lambda: PasswordAttack.open_file_wordlist(self))
        self.btn_clearDict.clicked.connect(lambda: PasswordAttack.clear(self))
        self.btn_showPasswordDict.clicked.connect(lambda: PasswordAttack.show_hide_password(self))
        self.dropdown_wordLists.activated.connect(lambda: PasswordAttack.select_wordlists(self))
        PasswordAttack.show_loadding(self)

        # --------------------- Message Digest ------------------------------

        # Load the list of hints from the JSON file
        with open('./data/hint.json', 'r') as openfile:
            json_object = json.load(openfile)
    
        # Fetch API Key from config file
        config = configparser.ConfigParser()
        configFilePath = './data/init.conf'
        config.read(configFilePath)
        if 'LineNotify' in config:
            line_api_key = config.get('LineNotify', 'LineAPIKEY')
            self.lineEdit_tokenMSDigest.setText(line_api_key)
            #print(f'Line API Key: {line_api_key}')
        else:
            print('Section "LineNotify" does not exist in the config file.')
        
        for item in json_object:
            self.hint_btn.append(str(item['tool_description']))
        
        # Event Button Page Message Digest
        self.btn_browseMSDigest.clicked.connect(lambda: MessageDigest.openFileDialog(self))
        self.btn_clearMSDigest.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_saveQR.clicked.connect(lambda: MessageDigest.saveQRCode(self))
        self.btn_lineAPI.clicked.connect(lambda: MessageDigest.showBtnLine(self))
        self.btn_sendMSDigest.clicked.connect(lambda: MessageDigest.processLineKey(self))
        self.btn_copy.clicked.connect(lambda: MessageDigest.copyOutput(self))
        self.btn_infoToken.clicked.connect(lambda: MessageDigest.infoToken(self))
        # --------------------- Malware Scan --------------------------------

        # Initialize the image
        MalwareScanning.show_resultimage(self, type='scan', status='default')

        # Fetch API Key from config file
        config = configparser.ConfigParser()
        configFilePath = './data/init.conf'
        config.read(configFilePath)
        if 'Malware' in config:
            self.api_vt_key = config.get('Malware', 'virustotal_api_key')
            self.api_url_scan = config.get('Malware', 'api_url_scan')
            self.api_file_scan = config.get('Malware', 'api_file_scan')
            self.api_file_analysis = config.get('Malware', 'api_file_analysis')
            # print(f'VT API Key: {self.api_vt_key}')
            # print(f'VT API URL: {self.api_url_scan}')
            # print(f'VT API File: {self.api_file_scan}')
            # print(f'VT API Analysis: {self.api_file_analysis}')
        else:
            print('Section "Malware" does not exist in the config file.')

        # Event Button Page Malware Scan
        self.btn_scanMalware.clicked.connect(lambda: MalwareScanning.scanMalware(self))
        self.btn_browseMalware.clicked.connect(lambda: MalwareScanning.openFileScanning(self))
        self.btn_clearMalware.clicked.connect(lambda: MalwareScanning.clear(self))
        self.btn_createReport.clicked.connect(lambda: MalwareScanning.createReport(self))
        self.btn_sendEmail.clicked.connect(lambda: MalwareScanning.sendEmail(self))

        # --------------------- Vulnerability -------------------------------

        # Event Button Page Vulnerability
        self.btn_scanVulner.clicked.connect(lambda: VulnerabilityScanning.scanVulnerability(self))
        self.btn_clearVulner.clicked.connect(lambda: VulnerabilityScanning.clear(self))
        self.dropdown_typeScan.activated.connect(lambda: VulnerabilityScanning.typeScan(self))

        # --------------------- HTTPS Testing -------------------------------

        # Event Button Page HTTPS Testing
        self.btn_scanHsts.clicked.connect(lambda: HSTSTesting.scanHSTS(self))
        #self.btn_clearHttps.clicked.connect(lambda: HSTSTesting.clear(self))
    
    # -------------------- Home ---------------------------------------
    def openHomePage(self):
        self.stackedWidget.setCurrentWidget(self.mainpage)
    
    # Advanced User ------------------------------------------
    def openAdvancedUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_advancedUser)

    def PasswordEvaluationHome(self):
        self.stackedWidget.setCurrentWidget(self.page_passwordEvaluation)
        self.btn_dictAttack.setVisible(False)
        self.label_outputSearchNordPass.setText('Start typing to see the entropy score')
    
    def Passowrd_Dictionary_Attack(self):
        self.lineEdit_passwordDict.setText(self.lineEdit_password.text())
        self.stackedWidget.setCurrentWidget(self.page_passwordAttack)
        PasswordAttack.init(self)
    
    def openMalwareHome(self):
        MalwareScanning.show_resultimage(self, type='scan', status='default')
        self.stackedWidget.setCurrentWidget(self.page_malware)

    def openMessageDigestHome(self):
        self.stackedWidget.setCurrentWidget(self.page_messageDigest)
        self.label_lineAPIDigest.setVisible(False)
        self.lineEdit_tokenMSDigest.setVisible(False)
        self.btn_sendMSDigest.setVisible(False)
        self.btn_infoToken.setVisible(False)
        self.lineEdit_MSdigest.textChanged.connect(lambda: MessageDigest.checkFile_Text(self))

    # Network User ------------------------------------------
    def openNetworkUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_networkUser)

    def openVulnerabilityHome(self):
        self.stackedWidget.setCurrentWidget(self.page_vulnerability)
    
    def openHttpsHome(self):
        self.stackedWidget.setCurrentWidget(self.page_hsts)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()

    # Exit the application
    try:
        sys.exit(app.exec())     
    except SystemExit:
        print('Closing Window...')