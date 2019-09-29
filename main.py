from openpyxl import load_workbook
from openpyxl import Workbook
add_log = "http://deviceman.caeri.com.cn:6037/Index/add_log.html"
cookies = {
    "thinkphp_show_page_trace": "0|0",
    "PHPSESSID": "4mktlnocsh734369guv5aoeko3"
}
# driver = webdriver.Chrome()
# driver.add_cookie(cookies)
# driver.get("http://deviceman.caeri.com.cn:6037/Index/device_list.html")

postData = {
    "data[name]": "",
    "data[num]": "",
    "data[dep]": "",
    "data[start_time]": "",
    "data[end_time]": "",
    "data[task_name]": "",
    "data[people]": "",
    "data[address]": "",
    "data[phone]": "",
    "data[real_name]": "",
    "data[obj_name]": "",
    "data[remark]": ""
}