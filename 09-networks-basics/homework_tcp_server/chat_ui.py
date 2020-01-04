# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_TCPchat(object):
    def setupUi(self, TCPchat):
        TCPchat.setObjectName("TCPchat")
        TCPchat.resize(350, 500)
        self.centralwidget = QtWidgets.QWidget(TCPchat)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        TCPchat.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TCPchat)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 535, 26))
        self.menubar.setObjectName("menubar")
        TCPchat.setMenuBar(self.menubar)


        self.retranslateUi(TCPchat)
        QtCore.QMetaObject.connectSlotsByName(TCPchat)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("TCPchat", "TCPchat"))
        self.pushButton.setText(_translate("TCPchat", "Enter message"))

