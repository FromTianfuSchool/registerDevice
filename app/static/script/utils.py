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



curdir = osp.abspath(osp.dirname(osp.dirname(__file__)))
doc_dirpath = osp.abspath(osp.join(curdir, 'docs'))
temp_dirpath = osp.abspath(osp.join(doc_dirpath, 'temp'))

# QRImgPath = osp.join(doc_dirpath, 'qrcode.jpg')
# save to app static dir
img_dir = osp.join(curdir, 'image')
qrcode_dir = osp.join(img_dir, 'qrcode')

cookiesPath = osp.join(doc_dirpath, 'cookies.json')
deviceinfoPath = osp.join(doc_dirpath, 'device_info.xlsx')
samplePath = osp.join(doc_dirpath, 'sample.json')


if __name__ == '__main__':
    print(curdir)
    print(doc_dirpath)
    print(QRImgPath)
    print(osp.dirname(curdir))
