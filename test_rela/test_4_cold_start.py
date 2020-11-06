"""
author :rain
Date : 2020/10/17
Description : 冷启动
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
    def get_main_ad(self):
        # 广告 banner广告
        url = "/interface/stay/appSystem!getMainAdvert.do"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='appSystem!getMainAdvert.do')

    @task(1)
    def test_resources(self):
        url = '/v3/interface/resources'
        params = {'key': self.key, 'language': 'zh_Hans', 'location': 'initAdv', 'resourceType': 2
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
                  'view_class': 'TLWatchLiveListViewController'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='interface/resources')

    @task(1)
    def get_getBindingList(self):
        # 我的关系
        url = "/interface/stay/binding/getBindingList"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304',
                  'view_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='getBindingList')

    @task(1)
    def get_init(self):
        # 我的关系
        url = "/v2/params/init"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304',
                  'view_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='params/init')

    @task(1)
    def get_notRead(self):
        # 我的关系
        url = "/friend/stay/moments/notRead"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304',
                  'view_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='getBindingList')

    @task(1)
    def get_listWithMusicMultiImg(self):
        # 我的日志
        url = "/v3/friend/stay/moments/listWithMusicMultiImg"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304',
                  'pageSize': 20, 'curPage': 1, 'mainType': 'moments'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='listWithMusicMultiImg')

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
    def get_getBindingList(self):
        # 我的关系
        url = "/interface/stay/binding/getBindingList"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304',
                  'view_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='getBindingList')

    @task(1)
    def get_arPreReleaselist(self):
        # 获取ar礼物列表
        url = '/v1/live/gift/arPreReleaselist'
        params = {
            'key': self.key,
            'appId': 'com.rela',
            'apptype': 'universal',
            'client': 'iPhone11%2C8',
            'clientVersion': '50304',
            'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
            'language': 'zh-Hans',
            'lat': '31.170296',
            'lng': '121.430487',
            'mobileOS': 'IOS%2014.000000',
            'view_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='gift/arPreReleaselist')

    @task(1)
    def get_hotTheme_viewList(self):
        # 获取热门话题
        url = '/v3/themes/hotTheme/viewList'
        params = {
            'cursor': '0',
            'limit': '100',
            'key': self.key,
            'lat': '31.170296',
            'lng': '121.430487',
            'language': 'zh - Hans',
            'mobileOS': 'iOS + 14.0.1',
            'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
            'apptype': 'universal',
            'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='hotTheme/viewList')

    @task(1)
    def get_recommend_moments(self):
        # 获取推荐日志
        url = '/v3/recommend/moments'
        params = {
            'cursor': '0',
            'limit': '20',
            'key': self.key,
            'lat': '31.170296',
            'lng': '121.430487',
            'language': 'zh - Hans',
            'mobileOS': 'iOS + 14.0.1',
            'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
            'apptype': 'universal',
            'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='recommend/moments')

    @task(1)
    def get_mainpage_subscribe(self):
        # 获取主页关注用户
        url = '/v3/mainpage/subscribe'
        params = {
            'key': self.key,
            'lat': '31.170296',
            'lng': '121.430487',
            'language': 'zh - Hans',
            'mobileOS': 'iOS + 14.0.1',
            'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
            'apptype': 'universal',
            'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='mainpage/subscribe')

    @task(1)
    def get_followpage_recommend_list(self):
        # 获取关注日志列表
        url = '/v3/followpage/recommend/list'
        params = {
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
        self.client.get(url, params=params, name='recommend/list')

    @task(1)
    def get_live_list(self):
        # 直播列表
        url = '/v1/live/list'
        params = {
            'cursor': '0',
            'sort': 'hot',
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
        self.client.get(url, params=params, name='live/list')

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
