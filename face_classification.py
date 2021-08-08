from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import functions_1 as func
import time


def face(self):
    start = time.time()
    func.cam_shot()
    names, accur = func.face_recognize()
    print(str(round(time.time()-start, 2))+" seconds")
    self.lbl3.setText(names + " is " + accur + "%")
    self.lbl3.repaint()
    return names


def classification(self, name):
    while True:
        if name == 'Unknown':
            self.lbl3.setText("Retry recognition")
            self.lbl3.repaint()
            break
        else:
            self.lbl3.setText("Welcome " + name)
            self.lbl3.repaint()
            break


class Form(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("UI/face.ui", self)
        gif = QMovie('image/pre_facing.gif')
        gif.setScaledSize(QSize().scaled(400, 400, Qt.KeepAspectRatio))
        self.ui.lbl4.setMovie(gif)
        gif.start()
        self.ui.btn_cap.clicked.connect(self.btn_cap_clicked)

    def btn_cap_clicked(self):
        classification(self, face(self))


if __name__ == "__main__":                  # start activity
    app = QApplication(sys.argv)
    Form = Form()
    Form.show()
    app.exec_()


