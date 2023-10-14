from PyQt6.QtWidgets import QDialog

class HTTPSTesting(QDialog):

    def __init__(self):
        #super(HTTPSTesting, self).__init__()
        super().__init__()

    def clear(self):
        self.lineEdit_https.setText('')

    def scanHTTPS(self):
        self.lineEdit_https.text()
        print("HSTS Testing")

    def checkHTTPS(self):
        text = self.lineEdit_https.text()
        print(text)