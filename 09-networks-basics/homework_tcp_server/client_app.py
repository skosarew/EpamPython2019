import socket

HEADER_LENGTH = 10
IP_address = "127.0.0.1"
Port = 1234

import chat_ui
import threading
import sys

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
        self.sockets_list = [sys.stdin, self.client_socket]

    def send_msg(self, msg):

        # User send message to server
        message = msg

        if message.strip() == 'q':
            print('We will miss you')
            self.online = False

        elif message:
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

    def send_msg(self):
        msg = self.ui.lineEdit.text()

        if not self.client.online:
            self.client.nickname = msg
            self.client.start(msg)
            receive_thread = threading.Thread(target=self.receive_msg)
            receive_thread.start()
            self.ui.textEdit.append(f"Welcome to chat, {msg}!")
        else:
            self.ui.textEdit.append(f"<You> {msg}")
            self.client.send_msg(msg)
            if msg == "q":
                self.closeEvent('dont know')
        self.ui.lineEdit.clear()

    def receive_msg(self):
        while self.client.online:
            username_header = self.client.client_socket.recv(HEADER_LENGTH)
            if not len(self.client.username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())
            # Receive and decode username
            username = self.client.client_socket.recv(username_length).decode(
                'utf-8')

            message_header = self.client.client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = self.client.client_socket.recv(message_length).decode(
                'utf-8')
            self.ui.textEdit.append(f'<{username}> {message}')

    def closeEvent(self, event):
        self.client.send_msg(r"Farewell...")
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())
