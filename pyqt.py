from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic
import random
import pickle
import functions as func
import time
import os
import serial

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from google.cloud import storage


def check_password(self):                   # checking password function
    if self.keypad is True:
        if len(self.password) == 6 and self.password == self.ans:
            self.ui.lbl.setText("Loading...")
            self.ui.lbl.repaint()
            self.password = ""
            self.disp = ""
            if self.facerecog is True:
                result_name, result_accur = face(self)
                if result_name == 'Unknown' or result_name == 'Joohyeong' or float(result_accur) < 97:
                    self.ui.lbl.setText("Retry")
                    self.pnp = False
                    self.ser.write(str(int(self.pnp)).encode())
                else:
                    self.ui.lbl.setText("Welcome")
                    self.pnp = True
                    self.ser.write(str(int(self.pnp)).encode())
                print("Face is " + str(self.pnp))
                random_keypad(self)
            else:
                self.pnp = True
                self.ser.write(str(int(self.pnp)).encode())
                print("Password is " + str(self.pnp))
                self.ui.lbl.setText("Welcome")

            random_keypad(self)
            return self.pnp

        elif len(self.password) == 6 and self.password != self.ans:
            self.password = ""
            self.disp = ""
            self.ui.lbl.setText("Retry!!")
            self.pnp = False
            self.ser.write(str(int(self.pnp)).encode())
            random_keypad(self)
            print("Password is " + str(self.pnp))
            return self.pnp

    elif self.facerecog is True and self.keypad is False:
        self.password = ""
        self.disp = ""
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        result_name, result_accur = face(self)
        if result_name == "Unknown" or result_name == 'Joohyeong' or float(result_accur) < 97:
            self.ui.lbl.setText("Retry!!")
            self.pnp = False
            self.ser.write(str(int(self.pnp)).encode())
        else:
            self.ui.lbl.setText("Welcome")
            self.pnp = True
            self.ser.write(str(int(self.pnp)).encode())

        print("Face is " + str(self.pnp))
        return self.pnp


def face(self):
    start = time.time()
    func.cam_shot()
    names, accur = func.face_recognize()
    print(str(round(time.time()-start, 2))+" seconds")
    if self.i==4:
        self.i = 0

    if names == 'Unknown' or names == 'Joohyeong' or float(accur) < 97:
        imagePath = "Faces/Pred/face.jpg"
        imageBlob = self.bucket.blob("User/"+self.count_fm[self.i]+".jpg")
        imageBlob.upload_from_filename(imagePath)
        self.i += 1

    return names, accur


def random_keypad(self):
    self.randkeypad = []            # allocating random keypad function
    for i in range(10):  # random number
        while self.rand in self.randkeypad:
            self.rand = random.randint(0, 9)
        self.randkeypad.append(self.rand)
    self.ui.btn0.setText(str(self.randkeypad[0])), self.ui.btn0.setStyleSheet("border:0px;")
    self.ui.btn1.setText(str(self.randkeypad[1])), self.ui.btn1.setStyleSheet("border:0px;")
    self.ui.btn2.setText(str(self.randkeypad[2])), self.ui.btn2.setStyleSheet("border:0px;")
    self.ui.btn3.setText(str(self.randkeypad[3])), self.ui.btn3.setStyleSheet("border:0px;")
    self.ui.btn4.setText(str(self.randkeypad[4])), self.ui.btn4.setStyleSheet("border:0px;")
    self.ui.btn5.setText(str(self.randkeypad[5])), self.ui.btn5.setStyleSheet("border:0px;")
    self.ui.btn6.setText(str(self.randkeypad[6])), self.ui.btn6.setStyleSheet("border:0px;")
    self.ui.btn7.setText(str(self.randkeypad[7])), self.ui.btn7.setStyleSheet("border:0px;")
    self.ui.btn8.setText(str(self.randkeypad[8])), self.ui.btn8.setStyleSheet("border:0px;")
    self.ui.btn9.setText(str(self.randkeypad[9])), self.ui.btn9.setStyleSheet("border:0px;")
    self.ui.btn_setting.setStyleSheet("border:0px;")
    self.ui.btn_reset.setStyleSheet("border:0px;")


class MyWindow(QMainWindow):
    password = ""                      # input password record
    with open('Utils/password.p', 'rb') as file:
        ans = pickle.load(file)
    rand = random.randint(0, 9)        # random number
    disp = ""                          # hide display "*"
    pnp = False                        # Boolean pass

    count_fm = ["007", "008", "009", "010"]
    i=0

    # real time Database
    cred = credentials.Certificate('Utils/capstone-ffa4f-firebase-adminsdk-qsa08-5ecf49e747.json')
    firebase_admin.initialize_app(cred,{
        'databaseURL': 'https://capstone-ffa4f.firebaseio.com/'})
    ref = db.reference('System/')
    facerecog = ref.get()['face_recog'] # System face_recog from DB
    keypad = ref.get()['keypad']        # System keypad from DB

    # Storage to take face photo
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Utils/capstone-ffa4f-firebase-adminsdk-qsa08-5ecf49e747.json"
    client = storage.Client()
    bucket = client.get_bucket('capstone-ffa4f.appspot.com')

    port = "/dev/ttyUSB0"
    ser = serial.Serial(port, 9600)

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("UI/keypadv2.ui", self)
        self.setWindowTitle("Smart Door Lock")
        self.facerecog = self.ref.get()['face_recog']  # System face_recog from DB
        self.keypad = self.ref.get()['keypad']  # System keypad from DB
        random_keypad(self)

        self.ui.btn0.clicked.connect(self.btn0_clicked)                 # 0~9 keypad button
        self.ui.btn1.clicked.connect(self.btn1_clicked)
        self.ui.btn2.clicked.connect(self.btn2_clicked)
        self.ui.btn3.clicked.connect(self.btn3_clicked)
        self.ui.btn4.clicked.connect(self.btn4_clicked)
        self.ui.btn5.clicked.connect(self.btn5_clicked)
        self.ui.btn6.clicked.connect(self.btn6_clicked)
        self.ui.btn7.clicked.connect(self.btn7_clicked)
        self.ui.btn8.clicked.connect(self.btn8_clicked)
        self.ui.btn9.clicked.connect(self.btn9_clicked)
        self.ui.btn_setting.clicked.connect(self.btn_setting_clicked)    # System Setting
        self.ui.btn_reset.clicked.connect(self.btn_reset_clicked)        # setting new password

    def btn0_clicked(self):
        self.password = self.password + str(self.randkeypad[0])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn1_clicked(self):
        self.password = self.password + str(self.randkeypad[1])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn2_clicked(self):
        self.password = self.password + str(self.randkeypad[2])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn3_clicked(self):
        self.password = self.password + str(self.randkeypad[3])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn4_clicked(self):
        self.password = self.password + str(self.randkeypad[4])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn5_clicked(self):
        self.password = self.password + str(self.randkeypad[5])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn6_clicked(self):
        self.password = self.password + str(self.randkeypad[6])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn7_clicked(self):
        self.password = self.password + str(self.randkeypad[7])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn8_clicked(self):
        self.password = self.password + str(self.randkeypad[8])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn9_clicked(self):
        self.password = self.password + str(self.randkeypad[9])
        self.disp = self.disp + "*"
        self.ui.lbl.setText(self.disp)
        self.ui.lbl.repaint()
        self.pnp = check_password(self)

    def btn_setting_clicked(self):
        if self.pnp is False:
            self.ui.lbl.setText("Enter your password")
            self.ui.lbl.repaint()
        else:
            new_password = NewPassword()
            new_password.exec_()
            self.ans = new_password.ans
            random_keypad(self)
            self.ui.lbl.setText("Newly applied!")
            self.ui.lbl.repaint()

    def btn_reset_clicked(self):
        self.facerecog = self.ref.get()['face_recog']   # System face_recog from DB
        self.keypad = self.ref.get()['keypad']          # System keypad from DB
        if self.pnp is True:
            class System(QDialog):
                # Firebase DB Data
                keypad = self.keypad
                facerecog = self.facerecog

                def __init__(self):
                    super().__init__()
                    self.ui = uic.loadUi("UI/system.ui", self)
                    self.setWindowTitle("System Setting")
                    self.ui.radbtn1.clicked.connect(self.radbtn_function)
                    self.ui.radbtn2.clicked.connect(self.radbtn_function)
                    self.ui.radbtn1.setChecked(self.facerecog)
                    self.ui.radbtn2.setChecked(self.keypad)
                    self.ui.btn1.clicked.connect(self.btn1_clicked), self.ui.btn1.setStyleSheet("border:0px;")
                    self.ui.btn2.clicked.connect(self.btn2_clicked), self.ui.btn2.setStyleSheet("border:0px;")

                def btn1_clicked(self):
                    self.facerecog = self.ui.radbtn1.isChecked()
                    self.keypad = self.ui.radbtn2.isChecked()
                    ## Firebase DB Upload
                    print("System : F=" + str(self.facerecog) + " K=" + str(self.keypad))
                    self.close()

                def btn2_clicked(self):
                    print("System : F=" + str(self.facerecog) + " K=" + str(self.keypad))
                    self.close()

                def radbtn_function(self):
                    if self.ui.radbtn2.isChecked() is False and self.ui.radbtn1.isChecked() is False:
                        self.ui.lbl.setText("More than one")
                        self.ui.lbl.repaint()
                        self.ui.btn1.setEnabled(False)
                        self.ui.btn2.setEnabled(False)
                    else:
                        self.ui.btn1.setEnabled(True)
                        self.ui.btn2.setEnabled(True)
                        self.ui.lbl.setText("")
            system = System()
            system.exec_()
            self.password = ""
            self.disp = ""
            self.ui.lbl.setText(self.disp)
            self.ui.lbl.repaint()
            self.facerecog = system.facerecog
            self.keypad = system.keypad
            # DB update start
            self.ref.update({'face_recog' : self.facerecog})
            self.ref.update({'keypad': self.keypad})
            # DB update end
            self.pnp = False
        else:
            self.pnp = False
            self.ui.lbl.setText("Enter PW")
            random_keypad(self)


class NewPassword(QDialog):
    password = ""                      # write to label
    with open('Utils/password.p', 'rb') as file:
        ans = pickle.load(file)
    rand = random.randint(0, 9)        # for random number
    disp = ""                          # hide password to display feedback
    pnp = False
    count = 1

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("UI/newpassword.ui", self)
        self.setWindowTitle("Setting new password")
        self.randkeypad = []  # allocating random keypad function
        for i in range(10):  # random number
            while self.rand in self.randkeypad:
                self.rand = random.randint(0, 9)
            self.randkeypad.append(self.rand)
        self.ui.btn0.setText(str(self.randkeypad[0])), self.ui.btn0.setStyleSheet("border:0px;")
        self.ui.btn1.setText(str(self.randkeypad[1])), self.ui.btn1.setStyleSheet("border:0px;")
        self.ui.btn2.setText(str(self.randkeypad[2])), self.ui.btn2.setStyleSheet("border:0px;")
        self.ui.btn3.setText(str(self.randkeypad[3])), self.ui.btn3.setStyleSheet("border:0px;")
        self.ui.btn4.setText(str(self.randkeypad[4])), self.ui.btn4.setStyleSheet("border:0px;")
        self.ui.btn5.setText(str(self.randkeypad[5])), self.ui.btn5.setStyleSheet("border:0px;")
        self.ui.btn6.setText(str(self.randkeypad[6])), self.ui.btn6.setStyleSheet("border:0px;")
        self.ui.btn7.setText(str(self.randkeypad[7])), self.ui.btn7.setStyleSheet("border:0px;")
        self.ui.btn8.setText(str(self.randkeypad[8])), self.ui.btn8.setStyleSheet("border:0px;")
        self.ui.btn9.setText(str(self.randkeypad[9])), self.ui.btn9.setStyleSheet("border:0px;")
        self.ui.btn_enter.setStyleSheet("border:0px;")

        self.ui.btn0.clicked.connect(self.btn0_clicked)  # 0~9 keypad button
        self.ui.btn1.clicked.connect(self.btn1_clicked)
        self.ui.btn2.clicked.connect(self.btn2_clicked)
        self.ui.btn3.clicked.connect(self.btn3_clicked)
        self.ui.btn4.clicked.connect(self.btn4_clicked)
        self.ui.btn5.clicked.connect(self.btn5_clicked)
        self.ui.btn6.clicked.connect(self.btn6_clicked)
        self.ui.btn7.clicked.connect(self.btn7_clicked)
        self.ui.btn8.clicked.connect(self.btn8_clicked)
        self.ui.btn9.clicked.connect(self.btn9_clicked)
        self.ui.btn_enter.clicked.connect(self.btn_enter_clicked)
        self.ui.lbl.setText("Enter new password")

    def btn0_clicked(self):
        self.password = self.password + str(self.randkeypad[0])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn1_clicked(self):
        self.password = self.password + str(self.randkeypad[1])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn2_clicked(self):
        self.password = self.password + str(self.randkeypad[2])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn3_clicked(self):
        self.password = self.password + str(self.randkeypad[3])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn4_clicked(self):
        self.password = self.password + str(self.randkeypad[4])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn5_clicked(self):
        self.password = self.password + str(self.randkeypad[5])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn6_clicked(self):
        self.password = self.password + str(self.randkeypad[6])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn7_clicked(self):
        self.password = self.password + str(self.randkeypad[7])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn8_clicked(self):
        self.password = self.password + str(self.randkeypad[8])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn9_clicked(self):
        self.password = self.password + str(self.randkeypad[9])
        self.ui.lbl.setText(self.password)
        self.ui.lbl.repaint()

    def btn_enter_clicked(self):
        if len(self.password) == 6:
            if self.count == 2 and self.password == self.ans:
                print(self.password)
                with open('Utils/password.p', 'wb') as file:
                    pickle.dump(self.ans, file)
                self.count = 1
                NewPassword.close(self)

            elif self.count == 2 and self.password != self.ans:
                self.ui.lbl.setText("Enter correctly")
                self.ui.lbl.repaint()
                self.password = ""

            else:
                self.ans = self.password
                self.password = ""
                self.ui.lbl.setText("Enter one more")
                self.count += 1

        else:
            self.password = ""
            self.ui.lbl.setText("Enter only six")
            self.ui.lbl.repaint()


if __name__ == "__main__":                  # start activity
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("image/icon.jpg"))
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

