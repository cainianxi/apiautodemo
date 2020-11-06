"""
author :rain
Date : 2020/10/15
Description :
"""

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
    def rebind(self):
        # 重新绑定 10
        url = '/v1/auth/rebind'
        params = {'key': self.key, 'language': 'zh_Hans', 'lat': '31.170315',
                  'lng': '121.430451', 'type': 'cell'
            , 'cell': self.phone, 'code': '5678', 'zone': "+99"}
        params['signature'] = signature(params)
        self.client.post(url, data=params, name='rebind')

    @task(1)
    def rebind_new(self):
        # 新重新绑定 10
        url = '/v1/auth/rebind-newformat'
        params = {'key': self.key, 'language': 'zh_Hans', 'lat': '31.170315',
                  'lng': '121.430451', 'type': 'cell', 'cell': self.phone, 'code': '5678', 'zone': "+99"}
        params['signature'] = signature(params)
        self.client.post(url, data=params, name='rebind-newformat')

    @task(1)
    def check_username(self):
        # 检查用户名 10
        url = '/v1/auth/check-username'
        params = {'key': self.key, 'language': 'zh_Hans', 'userName': "name"}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='check-username')

    @task(1)
    def test_live_friends(self):
        # 正在直播的朋友 10
        url = '/v1/live/living-friends'
        params = {'key': self.key, 'language': 'zh_Hans'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='living-friends')

    @task(1)
    def test_meta(self):
        # 排行榜信息 10
        url = '/v1/live/meta'
        params = {'key': self.key, 'language': 'zh_Hans'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='live/meta')

    @task(1)
    def test_type_list(self):
        # 直播类型列表 10
        url = '/v1/live/type-list'
        params = {'key': self.key, 'language': 'zh_Hans'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='type-list')

    @task(5)
    def arpre_releaselist(self):
        # ar礼物简要描述 50
        url = '/v1/live/gift/arPreReleaselist'
        params = {'key': self.key, 'language': 'zh_Hans'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='arPreReleaselist')

    @task(1)
    def get_user_level(self):
        # 用户等级 10
        url = '/v1/live/user-level'
        params = {'key': self.key, 'language': 'zh_Hans'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='user-level')

    @task(1)
    def get_user_perm(self):
        # 直播权限 10
        url = '/v1/live/perm'
        params = {'key': self.key, 'language': 'zh_Hans'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='live/perm')

    @task(1)
    def get_follow_secertly(self):
        # 悄悄关注列表 10
        url = '/interface/stay/appUserFollowerSecretly'
        params = {'key': self.key, 'language': 'zh_Hans', 'userid': self.uid, 'lat': '31.170315',
                  'lng': '121.430451'
            , 'curPage': '1', 'pageSize': '20', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='appUserFollowerSecretly')

    @task(1)
    def get_secertly_followdo(self):
        # 悄悄关注 10
        url = '/interface/stay/appUserFollower!secretlyFollow.do'
        params = {'key': self.key, 'language': 'zh_Hans', 'receivedId': '107277639', 'lat': '31.170315',
                  'lng': '121.430451'
            , 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
        params['signature'] = signature(params)
        self.client.post(url, data=params, name='secertly_followdo')

    @task(1)
    def get_secertly_follow(self):
        # v3悄悄关注 10
        url = '/v3/interface/stay/secretlyFollow'
        params = {'key': self.key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451'
            , 'receivedId': '107277639', 'actionType': '0'
            , 'curPage': '1', 'pageSize': '20', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
        params['signature'] = signature(params)
        self.client.post(url, data=params, name='secertly_follow')

    @task(1)
    def get_follow_anchors(self):
        # 我的信息 10
        url = '/v2/users/follow/anchors'
        params = {'key': self.key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451'
            , 'cursor': '1', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='follow/anchors')

    @task(1)
    def fans_remove(self):
        # 移除粉丝 10
        url = '/v2/users/fans/remove'
        params = {'key': self.key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451'
            , 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306', 'userId': '101136006'}
        params['signature'] = signature(params)
        self.client.post(url, data=params, name='fans/remove')




class WebsiteUser(HttpUser):
    host = "http://api.rela.me"
    tasks = [Follow]
    wait_time = between(5, 10)
