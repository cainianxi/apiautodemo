"""
author :rain
Date : 2020/10/15
Description :
"""
import json

from utilss.httpsample import signature, HttpSampler

hs = HttpSampler()

pro_url = 'https://api.rela.me'
test_url = 'https://test-api.rela.me'
pro_key = '8544002289011963093-106851715'
test_key = '1601426712855886906-106851715'

base_params = {'ua': 'theL/5.3.6_26 (iPhone 6s; iOS 13.50; zh-Hans; Wifi)', 'lat': '31.170315', 'lng': '121.430451',
               'language': 'zh-Hans', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306', 'apptype': 'universal'}


def test_checkusername(name):
    url = test_url + '/v1/auth/check-username'
    params = {'key': test_key, 'language': 'zh_Hans', 'userName': name}
    params['signature'] = signature(params)
    print(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_live_friends():
    # 正在直播的朋友
    url = test_url + '/v1/live/living-friends'
    params = {'key': test_key, 'language': 'zh_Hans'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_meta():
    # 排行榜信息
    url = pro_url + '/v1/live/meta'
    params = {'key': test_key, 'language': 'zh_Hans'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_type_list():
    # 直播类型列表
    url = pro_url + '/v1/live/type-list'
    params = {'key': test_key, 'language': 'zh_Hans'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_live_rank():
    # 榜单简要描述
    url = test_url + '/v1/live/rank'
    params = {'key': test_key, 'language': 'zh_Hans'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def arpre_releaselist():
    # ar礼物简要描述
    url = test_url + '/v1/live/gift/arPreReleaselist'
    params = {'key': test_key, 'language': 'zh_Hans'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def get_user_level():
    # 用户等级
    url = test_url + '/v1/live/user-level'
    params = {'key': test_key, 'language': 'zh_Hans'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def get_user_perm():
    # 直播权限
    url = test_url + '/v1/live/perm'
    params = {'key': test_key, 'language': 'zh_Hans'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


# def get_gift_detail():
#     # 礼物详情
#     # url = test_url + '/v1/live/gift/detail'
#     url =  'https://api.rela.me/v1/live/gift/detail'
#     params = {'key': '730995130632743129-106851715', 'language': 'zh_Hans'}
#     params['signature'] = signature(params)
#     r = hs.get(url, params=params)
#     # print(r)
#     print(json.dumps(r.json(), ensure_ascii=False))


def get_user_flowwer():
    # 我的关注
    url = test_url + '/interface/stay/appUserFollower!getNewFollowUser.do'
    params = {'key': test_key, 'language': 'zh_Hans', 'curPage': '1', 'pageSize': '20', 'userid': '104205815'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def rebind():
    # 重新绑定
    url = test_url + '/v1/auth/rebind'
    params = {'key': test_key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451', 'type': 'cell'
        , 'cell': '19999999120', 'code': '5678', 'zone': "+99"}
    params['signature'] = signature(params)
    r = hs.post(url, data=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def rebind_new():
    # 新重新绑定
    url = test_url + '/v1/auth/rebind-newformat'
    params = {'key': test_key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451', 'type': 'cell'
        , 'cell': '19999999120', 'code': '5678', 'zone': "+99"}
    params['signature'] = signature(params)
    r = hs.post(url, data=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def get_new_infoforfriend():
    # 我的速配资料
    url = test_url + '/v3/interface/stay/newUserInfoForFriend'
    params = {'key': test_key, 'language': 'zh_Hans', 'userId': '104205815', 'lat': '31.170315', 'lng': '121.430451'
        , 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def get_follow_secertly():
    # 悄悄关注列表
    url = test_url + '/interface/stay/appUserFollowerSecretly'
    params = {'key': test_key, 'language': 'zh_Hans', 'userid': '104205815', 'lat': '31.170315', 'lng': '121.430451'
        , 'curPage': '1', 'pageSize': '20', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def get_secertly_followdo():
    # 悄悄关注
    url = test_url + '/interface/stay/appUserFollower!secretlyFollow.do'
    params = {'key': test_key, 'language': 'zh_Hans', 'receivedId': '107277639', 'lat': '31.170315', 'lng': '121.430451'
        , 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
    params['signature'] = signature(params)
    r = hs.post(url, data=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def get_secertly_follow():
    # v3悄悄关注
    url = pro_url + '/v3/interface/stay/secretlyFollow'
    params = {'key': test_key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451'
        , 'receivedId': '107277639', 'actionType': '0'
        , 'curPage': '1', 'pageSize': '20', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
    params['signature'] = signature(params)
    r = hs.post(url, data=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))
    # todo


def get_myinfo_friend():
    # 我的信息
    url = pro_url + '/v3/interface/stay/myInfoForFriend'
    params = {'key': test_key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451'
        , 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def get_follow_user():
    # 我的关注列表
    url = pro_url + '/interface/stay/appUserFollower!getNewFollowUser.do'
    params = {'key': test_key, 'language': 'zh_Hans', 'userid': '104205815', 'lat': '31.170315', 'lng': '121.430451'
        , 'curPage': '1', 'pageSize': '20', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def get_follow_anchors():
    # 我的信息
    url = test_url + '/v2/users/follow/anchors'
    params = {'key': test_key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451'
        , 'cursor': '1', 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def fans_remove():
    # 移除粉丝
    url = test_url + '/v2/users/fans/remove'
    params = {'key': test_key, 'language': 'zh_Hans', 'lat': '31.170315', 'lng': '121.430451'
        , 'mobileOS': 'iOS 13.5.1', 'clientVersion': '50306', 'userId': '101136006'}
    params['signature'] = signature(params)
    r = hs.post(url, data=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


if __name__ == '__main__':
    # test_checkusername('name')
    # test_checkcell()
    # test_live_friends()
    # test_live_rank()
    # arpre_releaselist()
    # get_user_level()
    # get_user_perm()
    # get_gift_detail()
    # get_user_flowwer()
    # get_new_infoforfriend()
    get_follow_secertly()
    # get_secertly_follow()
    # get_myinfo_friend()
    # get_follow_user()
    get_follow_anchors()
    fans_remove()
    # test_meta()
    # test_type_list()
    # rebind()
    # rebind_new()
    get_secertly_followdo()
