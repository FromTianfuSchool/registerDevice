# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\admin\Desktop\programPi\Qt\showQRcode.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import pictures_rc
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_showQRcode(object):
    def setupUi(self, showQRcode):
        showQRcode.setObjectName("showQRcode")
        showQRcode.setEnabled(True)
        showQRcode.resize(320, 320)
        showQRcode.setMinimumSize(QtCore.QSize(320, 320))
        showQRcode.setMaximumSize(QtCore.QSize(320, 320))
        palette = QtGui.QPalette()
        showQRcode.setPalette(palette)
        showQRcode.setAutoFillBackground(False)
        showQRcode.setStyleSheet("#showQRcode { \n"
                                 "    border-image: url(:/background_1.jpg);\n"
                                 "    border-image: url(:/background_1.jpg); \n"
                                 "} \n"
                                 "#showQRcode * { \n"
                                 "border-image:url(); \n"
                                 "}")
        # showQRcode.setSizeGripEnabled(False)
        self.quitButton = QtWidgets.QPushButton(showQRcode)
        self.quitButton.setEnabled(True)
        self.quitButton.setGeometry(QtCore.QRect(230, 290, 75, 23))
        palette = QtGui.QPalette()
        self.quitButton.setPalette(palette)
        self.quitButton.setAutoDefault(True)
        self.quitButton.setObjectName("quitButton")
        self.label = QtWidgets.QLabel(showQRcode)
        self.label.setGeometry(QtCore.QRect(90, 10, 131, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("background: transparent;")
        self.label.setObjectName("label")

        self.retranslateUi(showQRcode)
        self.quitButton.clicked.connect(showQRcode.close)
        QtCore.QMetaObject.connectSlotsByName(showQRcode)

    def retranslateUi(self, showQRcode):
        _translate = QtCore.QCoreApplication.translate
        showQRcode.setWindowTitle(_translate("showQRcode", "Dialog"))
        self.quitButton.setText(_translate("showQRcode", "Quit"))
        self.label.setText(_translate(
            "showQRcode", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">扫码登录</span></p></body></html>"))
