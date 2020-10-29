#!/usr/local/python3

import json

from autotest.utils.obj_dict import ObjDict

import requests
from requests_toolbelt import MultipartEncoder

requests.packages.urllib3.disable_warnings()


class HttpSampler:
    def __init__(self):
        self._req_obj = requests.Session()
        self._def_args = {'timeout': 30, 'verify': False}
        self.req = None
        self.resp = None  # 返回

    def get(self, url, params=None, headers=None, data=None, **kwargs):
        if data and headers and headers.get("Content-Type").lower().find("application/json") >= 0:
            data = json.dumps(data)
        self.resp = self._req_obj.get(url, params=params, headers=headers, data=data, **dict(self._def_args, **kwargs))
        self.req = self.resp.request
        return self

    def post(self, url, data=None, headers=None, params=None, files=None, **kwargs):
        datax, headers = self._multipart_data(data, headers, files)
        self.resp = self._req_obj.post(url, data=datax, headers=headers, params=params, files=files,
                                       **dict(self._def_args, **kwargs))
        self.req = self.resp.request
        return self

    def put(self):
        pass

    def delete(self):
        pass

    def status_code(self):
        return self.resp.status_code

    def text(self):
        return self.resp.text

    def json(self):
        try:
            return ObjDict(self.resp.json())
        except Exception:
            return self.req.text()

    def url(self):
        return self.resp.url

    def headers(self):
        return ObjDict(self.resp.headers)

    @staticmethod
    def _multipart_data(data, headers, files):
        datax = data
        if files:
            try:
                if headers:
                    headers.pop("Content-Type", None)
            except:
                pass
        elif headers and headers.get("Content-Type").lower().find("multipart/form-data") >= 0:
            m = MultipartEncoder(files=data)
            headers["Content-Type"] = m.content_type
            datax = m
        elif headers and headers.get("Content-Type").lower().find("application/json") >=0 :
            datax= json.dumps(data)

        return datax, headers


# if __name__ == "__main__":
#     url1 = "http://39.100.178.112:7420/rela/api/chatroom/im/callback"
#     url = "http://39.100.178.112:7420/rela/api/chatroom/im/room/create"
#     # url = "http://39.100.178.112:7420/rela/api/chatroom/im/room/add_member"
#     sampler = HttpSampler()
#     headers = {
#         "Content-Type": "application/json"
#     }
#     #
#     # url2 = "http://test-api.rela.me/v1/live/detail-info?apptype=universal&client=iPhone7%2C1&clientVersion=50100&deviceId=sm_201907301123154b1e35a8001c063df96668cf83c63a170145b1a2332a1c56&from_class=RfSUniversalRouterRootViewController&id=88888106789926&key=MXw9rc62OtJJkjMLL4UZSNPtEoPOPD8n-106789945&language=zh-Hans-CN&lat=0&lng=0&mobileOS=IOS%2012.400000&view_class=TLWatchLiveListViewController"
#     # r = sampler.get(url2)
#     # token = r.json().get("data").get("livechat").get("token")
#     # token = ''
#     param = {"room_id": "88888106789926", "user_id": "106789926"}
    
    # 回调加入
    
    # join_params = {"CallbackCommand": "Group.CallbackBeforeSendMsg", "SdkAppid": "1400252440",
    #           "ClientIP": "210.13.93.225", "OptPlatform": "Android", "contenttype": "json"}
    #
    # ext = '{\"code\":\"init\",\"body\":\"{\\\"token\\\":\\\"' + token + '\\\", \\\"type\\\":\\\"msg\\\", \\\"userId\\\":\\\"106789945\\\" , \\\"channel\\\":\\\"88888106789931\\\", \\\"nickName\\\":\\\"test180\\\"}\"}'
    # join_data = {"GroupId": "88888106789926",
    #         "From_Account": "106789945",
    #         "Random": 8912478, "MsgBody": [{"MsgType": "TIMCustomElem", "MsgContent": {
    #         "Ext": ext}}]}
    
    # join_data = {"GroupId": "88888106789926",
    #         "From_Account": "106789864",
    #         "Random": 8912478, "MsgBody": [{"MsgType": "TIMCustomElem", "MsgContent": {
    #         "Ext": "{\"code\":\"init\",\"body\":\"{\\\"channel\\\":\\\"88888106789926\\\", \\\"token\\\":\\\"msg\\\", "
    #                "\\\"userId\\\":\\\"106789864\\\", \\\"nickName\\\":\\\"test177\\\"}\"}"}}]}
    
    
    # 回调消息
    # params = {"CallbackCommand": "Group.CallbackBeforeSendMsg", "SdkAppid": "1400252440",
    #           "ClientIP": "210.13.93.225", "OptPlatform": "Android", "contenttype": "json"}
    # data = {"GroupId": "88888106789926",
    #         "From_Account": "106789945",
    #         "Random": 8912478, "MsgBody": [{"MsgType": "TIMCustomElem", "MsgContent": {
    #         "Ext": "{\"code\":\"send\",\"body\":\"{\\\"content\\\":\\\"test11111111111\\\", \\\"type\\\":\\\"msg\\\"}\"}"}}]}
    
    # combo 连接次数
    
    # data = {"GroupId": "88888106789926",
    #         "From_Account": "106759850",
    #         "Random": 8912478, "MsgBody": [{"MsgType": "TIMCustomElem", "MsgContent": {
    #         "Ext": "{\"code\":\"sendgift\",\"body\":\"{\\\"hostUserId\\\":\\\"106789926\\\", \\\"combo\\\":1, \\\"id\\\": 1}\"}"}}]}

    #
    # tx = "https://console.tim.qq.com/v4/group_open_http_svc/add_group_member?sdkappid=1400247437&identifier=106759850&usersig={0}&random=99999999&contenttype=json".format(main(106759850))
    #
    # data1 = {
    #     "Identifier": "106759850",
    #     "Nick": "test110",
    #     "FaceUrl": "http://www.qq.com"
    # }
    
    # {"id": 1, "combo": 1, "hostUserId": "106789926", "reqId": 2}
    
    # 2 静默

    #  调用detail
    

    
    
    
    #  加入 腾讯
    
    #
    # r = sampler.post(url, params=param, headers=headers)

    # print(r.json())
    #
    # # 加入热拉
    # r = sampler.post(url1, data=join_data, params=join_params, headers=headers)
    #
    # print(r.json())
    #
    
    # r1 = sampler.post(url1, data=data, params=params, headers=headers)
    # print(r1.json())