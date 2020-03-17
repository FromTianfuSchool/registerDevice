"""
@author: Giraffe
@Contact :   gental_j@163.com
@time    :   2020/3/7 13:31:05
@file    :   choose_dev_info.py
@desc    :
"""

from flask import Blueprint
from flask import request
from flask import jsonify
from . import DEV_INFO

choose = Blueprint('choose', __name__)

dev_info = DEV_INFO


@choose.route('/choose_dev_info', methods=['POST', 'GET'])
def choose_dev_info():
    """
    根据前端返回的值，查找设备信息中对应的设备num或者设备名称
    """
    recv_data = request.get_json()
    print(recv_data)
    for key, value in dev_info.items():
        if value == recv_data[0]:
            # print(key)
            return jsonify({'val': key})
        if key == recv_data[0]:
            return jsonify({'val': value})
