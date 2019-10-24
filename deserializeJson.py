'''
@File    :   deserialize.py
@start   :   2019/10/03 12:33:51
@Author  :   Jiang Xin 
@Version :   1.0
@Contact :   gental_j@163.com
@License :   (C)Copyright 2018-2019, JiangXin
@Desc    :   deserialize json type data, create an excel file('info.xlsx') to save the format original data 
'''

import json
import pandas as pd


def loadFile():
    """
    description:
    @param :
    @return:
    """
    with open('coInfo.json', 'r', encoding='utf-8') as rb:
        d = json.load(rb)
    d_keys = list(d[0].keys())
    columns = []
    for i in d_keys:  # get columns name
        if d_keys.index(i) % 2 == 1:
            columns.append(i)
    df = pd.DataFrame(d)
    drop_col = [str(i) for i in range(19)]
    for i in drop_col:
        df = df.drop(i, axis=1)
    df.to_excel('info.xlsx')


if '__name__' == '__main__':
    loadFile()
