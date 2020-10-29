#!/usr/local/python3

import json
import base64
import hashlib
from requests_toolbelt import MultipartEncoder
from utils.obj_dict import ObjDict, str_eval

import requests

#
requests.packages.urllib3.disable_warnings()
NewSalt = {"get": "MAaFS5Zc6ZIEapnmhurNyLLFwf3xWm", "post": "879f30c4b1641142c6192acc23cfb733"}


def signature(params, NewSalt="MAaFS5Zc6ZIEapnmhurNyLLFwf3xWm"):
    sign_params = params if isinstance(params, dict) else str_eval(params)

    # sign_keys = sorted(sign_params.keys())
    sort_str_list = []
    for key, values in sign_params.items():
        if isinstance(values, list):
            for i in range(len(values)):
                sort_str_list.append(key + "=" + str(values[i]))
        else:
            sort_str_list.append(key + "=" + str(values))
    sign_str_list = sorted(sort_str_list)
    sign_str_new = '&'.join(sign_str_list)

    m = hashlib.md5((sign_str_new + NewSalt).encode(encoding="utf-8"))
    return m.hexdigest()


def signature_fj(params, method):
    sign_params = params if isinstance(params, dict) else str_eval(params)
    # sign_keys = sorted(sign_params.keys())
    sort_str_list = []
    if method.lower() == "get":
        for key, values in sign_params.items():
            if isinstance(values, list):
                for i in range(len(values)):
                    sort_str_list.append(key + "=" + str(values[i]))
            else:
                sort_str_list.append(key + "=" + str(values))
        sign_str_list = sorted(sort_str_list)
        sign_str_new = '&'.join(sign_str_list)
        m = hashlib.md5((sign_str_new + NewSalt.get("get")).encode(encoding="utf-8"))
    else:
        m = hashlib.md5((json.dumps(params) + NewSalt.get("post")).encode(encoding="utf-8"))
    return m.hexdigest()


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
        elif headers and headers.get("Content-Type").lower().find("application/json") >= 0:
            datax = json.dumps(data)

        return datax, headers

#
# if __name__ == "__main__":
#     # url_pro = "http://pre-api.fanjiao.co/walkman/api/user/verify_code"
#     headers = {
#         "Content-Type": "application/json"
#     }
#     # params = {
#     #     "zone": "99",
#     #     "phone": "19999999835"
#     # }
#     # params['signature'] = signature(params, "get")
#     sampler = HttpSampler()
#     # r = sampler.get(url_pro, params=params, headers=headers)
#     # pro_json = r.json()
#     # url_pro1 = "http://pre-api.fanjiao.co/walkman/api/user/login"
#     # headers1 = {
#     #     "Content-Type": "application/json"
#     # }
#     # data = {
#     #     "zone": "99",
#     #     "phone": "19999999175",
#     #     "verify_code": "0000",
#     #     "device_type": 1,
#     # }
#     #
#     # headers1['Signature'] = signature_fj(data, "post")
#     # print(data)
#     # print(headers1)
#     # r1 = sampler.post(url_pro1, data=data, headers=headers1)
#     # pro_json1 = r1.json()
#     # print(pro_json1)
#     url_pro3 = "http://pre-api.fanjiao.co/walkman/api/comment/publish"
# #
#     params3 = {
#     "audio_id": 2343,
#     "content": "ceshi",
#     "type": 1
#     }
#     headers["token"] ="J0JpZnVRaLRkk9uHcGtGtRXfQtfdeReC-1000072"
#     headers['Signature'] = signature_fj(params3, "POST")
#     r2 = sampler.post(url_pro3, data=params3, headers=headers)
#     pro_json2 = r2.json()
#     print(pro_json2)