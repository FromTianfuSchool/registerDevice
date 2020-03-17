from flask import Flask
from app.static.script import downloadDevInfo
from app.static.script.login import LoginInit, QRCODE_SCAN_BACK
from app.static.script.uploadInfo import Upload
from .views.user import UserManager

#
# from .views import choose_dev_info
# from .views import login
#
app = Flask(__name__)
#
# app.register_blueprint(choose_dev_info)
# app.register_blueprint(login)
DEV_INFO = downloadDevInfo.device_info()

# 初始化用户登录
login_init = LoginInit()

# 初始化用户管理
USER_INFO_DETAIL = ['username', 'phone', 'cookies']
user_manager = UserManager(USER_INFO_DETAIL)


