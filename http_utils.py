# 2017.01.16 18:54:53 �й���׼ʱ��
#Embedded file name: F:\YinHuSDK\tools\U8SDKTool-Win-P34\scripts\http_utils.py
import config_utils
if config_utils.is_py_env_2():
    import urllib2
    import urlparse
else:
    import urllib.request as urllib2
    import urllib.parse as urlparse

def get(url, params):
    full_url = url
    if params != None and len(params) > 0:
        data = urlparse.urlencode(params)
        full_url = full_url + '?' + data
    with urllib2.urlopen(full_url) as f:
        content = f.read()
    return content


def post(url, params):
    if params != None and len(params) > 0:
        data = urlparse.urlencode(params)
    else:
        data = ''
    data = data.encode('utf-8')
    request = urllib2.Request(url)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=utf-8')
    with urllib2.urlopen(request, data) as f:
        content = f.read()
    return content
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.01.16 18:54:53 �й���׼ʱ��
