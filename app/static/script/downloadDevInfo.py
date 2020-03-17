"""
@File    :   downloadDevInfo.py
@start   :   2019/09/28 17:22:11
@Author  :   Giraffe
@Version :   1.1
@Contact :   gental_j@163.com
@Desc    :   download Engine Emission Department's device information
"""
import requests
import json
import time
import os
from app.static.script import doc_dirpath, temp_dirpath, cookiesPath

DEV_LIST_URL = "http://deviceman.caeri.com.cn:6037/Index/device_list.html"

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
}


def load_json(path, encoding=None, **kw):
    # load device information from /docs
    # 必须先将json文件编码，不然解析会报错
    with open(path, 'r', encoding=encoding) as rb:
        # data is a list which consists of many dicts
        # to get data as this: print(data[1]['DeviceNO'])
        data = json.load(rb, **kw)
    return data


cookies = load_json(cookiesPath, encoding='utf-8')


def load_dep():
    """
    download department's name
    @return: file name dep.json
    """

    data = {"switch": "3"}
    r = requests.post(url=DEV_LIST_URL, headers=HEADERS, cookies=cookies, data=data)
    # r.encoding = 'askii'
    print(r.encoding)
    print('-' * 100)
    print(r.json())
    with open(doc_dirpath + 'department.json', 'w') as wb:
        json.dump(r.json(), wb, ensure_ascii=False)


def load_dev():
    """
    download device's name
    @return: file name dev.json
    """
    data = {"switch": "1", "page": "", "dep": "发动机排放检测部"}
    for i in range(1, 6):
        data["page"] = data["page"] + str(i)

        r = requests.post(url=DEV_LIST_URL,
                          headers=HEADERS,
                          cookies=cookies,
                          data=data)
        print(data["page"])
        print(r.json())
        time.sleep(0.5)
        with open(doc_dirpath + 'devName.json', 'a') as wb:
            json.dump(r.json(), wb, ensure_ascii=False)
        data["page"] = ""


def load_dev_num():
    """
    download device's number
    @return: file name num.json
    """
    data = {"switch": "2", "page": "", "dep": "发动机排放检测部"}
    for i in range(1, 8):
        data["page"] = data["page"] + str(i)

        filename = os.path.join(temp_dirpath, 'num' + str(i) + '.json')

        r = requests.post(url=DEV_LIST_URL,
                          headers=HEADERS,
                          cookies=cookies,
                          data=data)
        # print(data["page"])
        print(r.json())
        time.sleep(1)
        with open(filename, 'a') as wb:
            json.dump(r.json(), wb, ensure_ascii=False)
        data["page"] = ""


def load_dev_info():
    """
    Engine Emission Department's device information
    @return: file name coinfo.json in doc
    """
    url = "http://deviceman.caeri.com.cn:6037/Index/get_device.html"
    post_data = {"switch": "2", "num": "", "dep": "发动机排放检测部"}
    download_data = []
    for filename in os.listdir(temp_dirpath):
        # print(filename)
        filepath = os.path.join(temp_dirpath, filename)
        print(filepath)
        with open(filepath, 'r') as rb:
            tmp = json.load(rb)
            for _ in tmp:
                # print(_)
                post_data["num"] = _["0"]
                # print(post_data)
                r = requests.post(url=url,
                                  headers=HEADERS,
                                  cookies=cookies,
                                  data=post_data)
                # print(r.text)
                # print(r.json())
                download_data.extend(r.json())
                time.sleep(0.2)
                post_data["name"] = ""
    save_path = os.path.join(doc_dirpath, 'devInfo.json')
    with open(save_path, 'a', encoding='utf-8') as wb:
        json.dump(download_data, wb, ensure_ascii=False)
    print('download finished ！！！')


def device_info():
    """
    return a list consists of all device number
    """
    filepath = os.path.join(doc_dirpath, 'devInfo.json')
    dev_info_dicts = load_json(filepath, encoding='utf-8')
    dev_num = []
    dev_name = []
    dev_name_num_dict = {}
    temp_filter = [str(i) for i in range(20)]
    # the categories of details
    category = list(filter(lambda x: x not in temp_filter, dev_info_dicts[0].keys()))
    for data in dev_info_dicts:
        dev_num.append(data['DeviceNO'])
        dev_name.append(data['DeviceName'])
        # dev_name_num_dict[data['']]
    dev_name_num_dict = dict(zip(dev_name, dev_num))

    return dev_name_num_dict


if __name__ == '__main__':
    # print(cookies)
    # load_dev_num()
    # load_dev_info()
    print(device_info())

# 下载的数据编码不能正常被json解析，导致写入文件报错
# 改用如下创建文件时格式化文件编码即可解决！
# json写入文件默认为ascii编码，需使用'ensure_ascii=False'禁用，否则文件不能正常显示中文
# with open('coInfo.json', 'r') as wb:
#     t = json.load(wb)
#     with open('coInfo1.txt', 'w', encoding='utf-8') as rb:
