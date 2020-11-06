"""
author :rain
Date : 2020/10/15
Description :
"""

from locust import HttpLocust, TaskSet, task, between

# 定义用户行为
import constant
from utilss.httpsample import signature


class UserBehavior(TaskSet):

    def on_start(self):
        self.key = constant.KEY

    @task(1)
    def get_user_flowwer(self):
        # 我的关注 100
        url = '/interface/stay/appUserFollower!getNewFollowUser.do'
        params = {'key': self.key, 'language': 'zh_Hans', 'curPage': '1', 'pageSize': '20',
                  'userid': '104246500'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='appUserFollower!getNewFollowUser.do', )

    @task(2)
    def get_myinfo_friend(self):
        # 我的信息 200
        url = '/v3/interface/stay/myInfoForFriend'
        params = {'key': self.key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451'
            , 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
        params['signature'] = signature(params)
        r = self.client.get(url, params=params, name='stay/myInfoForFriend')

    @task(1)
    def test_live_rank(self):
        # 榜单简要描述  100
        url = '/v1/live/rank'
        params = {'key': self.key, 'language': 'zh_Hans'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='live/rank')


class WebsiteUser(HttpLocust):
    host = "https://api.rela.me"
    task_set = UserBehavior
    wait_time = between(5, 10)


if __name__ == '__main__':
    user = UserBehavior()
