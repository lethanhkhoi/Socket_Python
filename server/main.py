# This Python file uses the following encoding: utf-8
import sys
import os
import socket
import threading
import time
import signal
import pyautogui
import wmi

from PySide2.QtWidgets import QApplication, QWidget, QPushButton,QMessageBox
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

BUFFER_SIZE = 4096

class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.server_ = None
        self.setWindowTitle("server")
        self.load_ui()
        self.set_Button()


    def set_Button(self):
        self.button = self.findChild(QPushButton,"server_Button")
        self.button.clicked.connect(self.create)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
    def create(self):
        if self.server_ == None:
            self.server_ = Server()
        elif self.server_ != None:
            self.server_ = None
            self.server = Server()


class Server:
    def __init__(self,signal=False):
        super(Server,self).__init__()
        self.server = None
        self.signal = signal
        self.PORT = 5656
        self.SERVER = ""
        self.ADDR = (self.SERVER,self.PORT)
        self.address= self.ADDR
        self.create()
        self.run()

    def create(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.server.listen(1)
        self.conn, self.addr = self.server.accept()
        self.signal = True

    def __str__(self):
        return self.address

    def run(self):
        with self.conn:
            while True:
                data = self.conn.recv(4096)
                if data.decode() == "shutdown":
                    self.shut_down()
                elif data.decode() == "printscreen":
                    self.conn.send(str.encode("printscreen"))
                    self.print_screen()
                elif data.decode() == "runprocess":
                    self.conn.send(str.encode("runprocess"))
                    self.run_process()
                if not data:
                    break

    def shut_down(self):
        os.system("shutdown /s /t 30")
    def run_process(self):
        f = wmi.WMI()
        for process in f.Win32_Process():
            s1 = f"{process.ProcessID:<10}"
            s2 = f"{process.Name:<20}"
            s3 = f"{process.ThreadCount:<10}"
            #self.conn.send(bytes(str(s1)))
            self.conn.send(str.encode(s1))
            self.conn.recv(1)

            #self.conn.send(bytes(str(s2)))
            self.conn.send(str.encode(s2))
            self.conn.recv(1)

            #self.conn.send(bytes(str(s3))
            self.conn.send(str.encode(s3))
            self.conn.recv(1)


            print(str(s1)+str(s2)+str(s3))
        self.conn.send(str.encode("end"))



    def print_screen(self):
        img = pyautogui.screenshot()
        img.save(r'shot.jpg')
        file = open("shot.jpg",'rb')
        size = os.stat('shot.jpg').st_size
        self.conn.send(str.encode(str(size)))

        while True:
            sendData = file.read(4096)
            if not sendData: #send toi khi khong con data de gui thi break
                break
            self.conn.send(sendData)

        file.close()
        os.remove("shot.jpg")

def kill(socket):


if __name__ == "__main__":
    app = QApplication([])
    widget = Form()
    widget.show()
    sys.exit(app.exec_())
