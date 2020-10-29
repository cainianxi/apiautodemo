#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
解析api 配置信息
"""

from copy import deepcopy
from urllib.parse import urljoin
from os.path import join

from autotest.utils.obj_dict import ObjDict
from autotest.samples import YamlSampler

base_keys = ("url", "method", "headers")
api_keys = ("url", "method", "headers", "data", "params", "output", "r")


def _merge_dict(key, target, src):
    if isinstance(target, dict) and isinstance(src, dict):
        return dict(target, **src)
    elif isinstance(target, dict):
        if src is not None:
            raise Exception("{}: 必须为(dict, None),实际为{}".format(key, src))
        else:
            return target
    elif isinstance(src, dict):
        if target is not None:
            raise Exception("{}: 必须为(dict, None),实际为{}".format(key, target))
        else:
            return src
    elif target is None and src is None:
        return None
    else:
        raise Exception("{}: 必须为(dict, None)".format(key))


def api_config(config, datapath):  # 返回字典
    base = config.base  # api 基础配置
    apis = config.api  # api 配置信息
    if not isinstance(apis, dict) or not isinstance(base, dict):
        raise Exception("api 元素配置异常")
    for k in base:
        if k not in base_keys:
            base.pop(k)

    for name, info in apis.items():
        api_obj = dict.fromkeys(api_keys, None)  # 组成一个dict, 已api_keys中的值为key {"": None}
        if isinstance(info, str):
            api_obj["url"] = urljoin(base.get("url"), info)
            api_obj["method"] = base.get("method")
            api_obj["headers"] = deepcopy(base.get("headers"))
            apis[name] = api_obj
        elif isinstance(info, dict):
            api_obj["url"] = base.get("url")
            api_obj["method"] = base.get("method")
            api_obj["headers"] = base.get("headers")
            for key, value in info.items():
                if key == "url":
                    info[key] = urljoin(base.get(key), value)
                elif key == "method" and not value:
                    info[key] = base[key]
                elif key == "headers":
                    info[key] = _merge_dict(key, base.get(key), value)
                elif key in ("data", "params"):
                    if isinstance(value, str) and value.endswith(".json"):
                        json_file = join(datapath, value)
                        info[key] = YamlSampler.read_json(json_file)
                    else:
                        info[key] = _merge_dict(key, None, value)

            for key in set(info) & set(api_obj):
                api_obj[key] = info[key]

            apis[name] = api_obj
    for name, info in apis.items():
        if not isinstance(info, dict):
            raise Exception("{}: 必须为字典,实际为{}".format(name, type(info)))
        if not isinstance(info["url"], str):
            raise Exception("请输入正确的url")
        m = info["method"]
        if m:
            if str(m).upper() not in ("GET", "POST", "PUT", "DELETE"):
                raise Exception("不支持的HTTP请求方法：{}".format(m))
            else:
                info["method"] = m.upper()
        else:
            raise Exception("请提供HTTP请求方法")

    return ObjDict(apis)

