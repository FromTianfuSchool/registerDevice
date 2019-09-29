# from openpyxl import load_workbook
import simplejson as json

with open('coInfo.json', encoding='utf-8') as rb:
    tmp = json.load(rb)
    print(tmp[0])