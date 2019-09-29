'''
@File    :   uploadInfo.py
@start   :   2019/09/28 18:00:24
@Author  :   Jiang Xin 
@Version :   1.0
@Contact :   gental_j@163.com
@License :   (C)Copyright 2018-2019, JiangXin
@Desc    :   upload used device's information
'''
import requests
from openpyxl import load_workbook, Workbook
import json

url = "http://deviceman.caeri.com.cn:6037/Index/add_log.html"
cookies = {
    "thinkphp_show_page_trace": "0|0",
    "PHPSESSID": "4bknp8svurumnlcoc1bao4t006"
}
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
}


def upload(dev_info="name"):
    """
    description:
    @param dev_info: data of device information
    @return:
    """
    data_table = loadTemplate()
    load_data = loadDataExcel()
    for i in range(len(load_data)):
        for key in data_table.keys():
            data_table[key] = load_data[i][key]
        r = requests.post(url=url,
                          headers=headers,
                          cookies=cookies,
                          data=data_table)
        if r.status_code == 200 or r.status_code == '200':
            print('upload successful!')
    # print(data_table)


def loadDataExcel():
    """
    description:
    @param :
    @return: a list contains group data
    """
    wb = load_workbook('device_info.xlsx', data_only=True)
    workesheet = wb.active
    # rows = []
    rows_obj = list(workesheet.iter_rows())
    # print(rows_obj)
    # print(rows_obj[2][0])
    dict_list = []
    name_list = [cell.value for cell in rows_obj[2]]
    for row in rows_obj[3:]:
        if row[0].value:  #空白行为数据录入结束标志位
            value_list = [cell.value for cell in row]
            group = dict(zip(name_list, value_list))
            group['data[start_time]'] = group[
                'data[start_time]'] + ' ' + group['data[start_hour]']
            dict_list.append(group)
    return dict_list
    # 发动机排气采样分析测试系统 ZPJ190 发动机排放检测部 2019-09-06 00:00:00 8 None 蒋鑫 None 13368385052 蒋鑫 车用压燃式发动机排气污染物 None


# loadDataExcel()


def loadTemplate(template='format.json'):
    """
    description: get the parameter for upload data
    @param template: the path of template file 
    @return: dict
    """
    with open(template, 'r', encoding='utf-8') as rb:
        parm_dict = json.load(rb)
        return parm_dict
    # print(parm_dict)
    # print('-'*50)
    # print(type(parm_dict))


# loadTemplate('format.json')

upload()
