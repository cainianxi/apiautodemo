

import requests
from locust import HttpUser, TaskSet, task, between

# 定义用户行为
import constant
from utilss.httpsample import signature


class Follow(TaskSet):

    def on_start(self):
        # with open('/Users/rain/PycharmProjects/testuprela1/user_info.yaml', 'r', encoding='UTF-8') as f:
        #     self.user_info = yaml.safe_load(f)
        self.key = constant.KEY
        self.phone = constant.PHONE
        self.uid = constant.UID


    @task(1)
    def gold_list(self):
        # 软妹豆购买列表
        url = '/v1/gold/list'
        params = {
        'apptype': 'universal',
        'client': 'iPhone11 % 2C8',
        'clientVersion': '50306',
        'deviceId': 'sm_20190729221036225c7ee32c09a9f2f2b21e0f05bad5fc019ed9e4e084ae3f',
        'from_class': 'RfSUniversalRouterRootViewController',
        'key': '11194611009483590707 - 106759214',
        'language': 'zh - Hans',
        'lat': '31.170243',
        'lng': '121.430498',
        'mobileOS': 'IOS % 2013.600000',
        'view_class': 'TLAccountRechargeViewController',
        }
        #'key': self.key
        params['signature'] = signature(params)
        self.client.get(url, data=params, name='/v1/gold/list')
    # i = requests.get(url=url,params=params)
    # print(i.json())


    @task(1)
    def internal_gold_list(self):
        # 软妹豆购买列表
        url = '/v1/internal/gold/list'
        params = {
        'apptype': 'universal',
        'client': 'iPhone11 % 2C8',
        'clientVersion': '50306',
        'deviceId': 'sm_20190729221036225c7ee32c09a9f2f2b21e0f05bad5fc019ed9e4e084ae3f',
        'from_class': 'RfSUniversalRouterRootViewController',
        'key': '11194611009483590707 - 106759214',
        'language': 'zh - Hans',
        'lat': '31.170243',
        'lng': '121.430498',
        'mobileOS': 'IOS % 2013.600000',
        'view_class': 'TLAccountRechargeViewController',
        }
        #'key': self.key
        params['signature'] = signature(params)
        self.client.get(url, data=params, name='/v1/internal/gold/list')
    # i = requests.get(url=url,params=params)
    # print(i.json())


class WebsiteUser(HttpUser):
    host = "http://test-api.rela.me"
    tasks = [Follow]
    wait_time = between(5, 10)

# if __name__ == '__main__':
#     gold_list()