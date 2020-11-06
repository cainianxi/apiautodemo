"""
author :rain
Date : 2020/10/16
Description :
"""
import random

import yaml
from locust import HttpLocust, TaskSet, task

# 定义用户行为
from utilss.httpsample import signature


class UserBehavior:
    user = {}

    def __init__(self):
        # file_path = os.path.abspath(os.path.dirname(__file__)) + os.sep + 'user_info.yaml'
        with open('/Users/rain/PycharmProjects/testuprela1/user_info.yaml', 'r', encoding='UTF-8') as f:
            user_info = yaml.safe_load(f)
            self.user: dict = random.choice(user_info)

    def rebind(self):
        print(self.user)


if __name__ == '__main__':
    us = UserBehavior()
    us.rebind()
