"""
实名认证  创建短信模板 获取模板id
找到接口的 Appkey
保证有剩余次数
查看接口文档
接口地址
请求方式
返回值类型
请求参数  哪些是必填项  选填项

pip install requests
"""

import requests


def send_sms(mobile, captcha):
    url = "你的接口地址"
    params = {
        "mobile": mobile,
        "tpl_id": "你的模板id",
        "tpl_value": "#code#" + captcha,
        "key": ""
    }
    #  带着参数向接口地址发送请求
    response = requests.get(url, params)
    # 将结果序列化成json
    result = response.json()
    # 根据接口文档返回结果  0 表示短信发送成功
    if result['error_code'] == 0:
        return True
    else:
        return False
