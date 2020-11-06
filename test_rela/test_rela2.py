"""
author :rain
Date : 2020/10/16
Description :
"""
import json

from locust import task

from utilss.httpsample import signature, HttpSampler

hs = HttpSampler()

pro_url = 'https://api.rela.me'
test_url = 'https://test-api.rela.me'
pro_key = '9572070930129342419-104205815'
test_key = '1601426712855886906-106851715'
base_params = {'ua': 'theL/5.3.6_26 (iPhone 6s; iOS 13.50; zh-Hans; Wifi)', 'lat': '31.170315', 'lng': '121.430451',
               'language': 'zh-Hans', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306', 'apptype': 'universal'}


def test_notRead():
    url = pro_url + '/friend/stay/moments/notRead'
    params = {'key': pro_key, 'language': 'zh_Hans', 'cursor': 0
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_suggest():
    url = pro_url + '/v3/friend/stay/topic/suggest'
    params = {'key': pro_key, 'language': 'zh_Hans', 'topicName': 16, 'curPage': '1'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_comment_list():
    url = pro_url + '/v3/themes/comment/list'
    params = {'key': pro_key, 'language': 'zh_Hans', 'id': 160256284743510068, 'sortType': 1
        , 'cursor': 0, 'limit': 20
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_themes_detail():
    url = pro_url + '/v3/themes/detail'
    params = {'key': pro_key, 'language': 'zh_Hans', 'id': 160256284743510068
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_themes_recommend_check():
    url = pro_url + '/v3/themes/recommend/check'
    params = {'key': pro_key, 'language': 'zh_Hans', 'themeId': 160256284743510068
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_live_detail_info():
    url = pro_url + '/v1/live/detail-info'
    params = {'key': pro_key, 'language': 'zh_Hans', 'id': 88888103459922
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'view_class': 'TLWatchLiveListViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_live_gift_list():
    url = pro_url + '/v1/live/gift/list'
    params = {'key': pro_key, 'language': 'zh_Hans', 'appId': 'com.rela'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
              'view_class': 'TLWatchLiveListViewController'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_is_first_charge():
    url = pro_url + '/v1/gold/is-first-charge'
    params = {'key': pro_key, 'language': 'zh_Hans'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
              'view_class': 'TLWatchLiveListViewController'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_activityInfo():
    # TODO
    url = 'https://web-api.rela.me/live/activityInfo'
    params = {'key': pro_key, 'language': 'zh_Hans'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
              'view_class': 'TLWatchLiveListViewController'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_resources():
    url = pro_url + '/v3/interface/resources'
    params = {'key': pro_key, 'language': 'zh_Hans', 'location': 'initAdv', 'resourceType': 2
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
              'view_class': 'TLWatchLiveListViewController'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_myInfoForFriend():
    url = pro_url + '/v3/interface/stay/myInfoForFriend'
    params = {'key': pro_key, 'language': 'zh_Hans'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1',
              'view_class': 'TLWatchLiveListViewController'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_topicHead():
    url = pro_url + '/v3/friend/stay/moments/topicHead'
    params = {'key': pro_key, 'language': 'zh_Hans', 'topicId': 366
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_roamWorld_config():
    url = pro_url + '/v3/roamWorld/config'
    params = {'key': pro_key, 'language': 'zh_Hans', 'topicId': 366
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


# def test_activityConfigurable():
#     url = 'https://web-api.rela.me/activityConfigurable/list'
#     params = {'key': pro_key, 'id': 83, 'topicId': 366, 'userId': 104205815}
#     params['signature'] = signature(params)
#     r = hs.post(url, data=params)
#     print(json.dumps(r.json(), ensure_ascii=False))

def test_newUserInfoForFriend():
    url = pro_url + '/v3/interface/stay/newUserInfoForFriend'
    params = {'key': pro_key, 'language': 'zh_Hans', 'userId': 104205815
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_vip_detail():
    url = pro_url + '/v2/users/vip/detail'
    params = {'key': pro_key, 'language': 'zh_Hans', 'userId': 104205815
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


@task(1)
def test_live_rank(self):
    # 榜单简要描述  100
    url = '/v1/live/rank'
    params = {'key': self.key, 'language': 'zh_Hans'}
    params['signature'] = signature(params)
    self.client.get(url, params=params)

def test_commentReply():
    url = pro_url + '/v3/moments/commentReply/list'
    params = {'key': pro_key, 'language': 'zh_Hans', 'id': 160228730570310003, 'cursor': 0, 'limit': 50
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_appUserView():
    url = pro_url + '/interface/stay/appUserView!cheackView.do'
    params = {'key': pro_key, 'language': 'zh_Hans', 'curPage': 1
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_gold_list():
    url = pro_url + '/v1/gold/list'
    params = {'key': pro_key, 'language': 'zh_Hans'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_getMainAdvert():
    url = pro_url + '/v3/interface/stay/getMainAdvert'
    params = {'key': pro_key, 'language': 'zh_Hans'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_category_config():
    url = pro_url + '/v3/themes/category/config'
    params = {'key': pro_key, 'language': 'zh_Hans'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_adv_list():
    url = pro_url + '/v3/interface/adv/list'
    params = {'key': pro_key, 'language': 'zh_Hans', 'advType': 'init'
        , 'lat': '31.170315', 'lng': '121.430451', 'mobileOS': 'iOS 13.5.1'
        , 'clientVersion': '50306', 'apptype': 'universal', 'from_class': 'RfSUniversalRouterRootViewController'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    print(json.dumps(r.json(), ensure_ascii=False))


if __name__ == '__main__':
    test_adv_list()
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
