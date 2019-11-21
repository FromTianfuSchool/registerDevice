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
import json
import time
import utils

# Request URL: https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid=ww80c0c4961a9e94c4&agentid=1000008&
# redirect_uri=http://deviceman.caeri.com.cn:6037/Index/login.html&state=IA07382995555793


class loginInit():
    def __init__(self, headers):

        # self.projpath = projPath()
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

        # curdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        # self.doc_dirpath = os.path.abspath(os.path.join(curdir, 'docs'))
        # self.QRImgPath = os.path.join(self.doc_dirpath, 'QrImge.jpg')
        # self.cookiesPath = os.path.join(self.doc_dirpath, 'cookies.json')

    def login_index(self):

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
        # print(requests.utils.dict_from_cookiejar(response.cookies))

        self.urls.update({'imgUrl': imgUrl})

        response = self.session.get(url=self.urls['imgUrl'],
                                    headers=self.headers,
                                    cookies=self.cookies)
        self.cookies.update(response.cookies)

        self._save(response.content, utils.QRImgPath)

        # response = self.session.get(
        #     url="http://deviceman.caeri.com.cn:6037/Index/device_list.html",
        #     headers=self.headers,
        #     cookies=self.cookies)
        # cont = response.text
        # self._save(cont, 'index.html')
        # print(requests.utils.dict_from_cookiejar(response.cookies))

    def check_status(self, func=None):

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
            func('请打开企业微信扫描二维码: {}'.format(result.group(1)))
            # response_code = 'ERR'
            return
        if result.group(1) == 'QRCODE_SCAN_NEVER':
            func('请打开企业微信扫描二维码: {}'.format(result.group(1)))
            return

        if result.group(1) == 'QRCODE_SCAN_ING':
            func('扫码中请在企业微信确认登录: {}'.format(result.group(1)))
            return

        if result.group(1) == 'QRCODE_SCAN_SUCC':
            func('扫码成功: {}'.format(result.group(1)))

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
                    func("登录成功")
                    self._save(self.cookies, utils.cookiesPath)
                    return True
                else:
                    func('登录失败！')
                    return

    def _save(self, obj, filename):

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
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        'Connection': 'keep-alive',
    }

    login = loginInit(headers)
    login.login_index()
    # 测试二维码是否有效
    qr = Image.open(utils.QRImgPath)
    qr.show()
    # login.check_status()
