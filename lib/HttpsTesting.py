
import sys
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QWidget, QDialog
from PyQt6 import QtWidgets, uic
import re
import smtplib
import hstspreload
from urllib.parse import urlparse
'''import csv

filename = "summary_msu.csv"
value_to_search = 'Final Score'
data = []

with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
            cleaned_row = [elem.replace("\x1b[1m", "").replace("\x1b[m", "").replace("Final Score","").replace(" ","") for elem in row]
            print(cleaned_row)
            data.append(cleaned_row)'''

class httpsScreen(QDialog):
    def __init__(self):
        super(httpsScreen, self).__init__()
        loadUi("./assets/ui/HTTPS_Testing.ui", self)
        #self.back_Button.clicked.connect(self.gotonetworkmenu)
        self.scan_Button.clicked.connect(self.summary)
        self.send_Button.clicked.connect(self.sendmail)

        
    def summary(self):

        self.input_mail.setText('')
        self.warning_mail.setText('')
        url_pattern = re.compile(r'http?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        input = self.input_Text.text()
        print(input)

        if url_pattern.match(input):
            print("HTTP")
            self.warning_Label.setText('Fatal error: "http" is not what you meant probably')
        else:
            print("HTTPS")
            self.warning_Label.setText('')
        
         #check HSTS preload 
        domain = urlparse(input).netloc.split(':')[0]    
        
        if hstspreload.in_hsts_preload(domain):
            print(f"{domain} is eligible for HSTS preloading")
            self.HSTS_Result.setText(f"{domain} is eligible for HSTS preloading")
        else:
            print(f"{domain} is not eligible for HSTS preloading.")
            self.HSTS_Result.setText(f"{domain} is eligible for HSTS preloading")
                
       
    def sendmail(self):

        mail_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
        email = self.input_mail.text()
        
        if mail_pattern.match(email):
            print("EMAIL")
            print(email)
            self.warning_mail.setText('')
           
        else:
            print("NOT EMAIL")
            self.warning_mail.setText('Plaest Enter Email!')



             #send Email
            sender_email = "kanjanatk16@gmail.com"
            receiver_email = email
            password = "vaox msyy dtvn dper"

            message = "Subject: This is a test email\n\nHello,\n\nThis is a test email sent using Python."
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
            self.warning_mail.setText('Sended to Email')
  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = httpsScreen()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())



