import socket

HEADER_LENGTH = 10
IP_address = "127.0.0.1"
Port = 1234

import chat_ui
import threading
import sys
import signal

from PyQt5 import QtWidgets


class Client:
    def __init__(self, ip, port):
        self.server = (ip, port)
        self.my_username = ''
        self.username_current = ''
        self.username_header = ''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.online = False

    def start(self, msg):
        self.my_username = msg
        self.client_socket.connect(self.server)
        self.username_current = self.my_username.encode('utf-8')
        self.username_header = \
            f"{len(self.username_current):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(self.username_header + self.username_current)
        self.online = True

    def send_msg(self, msg):

        # User send message to server
        message = msg

        if message.strip() == 'q':
            print('We will miss you')
            self.online = False

        else:
            # message:
            message = message.encode('utf-8')
            message_header = \
                f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(message_header + message)


class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = chat_ui.Ui_TCPchat()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send_msg)
        self.client = Client(IP_address, Port)
        self.receive_thread = None
        self.msg = ''

    def send_msg(self):
        self.msg = self.ui.lineEdit.text()

        if not self.client.online:
            self.client.nickname = self.msg
            self.client.start(self.msg)
            self.receive_thread = threading.Thread(target=self.receive_msg)
            self.receive_thread.start()

            self.ui.textEdit.append(f"Welcome to chat, {self.msg}!")
        else:
            # self.ui.textEdit.append(f"<You> {msg}")
            if self.msg == 'members':
                self.ui.textEdit.append(f"<You> {self.msg}")
            elif self.msg == "q":
                self.client.online = False
                self.closeEvent('dont know')
            elif self.msg.startswith('@'):
                self.ui.textEdit.append(f"<You> {self.msg}")
            self.client.send_msg(self.msg)

        self.ui.lineEdit.clear()

    def receive_msg(self):
        while self.client.online:
            self.client.username_header = self.client.client_socket.recv(
                HEADER_LENGTH)

            if not self.client.username_header:
                sys.exit()

            # Convert header to int value
            username_length = int(
                self.client.username_header.decode('utf-8').strip())
            # Receive and decode username
            username = self.client.client_socket.recv(username_length).decode(
                'utf-8')

            # Check whether message was send by another person
            message_header = self.client.client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = self.client.client_socket.recv(message_length).decode(
                'utf-8')
            if self.client.my_username != username:
                self.ui.textEdit.append(f'<{username}> {message}')
            elif self.client.my_username == username:
                if self.msg != 'members':
                    self.ui.textEdit.append(f"<You> {message}")
                elif self.msg == 'members':
                    self.ui.textEdit.append(f"    *{message}")

    def closeEvent(self, event):
        self.client.send_msg(r"Farewell...")
        self.client.online = False
        self.close()
        # signal.signal(signal.SIGTERM, True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())
