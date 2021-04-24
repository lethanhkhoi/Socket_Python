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
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
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
            self.picture = Pic(self.client_)
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
            self.list_app = Process(self.client_)
            self.list_app.show()

    def app_r(self):
        if self.client_ == None:
            self.message()
        elif  self.client_ != None:
            self.list_app = Process(self.client_)
            self.list_app.show()

    def exit_(self):
        exit()

    def check(self,client_):
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
        self.killbutton.clicked.connect(self.check)
    def check(self):
        exit()

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

class Process(QWidget):
    def __init__(self,Client):
        super(Process,self).__init__()
        self.client_ = Client
        self.setWindowTitle("Process Running")
        self .load_ui()
        self.name = []
        self.id = []
        self.count = []

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"listapp.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()
        self.list = self.findChild(QTableWidget,"tableWidget")
        self.list.setColumnWidth(0,150)
        self.list.setColumnWidth(1,150)
        self.list.setColumnWidth(0,150)

        self.kbutton = self.findChild(QPushButton,"kill_Button")
        self.sbutton = self.findChild(QPushButton,"start_Button")
        self.dbutton = self.findChild(QPushButton,"delete_Button")
        self.vbutton = self.findChild(QPushButton,"view_Button")


        #hàm liên kết action khi kết nối được với server
        self.kbutton.clicked.connect(self.kill_app)
        self.sbutton.clicked.connect(self.start_app)
        self.vbutton.clicked.connect(self.view_start)
        self.dbutton.clicked.connect(self.delete_app)

    def delete_app(self):
        self.list.clearContents()

    def view_start(self):
        process_(self.client_)
        self.receive_process()
        self.view_app()
    def view_app(self):
        self.row = 0

        #f = wmi.WMI()
        # Printing the header for the later columns
        print("Printing")
        # Iterating through all the running processes
        data = self.client_.recv(2048)
        while True:
        #for process in f.Win32_Process():
         #   s1 = f"{process.ProcessID:<10}"
          #  s2 = f"{process.Name:<20}"
           # s3 = f"{process.ThreadCount:<10}"
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
           if(data.decode()=="end"):
               break
        self.list.setRowCount(self.row)
        for i in range(len(self.name)):
            self.list.setItem(i,0,QTableWidgetItem(self.name[i]))
            self.list.setItem(i,1,QTableWidgetItem(self.id[i]))
            self.list.setItem(i,2,QTableWidgetItem(self.count[i]))
            #print(self.id[i] + self.nam[i] + self.count[i])




    def kill_app(self):
        self.kill_ = kill(self.client_)
        self.kill_.show()

    def start_app(self):
        self.start_ = start()
        self.start_.show()

    def receive_process(self):
        while True:
            try:
                command = self.client_.recv(4096)
                if (command.decode() == "runprocess"):
                    return
            except:
                break


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
class Pic(QWidget):
    def __init__(self,Client):
        super(Pic,self).__init__()
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

#function client
def create(ipline: str):
    PORT = 5656
    FORMAT = 'utf-8'
    SERVER = ipline
    ADDR = (SERVER,PORT)

    Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Client.connect(ADDR)
    return Client
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


def process_(socket):
    socket.send(str.encode("runprocess"))

def print_screen(socket):
    socket.send(str.encode("printscreen"))

def shut_down(socket):
    socket.send(str.encode("shutdown"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Form()
    widget.show()


    sys.exit(app.exec_())
