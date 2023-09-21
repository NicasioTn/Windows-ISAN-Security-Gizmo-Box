from PyQt6.QtWidgets import QDialog

class HSTSTesting(QDialog):

    def __init__(self):
        super(HSTSTesting, self).__init__()

    def clear(self):
        self.lineEdit_https.setText('')

    def scanHSTS(self):
        self.lineEdit_https.text()
        print("HSTS Testing")