"""
@File    :   login.py
@start   :   2019/11/01 00:16:41
@Author  :   Jiang Xin
@Version :   1.0
@Contact :   gental_j@163.com
@License :   (C)Copyright 2018-2019, JiangXin
@Desc    :   Just for login CAERI device website and keep alive
"""
import requests
import re
import json
import time
from . import *
# from utils import *
import uuid
import os

# Request URL: https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid=ww80c0c4961a9e94c4&agentid=1000008&
# redirect_uri=http://deviceman.caeri.com.cn:6037/Index/login.html&state=IA07382995555793


QRCODE_SCAN_BACK = {
    1: 'QRCODE_SCAN_ERR',
    2: 'QRCODE_SCAN_NEVER',
    3: 'QRCODE_SCAN_ING',
    4: 'QRCODE_SCAN_SUCC',
}


class LoginInit:
    def __init__(self):

        self.session = requests.Session()

        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            'Connection': 'keep-alive',
        }

        self.urls = {
            "baseUrl": "https://open.work.weixin.qq.com/wwopen/sso/qrConnect"
        }

        self._appid = 'ww80c0c4961a9e94c4'
        self._agentid = '1000008'
        self._key = None

        self._redirect = 'http://deviceman.caeri.com.cn:6037/Index/login.html'
        self._rand_url = "http://deviceman.caeri.com.cn:6037/Index/get_rand.html"
        self.cookies = self.read_cookies()

    @staticmethod
    def read_cookies(arg=cookiesPath):
        try:
            with open(arg, 'r') as rb:
                content = json.load(rb)
                return content
        except FileNotFoundError as e:
            print('an error occur:{}'.format(e))

    def login_index(self, imgpath=qrcode_dir):

        response = self.session.get(url=self._redirect, headers=self.headers)

        if response.status_code != requests.codes.OK:
            print(f"获取登录页失败:{response.status_code}")
            return
        # update cookies
        self.cookies.update(response.cookies)

        # 获取随机生成码
        response = self.session.get(self._rand_url,
                                    headers=self.headers,
                                    cookies=self.cookies)
        self._state = response.text
        # self.cookies.update(response.cookies)

        # 从网站抓取二维码图片登录
        # <img class="qrcode lightBorder" src="//open.work.weixin.qq.com/wwopen/sso/qrImg?key=6abb43bb7ee10cdc">

        regx = r'<img class="qrcode lightBorder" src="(.*?)">'
        regx_key = '.*?key=(.*)'

        response = self.session.get(url=self.urls['baseUrl'],
                                    headers=self.headers,
                                    cookies=self.cookies,
                                    params={
                                        'appid': self._appid,
                                        'agentid': self._agentid,
                                        'redirect_uri': self._redirect,
                                        'state': self._state
                                    })
        imgUrl = 'http:' + re.search(regx, response.text).group(1)
        self._key = re.search(regx_key, imgUrl).group(1)
        # print(requests.dict_from_cookiejar(response.cookies))

        self.urls.update({'imgUrl': imgUrl})

        response = self.session.get(url=self.urls['imgUrl'],
                                    headers=self.headers,
                                    cookies=self.cookies)
        self.cookies.update(response.cookies)

        # 保存QR图片到本地
        uu_str = uuid.uuid4().hex
        img_name = '{}.jpg'.format(uu_str)
        img = os.path.join(imgpath, img_name)
        self._save(response.content, img)
        print(self.cookies)

        # response = self.session.get(
        #     url="http://deviceman.caeri.com.cn:6037/Index/device_list.html",
        #     headers=self.headers,
        #     cookies=self.cookies)
        # cont = response.text
        # self._save(cont, 'index.html')
        # print(requests.dict_from_cookiejar(response.cookies))
        return img_name

    def check_status(self, func=None):
        """
        check that you have correct login the website
        """

        # https://open.work.weixin.qq.com/wwopen/sso/l/qrConnect?callback=jsonpCallback&
        # key=954ec9860d9326b5&redirect_uri=http%3A%2F%2Fdeviceman.caeri.com.cn%3A6037%2FIndex%2Flogin.html&
        # appid=ww80c0c4961a9e94c4&_=1571997802388
        #
        # jsonpCallback({"status":"QRCODE_SCAN_SUCC","auth_code":"58BCceueQnUZL_nOw5IbQM6fYmpK3GIs8v-GQsWqC9E"})

        if func is None:
            func = print
        regx = r'"status":"(.*?)","auth_code":"(.*?)"'
        url = 'https://open.work.weixin.qq.com/wwopen/sso/l/qrConnect'
        auth_code = ''

        loctime = time.time() * 1000
        response = self.session.get(url=url,
                                    headers=self.headers,
                                    params={
                                        'callback': 'jsonpCallback',
                                        'key': self._key,
                                        'statusCode': 'QRCODE_SCAN_ING',
                                        'redirect_uri': self._redirect,
                                        'appid': self._appid,
                                        'agentid': self._agentid,
                                        '_': loctime
                                    })
        result = re.search(regx, response.text)

        if result.group(1) == 'QRCODE_SCAN_ERR':
            # have some unknown problems with scan the code
            # web back 'QRCODE_SCAN_ERR'
            func('请打开企业微信扫描二维码: {}'.format(result.group(1)))
            return 'QRCODE_SCAN_ERR'
        if result.group(1) == 'QRCODE_SCAN_NEVER':
            # haven't scan the code
            # web back 'QRCODE_SCAN_NEVER'
            func('请打开企业微信扫描二维码: {}'.format(result.group(1)))
            return 'QRCODE_SCAN_NEVER'
        if result.group(1) == 'QRCODE_SCAN_ING':
            # have scan, during the web deal with the information
            # web back 'QRCODE_SCAN_ING'
            func('扫码中请在企业微信确认登录: {}'.format(result.group(1)))
            return 'QRCODE_SCAN_ING'
        if result.group(1) == 'QRCODE_SCAN_SUCC':
            # check if the web have the correct response
            # web back 'QRCODE_SCAN_SUCC'
            func('扫码成功: {}'.format(result.group(1)))

            auth_code = result.group(2)

            response = self.session.get(url=self._redirect,
                                        headers=self.headers,
                                        params={
                                            'switch': 1,
                                            'code': auth_code,
                                            'state': self._state,
                                        })
            # response = r'{"error":0,"info":"\d{11}"}'
            regx = r'\d{11}'
            if response.status_code == 200:
                succ_back = re.search(regx, response.text)
                if succ_back:
                    # get the telephone number of user
                    try:
                        print(succ_back)
                        tel = succ_back.group()
                        self._save(tel, doc_dirpath + 'tel.txt')
                    except Exception as e:
                        print('电话号码保存失败%s', e)
                    func("登录成功")
                    # 保存cookies
                    self._save(self.cookies, cookiesPath)
                    print("save:{}".format(self.cookies))
                    return 'QRCODE_SCAN_SUCC'
                else:
                    func('登录失败！')
                    return 'failed'

    def get_user_and_tel(self):
        """
        从用户填写页面获取用户名和电话号码
        @return: 默认返回用户名和电话号码的字典，解析失败返回False
        """
        log_url = "http://deviceman.caeri.com.cn:6037/Index/log_list.html"
        response = self.session.get(url=log_url,
                                    headers=self.headers,
                                    cookies=self.cookies)
        print("log{}".format(self.cookies))
        if response.status_code == 200:
            content = response.text
            regx_phone = r'phone = "(\d{11})"'
            regx_username = r'real_name = "(.*?)"'
            try:
                phone = re.search(regx_phone, content).group(1)
                username = re.search(regx_username, content).group(1)
            except AttributeError as e:
                # 若解析失败，'NoneType' object has no attribute 'group'
                print('你还未登录,解析用户名失败:', e)
                return False
            print("用户保存成功，username:{} phone:{}".format(username, phone))
            return {"username": username, "phone": phone, "cookies": self.cookies}

    def _save(self, obj, filename):
        """
        for save the QRCode or Cookies
        """
        if filename.split('.')[-1] == 'json':
            with open(filename, 'w') as wf:
                json.dump(obj, wf)

        elif filename.split('.')[-1] == 'jpg':
            with open(filename, 'wb') as wf:
                wf.write(obj)
        else:
            with open(filename, 'w') as wf:
                wf.writelines(obj)


if __name__ == "__main__":
    from PIL import Image

    login = LoginInit()
    # name = login.login_index()
    # 测试二维码是否有效
    # qr = Image.open(qrcode_dir + '/' + name)
    # qr.show()

    start_time = time.time()
    print("start:{}".format(start_time))
    while time.time() - start_time < 10:
        # while 1:
        code_back = login.check_status()
        if code_back == QRCODE_SCAN_BACK[4]:
            print('ok')
        time.sleep(1)
    print("end:{}".format(time.time()))
    print('No')

    # login.get_user_and_tel()
