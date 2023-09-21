import os
import sys
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from pathlib import Path
from PyQt6.QtGui import QIcon
import hashlib
import qrcode
import json

class Hashing:
    
    def md5(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def sha1(self, data):
        return hashlib.sha1(data.encode('utf-8')).hexdigest()

    def sha224(self, data):
        return hashlib.sha224(data.encode('utf-8')).hexdigest()

    def sha256(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def sha384(self, data):
        return hashlib.sha384(data.encode('utf-8')).hexdigest()

    def sha512(self, data):
        return hashlib.sha512(data.encode('utf-8')).hexdigest()

    def sha3_224(self, data):
        return hashlib.sha3_224(data.encode('utf-8')).hexdigest()

    def sha3_256(self, data):
        return hashlib.sha3_256(data.encode('utf-8')).hexdigest()

    def sha3_384(self, data):
        return hashlib.sha3_384(data.encode('utf-8')).hexdigest()

    def sha3_512(self, data):
        return hashlib.sha3_512(data.encode('utf-8')).hexdigest()

class MessageDigest(QDialog):
    # properties
    state_browse_file = False

    hint_btn = []

    def __init__(self):
        super(MessageDigest, self).__init__()
        loadUi("./assets/ui/Message_Digest.ui", self)
        self.setWindowTitle("Message Digest")
        self.window_icon = QIcon("./assets/icons/logo.png")
        self.logo = QPixmap("./assets/icons/logo.png")

        ## Run on Kali Linux
        '''
        loadUi("/home/kali/Gizmo/Files/Message_Digest.ui", self)
        self.setWindowTitle("Message Digest")
        self.window_icon = QIcon("/home/kali/Gizmo/Images/logo.png")
        self.logo = QPixmap("/home/kali/Gizmo/Images/logo.png")
        
        '''
        
        self.setWindowIcon(self.window_icon)
        self.logo_Label.setPixmap(self.logo)
        
        # Event Clicked
        self.MD5_Button.clicked.connect(self.Md5)
        self.SHA1_Button.clicked.connect(self.Sha1)
        self.SHA2_224_Button.clicked.connect(self.Sha2_224)
        self.SHA2_256_Button.clicked.connect(self.Sha2_256)
        self.SHA2_384_Button.clicked.connect(self.Sha2_384)
        self.SHA2_512_Button.clicked.connect(self.Sha2_512)
        self.SHA3_224_Button.clicked.connect(self.Sha3_224) 
        self.SHA3_256_Button.clicked.connect(self.Sha3_256)
        self.SHA3_384_Button.clicked.connect(self.Sha3_384)
        self.SHA3_512_Button.clicked.connect(self.Sha3_512)
        self.clear_Button.clicked.connect(self.input.clear)
        self.clear_Button.clicked.connect(self.clearResult)
        self.save_Button.clicked.connect(self.saveQR)
        self.browse_Button.clicked.connect(self.open_file_dialog)

        # Load the list of hints from the JSON file
        with open('./data/hint.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        for item in json_object:
            self.hint_btn.append(str(item['tool_description'])) 

        # Set the tooltips for the buttons
        self.MD5_Button.setToolTip(self.hint_btn[0])
        self.SHA1_Button.setToolTip(self.hint_btn[1])
        self.SHA2_224_Button.setToolTip(self.hint_btn[2])
        self.SHA2_256_Button.setToolTip(self.hint_btn[3])
        self.SHA2_384_Button.setToolTip(self.hint_btn[4])
        self.SHA2_512_Button.setToolTip(self.hint_btn[5])
        self.SHA3_224_Button.setToolTip(self.hint_btn[6])
        self.SHA3_256_Button.setToolTip(self.hint_btn[7])
        self.SHA3_384_Button.setToolTip(self.hint_btn[8])
        self.SHA3_512_Button.setToolTip(self.hint_btn[9])

        self.save_Button.setToolTip("Save QR Code to a file on your computer")
    # Save QR-Code Section ---------------------------------------------
    def saveQR(self,):
        pathfile, ok = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Images (*.png *.jpg)")
        
        # Check if a filename was provided
        if pathfile: # show place to save
            print("Save at: ", pathfile)
            # Save QR-Code with pixmap at pathfile
            if not self.output_QR_Label.pixmap().isNull():
                # Save the pixmap to the specified file path
                self.output_QR_Label.pixmap().save(pathfile, 'PNG')
                # Set the text of the save button to "SAVED!" to indicate successful save
                self.save_Button.setText("SAVED!")
            else:
                print("Error: QR-Code is Not Generated")
        else:
            print("Error: No file name specified")
    
    # Clear Section ---------------------------------------------
    def clearResult(self):
        self.output_hash_Label.setText('')
        self.output_QR_Label.setText(' ')
        self.save_Button.setText("SAVE")
    
    # Hash Algorithms Section ---------------------------------------------
    def Md5(self):
        if os.path.isfile(self.input.text()):
            path_direct = self.getPath()
            init_hash = hashlib.md5()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash MD5: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                md5 = Hashing.md5(self, self.input.text())
                print(f'MD5: {md5}')
                self.output_hash_Label.setText(f'{md5}')
                self.qrCodeGenerator(md5)
                
    def Sha1(self):
        if os.path.isfile(self.input.text()):
            path_direct = self.getPath()
            init_hash = hashlib.sha1()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA1: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha1 = Hashing.sha1(self, self.input.text())
                print(f"SHA1: {sha1}")
                self.output_hash_Label.setText(f'{sha1}')
                self.qrCodeGenerator(sha1)
               
    def Sha2_224(self):
        if os.path.isfile(self.input.text()):
            init_hash = hashlib.sha224() 
            path_direct = self.getPath()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA2_224: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha2 = Hashing.sha256(self, self.input.text())
                print(f'SHA2_224: {sha2}')
                self.output_hash_Label.setText(f'{sha2}')
                self.qrCodeGenerator(sha2)
                
    def Sha2_256(self):
        if os.path.isfile(self.input.text()):
            init_hash = hashlib.sha256()
            path_direct = self.getPath()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA2_256: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha2 = Hashing.sha256(self, self.input.text())
                print(f'SHA2_256: {sha2}')
                self.output_hash_Label.setText(f'{sha2}')
                self.qrCodeGenerator(sha2)
    
    def Sha2_384(self):
        if os.path.isfile(self.input.text()):
            init_hash = hashlib.sha384()
            path_direct = self.getPath()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA2_384: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha2 = Hashing.sha384(self, self.input.text())
                print(f'SHA2_384: {sha2}')
                self.output_hash_Label.setText(f'{sha2}')
                self.qrCodeGenerator(sha2)
                
    def Sha2_512(self):
        if os.path.isfile(self.input.text()):
            init_hash = hashlib.sha512()
            path_direct = self.getPath()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA2_512: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha2 = Hashing.sha512(self, self.input.text())
                print(f'SHA2_512: {sha2}')
                self.output_hash_Label.setText(f'{sha2}')
                self.qrCodeGenerator(sha2)
                
    def Sha3_224(self):
        if os.path.isfile(self.input.text()):
            init_hash = hashlib.sha3_224()
            path_direct = self.getPath()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA3_224: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha3 = Hashing.sha3_256(self, self.input.text())
                print(f'SHA3_224: {sha3}')
                self.output_hash_Label.setText(f'{sha3}')
                self.qrCodeGenerator(sha3)
    
    def Sha3_256(self):
        if os.path.isfile(self.input.text()):
            init_hash = hashlib.sha3_256()
            path_direct = self.getPath()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA3_256: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha3 = Hashing.sha3_256(self, self.input.text())
                print(f'SHA3_256: {sha3}')
                self.output_hash_Label.setText(f'{sha3}')
                self.qrCodeGenerator(sha3)
            
    def Sha3_384(self):
        if os.path.isfile(self.input.text()):
            init_hash = hashlib.sha3_384()
            path_direct = self.getPath()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA3_384: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha3 = Hashing.sha3_384(self, self.input.text())
                print(f'SHA3_512: {sha3}')
                self.output_hash_Label.setText(f'{sha3}')
                self.qrCodeGenerator(sha3)
                
    def Sha3_512(self):
        if os.path.isfile(self.input.text()):
            init_hash = hashlib.sha3_512()
            path_direct = self.getPath()
            file = path_direct 
            BLOCK_SIZE = 65536 
            with open(file, 'rb') as f: 
                fb = f.read(BLOCK_SIZE) 
                while len(fb) > 0: 
                    init_hash.update(fb) 
                    fb = f.read(BLOCK_SIZE) 
            file_hashed =  init_hash.hexdigest()
            print (f"This is file hash SHA3_512: {file_hashed}") 
            self.output_hash_Label.setText(f'{file_hashed}')
            self.qrCodeGenerator(file_hashed)
        else:
            if(self.input.text() == ''):
                print("Error: Text is Empty")
            else:
                sha3 = Hashing.sha3_512(self, self.input.text())
                print(f'SHA3_512: {sha3}')
                self.output_hash_Label.setText(f'{sha3}')
                self.qrCodeGenerator(sha3)
                
    # QR-Code Section ---------------------------------------------
    def qrCodeGenerator(self, hash):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(hash)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("./data/MessageDigest-QRCode.png")
        ## Run on Kali Linux
        '''
        img.save("/home/kali/Gizmo/SaveQR/MessageDigest-QRCode.png")
        '''
        self.ShowImage_QR() # show image
        
    
    # Browse File Section ---------------------------------------------
    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            # self,
            # "Select a File", 
            # "D:\\icons\\avatar\\", 
            # "Images (*.png *.jpg)"
            self,
            "Select a File", 
            "D:\\icons\\avatar\\", 
            "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            path = Path(filename)
            self.input.setText(str(path))
            if path.exists(): # check if file exists 
                print("File exists")
            print(path) 
            
            self.state_browse_file = True # browsed file 
            if(self.state_browse_file == True):
                #hashfile = self.hash_file(path, self.state)
                self.setPath(path)
                
    # Show Image Section ---------------------------------------------
    def ShowImage_QR(self):
        imagePath = "./data/MessageDigest-QRCode.png"
        ## Run on Kali Linux
        '''
        imagePath = "/home/kali/Gizmo/SaveQR/MessageDigest-QRCode.png"
        '''
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaledToWidth(200)
        pixmap = pixmap.scaledToHeight(200)
        self.output_QR_Label.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())
            
    def setPath(self, path):
        self.path = path
    
    def getPath(self):
        return self.path
    
    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MessageDigest()
    window.setFixedHeight(700)
    window.setFixedWidth(1200)
    window.setMinimumSize(1200, 700)
    window.setMaximumSize(1200, 700)
    window.show()
    sys.exit(app.exec())     
    
