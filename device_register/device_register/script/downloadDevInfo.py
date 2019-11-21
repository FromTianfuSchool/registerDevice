'''
@File    :   registerEquipment.py
@start   :   2019/09/28 17:22:11
@Author  :   Jiang Xin 
@Version :   1.0
@Contact :   gental_j@163.com
@License :   (C)Copyright 2018-2019, JiangXin
@Desc    :   download Engine Emission Department's device information
'''
import requests
import json
import time
# from urllib.parse import urlencode

url = "http://deviceman.caeri.com.cn:6037/Index/device_list.html"
cookies = {
    "thinkphp_show_page_trace": "0|0",
    "PHPSESSID": "ps5m47s4j0phdb9esqcmqs8io4"
}
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
}


def loadDep():
    """
    download department's name
    @return: file name dep.json
    """

    formdata = {"switch": "3"}
    r = requests.post(url=url, headers=headers, cookies=cookies, data=formdata)
    # r.encoding = 'askii'
    print(r.encoding)
    print('-' * 100)
    print(r.json())
    with open('department.json', 'w') as wb:
        json.dump(r.json(), wb, ensure_ascii=False)


# downloadParm()
def loadDevice():
    '''
    download device's name
    @return: file name dev.json
    '''
    formdata = {"switch": "1", "page": "", "dep": "发动机排放检测部"}
    for i in range(1, 6):
        formdata["page"] = formdata["page"] + str(i)

        r = requests.post(url=url,
                          headers=headers,
                          cookies=cookies,
                          data=formdata)
        print(formdata["page"])
        print(r.json())
        time.sleep(0.5)
        with open('dev.json', 'a') as wb:
            json.dump(r.json(), wb, ensure_ascii=False)
        formdata["page"] = ""


# loadDevice()


def loadNum():
    '''
    download device's number
    @return: file name num.json
    '''
    formdata = {"switch": "2", "page": "", "dep": "发动机排放检测部"}
    for i in range(1, 8):
        formdata["page"] = formdata["page"] + str(i)

        r = requests.post(url=url,
                          headers=headers,
                          cookies=cookies,
                          data=formdata)
        print(formdata["page"])
        print(r.json())
        time.sleep(0.5)
        with open('num.json', 'a') as wb:
            json.dump(r.json(), wb, ensure_ascii=False)
        formdata["page"] = ""


# loadNum()
def loadCoInfo():
    '''
    Engine Emission Department's device information
    @return: file name coinfo.json
    '''
    url = "http://deviceman.caeri.com.cn:6037/Index/get_device.html"
    formdata = {"switch": "2", "num": "", "dep": "发动机排放检测部"}
    with open('num.json', 'r') as rb:
        tmp = json.load(rb)
        for _ in tmp:
            # print(_)
            formdata["num"] = _["0"]
            # print(formdata)
            r = requests.post(url=url,
                              headers=headers,
                              cookies=cookies,
                              data=formdata)
            # print(r.text)
            # print(r.json())
            with open('coInfo.json', 'a', encoding='utf-8') as wb:
                json.dump(r.json(), wb, ensure_ascii=False)
            time.sleep(0.5)
            formdata["name"] = ""
    print('download finished ！！！')


# loadCoInfo()

# 下载的数据编码不能正常被json解析，导致写入文件报错
# 改用如下创建文件时格式化文件编码即可解决！
# json写入文件默认为ascii编码，需使用'ensure_ascii=False'禁用，否则文件不能正常显示中文
# with open('coInfo.json', 'r') as wb:
#     t = json.load(wb)
#     with open('coInfo1.txt', 'w', encoding='utf-8') as rb:
#         json.dump(t, rb, ensure_ascii=False)