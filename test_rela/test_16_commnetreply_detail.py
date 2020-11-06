"""
author :rain
Date : 2020/10/17
Description :评论回复详情页
"""


from locust import HttpLocust, TaskSet, task, between

import constant
from utilss.httpsample import signature


# 定义用户行为
class UserBehavior(TaskSet):

    def on_start(self):
        self.key = constant.KEY
        self.uid = constant.UID

    @task(1)
    def get_ab_config(self):
        # ab配置
        url = "/v3/interface/ab/config"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='ab_config')


    @task(1)
    def test_notRead(self):
        url = '/friend/stay/moments/notRead'
        params = {'key': self.key, 'language': 'zh_Hans', 'cursor': 0
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='moments/notRead')


    @task(1)
    def test_getMainAdvert(self):
        url = '/v3/interface/stay/getMainAdvert'
        params = {'key': self.key, 'language': 'zh_Hans'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='stay/getMainAdvert')

    @task(1)
    def get_interface_resources(self):
        # 广告初始化资源
        url = '/v3/interface/resources'
        params = {
            'client': 'iPhone11 % 2C8',
            'location': 'initAdv',
            'resourceType': '2',
            'cursor': '0',
            'limit': '10',
            'key': self.key,
            'lat': '31.170296',
            'lng': '121.430487',
            'language': 'zh - Hans',
            'mobileOS': 'iOS + 14.0.1',
            'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
            'apptype': 'universal',
            'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='interface/resources')


    @task(1)
    def get_user_params_init(self):
        # 用户初始化
        url = '/v2/params/init'
        params = {
            'view_class': 'RfSUniversalRouterRootViewController',
            'client': 'iPhone11 % 2C8',
            'key': self.key,
            'lat': '31.170296',
            'lng': '121.430487',
            'language': 'zh - Hans',
            'mobileOS': 'iOS + 14.0.1',
            'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
            'apptype': 'universal',
            'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='params/init')

    @task(1)
    def get_myInfoForFriend(self):
        # 我的信息
        url = "/v3/interface/stay/myInfoForFriend"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='myInfoForFriend')


    @task(1)
    def test_commentReply(self):
        url = '/v3/moments/commentReply/list'
        params = {'key': self.key, 'language': 'zh_Hans', 'id': 160228730570310003, 'cursor': 0, 'limit': 50
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='commentReply/list')

    @task(1)
    def get_user_blacklist(self):
        # 用户屏蔽列表
        url = '/v2/users/blacklist'
        params = {
            'view_class': 'RfSUniversalRouterRootViewController',
            'client': 'iPhone11 % 2C8',
            'key': self.key,
            'lat': '31.170296',
            'lng': '121.430487',
            'language': 'zh - Hans',
            'mobileOS': 'iOS + 14.0.1',
            'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
            'apptype': 'universal',
            'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='users/blacklist')



class WebsiteUser(HttpLocust):
    host = "https://api.rela.me"
    task_set = UserBehavior
    wait_time = between(5, 10)
