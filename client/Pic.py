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
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,QRadialGradient)
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QListWidget,QFileDialog
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

def receive_image(socket):
    while True:
        try:
            command = socket.recv(4096)
            if (command.decode() == "printscreen"):
                data = socket.recv(4096)
                size = int(data.decode())
                recv_fz = 0
                file = open('shot.jpg','wb')
                while not recv_fz == size:       # receive binary data relatively
                      if size - recv_fz > 4096:
                         recv_data = socket.recv(4096)
                         recv_fz +=len(recv_data)
                      else:
                         recv_data = socket.recv(size - recv_fz)
                         recv_fz = Size
                      file.write(recv_data)             #write all the received binary data to file
                file.close()
        except:
            break
def print_screen(socket):
    socket.send(str.encode("printscreen"))

class pic(QWidget):
    def __init__(self,Client):
        super(pic,self).__init__()
        self.client_ = Client
        self.signal = True #do ket noi roi moi dung duoc chuc nang chup hinh
        self.setWindowTitle("Picture")
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"pic.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()

        self.label = self.findChild(QLabel,"label")
        self.label.setAutoFillBackground(True)
        self.label.setScaledContents(False)
        self.label.setText("")
        self.takebutton = self.findChild(QPushButton,"pic_Button")
        self.savebutton = self.findChild(QPushButton,"save_Button")

        self.takebutton.clicked.connect(self.capture)
        self.savebutton.clicked.connect(self.save)


    def capture(self):
        print_screen(self.client_)
        receive_image(self.client_)
        self.displayImg()

    def displayImg(self):
        img = (QPixmap("shot.jpg"))
        scaled = img.scaled(self.label.size(),Qt.KeepAspectRatio)
        self.label.setPixmap(scaled)
        self.label.setScaledContents(True)

    def save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save screenshot as","","All Files (*);;Image Files (*jpg)",options = options)
        #### write binary file

        file = open(fileName,'wb')
        f = open ("shot.jpg",'rb')
        data = f.read()
        file.write(data)
        f.close()
        file.close()
