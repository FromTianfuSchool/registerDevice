import requests
import re
import os
import tkinter as tk
from PIL import Image, ImageTk
from time import sleep

# Request URL: https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid=ww80c0c4961a9e94c4&agentid=1000008&
# redirect_uri=http://deviceman.caeri.com.cn:6037/Index/login.html&state=IA07382995555793

session = requests.Session()


def getQRImageUrl():
    '''
    从网站抓取二维码图片地址
    '''

    param = {
        'appid': 'ww80c0c4961a9e94c4',
        'agentid': '1000008',
        'redirect_uri': 'http://deviceman.caeri.com.cn:6037/Index/login.html',
        'state': get_state()
    }
    # <img class="qrcode lightBorder" src="//open.work.weixin.qq.com/wwopen/sso/qrImg?key=6abb43bb7ee10cdc">
    regx = r'<img class="qrcode lightBorder" src="//(.*?)">'

    request_url = 'https://open.work.weixin.qq.com/wwopen/sso/qrConnect?'

    for name, value in param.items():
        request_url = request_url + name + '=' + value + '&'

    request_url = request_url[:-1]

    r = session.get(request_url)

    QRImage_url = re.search(regx, r.text)

    return QRImage_url.group(1)


def get_state():
    '''
    获取随机生成码
    '''
    url = "http://deviceman.caeri.com.cn:6037/Index/get_rand.html"

    r = session.get(url)
    state = r.text

    return state


def showQRImage():
    '''
    弹出二维码图片，扫描登录
    '''

    QRImgPath = os.path.split(os.path.realpath(__file__))[
        0] + os.sep + 'QrImage.jpg'

    url = 'https://' + getQRImageUrl()

    r = session.get(url)

    with open(QRImgPath, 'wb') as f:
        f.write(r.content)
        f.close()

    # qr = Image.open(QRImgPath)
    # qr.show()

    print('请使用企业微信扫描二维码以登录')


def getCookies():
    url = 'http://deviceman.caeri.com.cn:6037/Index/login.html'

    r = session.get(url)
    cookiejar = r.cookies

    cookies = requests.utils.dict_from_cookiejar(cookiejar)
    print(cookies)


class Window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=400, height=300)
        self.pack()
        self.pilImage = Image.open("QrImage.jpg")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.label = tk.Label(self, image=self.tkImage)
        self.label.pack()

    # def processEvent(self, event):
    #     pass


# showQRImage()
# root = tk.Tk()
# app = Window(root)
# root.mainloop()

# sleep(3)
getCookies()
