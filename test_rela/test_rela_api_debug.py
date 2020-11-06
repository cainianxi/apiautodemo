"""
author :rain
Date : 2020/09/07
Description :
"""
import json

from utilss.httpsample import HttpSampler, signature

hs = HttpSampler()


def test_my_guanzhuliebiao():
    url = 'https://api.rela.me/v3/friend/stay/moments/listWithMusicMultiImg'
    params = {'userId': 143958, 'pageSize': 20, 'curPage': 1, 'mainType': 'moments',
              'key': '12559707953913601549-143958', 'lat': 31.170336,
              'lng': 121.430498, 'language': 'zh-Hans', 'mobileOS': 'iOS 13.5.1',
              'deviceId': 'sm_20190411160642ade026b965810f1d2fc433ac1dfd0d8a0135b82a64d134bf'
        , 'apptype': 'universal', 'clientVersion': '50304'}
    params['signature'] = signature(params)

    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def testmyimage():
    url = 'https://api.rela.me/interface/stay/appUserImage!myImagesList.do'
    params = {'userId': 103504121, 'pageSize': 20, 'curPage': 1, 'from_class': 'RfSUniversalRouterRootViewController',
              'view_class': 'TLProfilesViewController',
              'key': 'cm421m7qSje1VstOrgNnFiZS2dYjo3c2-103504121', 'lat': 31.170336,
              'lng': 121.430498, 'language': 'zh-Hans', 'mobileOS': 'iOS 13.5.1',
              'deviceId': 'sm_20190411160642ade026b965810f1d2fc433ac1dfd0d8a0135b82a64d134bf'
        , 'apptype': 'universal', 'clientVersion': '50304', 'client': 'iPhone8,1'}
    params['signature'] = signature(params)

    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_notread():
    url = 'https://ali-pre-api.rela.me/friend/stay/moments/notRead'
    params = {'apptype': 'universal', 'client': 'iPhone8,1', 'clientVersion': '50304', 'cursor': 0,
              'view_class': 'RfSUniversalRouterRootViewController',
              'key': '5E5GJPbt8Fw8ToONDHZLlmCJ7onySVxA-101682997', 'lat': 31.170336,
              'lng': 121.430498, 'mobileOS': 'iOS 13.5.1',
              'deviceId': 'sm_20190411160642ade026b965810f1d2fc433ac1dfd0d8a0135b82a64d134bf', 'language': 'zh-Hans'}
    # params['signature'] = signature(params)

    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_nearby():
    url = 'https://api.rela.me/v3/interface/stay/appUser!nearbySimpleList.do'
    params = {'pageSize': '40', 'curPage': '1', 'search': '0', 'secondLng': '113.284645', 'secondLat': '23.120339',
              'key': '12169994561673862520-104338341', 'recommendType': 'ai',
              'lat': 31.170336, 'lng': 121.430498, 'mobileOS': 'iOS 13.5.1',
              # 'supStar': None, 'newRegist': None, 'her_role_name': None, 'age': None, 'affection': '', 'active': '', 'vip': '',
              # 'have_photo': '','horoscope': '',
              'deviceId': 'sm_20190411160642ade026b965810f1d2fc433ac1dfd0d8a0135b82a64d134bf', 'language': 'zh-Hans',
              'apptype': 'universal', 'clientVersion': '50304'}
    params['signature'] = signature(params)

    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


def test_album():
    '''修改资料相册图片'''
    url = 'https://api.rela.me/interface/stay/appUserImage!myImagesList.do'
    params = {'curPage': '1', 'pageSize': '20',
              'key': '6877502430713972921-103504121', 'from_class': 'RfSUniversalRouterRootViewController',
              'lat': 31.170336, 'lng': 121.430498, 'mobileOS': 'iOS 13.5.1', 'client': 'iPhone8,1',
              'deviceId': 'sm_20190411160642ade026b965810f1d2fc433ac1dfd0d8a0135b82a64d134bf', 'language': 'zh-Hans',
              'apptype': 'universal', 'clientVersion': '50304'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))

    #获取用户直播等级
def test_user_level():
    url = 'http://ali-pre-api.rela.me/v1/live/user-level'
    params = {'key': '16096635682580962356-104564661', 'debug': '0', 'lat': 31.170336, 'lng': 121.430498,
              'mobileOS': 'Android 8.1.0', 'clientVersion': '50306', 'language': 'zh_Hans',
              'deviceId': 'sm_20200825143722f3ef21646235522c2a9adef65a75040201e5cc200498bd39'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))


#
#     apptype	universal
# cell	19999999836
# client	iPhone8,1
# clientVersion	50306
# deviceId	sm_20190411160642ade026b965810f1d2fc433ac1dfd0d8a0135b82a64d134bf
# from_class	TLSystemSetViewController
# key	8544002289011963093-106851715
# language	zh-Hans
# lat	31.170305
# lng	121.430460
# mobileOS	IOS 13.500000
# view_class	TLPhoneViewController
# zone	+86
def test_checkcell():
    url = 'https://test-api.rela.me/v1/auth/check-cell'
    params = {'key': '8544002289011963093-106851715', 'language': 'zh_Hans', 'zone': "+86", 'cell': '19999999836'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))



def test_old_themes_hottheme():
    #老版本获取热门话题列表接口
    url = 'https://api.rela.me/v3/themes/hotTheme/viewList'
    params = {'key': '5642750266735215454-105177953', 'language': 'zh_Hans', 'zone': "+86", 'cell': '19999999836'}
    params['signature'] = signature(params)
    r = hs.get(url, params=params)
    # print(r)
    print(json.dumps(r.json(), ensure_ascii=False))




if __name__ == '__main__':
    # test_myguanzhuliebiao()
    # testmyimage()
    # test_notread()
    # test_nearby()
    # test_album()
    test_user_level()
    # test_checkcell()
    # test_old_themes_hottheme()