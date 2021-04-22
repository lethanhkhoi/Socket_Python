# This Python file uses the following encoding: utf-8
import sys
import os
import socket
import threading


from PySide2.QtWidgets import QApplication, QWidget,QPushButton,QMessageBox, QLineEdit, QTableWidget
from PySide2.QtWidgets import QListWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine


class client(QWidget):
    def __init__(self):
        super(client, self).__init__()
        self.setWindowTitle("client")
        self.load_ui()
        self.set_icon()
        self.set_Button()
        self.create()


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

        self.cbutton.clicked.connect(self.check)
        self.ebutton.clicked.connect(self.exit_)
        self.abutton.clicked.connect(self.app_r)
        self.pbutton.clicked.connect(self.process_r)
        self.kbutton.clicked.connect(self.keystroke_r)
        self.rbutton.clicked.connect(self.reg)

    def reg(self):
        self.regis = Registry()
        self.regis.show()

    def keystroke_r(self):
        self.key = Keystroke()
        self.key.show()

    def process_r(self):
        self.list_app = List_App()
        self.list_app.show()

    def app_r(self):
        self.list_app = List_App()
        self.list_app.show()

    def exit_(self):
        exit()

    def check(self):
        self.ipline = self.findChild(QLineEdit,"lineEdit").text()
        try:
            create(self.ipline)
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
    def __init__(self):
        super(kill, self).__init__()
        self.setWindowTitle("Kill")
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "kill.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()

class start(QWidget):
    def __init__(self):
        super(start,self).__init__()
        self.setWindowTitle("Start")
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"start.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()

class List_App(QWidget):
    def __init__(self):
        super(List_App,self).__init__()
        self.setWindowTitle("List App")
        self .load_ui()
        self.list = self.findChild(QTableWidget,"list_app")
        self.list.setColumnWidth(0,130)

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


        #hàm liên kết action khi kết nối được với server
        self.kbutton.clicked.connect(self.kill_app)
        self.sbutton.clicked.connect(self.start_app)
        self.vbutton.clicked.connect(self.view_app)
        self.dbutton.clicked.connect(self.delete_app)

    def delete_app(self):
        self.list = self.findChild(QTableWidget,"list_app")
        self.list.clearContents()

    def view_app(self):
        self.list = self.findChild(QTableWidget,"listapp")
        row = 0


    def kill_app(self):
        self.kill_ = kill()
        self.kill_.show()

    def start_app(self):
        self.start_ = start()
        self.start_.show()

class Keystroke(QWidget):
    def __init__(self):
        super(Keystroke,self).__init__()
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
    def __init__(self):
        super(Registry,self).__init__()
        self.setWindowTitle("registry")
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"reg.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file,self)
        ui_file.close()


def create(ipline: str):
    PORT = 5656
    FORMAT = 'utf-8'
    SERVER = ipline
    ADDR = (SERVER,PORT)

    Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    Client.connect(ADDR)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = client()
    widget.show()


    sys.exit(app.exec_())
