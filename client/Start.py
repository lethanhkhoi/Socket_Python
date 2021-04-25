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

def start_process(socket):
    socket.send(str.encode("startapp"))

class start(QWidget):
    def __init__(self,Client):
        super(start,self).__init__()
        self.client_ = Client
        self.setWindowTitle("Start")
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"start.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()

        self.sbutton = self.findChild(QPushButton,"Start_Button")

        self.sbutton.clicked.connect(self.start_app)
    def start_app(self):
        while True:
            start_process(self.client_)
            self.client_.recv(4096)
            self.app_name = self.findChild(QLineEdit,"Name").text()
            self.client_.send(str.encode(self.app_name))
            data = self.client_.recv(2)
            if data.decode()=="ok":
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Khởi động thành công")
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

