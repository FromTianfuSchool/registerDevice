'''
@File    :   utils.py
@start   :   2019/11/20 23:07:25
@Author  :   Jiang Xin 
@Version :   1.0
@Contact :   gental_j@163.com
@License :   (C)Copyright 2018-2019, JiangXin
@Desc    :   construction of project
'''

import os.path as osp


class projPath:

    def __init__(self):

        self.curdir = osp.abspath(osp.dirname(osp.dirname(__file__)))
        self.doc_dirpath = osp.abspath(osp.join(self.curdir, 'docs'))
        self.QRImgPath = osp.join(self.doc_dirpath, 'QrImge.jpg')
        self.cookiesPath = osp.join(self.doc_dirpath, 'cookies.json')


curdir = osp.abspath(osp.dirname(osp.dirname(__file__)))
doc_dirpath = osp.abspath(osp.join(curdir, 'docs'))
QRImgPath = osp.join(doc_dirpath, 'QrImge.jpg')
cookiesPath = osp.join(doc_dirpath, 'cookies.json')
deviceinfoPath = osp.join(doc_dirpath, 'device_info.xlsx') 
samplePath = osp.join(doc_dirpath, 'sample.json') 
