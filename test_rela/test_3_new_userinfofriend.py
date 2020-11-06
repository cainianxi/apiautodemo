"""
author :rain
Date : 2020/10/16
Description :
"""

from locust import HttpLocust, TaskSet, task, between

# 定义用户行为
import constant
from utilss.httpsample import signature


class UserBehavior(TaskSet):

    def on_start(self):
        self.key = constant.KEY
        self.uid = constant.UID

    @task(1)
    def get_new_infoforfriend(self):
        # 我的速配资料 300
        url = '/v3/interface/stay/newUserInfoForFriend'
        params = {'key': self.key, 'language': 'zh_Hans', 'userId': constant.UID,
                  'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='stay/newUserInfoForFriend')


class WebsiteUser(HttpLocust):
    host = "https://api.rela.me"
    task_set = UserBehavior
    wait_time = between(5, 10)
