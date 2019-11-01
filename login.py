'''
@File    :   login.py
@start   :   2019/11/01 00:16:41
@Author  :   Jiang Xin 
@Version :   1.0
@Contact :   gental_j@163.com
@License :   (C)Copyright 2018-2019, JiangXin
@Desc    :   Just for login CAERI device website and keep alive
'''
import requests
import re
import os
import json
import time
from PIL import Image

# Request URL: https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid=ww80c0c4961a9e94c4&agentid=1000008&
# redirect_uri=http://deviceman.caeri.com.cn:6037/Index/login.html&state=IA07382995555793


class loginInit:
    def __init__(self, headers):

        self.session = requests.Session()

        self.headers = headers
        self.cookies = {
            "thinkphp_show_page_trace": "0|0",
        }

        self.urls = {
            "baseUrl": "https://open.work.weixin.qq.com/wwopen/sso/qrConnect"
        }

        self._appid = 'ww80c0c4961a9e94c4'
        self._agentid = '1000008'
        self._key = None

        self._redirect = 'http://deviceman.caeri.com.cn:6037/Index/login.html'
        self._rand_url = "http://deviceman.caeri.com.cn:6037/Index/get_rand.html"

    def login_index(self):

        response = self.session.get(url=self._redirect, headers=self.headers)

        if response.status_code != requests.codes.OK:
            print(f"获取登录页失败:{response.status_code}")
            return False
        # update cookies
        self.cookies.update(response.cookies)

        # 获取随机生成码
        response = self.session.get(self._rand_url,
                                    headers=headers,
                                    cookies=self.cookies)
        self._state = response.text
        # self.cookies.update(response.cookies)

        # 从网站抓取二维码图片登录
        '''
        返回base url 以及 验证是否登录的key值
        '''
        # <img class="qrcode lightBorder" src="//open.work.weixin.qq.com/wwopen/sso/qrImg?key=6abb43bb7ee10cdc">

        regx = r'<img class="qrcode lightBorder" src="(.*?)">'
        regx_key = '.*?key=(.*)'

        response = self.session.get(url=self.urls['baseUrl'],
                                    headers=headers,
                                    cookies=self.cookies,
                                    params={
                                        'appid': self._appid,
                                        'agentid': self._agentid,
                                        'redirect_uri': self._redirect,
                                        'state': self._state
                                    })
        imgUrl = 'http:' + re.search(regx, response.text).group(1)
        self._key = re.search(regx_key, imgUrl).group(1)
        # print(requests.utils.dict_from_cookiejar(response.cookies))

        self.urls.update({'imgUrl': imgUrl})
        # self.cookies.update(response.cookies)

        # QrIamgeurl = 'https://' + uri + k_value

        # 保存二维码并显示

        QRImgPath = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + 'QrImage.jpg'
        response = self.session.get(url=self.urls['imgUrl'],
                                    headers=self.headers,
                                    cookies=self.cookies)
        self.cookies.update(response.cookies)

        self._save(response.content, QRImgPath)

        qr = Image.open(QRImgPath)
        qr.show()
        # time.sleep(10)
        self.check_status(self._key)

        response = self.session.get(
            url="http://deviceman.caeri.com.cn:6037/Index/device_list.html",
            headers=self.headers,
            cookies=self.cookies)
        cont = response.text
        # with open('index.html', 'w') as wf:
        #     wf.writelines(cont)
        # print(requests.utils.dict_from_cookiejar(response.cookies))
        # print(cont)

    def check_status(self, key):

        # https://open.work.weixin.qq.com/wwopen/sso/l/qrConnect?callback=jsonpCallback&
        # key=954ec9860d9326b5&redirect_uri=http%3A%2F%2Fdeviceman.caeri.com.cn%3A6037%2FIndex%2Flogin.html&
        # appid=ww80c0c4961a9e94c4&_=1571997802388
        #
        # jsonpCallback({"status":"QRCODE_SCAN_SUCC","auth_code":"58BCceueQnUZL_nOw5IbQM6fYmpK3GIs8v-GQsWqC9E"})
        regx = r'"status":"(.*?)","auth_code":"(.*?)"'
        url = 'https://open.work.weixin.qq.com/wwopen/sso/l/qrConnect'
        auth_code = ''

        loctime = time.time() * 1000
        response = self.session.get(url=url,
                                    headers=self.headers,
                                    params={
                                        'callback': 'jsonpCallback',
                                        'key': key,
                                        'statusCode': 'QRCODE_SCAN_ING',
                                        'redirect_uri': self._redirect,
                                        'appid': self._appid,
                                        'agentid': self._agentid,
                                        '_': loctime
                                    })
        result = re.search(regx, response.text)

        if result.group(1) == 'QRCODE_SCAN_NEVER':
            print('请打开企业微信扫描二维码: {}'.format(result.group(1)))
            self.check_status(self.urls['key'])

        if result.group(1) == 'QRCODE_SCAN_ING':
            print('扫码中请等待: {}'.format(result.group(1)))
            time.sleep(1)
            self.check_status(self.urls['key'])

        if result.group(1) == 'QRCODE_SCAN_SUCC':
            print('扫码成功: {}'.format(result.group(1)))

            auth_code = result.group(2)

            response = self.session.get(url=self._redirect,
                                        headers=self.headers,
                                        params={
                                            'switch': 1,
                                            'code': auth_code,
                                            'state': self._state,
                                        })
            regx = r'{"error":0,"info":"\d{11}"}'
            if response.status_code == 200:
                if re.search(regx, response.text):
                    print("登录成功")
                    self._save(self.cookies, 'cookies.json')
                else:
                    print('登录失败！')

    def _save(self, obj, filename):

        if obj.split('.')[-1] == 'json':
            with open(filename, 'w') as wf:
                json.dump(obj, filename)

        else:
            with open(filename, 'w') as wf:
                wf.writelines(obj)


if __name__ == "__main__":

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        'Connection': 'keep-alive',
    }

    # 二维码本地保存地址

    login = loginInit(headers)
    login.login_index()
    # c2 = login.coo()
    # c1 = login.getCookies()
    # time.sleep(10)
    # c2 = login.getcontent(
    #     url="http://deviceman.caeri.com.cn:6037/Index/device_list.html")

    # with open('index.html', 'w') as wf:

# for sec in range(15):
#     time.sleep(1)
#     print(sec)

# if login.check_status(ImgKey):
#     login.getCookies()
