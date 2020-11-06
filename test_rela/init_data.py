"""
author :rain
Date : 2020/10/15
Description :
"""
#


#
# smsRequestId
#
# key
import json
import os
import yaml

from utilss.httpsample import signature, HttpSampler

hs = HttpSampler()

user_info = []

base_params = {'ua': 'theL/5.3.6_26 (iPhone 6s; iOS 13.50; zh-Hans; Wifi)', 'lat': '31.170315', 'lng': '121.430451',
               'language': 'zh-Hans', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306', 'apptype': 'universal'}
file_path = os.path.abspath(os.path.dirname(__file__)) + os.sep + 'user_info.yaml'


def login(cell):
    url = 'https://test-api.rela.me/v1/auth/signin-newformat'
    params = {'type': 'cell', 'cell': cell, 'zone': '99', 'code': '5678', 'mobid': '21',
              'deviceId': 'sm_20190411160642ade026b965810f1d2fc433ac1dfd0d8a0135b82a64d134bf'
              }
    params['signature'] = signature(params)
    print(params)
    r = hs.post(url, params=params)
    data = r.json()
    key = data.get('data').get('key')
    uid = data.get('data').get('user').get('id')
    nickname = data.get('data').get('user').get('nickName')
    relaid = data.get('data').get('user').get('userName')
    cell: str = data.get('data').get('auth').get('cell')
    cell = cell[cell.find('-') + 1:]
    uinfo = {'key': key, 'uid': uid, 'nickname': nickname, 'relaid': relaid, 'cell': cell}
    global user_info
    user_info.append(uinfo)

    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def save_user_info():
    with open(file_path, 'w', encoding='UTF-8') as f:
        yaml.dump(user_info, f, allow_unicode=True, encoding='UTF-8')


def create_data():
    # 存储用户登录信息
    for i in range(750, 800):
        cell = '19999999' + str(i)
        login(cell)
    save_user_info()


def get_user_info():
    # 获取用户信息
    with open(file_path, 'r', encoding='UTF-8') as f:
        global user_info
        user_info = yaml.safe_load(f)
        # print('init:' + str(user_info))
    return user_info


if __name__ == '__main__':
    # create_data()
    data=get_user_info()
    print(data[1])
