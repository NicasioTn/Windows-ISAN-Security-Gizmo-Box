from PyQt6.QtWidgets import QDialog

class HSTSTesting(QDialog):

    def __init__(self):
        #super(HSTSTesting, self).__init__()
        super().__init__()

    def clear(self):
        self.lineEdit_hsts.setText('')

    def scanHSTS(self):
        self.lineEdit_hsts.text()
        print("HSTS Testing")