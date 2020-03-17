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

QRCODE_SCAN_BACK = {
    1: 'QRCODE_SCAN_ERR',
    2: 'QRCODE_SCAN_NEVER',
    3: 'QRCODE_SCAN_ING',
    4: 'QRCODE_SCAN_SUCC',
}
