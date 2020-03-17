from flask import render_template, url_for, request, jsonify
from . import app, login_init, user_manager
from . import DEV_INFO, QRCODE_SCAN_BACK
from . import Upload
from pprint import pprint

dev_info = DEV_INFO
userinfo = {
    "username": "蒋鑫",
    "phone": "13368385052",
    "cookies": "fdsafdsagewrger",
}
user_manager.append(userinfo)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', device_info=dev_info, userinfo=userinfo)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    登录验证
    """

    img = login_init.login_index()
    return jsonify({
        "url": url_for('static', filename='image/qrcode/{}'.format(img)),
    })


@app.route('/check_login', methods=['GET'])
def check_login():
    print("请求验证")
    import time
    start_time = time.time()
    while time.time() - start_time < 10:
        code_back = login_init.check_status()
        if code_back == QRCODE_SCAN_BACK[4]:
            print("out ok")
            userinfo = login_init.get_user_and_tel()
            user_manager.append(userinfo)
            return jsonify({
                "url": url_for('static', filename='/image/success.png'),
                "userinfo": userinfo
            })
        time.sleep(1)
    print("out no")
    return url_for('static', filename='/image/failed.png')


@app.route('/select_dev_num', methods=['POST', 'GET'])
def select_dev_num():
    """
    根据输入信息，返回对应的设备num或者名称
    """
    recv_data = request.get_json()
    print(recv_data)
    for key, value in dev_info.items():
        # pprint("key:{0}, value:{1}".format(key, value))
        if value == recv_data[0]:
            return jsonify({'val': key})
        # if key == recv_data[0]:
        #     return jsonify({'val': value})


@app.route('/send', methods=['POST'])
def send_table():
    resp = request.get_json()
    user = resp.pop(-1)
    try:
        if user['username'] not in user_manager:
            return jsonify({"error": "你还没有登录"})
    except KeyError as e:
        return jsonify({"error": "你还没有登录"})

    table = []
    info_upload = Upload(user_manager[user['username']].cookies)
    for item in resp:
        # 将返回中的key='3'的日期和开始时间key='4'组合起来, 并将开始时间删除
        # {'0': 'ZPJ065', '1': '分流稀释系统', '2': '发动机排放检测部',
        # '3': '2019-02-12', '4': '8', '5': '12',
        # '6': 'W19009313 - 发动机 - 东风康明斯发动机有限公司',
        # '7': '蒋鑫', '8': '发动机排放检测部', '9': '排气污染物', '10': ''}
        # ================================================================
        # {
        #     "data[name]": "发动机排气采样分析测试系统",
        #     "data[num]": "ZPJ190",
        #     "data[dep]": "发动机排放检测部",
        #     "data[start_time]": "2019-09-05 08",
        #     "data[end_time]": "8",
        #     "data[task_name]": "W19009313 - 发动机 - 东风康明斯发动机有限公司",
        #     "data[people]": "蒋鑫",
        #     "data[address]": "",
        #     "data[phone]": "13368385052",
        #     "data[real_name]": "蒋鑫",
        #     "data[obj_name]": "车用压燃式发动机排气污染物",
        #     "data[remark]": ""
        # }
        if item['0'] == "":
            continue
        item['3'] = item['3'].split(' ')[0] + ' ' + item['4']
        item.pop('4')
        temp = {
            "data[name]": item['1'],
            "data[num]": item['0'],
            "data[dep]": item['2'],
            "data[start_time]": item['3'],
            "data[end_time]": item['5'],
            "data[task_name]": item['6'],
            "data[people]": item['7'],
            "data[address]": item['8'],
            "data[phone]": user_manager[user['username']].phone,
            "data[real_name]": user_manager[user['username']].username,
            "data[obj_name]": item['9'],
            "data[remark]": item['10']
        }
        # table.append(temp)
        pprint(temp)
        info_upload.upload(temp)
    return "ok"


if __name__ == '__main__':
    app.debug = True
    app.run()
    # --host=0.0.0.0 --port=5000
    # app.run(host='0.0.0.0', port=5000)
