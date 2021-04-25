# This Python file uses the following encoding: utf-8
import sys
import os
import socket
import threading
import pyautogui
import subprocess
import wmi
import time

import PIL.Image
import PIL.ImageTk
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,QFontDatabase, QIcon, QLinearGradient)
from PySide2.QtGui import (QPalette, QPainter, QPixmap,QRadialGradient)
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QListWidget,QFileDialog
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

import Kill
import Process
import Pic
import App

class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.setWindowTitle("client")
        self.load_ui()
        self.set_icon()
        self.client_ = None
        self.signal = False #check xem ket noi chua
        self.set_Button()


    def load_ui(self):
        loader = QUiLoader()  #gọi công cụ để load
        path = os.path.join(os.path.dirname(__file__), "form.ui")  #địa chỉ và tên của file mà mình muốn load file ở đây là form.ui
        ui_file = QFile(path) # tạo 1 biến là file đó
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self) #load file đó để hiện thị lên
        ui_file.close()

    def set_icon(self):
        appIcon = QIcon("logo.jpg")
        self.setWindowIcon(appIcon)


    def set_Button(self):

        self.cbutton = self.findChild(QPushButton,"ketnoi_Button")
        self.ebutton = self.findChild(QPushButton,"Exit_Button")
        self.abutton = self.findChild(QPushButton,"App_R_Button")
        self.pbutton = self.findChild(QPushButton,"Process_R_Button")
        self.kbutton = self.findChild(QPushButton,"Key_Stroke_Button")
        self.rbutton = self.findChild(QPushButton,"Fix_Reg_Button")
        self.picbutton = self.findChild(QPushButton,"Pic_Button")
        self.shutdown = self.findChild(QPushButton,"Turn_off_Button")

        self.cbutton.clicked.connect(self.check)
        self.ebutton.clicked.connect(self.exit_)
        self.abutton.clicked.connect(self.app_r)
        self.pbutton.clicked.connect(self.process_r)
        self.kbutton.clicked.connect(self.keystroke_r)
        self.rbutton.clicked.connect(self.reg)
        self.picbutton.clicked.connect(self.take_pic)
        self.shutdown.clicked.connect(self.turn_off)
    def turn_off(self):
        if self.client_ == None:
            self.message()
        elif self.client_ !=None:
            shut_down(self.client_)
    def take_pic(self):
        if self.client_ == None:
            self.message()
        elif self.client_ !=None:
            self.picture = Pic.pic(self.client_)
            self.picture.show()

    def reg(self):
        if self.client_ == None:
            self.message()
        elif  self.client_ != None:
            self.regis = Registry(self.client_)
            self.regis.show()

    def keystroke_r(self):
        if self.client_ == None:
            self.message()
        elif  self.client_ != None:
            self.key = Keystroke(self.client_)
            self.key.show()

    def process_r(self):
        if self.client_ == None:
            self.message()
        elif  self.client_ != None:
            self.list_app = Process.Process(self.client_)
            self.list_app.show()

    def app_r(self):
        if self.client_ == None:
            self.message()
        elif  self.client_ != None:
            self.list_app = App.Application(self.client_)
            self.list_app.show()

    def exit_(self):
        exit()

    def check(self):
        self.ipline = self.findChild(QLineEdit,"lineEdit").text()
        try:
            self.client_ = create(self.ipline)
            if self.client_ != None:
                self.signal = True
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Kết nối thành công")
            x = msg.exec_()
        except OSError:
            self.message()
    def message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Lỗi kết nối hệ thống")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()



class Keystroke(QWidget):
    def __init__(self,Client):
        super(Keystroke,self).__init__()
        self.client_ = Client
        self.setWindowTitle("Keystroke")
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"key.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()

        self.hbutton = self.findChild(QPushButton,"hook_Button")
        self.ubutton = self.findChild(QPushButton,"unhook_Button")
        self.dbutton = self.findChild(QPushButton,"delete_Button")
        self.prbutton = self.findChild(QPushButton,"printkey_Button")

        self.list = self.findChild(QListWidget,"list")
        self.dbutton.clicked.connect(self.delete_)

    def delete_(self):
        self.list = self.findChild(QListWidget,"list")
        self.list.clear()

class Registry(QWidget):
    def __init__(self,Client):
        super(Registry,self).__init__()
        self.client_ = Client
        self.setWindowTitle("registry")
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"reg.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()

#function client
def create(ipline: str):
    PORT = 5656
    FORMAT = 'utf-8'
    SERVER = ipline
    ADDR = (SERVER,PORT)

    Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Client.connect(ADDR)
    return Client


def shut_down(socket):
    socket.send(str.encode("shutdown"))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Form()
    widget.show()


    sys.exit(app.exec_())
