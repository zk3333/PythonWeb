"""
#!/usr/bin/python
#-*- coding:utf-8 -*-
-------------------------------------------------
# @Project  :PythonWeb
# @File     :locust_demo.py
# @Date     :2022/7/26 23:13
# @Author   :张铠
# @IDE :PyCharm
-------------------------------------------------
"""
import json

import jsonpath
import yaml
from locust import HttpUser, task, between, TaskSet

def read_session_txt():
    with open(file='SessionData.txt',mode="r", encoding='utf-8') as file_txt:
        return file_txt.readlines()

def read_extract_file(filename, node_name):
    """
    读取token.yml文件
    :return:
    """
    with open(file=filename, mode='r', encoding='utf-8') as f:
        value_data = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value_data[node_name]


def write_extract_file(filename, data):
    """
    写入token.yml文件
    :return:
    """
    with open(file=filename, mode='a', encoding='utf-8') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


class UserBehavior(TaskSet):
    # wait_time让模拟用户在每个任务执行后等待 1 到 5 秒
    wait_time = between(1, 5)
    '''
    # @task对于每个正在运行的用户，Locust 都会创建一个 greenlet（微线程），它将调用这些方法, 设置task权重 --> @task(3)
    @task
    # 获取授权返回的token信息
    def get_login_by_openid(self):
        url = 'https://t-consult-server.aegis-info.com/api/client/login_by_openid'
        json = {"certRole": "normal", "way": "longhua_court", "courtCode": "", "platformName": "12368平台（全国）",
                "openId": "orin85FOoFj3y0CiEXMg9Un_BU2c"}
        headers = {
            "userType": "4"
        }
        res = self.client.post(url=url, json=json, headers=headers)
        res_json = res.json()
        token = jsonpath.jsonpath(res_json, '$..token')
        print(token)
        token_str = ''.join(token)
        dict_data = {'token': token_str}
        write_extract_file('./token.yml', dict_data)
    '''

    @task
    # 获取返回的sessionId
    def save_session_visitor(self):
        url = 'https://t-consult-server.aegis-info.com/api/ws_session/save_session_visitor'
        data = {
            "courtId": "1732"
        }
        headers = {
            "userType": "1",
            "Authorization": read_extract_file(filename='./token.yml', node_name='token')
        }
        res = self.client.post(url=url, data=data, headers=headers)
        res_json = res.json()
        sessionId = jsonpath.jsonpath(res_json, '$..id')
        print(sessionId)
        sessionId_str = ''.join(sessionId)
        sessionId_data = {'sessionId': sessionId_str}
        print(sessionId_data)
        write_extract_file('./sessionMsg.yml', sessionId_data)

    # @task
    # def (self):
    #     url = 'https://t-consult-server.aegis-info.com/api/ws_session/save_session_visitor'
    #     data = {
    #         "courtId": "1732"
    #     }
    #     headers = {
    #         "Authorization": "JSESSIONID=A0BCDD3936C614AF3030EF6BF6693106"
    #     }
    #     res = self.client.post(url=url, headers=headers, data=data)
    #     result = res.json()
    #     print(result)
    #     token = jsonpath.jsonpath(result, '$..token')
    #     token_str = ''.join(token)
    #     token_data = {"token": token_str}
    #     # print(token_data)
    #     write_extract_file(token_data)
    #
    # @task
    # def get_work_all_data(self):
    #     url = 'http://192.168.50.218/api/v1/authority/all'
    #     headers = {
    #         "Authorization": read_extract_file('token')
    #     }
    #     res = self.client.get(url=url, headers=headers)
    #     print(res.json())


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    host = "https://t-consult-server.aegis-info.com"
    min_wait = 1000
    max_wait = 2000


if __name__ == '__main__':
    import os

    os.system("locust -f locust_demo.py --host=https://t-consult-server.aegis-info.com")
    # for SessionData in read_session_txt():
    #     print(SessionData.strip('\n'))





