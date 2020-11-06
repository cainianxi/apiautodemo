
#from locust import HttpLocust, TaskSet, task, between

# 定义用户行为
from locust import HttpUser, TaskSet, task, between

from utilss.httpsample import signature


class UserBehavior(TaskSet):

    def on_start(self):
        self.key = '9009003902675441808-106703001'

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
        self.client.get(url, params=params, name='notRead')

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
        # 我的关注列表日志
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




class WebsiteUser(HttpUser):
    host = "https://api.rela.me"
    tasks = [UserBehavior]
    wait_time = between(5, 10)

