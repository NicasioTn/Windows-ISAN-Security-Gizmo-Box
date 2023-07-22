import sys
import os
from math import log2
import time
from PyQt6.QtWidgets import ( QApplication, QDialog, )
from math import log2
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi

class Main(QDialog):

    def __init__(self):
        super(Main, self).__init__()
        loadUi("./assets/ui/main.ui", self)

        self.setWindowTitle("Main")
        self.setWindowIcon(QIcon("./assets/icons/Logo.png"))

        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    