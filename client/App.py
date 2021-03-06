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

import Kill
import Start

def app_(socket):
    socket.send(str.encode("runapp"))

class Application(QWidget):
    def __init__(self,Client):
        super(Application,self).__init__()
        self.client_ = Client
        self.setWindowTitle("Application")
        self.name = []
        self.id = []
        self.count = []
        self.row = 0
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"listapp.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()


        self.kbutton = self.findChild(QPushButton,"kill_Button")
        self.sbutton = self.findChild(QPushButton,"start_Button")
        self.dbutton = self.findChild(QPushButton,"delete_Button")
        self.vbutton = self.findChild(QPushButton,"view_Button")
        self.list = self.findChild(QTableWidget,"list")
        self.list.setColumnWidth(0,150)
        self.list.setColumnWidth(1,150)
        self.list.setColumnWidth(2,150)

        self.kbutton.clicked.connect(self.kill_app)
        self.sbutton.clicked.connect(self.start_app)
        self.dbutton.clicked.connect(self.delete_app)
        self.vbutton.clicked.connect(self.view_start)
    def view_start(self):
        app_(self.client_)
        self.client_.recv(4096)
        self.view_app()

    def view_app(self):
        if self.row != 0:
            self.name =[]
            self.id = []
            self.count = []
            self.row =0
        print("Printing")

        # Iterating through all the running processes
        data = self.client_.recv(2048)
        while True:
         #   s1 = f"{process.ProcessID:<10}"
          #  s2 = f"{process.Name:<20}"
           # s3 = f"{process.ThreadCount:<10}"
           if(data.decode()=="end"):
               break
           self.client_.send(bytes('1','utf-8'))
           s1 = data.decode()
           self.id.append(str(s1))

           data = self.client_.recv(2048)
           self.client_.send(bytes('1','utf-8'))
           s2 = data.decode()
           self.name.append(str(s2))

           data = self.client_.recv(2048)
           self.client_.send(bytes('1','utf-8'))
           s3 = data.decode()
           self.count.append(str(s3))
           print(str(s1) + str(s2) + str(s3))
           self.row +=1
           data = self.client_.recv(2048)
            # Displaying the P_ID and P_Name of the process

        #save data to string[] and input to table widget
        self.list.setRowCount(self.row)
        for i in range(len(self.name)):
            self.list.setItem(i,0,QTableWidgetItem(self.name[i]))
            self.list.setItem(i,1,QTableWidgetItem(self.id[i]))
            self.list.setItem(i,2,QTableWidgetItem(self.count[i]))


    def kill_app(self):
        self.kill_ = Kill.kill(self.client_)
        self.kill_.show()

    def start_app(self):
        self.start_ = Start.start(self.client_)
        self.start_.show()
    def delete_app(self):
        row = self.row -1
        for i in range(len(self.name)):
            self.list.removeRow(row-i)

        self.name =[]
        self.id = []
        self.count = []
        self.row =0

