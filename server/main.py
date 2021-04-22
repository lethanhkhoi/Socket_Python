# This Python file uses the following encoding: utf-8
import sys
import os
import socket
import threading

from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class server(QWidget):
    def __init__(self):
        super(server, self).__init__()
        self.setWindowTitle("server")
        self.load_ui()
        self.set_Button()


    def set_Button(self):
        self.button = self.findChild(QPushButton,"server_Button")
        self.button.clicked.connect(create)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()


def create():
    PORT = 5656
    SERVER = ""
    ADDR = (SERVER,PORT)
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(1)
    conn, addr = server.accept()




if __name__ == "__main__":
    app = QApplication([])
    widget = server()
    widget.show()
    sys.exit(app.exec_())
