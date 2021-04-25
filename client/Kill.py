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

import main

class kill(QWidget):
    def __init__(self,Client):
        super(kill, self).__init__()
        self.client_ = Client
        self.setWindowTitle("Kill")
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "kill.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()

        self.killbutton = self.findChild(QPushButton,"Kill_Button")

        self.killbutton.clicked.connect(self.killapp)

    def killapp(self):
        while True:
            kill_process(self.client_)
            self.client_.recv(4096)
            self.p_id = self.findChild(QLineEdit,"pID").text()
            self.client_.send(str.encode(self.p_id))
            data = self.client_.recv(2)
            if data.decode()=="ok":
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Diệt thành công")
                x = msg.exec_()
                break
            elif data.decode() == "er":
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Lỗi")
                msg.setIcon(QMessageBox.Critical)
                x = msg.exec_()
                break
            if not data:
                break

def kill_process(socket):
    socket.send(str.encode("killid"))
