"""
@author: Giraffe
@Contact :   gental_j@163.com
@time    :   2020/3/7 13:48:46
@file    :   login.py
@desc    :   
"""

from flask import Blueprint


wechat = Blueprint('wechat', __name__)


@wechat.route('/login', methods=['POST', 'GET'])
def login():
    from app.static.script.login import LoginInit
    from app.static.script import QRImgPath
    login_web = LoginInit()
    imgpath = 'static/image/qrcode.jpg'
    # copyfile(QRImgPath, imgpath)
    login_web.login_index(QRImgPath)

    return imgpath
