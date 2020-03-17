"""
@author: Giraffe
@Contact :   gental_j@163.com
@time    :   2020/3/7 13:32:02
@file    :   __init__.py.py
@desc    :
"""

from app.static.script import downloadDevInfo


# from . import login
# from . import choose_dev_info

# 设备信息中的名称和id,返回一个对应的字典
DEV_INFO = downloadDevInfo.device_info()
