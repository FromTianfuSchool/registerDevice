'''
@File    :   main.py
@start   :   2019/11/21 19:31:23
@Author  :   Jiang Xin 
@Version :   1.0
@Contact :   gental_j@163.com
@License :   (C)Copyright 2018-2019, JiangXin
@Desc    :   UI interface for user
'''
import sys
import time
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
# from uPapp import Ui_CAERIdevices
from Ui_uPapp import Ui_CAERIdevices
from Ui_showQRcode import Ui_showQRcode
# from Qt.Ui_uPapp import Ui_CAERIdevices
# from Qt.Ui_showQRcode import Ui_showQRcode
from PIL import Image
from threading import Thread
import utils
# from PyQt5 import uic

# qtCreatorFile = "tax_calc.ui" # Enter file here.
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class window(QtWidgets.QMainWindow, Ui_CAERIdevices):
    def __init__(self, arg):
        super(window, self).__init__()
        self.setupUi(self)
        self.childwindow = arg
        self.childwindow_open = False
        self.threads = []
        self.upload.clicked.connect(self.upload_func)
        self.login.clicked.connect(self.open_childwindow)
        self.login.clicked.connect(self.childwindow.show)

    def open_childwindow(self):
        if self.childwindow_open is False:
            self.messages.append('请使用企业微信扫描二维码')
            self.childwindow.qrCode()

            self.t1 = Lthread(function=self.confirm)
            self.threads.append(self.t1)
            self.t1.setDaemon(True)
            self.t1.start()
            self.childwindow_open = True
            self.threads.append(self.t1)

    def close_childwindow(self):
        if self.childwindow_open:
            self.childwindow.close()
            self.childwindow_open = False
            self.t1._terminate()
            # self.t1.join()

    def confirm(self):

        def get_print(arg):
            self.messages.append(arg)

        self.childwindow.confirm(get_print)

    def upload_func(self):
        self.close_childwindow()

        from uploadInfo import Upload
        self.upload = Upload()
        # self.t2 = Thread(target=self.display)
        # self.threads.append(self.t2)
        # self.t2.setDaemon(True)
        # self.t2.start()
        if self.upload.login_is_ok():
            self.messages.append('上传数据中')
            self.upload.upload(print_fuc=self.messages.append)
        else:
            self.messages.append('你还没有登录，请扫码登录后再上传数据！')


class showQrcode(QtWidgets.QMainWindow, Ui_showQRcode):
    def __init__(self):
        super(showQrcode, self).__init__()
        self.setupUi(self)
        from login import loginInit
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            'Connection': 'keep-alive',
        }
        self.scan = loginInit(headers=headers)

    def qrCode(self):
        self.scan.login_index()

        # im = Image.open('QrImage.jpg')
        img = utils.QRImgPath
        im = Image.open(img)
        im.save(img)
        # 二维码实际为png格式，QPixmap不能打开
        pix = QtGui.QPixmap(img)

        lb1 = QtWidgets.QLabel(self)
        lb1.setGeometry(60, 50, 200, 200)
        lb1.setStyleSheet("border: 2px solid grey")
        lb1.setPixmap(pix)
        lb1.setScaledContents(True)

    def confirm(self, func=None):

        self.scan.check_status(func)


class Lthread(Thread):
    def __init__(self, function):
        Thread.__init__(self)
        self._del = False
        self._func = function

    def _terminate(self):
        self._del = True

    def run(self):
        while True:
            if self._del:
                print(self.getName() + ': end')
                break
            print(self.getName())
            self._func()
            time.sleep(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = window(showQrcode())
    ui.show()
    sys.exit(app.exec_())
    # # def add():
    # #     return 1+1
    # # t = Lthread(function=add)
    # # t.start()
    # # time.sleep(2)
    # # t._terminate()
