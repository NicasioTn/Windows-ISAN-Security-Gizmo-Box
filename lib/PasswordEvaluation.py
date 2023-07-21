import sys
import os
from math import log2
from PyQt6.QtWidgets import ( QApplication, QLineEdit,  QWidget, QLabel, QDialog, )
from PyQt6.QtCore import Qt
from math import log2
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap

import json

class PasswordEvaluation(QDialog):
    
    # Initialize the properties of the class
    hide = True
    
    number = False
    lower = False
    upper = False
    symbol = False
    shift = False
    
    nordpass_common_passwords = []

    def __init__(self):
        super(PasswordEvaluation, self).__init__()
        loadUi("./assets/ui/Password_Evaluation.ui", self)
        # If you run on linux, you need to change the path of the ui file
        ### loadUi("/home/kali/Gizmo/Files/Password_Evaluation.ui", self)
        
        self.setWindowTitle("Password Evaluation")

        # Load the list of weak passwords
        with open('./data/nordpass_wordlist.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        for item in json_object:
            self.nordpass_common_passwords.append(str(item['Password'])) # Add the password to the list of weak passwords


        # Icons Init
        self.warning_icon = QIcon("./assets/icons/warning.png")
        self.check_icon = QIcon("./assets/icons/Checked.png")
        self.hide_icon = QIcon("./assets/icons/hide.png")
        self.unhid_icon = QIcon("./assets/icons/unhide.png")
        self.logo = QPixmap("./assets/icons/logo.png")
        self.window_icon = QIcon("./assets/icons/logo.png")
        
        '''
        self.warning_icon = QIcon("/home/kali/Gizmo/Images/warning.png")
        self.check_icon = QIcon("/home/kali/Gizmo/Images/Checked.png")
        self.hide_icon = QIcon("/home/kali/Gizmo/Images/hide.png")
        self.unhid_icon = QIcon("/home/kali/Gizmo/Images/unhide.png")
        self.logo = QPixmap("/home/kali/Gizmo/Images/logo.png")
        self.window_icon = QIcon("/home/kali/Gizmo/Images/logo.png")
        '''
        self.setWindowIcon(self.window_icon)
        self.logo_Label.setPixmap(self.logo)
        # Hide Input
        self.show_Button.setIcon(self.hide_icon)
        
        self.show_Button.setStyleSheet("background-color: transparent; border: none;")
        self.input_Text.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_Text.setMaxLength(100)
        self.show_Button.clicked.connect(self.showPasswd)
        # redirec to update input
        self.input_Text.textChanged.connect(self.update)
        
        
        
        # Initial hide checkboxes
        self.length8_check.setIcon(self.warning_icon)
        self.number_check.setIcon(self.warning_icon)
        self.upper_check.setIcon(self.warning_icon)
        self.lower_check.setIcon(self.warning_icon)
        self.symbol_check.setIcon(self.warning_icon)
       
        
    def showPasswd(self):
        if self.hide:
            self.input_Text.setEchoMode(QLineEdit.EchoMode.Normal)
            self.hide = False
            self.show_Button.setIcon(self.unhid_icon)
        else:
            self.input_Text.setEchoMode(QLineEdit.EchoMode.Password)
            self.hide = True
            self.show_Button.setIcon(self.hide_icon)
        
    def update(self):
        # Get the current password from the password edit widget
        password = self.input_Text.text()

        # Reset the checkbox states to unchecked
        self.length8_check.setChecked(False)
        self.number_check.setChecked(False)
        self.upper_check.setChecked(False)
        self.lower_check.setChecked(False)
        self.symbol_check.setChecked(False)
        
        # Find the password in the list of weak passwords
        if password == '':
            self.entropy_Label.setText('')
            self.warning_Start.setText('Start typing to see the entropy score')
            self.quality_Label.setText('')
        else:
            if password in self.nordpass_common_passwords:
                print(self.nordpass_common_passwords.index(password))
                self.warning_Start.setText('Found in the top 200 most common passwords by NordPass')
            else:
                self.warning_Start.setText('Not found in the list')
        
        
        for char in password:
            if char.isdigit():
                self.number_check.setChecked(True)
                self.number_check.setIcon(self.check_icon)
            elif char.isupper():
                self.upper_check.setChecked(True)
                self.upper_check.setIcon(self.check_icon)
            elif char.islower():
                self.lower_check.setChecked(True)
                self.lower_check.setIcon(self.check_icon)
            else:
                self.symbol_check.setChecked(True)
                self.symbol_check.setIcon(self.check_icon)
                
            if len(self.input_Text.text()) >= 8:
                self.length8_check.setChecked(True)
                self.length8_check.setIcon(self.check_icon)
        
        # Calculate the entropy of the password
        entropy = self.calculate_entropy(password)
        if entropy == 0:
            self.entropy_Label.setText(f'-- Bits')
            self.quality_Label.setText('')
        elif entropy > 999:
            self.entropy_Label.setText(f'~NaN Bits')
        else:
            self.entropy_Label.setText(f'~{entropy:.0f} Bits')

        # Check if the password meets the length and complexity requirements and display a warning if it doesn't
        length = len(password)        
        if length < 8:
            self.quality_Label.setText('So very, very bad Password length should be at least 8 characters')
            if length == 0:
                self.quality_Label.setText('')
        else : 
            if entropy < 50 :
                self.quality_Label.setText('Weak password')
            elif entropy < 80 :
                self.quality_Label.setText('Medium strength')
            else:
                self.quality_Label.setText('Good password')
        
        # Update the input length label
        self.charLength8_Label.setText(f'{length} Chars')

        # Update the time to crack label
        self.time_to_crack_Label.setText(f'Time To Crack: {self.time_to_Crack()}')
        
        
    def calculate_entropy(self, password):
        # Get the number of possible characters in the password
        if password == '':
            self.length8_check.setIcon(self.warning_icon)
            self.number_check.setIcon(self.warning_icon)
            self.upper_check.setIcon(self.warning_icon)
            self.lower_check.setIcon(self.warning_icon)
            self.symbol_check.setIcon(self.warning_icon)
            return 0
        
        possible_characters = 0
        if self.number_check.isChecked(): # 0-9
            possible_characters += 10
        if self.upper_check.isChecked(): # A-Z
            possible_characters += 26
        if self.lower_check.isChecked(): # a-z
            possible_characters += 26
        if self.symbol_check.isChecked(): # !@#$%^&*()_+-=
            possible_characters += 32
        # Calculate the entropy using the formula log2(possible_characters^password_length)
        self.total_Label.setText(f'Total {possible_characters} Chars')
        return log2(possible_characters) * len(password)
    

    def time_to_Crack(self):
        
        # Get the current password from the password edit widget
        password = self.input_Text.text()

        # check if password is empty
        if password == '':
            self.length8_check.setIcon(self.warning_icon)
            self.number_check.setIcon(self.warning_icon)
            self.upper_check.setIcon(self.warning_icon)
            self.lower_check.setIcon(self.warning_icon)
            self.symbol_check.setIcon(self.warning_icon)
            return 0
        # Get the number of possible characters in the password
        possible_characters = 0
        if self.number_check.isChecked(): # 0-9
            possible_characters += 10
        if self.upper_check.isChecked(): # A-Z
            possible_characters += 26
        if self.lower_check.isChecked(): # a-z
            possible_characters += 26
        if self.symbol_check.isChecked(): # !@#$%^&*()_+-=
            possible_characters += 32

        passwordType = possible_characters        
        combinations = passwordType ** len(password)
        
        KPS_2020 = 17042497.3 # 17 Million
        seconds = combinations / KPS_2020
        seconds = f'{seconds:.0f}'
        seconds = int(seconds)

        # hours = seconds // 3600  # Number of whole hours
        # minutes = (seconds % 3600) // 60  # Number of whole minutes remaining
        # seconds = seconds % 60  # Number of seconds remaining

        # return f'{hours} Hours, {minutes} Minutes, {seconds} Seconds' #f'{hours}:{minutes}:{seconds}'

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        weeks, days = divmod(days, 7)
        months, weeks = divmod(weeks, 4)
        years, months = divmod(months, 12)

        if years > 10:
            return "Please sleep wait for your next life."
    
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

        return ", ".join(time_parts)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordEvaluation()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    