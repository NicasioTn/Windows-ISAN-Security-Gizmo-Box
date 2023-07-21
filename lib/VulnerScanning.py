
import os
import sys
import time
import nmap
from PyQt6.uic import loadUi
from datetime import datetime
from tabulate import tabulate
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,  QDialog, QFileDialog
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QThread, pyqtSignal, QCoreApplication, Qt

# Reference Tool path for Nmap
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Nmap"

class NmapScanThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool)
    
    def __init__(self, target, options):
        super().__init__()
        self.target = target
        self.options = options
        
    def run(self):
        nm = nmap.PortScanner()
        nm.scan(self.target, arguments=self.options)
        self.finished_signal.emit(True)
        
        result = []
        
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    state = nm[host][proto][port]['state']
                    service = nm[host][proto][port]['name']
                    version = nm[host][proto][port]['version']
                    cve = nm[host][proto][port]['cpe']
                    result.append([port, state, service, version, cve])
                    
        #print(result)
        # for host in nm.all_hosts():
        #     print('----------------------------------------------------')
        #     print('Host : %s (%s)' % (host, nm[host].hostname()))
        #     print('State : %s' % nm[host].state())
        #     for proto in nm[host].all_protocols():
        #         print('----------')
        #         print('Protocol : %s' % proto)
                
        #         listport = nm[host][proto].keys()
        #         listport.sort()
        #         for port in list:
        #             print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
                    
            
        table = tabulate(result, headers=["Port", "State", "Service", "Version", "CVE"])
        self.result = (table, result)

        # Calculate progress and emit signal
        total = len(nm.all_hosts())
        progress = 0
        for host in nm.all_hosts():
            if nm[host].state() != "up":
                continue
            progress += 1
            self.progress_signal.emit(int(progress / total * 100))

class VulnerabilityScan(QDialog):
    # properties
    mode = "Default Fast Scan"
    
    def __init__(self):
        super(VulnerabilityScan, self).__init__()
        loadUi("./Files/Vulnerability_Scanning.ui", self)
        self.setWindowTitle("Vulnerability Scan")
        self.window_icon = QIcon("./Images/logo.png")
        
        self.logo = QPixmap("./Images/logo.png")
        
        self.setWindowIcon(self.window_icon)
        self.logo_Label.setPixmap(self.logo)
        
        self.progressBar.setVisible(False)
        # Events Click
        self.scan_Button.clicked.connect(self.scan)
        
        self.result_tabWidget.setColumnCount(5)
        self.result_tabWidget.setHorizontalHeaderLabels(["Port", "State", "Service", "Version", "CVE"])
        self.result_tabWidget.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F2F2F2;
                selection-background-color: #BBD8E9;
                selection-color: #000000;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #D9E5EF;
                color: #000000;
                padding: 5px;
                border: 1px solid #CCCCCC;   
            }
        """)
        self.clear_Button.clicked.connect(self.clear)
        self.stealth_Button.clicked.connect(self.stealth)
        self.aggressive_Button.clicked.connect(self.aggressive)
        self.adaptive_Button.clicked.connect(self.adaptive)
        self.vulner_Button.clicked.connect(self.vulner)
    
    def stealth(self):
        self.options_LineEdit.setText("-sS -sF")
        self.setMode("Stealth")
    
    def aggressive(self):
        self.options_LineEdit.setText("-sS -sV -O ")
        self.setMode("Aggressive")
        
    def adaptive(self):
        self.options_LineEdit.setText("-sS -sV -O -T4 -A -v -p- ")
        self.setMode("Adaptive")
        
    def vulner(self):
        self.options_LineEdit.setText("--script vuln --script-args vulscandb=scipvuldb.csv")
        self.setMode("Vulner.NSE Script")
        
    def setMode(self, mode):
        self.mode = mode
        
    def getMode(self):
        return self.mode
    
    def clear(self):
        self.result_tabWidget.clear()
        self.result_tabWidget.setHorizontalHeaderLabels(["Port", "State", "Service", "Version", "CVE"])
        self.date_Label.clear()
        self.host_Label.clear()
        self.target_LineEdit.clear()
        self.options_LineEdit.clear()
        self.statusScan_Label.clear()
        self.date_Label.setText("Date-Time:")
        self.progressBar.setVisible(False)
        
                
    def scan(self):
        self.statusScan_Label.clear()
        target = self.target_LineEdit.text()
        if target == "":
            self.statusScan_Label.setText("Please enter the target to scan!!")
            return
        options = self.options_LineEdit.text()
        
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_Label.setText(f"Date-Time: {date_time}")
        self.host_Label.setText(f"Target: {target}\nScan Mode: {self.getMode()}\nOptions: {options}")
        
        self.progressBar.setValue(0)
        time.sleep(2)
        self.progressBar.setVisible(True)
        
        self.thread = NmapScanThread(target, options)
        self.thread.progress_signal.connect(self.update_progress_bar)
        self.thread.finished_signal.connect(self.handle_scan_finished)
        self.thread.start()

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)

    def handle_scan_finished(self, success):
        if success:
            self.progressBar.setValue(100)
            time.sleep(2)  # import time
            self.progressBar.setVisible(False)
            table, result = self.thread.result
            self.statusScan_Label.setText("Scan Success")
            self.result_tabWidget.setRowCount(len(result))
            for i, row in enumerate(result):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.result_tabWidget.setItem(i, j, item)
        else:
            self.statusScan_Label.setText("Scan Failed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VulnerabilityScan()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    
    
