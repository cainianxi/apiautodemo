"""
author :rain
Date : 2020/10/16
Description :
"""

from locust import task, TaskSet

import constant
from utilss.httpsample import signature, HttpSampler

hs = HttpSampler()

pro_url = 'https://api.rela.me'
test_url = 'https://test-api.rela.me'
pro_key = '9572070930129342419-104205815'
test_key = '1601426712855886906-106851715'
base_params = {'ua': 'theL/5.3.6_26 (iPhone 6s; iOS 13.50; zh-Hans; Wifi)', 'lat': '31.170315', 'lng': '121.430451',
               'language': 'zh-Hans', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306', 'apptype': 'universal'}


class test(TaskSet):
    def on_start(self):
        # with open('/Users/rain/PycharmProjects/testuprela1/user_info.yaml', 'r', encoding='UTF-8') as f:
        #     self.user_info = yaml.safe_load(f)
        self.key = constant.KEY
        self.phone = constant.PHONE

    @task(1)
    def test_notRead(self):
        url = '/friend/stay/moments/notRead'
        params = {'key': self.key, 'language': 'zh_Hans', 'cursor': 0
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='moments/notRead')

    @task(1)
    def test_suggest(self):
        url = '/v3/friend/stay/topic/suggest'
        params = {'key': self.key, 'language': 'zh_Hans', 'topicName': 16, 'curPage': '1'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='topic/suggest')

    @task(1)
    def test_comment_list(self):
        url = '/v3/themes/comment/list'
        params = {'key': self.key, 'language': 'zh_Hans', 'id': 160256284743510068, 'sortType': 1
            , 'cursor': 0, 'limit': 20
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='comment/list')

    @task(1)
    def test_themes_detail(self):
        url = '/v3/themes/detail'
        params = {'key': self.key, 'language': 'zh_Hans', 'id': 160256284743510068
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='themes/detail')

    @task(1)
    def test_themes_recommend_check(self):
        url = '/v3/themes/recommend/check'
        params = {'key': self.key, 'language': 'zh_Hans', 'themeId': 160256284743510068
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='recommend/check')

    @task(1)
    def test_live_detail_info(self):
        url = '/v1/live/detail-info'
        params = {'key': self.key, 'language': 'zh_Hans', 'id': 88888103459922
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'view_class': 'TLWatchLiveListViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='live/detail-info')

    @task(1)
    def test_live_gift_list(self):
        url = '/v1/live/gift/list'
        params = {'key': self.key, 'language': 'zh_Hans', 'appId': 'com.rela'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
                  'view_class': 'TLWatchLiveListViewController'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='gift/list')

    @task(1)
    def test_is_first_charge(self):
        url = '/v1/gold/is-first-charge'
        params = {'key': self.key, 'language': 'zh_Hans'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
                  'view_class': 'TLWatchLiveListViewController'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='is-first-charge')

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
    def test_myInfoForFriend(self):
        url = '/v3/interface/stay/myInfoForFriend'
        params = {'key': self.key, 'language': 'zh_Hans'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
                  'view_class': 'TLWatchLiveListViewController'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='stay/myInfoForFriend')

    @task(1)
    def test_topicHead(self):
        url = '/v3/friend/stay/moments/topicHead'
        params = {'key': self.key, 'language': 'zh_Hans', 'topicId': 366
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='moments/topicHead')

    @task(1)
    def test_roamWorld_config(self):
        url = '/v3/roamWorld/config'
        params = {'key': self.key, 'language': 'zh_Hans', 'topicId': 366
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='roamWorld/config')

    @task(1)
    def test_newUserInfoForFriend(self):
        url = '/v3/interface/stay/newUserInfoForFriend'
        params = {'key': self.key, 'language': 'zh_Hans', 'userId': 104205815
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='stay/newUserInfoForFriend')

    @task(1)
    def test_vip_detail(self):
        url = '/v2/users/vip/detail'
        params = {'key': self.key, 'language': 'zh_Hans', 'userId': 104205815
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='vip/detail')

    @task(1)
    def test_live_rank(self):
        # 榜单简要描述  100
        url = '/v1/live/rank'
        params = {'key': self.key, 'language': 'zh_Hans'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='live/rank')

    @task(1)
    def test_commentReply(self):
        url = '/v3/moments/commentReply/list'
        params = {'key': self.key, 'language': 'zh_Hans', 'id': 160228730570310003, 'cursor': 0, 'limit': 50
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='commentReply/list')

    @task(1)
    def test_appUserView(self):
        url = '/interface/stay/appUserView!cheackView.do'
        params = {'key': self.key, 'language': 'zh_Hans', 'curPage': 1
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='appUserView!cheackView.do')

    @task(1)
    def test_gold_list(self):
        url = '/v1/gold/list'
        params = {'key': self.key, 'language': 'zh_Hans'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='gold/list')

    @task(1)
    def test_getMainAdvert(self):
        url = '/v3/interface/stay/getMainAdvert'
        params = {'key': self.key, 'language': 'zh_Hans'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='stay/getMainAdvert')

    @task(1)
    def test_category_config(self):
        url = '/v3/themes/category/config'
        params = {'key': self.key, 'language': 'zh_Hans'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='category/config')

    @task(1)
    def test_adv_list(self):
        url = '/v3/interface/adv/list'
        params = {'key': self.key, 'language': 'zh_Hans', 'advType': 'init'
            , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
            , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='adv/list')

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
    def get_moments_notread(self):
        # 启动初始化
        url = '/friend/stay/moments/notRead'
        params = {
            'cursor': '0',
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
        self.client.get(url, params=params, name='moments/notRead')


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
        url = "v2/params/init"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304',
                  'view_class': 'RfSUniversalRouterRootViewController'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='getBindingList')

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
    def get_ab_config(self):
        # ab配置
        url = "/v3/interface/ab/config"
        params = {'key': self.key, 'apptype': 'universal', 'client': 'iPhone11%2C8', 'language': 'zh_Hans',
                  'deviceId': 'sm_20191114115308e49289ad37d59211f1c6571595d5086001c967eb845c87af',
                  'lat': '31.170296', 'lng': '121.430487', 'mobileOS': 'IOS%2014.000000', 'clientVersion': '50304'}
        params['signature'] = signature(params)
        self.client.get(url, params=params, name='ab_config')

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


if __name__ == '__main__':
    pass
    # test_adv_list()
    # test_category_config()
    # test_getMainAdvert()
    # test_gold_list()
    # test_appUserView()
    # test_commentReply()
    # test_vip_detail()
    # test_newUserInfoForFriend()
    # test_activityConfigurable()
    # test_roamWorld()
    # test_topicHead()
    # test_myInfoForFriend()
    # test_resources()
    # test_activityInfo()
    # test_is_first_charge()
    # test_live_gift_list()
    # test_live_detail_info()
    # test_notRead()
    # test_suggest()
    # test_comment_list()
    # test_themes_detail()
    # test_themes_recommend_check()
