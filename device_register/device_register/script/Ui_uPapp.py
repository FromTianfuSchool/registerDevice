# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\admin\Desktop\programPi\Qt\uPapp.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CAERIdevices(object):
    def setupUi(self, CAERIdevices):
        CAERIdevices.setObjectName("CAERIdevices")
        CAERIdevices.resize(421, 363)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        CAERIdevices.setFont(font)
        CAERIdevices.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        CAERIdevices.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(CAERIdevices)
        self.centralwidget.setObjectName("centralwidget")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(120, 10, 161, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.login.setFont(font)
        self.login.setMouseTracking(True)
        self.login.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.login.setAutoFillBackground(False)
        self.login.setAutoDefault(False)
        self.login.setObjectName("login")
        self.messages = QtWidgets.QTextBrowser(self.centralwidget)
        self.messages.setGeometry(QtCore.QRect(0, 170, 421, 141))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.messages.setFont(font)
        self.messages.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.messages.setObjectName("messages")
        self.upload = QtWidgets.QPushButton(self.centralwidget)
        self.upload.setGeometry(QtCore.QRect(120, 70, 161, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.upload.setFont(font)
        self.upload.setObjectName("upload")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 310, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        CAERIdevices.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CAERIdevices)
        self.statusbar.setObjectName("statusbar")
        CAERIdevices.setStatusBar(self.statusbar)

        self.retranslateUi(CAERIdevices)
        QtCore.QMetaObject.connectSlotsByName(CAERIdevices)

    def retranslateUi(self, CAERIdevices):
        _translate = QtCore.QCoreApplication.translate
        CAERIdevices.setWindowTitle(_translate("CAERIdevices", "MainWindow"))
        self.login.setText(_translate("CAERIdevices", "登录"))
        self.upload.setText(_translate("CAERIdevices", "上传数据"))
        self.label.setText(_translate("CAERIdevices", "Designed by GentalJ"))
