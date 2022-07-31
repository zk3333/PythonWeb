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
import random
from flask import Flask, request

app = Flask(__name__)


def getRandomNum():
    return random.randint(100000000, 999999999)


@app.route('/login', methods=['POST'])
def loginApi():
    username = request.json.get('username')
    password = request.json.get('password')
    if username == 'admin' and password == '123456':
        return {
            'data': {
                'status': 'success',
                'code': 0,
                'msg': '登录成功！！！',
                'token': getRandomNum()
            }
        }
    else:
        return {
            'data': {
                'status': 'fail',
                'code': -1,
                'msg': '用户名或者密码错误，登录失败！！！'
            }
        }


if __name__ == '__main__':
    app.run()
