from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import random


def random_number():
    string = ""
    for i in range(6):
        number = random.randint(0, 9)
        string += str(number)
    return string


def aliyun_code(telephone, code_dict):
    client = AcsClient('LTAI4Fh7VCRkALLAstsDp7cT', 'cboI2jOBgURBNBB3t5Ceben6pOkuWS', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', telephone)
    request.add_query_param('SignName', "论坛管理系统")
    request.add_query_param('TemplateCode', "SMS_174585804")
    request.add_query_param('TemplateParam', code_dict)

    response = client.do_action(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))

