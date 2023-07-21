import sys
import os
from math import log2
import time
from PyQt6.QtWidgets import ( QApplication, QLineEdit,  QWidget, QLabel, QDialog, )
from PyQt6.QtCore import Qt
from math import log2
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
import subprocess

class DictAttack(QDialog):

    def __init__(self):
        super(DictAttack, self).__init__()
        loadUi("./assets/ui/Dict_attack.ui", self)

        self.setWindowTitle("Dictionary Attack")
        self.setWindowIcon(QIcon("./assets/icons/Logo.png"))

        self.start_Button.clicked.connect(self.startDickAttack)
        self.clear_Button.clicked.connect(self.clearState)


    def showResult(self, result):
        
        self.Result_Label.setText(str(result))
        self.Result_Label.setStyleSheet("color: rgb(255, 255, 255); font: 75 14pt \"MS Shell Dlg 2\";")

    def clearState(self):
        self.input_LineEdit.clear()

    def startDickAttack(self):
        password = self.getPasswords()
        return 0
        if password != "":
            os.system("cd D:\\Hashcat\\hashcat-6.2.5")
            command = "hashcat -m 0 -a 0 -o D:\\Github\\Gizmo\\Credentials\\Cracked\\Cracked.txt D:\\Github\\Gizmo\\Credentials\\Password\\Password.txt D:\\Github\\Gizmo\\Credentials\\Wordlist\\rockyou-30.txt"
            # Run the 'dir' command and capture the output in a temporary file
            os.system(f"{command} > D:\\Github\\Gizmo\\EveryThing\\temp.txt")

            # Read the output from the temporary file
            with open("D:\\Github\\Gizmo\\EveryThing\\temp.txt", "r") as file:
                output = file.read()

            # Remove the temporary file
            os.remove("D:\\Github\\Gizmo\\EveryThing\\temp.txt")

            # Print or use the 'output' variable as needed
            print(output)


        
        self.showResult(output)

    def getPasswords(self):
        passowrd = self.input_LineEdit.text()
        if passowrd == "":
            self.input_LineEdit.setPlaceholderText("Please Enter Password")
            self.input_LineEdit.setStyleSheet(
                " border: 5px solid rgba(255,0,0,255); color: rgb(255, 255, 255); text-align: center; border-top-left-radius :20px; border-top-right-radius :20px;  border-bottom-left-radius : 20px; border-bottom-right-radius : 20px;"  
            )
        else:
            self.input_LineEdit.setStyleSheet(
                " border: 5px solid rgba(0,255,0,255); color: rgb(255, 255, 255); text-align: center; border-top-left-radius :20px; border-top-right-radius :20px;  border-bottom-left-radius : 20px; border-bottom-right-radius : 20px;"  
            )

        return passowrd 
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DictAttack()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    