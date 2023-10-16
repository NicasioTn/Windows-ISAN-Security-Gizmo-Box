import sys
import configparser

from PyQt6.QtWidgets import ( QApplication, QLineEdit, QMainWindow )
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.uic import loadUi

# Import all the classes from the lib folder
from PasswordEvaluation import *
from MessageDigest import *
from MalwareScanning import *
from VulnerabilityScanning import *
from HTTPSTesting import *

class Main(QMainWindow):
    
    state_api_line = False
    state_api_virustotal = False

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/mainWindow.ui", self)
         
        # initialize Icon
        self.setWindowTitle("ISAN Security Gizmo Box v1.0")
        self.setWindowIcon(QIcon("./assets/icons/icons8-stan-marsh-96.png"))
        self.hide_icon = QIcon("./assets/icons/icon_closedeye.png")
        self.unhide_icon = QIcon("./assets/icons/icon_openeye.png")
        self.warning_icon = QIcon("./assets/icons/warning-red.png")
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
        self.btn_backHttps.clicked.connect(self.openNetworkUserHome)
        self.btn_backSettings.clicked.connect(self.openHomePage)

        # clear cache data after back button
        self.btn_backPassword.clicked.connect(lambda: PasswordEvaluation.clear(self))
        self.btn_backDict.clicked.connect(lambda: PasswordAttack.clear(self))
        self.btn_backMalware.clicked.connect(lambda: MalwareScanning.clear(self))
        self.btn_backMSDigest.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_backVulner.clicked.connect(lambda: VulnerabilityScanning.clear(self))
        self.btn_backHttps.clicked.connect(lambda: HTTPSTesting.clear(self))

        # --------------------- Get Started ---------------------------------
        self.btn_getStart.clicked.connect(self.openHomePage)

        # --------------------- Setting -----------------------------------
        self.btn_settings.clicked.connect(self.openSettings)

        # -------------------- Home ---------------------------------------
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.mainpage))
        self.btn_home.clicked.connect(lambda: PasswordEvaluation.clear(self))
        self.btn_home.clicked.connect(lambda: PasswordAttack.clear(self))
        self.btn_home.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_home.clicked.connect(lambda: MalwareScanning.clear(self))
        self.btn_home.clicked.connect(lambda: VulnerabilityScanning.clear(self))
        self.btn_home.clicked.connect(lambda: HTTPSTesting.clear(self))

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

        ### --------------------- Password Evaluation -------------------------
        PasswordEvaluation.init(self) # Initialize the password evaluation page
        PasswordEvaluation.LoadWordlist(self) # Load the wordlist from the file

        # Initialize the password field
        self.btn_showPassword.setIcon(self.hide_icon)
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        
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

        ### --------------------- Message Digest ------------------------------
        MessageDigest.LoadAPIKey(self) # Load API Key from config file
        
        # Event Button Page Message Digest
        self.btn_browseMSDigest.clicked.connect(lambda: MessageDigest.openFileDialog(self))
        self.btn_clearMSDigest.clicked.connect(lambda: MessageDigest.clear(self))
        self.btn_saveQR.clicked.connect(lambda: MessageDigest.saveQRCode(self))
        self.btn_lineAPI.clicked.connect(lambda: MessageDigest.showBtnLine(self, MessageDigest.state_line))
        self.btn_sendMSDigest.clicked.connect(lambda: MessageDigest.processLineKey(self))
        self.btn_copy.clicked.connect(lambda: MessageDigest.copyOutput(self))
        self.btn_infoToken.clicked.connect(lambda: MessageDigest.infoToken(self))
        self.lineEdit_outputTextMSDigest.textChanged.connect(lambda: MessageDigest.qrCodeGenerator(self, self.lineEdit_outputTextMSDigest.text()))
        
        ### --------------------- Malware Scan --------------------------------
        MalwareScanning.show_resultimage(self, type='scan', status='default') # Initialize the image
        MalwareScanning.loadAPIKey(self) # Load API Key from config file
        
        # Event Button Page Malware Scan
        self.btn_scanMalware.clicked.connect(lambda: MalwareScanning.scanMalware(self))
        self.btn_browseMalware.clicked.connect(lambda: MalwareScanning.openFileScanning(self))
        self.btn_clearMalware.clicked.connect(lambda: MalwareScanning.clear(self))
        self.btn_createReport.clicked.connect(lambda: MalwareScanning.createReport(self))
        self.btn_sendEmail.clicked.connect(lambda: MalwareScanning.sendEmail(self))

        ### --------------------- Vulnerability -------------------------------

        # Event Button Page Vulnerability
        self.btn_scanVulner.clicked.connect(lambda: VulnerabilityScanning.prepareCommand(self))
        self.btn_clearVulner.clicked.connect(lambda: VulnerabilityScanning.clear(self))
        self.dropdown_typeScan.activated.connect(lambda: VulnerabilityScanning.typeScan(self))

        ### --------------------- HTTPS Testing -------------------------------

        # Event Button Page HTTPS Testing
        self.btn_scanHttps.clicked.connect(lambda: HTTPSTesting.scanHTTPS(self))
        self.btn_clearHttps.clicked.connect(lambda: HTTPSTesting.clear(self))
        self.lineEdit_https.textChanged.connect(lambda: HTTPSTesting.checkHTTPS(self))
    
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
        self.lineEdit_MSdigest.textChanged.connect(lambda: MessageDigest.checkFile_Text(self))
        MessageDigest.showBtnLine(self, False) # Hide the Line Notify button

    # Network User ------------------------------------------
    def openNetworkUserHome(self):
        self.stackedWidget.setCurrentWidget(self.page_networkUser)

    def openVulnerabilityHome(self):
        self.stackedWidget.setCurrentWidget(self.page_vulnerability)
        VulnerabilityScanning.showWellKnownPorts(self)
    
    def openHttpsHome(self):
        self.stackedWidget.setCurrentWidget(self.page_https)

    def openSettings(self):
        self.stackedWidget.setCurrentWidget(self.page_settings)

        # Load Message Digest API Key from file config
        line_api_key = MessageDigest.LoadAPIKey(self)
        self.lineEdit_LineAPISettings.setText(line_api_key)

        # Load Malware API Key from file config
        virustotal_api_key = MalwareScanning.getAPIKey(self)
        self.lineEdit_virusTotalAPISettings.setText(virustotal_api_key)
    
    def saveSetting(self):
        pass

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