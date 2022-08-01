"""
#!/usr/bin/python
#-*- coding:utf-8 -*-
-------------------------------------------------
# @Project  :PythonWeb
# @File     :demo_route.py
# @Date     :2022/7/26 10:21
# @Author   :张铠
# @IDE :PyCharm
-------------------------------------------------
"""
# 导包
import json
import random
from flask import Flask, request

app = Flask(__name__)

def read_jsondata(keyvalue):
    """
    获取json数据
    :return:
    """
    with open(file='./login_msg.json', mode='r', encoding='utf-8') as json_file:
        for msg_data in json.load(json_file):
            return msg_data[keyvalue]


def getRandomNum():
    return random.randint(100000000, 999999999)


@app.route('/login', methods=['POST'])
def loginApi():
    username = request.json.get('username')
    password = request.json.get('password')
    result_data = None
    if username == 'admin' and password == '123456':
        return read_jsondata('success')
    elif username == 'admin' and password != '123456':
        return read_jsondata('pwd_error')
    elif username != 'admin' and password == '123456':
        return read_jsondata('user_error')
    else:
        return read_jsondata('error')


if __name__ == '__main__':
    app.run()