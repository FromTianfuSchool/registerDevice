"""
@File    :   uploadInfo.py
@start   :   2019/09/28 18:00:24
@Author  :   Jiang Xin
@Version :   1.0
@Contact :   gental_j@163.com
@License :   (C)Copyright 2018-2019, JiangXin
@Desc    :   upload used device's information
"""
import requests
import json
import re


# 扫码登陆随机数生成地址
# url1 = "http://deviceman.caeri.com.cn:6037/Index/get_rand.html"
# cookies = {
#     "thinkphp_show_page_trace": "0|0",
#     "PHPSESSID": "4bknp8svurumnlcoc1bao4t006"
# }

class Upload:
    def __init__(self, cookies=None):
        self._headers = {
                     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/75.0.3770.142 Safari/537.36"
                    }
        self._url = "http://deviceman.caeri.com.cn:6037/Index/add_log.html"
        self.device_url = "http://deviceman.caeri.com.cn:6037/Index/device_list.html"
        self._cookies = cookies

    def read_cookies(self, arg):
        try:
            with open(arg, 'r') as rb:
                content = json.load(rb)
                return content
        except FileNotFoundError as e:
            print('an error occur:{}'.format(e))

    def login_is_ok(self):

        regx = r'<title>(.*?)</title>'
        response = requests.get(url=self.device_url,
                                headers=self._headers,
                                cookies=self._cookies,
                                timeout=1)
        try:
            title = re.search(regx, response.text).group(1)
        except Exception as e:
            print('an error occur:{}'.format(e))
            return False
        if title == '设备信息':
            return True
        else:
            print("请求页面错误")
            return False

    def upload(self, data):
        """
        @param data: data of device information to register web
        """
        print('uploading!')
        r = requests.post(url=self._url,
                          headers=self._headers,
                          cookies=self._cookies,
                          data=data)
        if r.status_code == 200 or r.status_code == '200':
            print('upload successful!')
            return True


if __name__ == '__main__':
    upload = Upload()
    upload.login_is_ok()
