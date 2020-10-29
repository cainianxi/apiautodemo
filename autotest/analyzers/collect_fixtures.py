#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
收集fixture 用例信息
"""
import string
from os.path import join
from copy import deepcopy
from collections import ChainMap

from autotest.samples.yaml_sampler import YamlSampler
from autotest.utils import ObjDict, merge_dict, merge_body
from autotest.utils import variable_replace, function_replace_nest, object_access, analyzer_expression
from autotest.analyzers.run_config import get_file_content, get_db_conn, get_upload_file

setup_keys = teardown_keys = ("sql", "api", "function")  # setup teardown keys
sql_keys = ("query", "conn", "output", "index")
api_keys = ("url", "method", "headers", "params", "data", "files", "output", "r")
assert_keys = ("json-sql", "json-json", "sql-json", "log", "function")
OP_PATH_DEFAULT = "$.*"


def collect_session_fixture(dic, config, run_var):
    if not dic:
        return ChainMap(run_var), [], []

    session_var = collect_var(dic.get("var"), None, config)
    if session_var:
        session_var = dict(session_var)

    session_var = merge_dict(session_var, run_var)
    session_setup = collect_setup(dic.get("setup"), session_var, config)
    session_teardown = collect_teardown(dic.get("teardown"), session_var, config)

    return session_var, session_setup, session_teardown


def collect_case_fixture(dic, session_var, config):
    if not dic:
        return session_var, {}

    case_var = collect_var(dic.pop("var", None), session_var, config)

    fixture_dic = dict()
    for key, value in dic.items():
        if value:
            case_setup = collect_setup(value.get("setup"), case_var, config)
            case_teardown = collect_teardown(value.get("teardown"), case_var, config)
            fixture_dic[key] = ObjDict({"setup": case_setup, "teardown": case_teardown})

    return case_var, fixture_dic


# 返回字典
def collect_assert(assert_element, config):
    if not assert_element:
        return {}
    if not isinstance(assert_element, dict):
        raise Exception("assert 元素配置错误:\n{}".format(assert_element))

    assert_obj = dict.fromkeys(assert_keys, None)

    for key in set(assert_element) & set(assert_keys):
        assert_obj[key] = assert_element[key]

    if assert_obj["json-sql"]:
        assert_obj["json-sql"] = collect_json_sql(assert_obj["json-sql"], config)
    if assert_obj["sql-json"]:
        assert_obj["sql-json"] = collect_json_sql(assert_obj["sql-json"], config)
    if assert_obj["json-json"]:
        r = assert_obj["json-json"]
        if not isinstance(r, list):
            r = [r]
        assert_obj["json-json"] = r
    # if assert_obj["log"]:
    #     assert_obj["log"] = collect_log_keywords(assert_obj["log"], config)

    if assert_obj["function"]:
        assert_obj["function"] = collect_function(assert_obj["function"])

    return assert_obj


def collect_json_sql(element, config):  # 返回列表
    json_sql_list = []

    if isinstance(element, str):
        json_sql_list.append(ObjDict({"json": {"obj": None, "path": OP_PATH_DEFAULT},
                                      "sql": collect_sql(element, config)[0]}))
    elif isinstance(element, dict):
        json_sql = {"json": {"obj": None, "path": OP_PATH_DEFAULT}, "sql": None}
        _json = element.get("json")
        _sql = element.get("sql")

        if _json:
            if isinstance(_json, str):
                json_sql["json"]["path"] = _json
            else:
                json_sql["json"]["obj"] = _json

        if _sql:
            r_list = collect_sql(_sql, config)
            if r_list:
                json_sql["sql"] = r_list[0]
            json_sql_list.append(ObjDict(json_sql))
    elif isinstance(element, list):
        for v in element:
            _v = collect_json_sql(v, config)
            _v and json_sql_list.extend(_v)
    else:
        raise Exception("json-sql/sql-json 元素配置错误:\n{}".format(element))

    return json_sql_list


def collect_var(var_element, chain_map, config):  # 返回ChainMap
    if not var_element:
        return chain_map
    if not isinstance(var_element, dict):
        raise Exception("var 元素配置错误:\n{}".format(var_element))

    var = analyzer_expression(var_element, chain_map, config.keywords_mod)
    if chain_map:
        return chain_map.new_child(var)
    else:
        return ChainMap(var)


# def collect_log_keywords(log_element, config):
#     log_list = []
#     log_obj = dict.fromkeys(log_keys, None)
#
#     if isinstance(log_element, (str, int, float, bool)):
#         log_obj["text"] = [str(log_element)]
#         log_obj["conn"] = config.default_log_conn
#         log_list.append(ObjDict(log_obj))
#     elif isinstance(log_element, dict):
#         if not log_element.get("text") or not isinstance(log_element.get("text"), (str, list)):
#             # return sql_list
#             raise Exception("log text元素配置错误:\n{}".format(log_element.get("text")))
#
#         for key in set(log_element) & set(log_keys):
#             log_obj[key] = log_element[key]
#
#         if not isinstance(log_obj["text"], list):
#             log_obj["text"] = [log_obj["text"]]
#
#         _conn = get_log_conn(config.confile, log_obj["conn"])
#         isinstance(_conn, dict) and _conn.pop("default", None)
#         log_obj["conn"] = _conn
#
#         log_list.append(ObjDict(log_obj))
#     else:
#         raise Exception("log 元素配置错误:\n{}".format(log_element))
#
#     return log_list


# 返回字典列表，只对query元素进行变量和对象访问
def collect_sql(sql_element, config):
    sql_list = []
    sql_obj = dict.fromkeys(sql_keys, None)
    sql_obj["index"] = 0

    if isinstance(sql_element, str):
        if sql_element.endswith(".sql"):
            sql_element = get_file_content(sql_element, config.datapath)
        sql_obj["query"] = sql_element
        sql_obj["conn"] = config.default_db_conn
        sql_list.append(ObjDict(sql_obj))
    elif isinstance(sql_element, dict):
        if not sql_element.get("query") or not isinstance(sql_element.get("query"), str):
            # return sql_list
            raise Exception("sql query元素配置错误:\n{}".format(sql_element.get("query")))

        for key in set(sql_element) & set(sql_keys):
            sql_obj[key] = sql_element[key]

        sql = sql_obj["query"]
        if sql.endswith(".sql"):
            sql = get_file_content(sql_obj["query"], config.datapath)
        sql_obj["query"] = sql

        if not sql_obj["index"]:
            sql_obj["index"] = 0
        _conn = get_db_conn(config.confile, sql_obj["conn"])
        isinstance(_conn, dict) and _conn.pop("default", None)
        sql_obj["conn"] = _conn

        sql_list.append(ObjDict(sql_obj))
    elif isinstance(sql_element, list):
        for v in sql_element:
            _sql = collect_sql(v, config)
            _sql and sql_list.extend(_sql)
    else:
        raise Exception("sql 元素配置错误:\n{}".format(sql_element))

    return sql_list


# 返回列表，元素为mod.func(p1, p2)形式的字符串
def collect_function(function_element):
    func_list = []

    if isinstance(function_element, str):
        if function_element.startswith("$(") and function_element.endswith(")"):
            func_list.append(function_element[2:-1])
        else:
            func_list.append(function_element)
    elif isinstance(function_element, list):
        for func in function_element:
            if isinstance(func, str):
                if func.startswith("$(") and func.endswith(")"):
                    func_list.append(func[2:-1])
                else:
                    func_list.append(func)
    else:
        raise Exception("function元素配置错误:\n{}".format(function_element))

    return [func if func.endswith(")") else func + "()" for func in func_list]


# 返回字典列表
def collect_setup(setup_element, chain_map, config):
    setup_list = []
    setup_obj = dict.fromkeys(setup_keys, None)

    if isinstance(setup_element, dict):
        for key in set(setup_element) & set(setup_keys):
            setup_obj[key] = setup_element[key]

        if setup_obj["sql"]:
            setup_list.append(ObjDict({"sql": collect_sql(variable_replace(setup_obj["sql"], chain_map), config)}))
        if setup_obj["api"]:
            setup_list.append(ObjDict({"api": collect_api(setup_obj["api"], None, config, chain_map)}))
        if setup_obj["function"]:
            setup_list.append(ObjDict({"function": collect_function(setup_obj["function"])}))
    elif isinstance(setup_element, list):
        for v in setup_element:
            if isinstance(v, dict) and len(v) == 1:
                key, value = v.popitem()
                if value:
                    if key == "sql":
                        setup_list.append(ObjDict({"sql": collect_sql(variable_replace(value, chain_map), config)}))
                    elif key == "api":
                        setup_list.append(ObjDict({"api": collect_api(value, None, config, chain_map)}))
                    if key == "function":
                        setup_list.append(ObjDict({"function": collect_function(value)}))
            else:
                raise Exception("setup/teardown 元素配置错误:\n{}".format(setup_element))
    elif setup_element:
        raise Exception("setup/teardown 元素配置错误:\n{}".format(setup_element))

    return setup_list


def collect_teardown(teardown_element, chain_map, config):
    return collect_setup(teardown_element, chain_map, config)


# 返回字典列表
def collect_api(api_element, _api_name, config, chain_map):
    api_list = []
    if isinstance(api_element, (str, dict)):
        api = _collect_api(api_element, _api_name, config, chain_map)
        api and api_list.append(api)
    elif isinstance(api_element, list):
        for v in api_element:
            api = _collect_api(v, _api_name, config, chain_map)
            api and api_list.append(api)
    else:
        raise Exception("api 元素配置错误:\n{}".format(api_element))

    return api_list


def _collect_api(api_element, _api_name, config, chain_map):
    special_data = {}
    comm_key = set()

    if isinstance(api_element, str):
        _name = _api_name or api_element
        _api = config.api_config.get(_name)
        if _api:  # 过滤api.yaml文件中不存在的接口
            return {api_element: _api}
        else:
            raise Exception("api 元素配置错误:\n{}".format(api_element))
    elif isinstance(api_element, dict):
        for name, info in api_element.items():
            _name = _api_name or name
            _api = config.api_config.get(_name)
            _var = None
            if info and info.get("var"):
                _var = info.get("var")

            info = info or _api  # 没有任何数据，直接取配置数据执行
            if _api and info:
                api_obj = dict.fromkeys(api_keys, None)
                comm_key = set(api_obj) & set(info)
                for key in comm_key:
                    special_data[key] = info[key]
                    if key == "output":
                        api_obj[key] = info[key]
                    elif isinstance(_api[key], dict):
                        pjson = info[key]

                        if isinstance(pjson, str):
                            pjson = variable_replace(pjson, chain_map)

                            if isinstance(pjson, str) and pjson.endswith(".json"):
                                json_file = join(config.datapath, pjson)
                                pjson = YamlSampler.read_json(json_file)

                        if _api[key]:
                            if isinstance(pjson, dict):
                                ao = deepcopy(_api[key])
                                api_obj[key] = merge_body(ao, pjson)
                            elif pjson:
                                raise Exception("api 元素配置错误:\n{}".format(api_element))
                            else:
                                api_obj[key] = _api[key]
                        else:
                            api_obj[key] = pjson
                    else:
                        api_obj[key] = info[key]
                for key in api_keys:
                    if not api_obj[key]:
                        api_obj[key] = _api.get(key, None)

                api_obj["spec"] = special_data

                if _var:
                    api_obj["var"] = _var

                if api_obj["files"]:
                    api_obj["files"] = get_upload_file(api_obj["files"], config.datapath)

                return ObjDict({name: api_obj})


def self_ref_replace(obj, key, chain_map, keywords_mod, r):  # data和params部分支持嵌套函数
    if not isinstance(obj, dict):
        return function_replace_nest(object_access(variable_replace(obj, chain_map)), keywords_mod, r)

    # 字典内部值引用自身可以有两种引用方式
    # 例如 {"data": {"a":1, "b":2, "c": "${self}", "d": "${data}"}}解析为
    # {"data": {"a":1, "b":2, "c": {"a":1, "b":2}, "d": {"a":1, "b":2"}}
    ref_id = ["self", key]
    replace_k_v = {}

    for k, v in obj.items():
        if isinstance(v, str):
            has_ref = False
            for ref in ref_id:
                if v.find("$" + ref) >= 0 or v.find("${" + ref + "}") >= 0:
                    has_ref = True
                    break
            if not has_ref:
                continue
            replace_k_v[k] = v
        elif isinstance(v, dict):
            obj[k] = self_ref_replace(v, k, chain_map, keywords_mod, r)
        else:
            continue

    if not replace_k_v:
        return function_replace_nest(object_access(variable_replace(obj, chain_map)), keywords_mod, r)

    for k in replace_k_v:
        obj.pop(k)

    obj = function_replace_nest(object_access(variable_replace(obj, chain_map)), keywords_mod, r)

    for k, v in replace_k_v.items():
        for ref in ref_id:
            v = string.Template(v).safe_substitute({ref: obj})
        v = function_replace_nest(object_access(variable_replace(v, chain_map)), keywords_mod, r)

        obj[k] = v

    return obj


if __name__ == "__main__":
    cm = ChainMap({
        'pri_key': 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIkF7VZPVNfrSiMHOFQQMz+Ajp90vLU3wZNARGBqzcdFSYYiMMuP6+GLeFA2KxDjYzDlRQXlU12Bl/dEdnfxCo+zhxTtZNVkv/W/6U3R1dVwJDkDp887Q78fofaFmRE6E5dCV+iVVRvEzm4W+4ft+HL3fPG3wqT9qkJqJRNqfuQfAgMBAAECgYBRdFuNdmV6Yd3ViuI6XtMISfT+55eSps2FKqw7IOKpNhAqE8MsD6dqkc146WqahIIfu/tXMOdo67QaAvHmBT2AIkuCRq3LnQD2shfb4axtzyF1J2Qzj5mzLxrTdUNEeFUP4i51MyjQ1ld85NSDTXv7smi5F5alhlstZwqMdUlNgQJBAOTxuI0qjUdvXyvcRWoL1bZX2t1Dh/Jo2BB6nw5OgMfJ8It9kToRC/kiO3QVNyVNdB9DjPRSKlmR457DoS2gXsECQQCZN05kPEpeo9abGsKE7EHLKerZdLuKS0gKwfKAd1jxmPfuLAePiBW3DPleLWgNRHXSxik8Dv2lr/VhgJU+HNrfAkEAik1TdUOtUOgAkBhifmtj0OFFv8BZ0aBwVZQdnaDivs5I15slLfS6TOfXDor6Yzhk27YM4lL4bl9pJ7F6HnvwgQJAOKTWyX30rLp7q8of4g6KYHb1yUE72GvujXOYmOAGtQMtnhMPFIRmKs+UHbpBvq3xtWPneLm+EpRT7qEgC9+VFwJAEvlKD2m/Qu+tCctCiFQkYqKwjWRtTshRADLKmQIDWy4FvoKK+s7U3KvoT1Nyz0DumIbhYO5vAp3gsFbPrOvDbA=='},
        ChainMap({
            'pri_key': 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIkF7VZPVNfrSiMHOFQQMz+Ajp90vLU3wZNARGBqzcdFSYYiMMuP6+GLeFA2KxDjYzDlRQXlU12Bl/dEdnfxCo+zhxTtZNVkv/W/6U3R1dVwJDkDp887Q78fofaFmRE6E5dCV+iVVRvEzm4W+4ft+HL3fPG3wqT9qkJqJRNqfuQfAgMBAAECgYBRdFuNdmV6Yd3ViuI6XtMISfT+55eSps2FKqw7IOKpNhAqE8MsD6dqkc146WqahIIfu/tXMOdo67QaAvHmBT2AIkuCRq3LnQD2shfb4axtzyF1J2Qzj5mzLxrTdUNEeFUP4i51MyjQ1ld85NSDTXv7smi5F5alhlstZwqMdUlNgQJBAOTxuI0qjUdvXyvcRWoL1bZX2t1Dh/Jo2BB6nw5OgMfJ8It9kToRC/kiO3QVNyVNdB9DjPRSKlmR457DoS2gXsECQQCZN05kPEpeo9abGsKE7EHLKerZdLuKS0gKwfKAd1jxmPfuLAePiBW3DPleLWgNRHXSxik8Dv2lr/VhgJU+HNrfAkEAik1TdUOtUOgAkBhifmtj0OFFv8BZ0aBwVZQdnaDivs5I15slLfS6TOfXDor6Yzhk27YM4lL4bl9pJ7F6HnvwgQJAOKTWyX30rLp7q8of4g6KYHb1yUE72GvujXOYmOAGtQMtnhMPFIRmKs+UHbpBvq3xtWPneLm+EpRT7qEgC9+VFwJAEvlKD2m/Qu+tCctCiFQkYqKwjWRtTshRADLKmQIDWy4FvoKK+s7U3KvoT1Nyz0DumIbhYO5vAp3gsFbPrOvDbA=='}),
        {
            'pri_key': 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIkF7VZPVNfrSiMHOFQQMz+Ajp90vLU3wZNARGBqzcdFSYYiMMuP6+GLeFA2KxDjYzDlRQXlU12Bl/dEdnfxCo+zhxTtZNVkv/W/6U3R1dVwJDkDp887Q78fofaFmRE6E5dCV+iVVRvEzm4W+4ft+HL3fPG3wqT9qkJqJRNqfuQfAgMBAAECgYBRdFuNdmV6Yd3ViuI6XtMISfT+55eSps2FKqw7IOKpNhAqE8MsD6dqkc146WqahIIfu/tXMOdo67QaAvHmBT2AIkuCRq3LnQD2shfb4axtzyF1J2Qzj5mzLxrTdUNEeFUP4i51MyjQ1ld85NSDTXv7smi5F5alhlstZwqMdUlNgQJBAOTxuI0qjUdvXyvcRWoL1bZX2t1Dh/Jo2BB6nw5OgMfJ8It9kToRC/kiO3QVNyVNdB9DjPRSKlmR457DoS2gXsECQQCZN05kPEpeo9abGsKE7EHLKerZdLuKS0gKwfKAd1jxmPfuLAePiBW3DPleLWgNRHXSxik8Dv2lr/VhgJU+HNrfAkEAik1TdUOtUOgAkBhifmtj0OFFv8BZ0aBwVZQdnaDivs5I15slLfS6TOfXDor6Yzhk27YM4lL4bl9pJ7F6HnvwgQJAOKTWyX30rLp7q8of4g6KYHb1yUE72GvujXOYmOAGtQMtnhMPFIRmKs+UHbpBvq3xtWPneLm+EpRT7qEgC9+VFwJAEvlKD2m/Qu+tCctCiFQkYqKwjWRtTshRADLKmQIDWy4FvoKK+s7U3KvoT1Nyz0DumIbhYO5vAp3gsFbPrOvDbA=='})

    js = {
        'outUserId': '$(installment_random())',
        'platform': 'beibei',
        'randomNum': '$(installment_random())',
        'idCardNo': '622424199301021624',
        'mobile': '18817938005',
        'cityCode': '310000',
        'addrDetail': '上海徐汇区龙漕路',
        'contactsInfo': '{}',
        'expandInfo': '',
        'notifyUrl': '',
        'sign': "$(installment_sign('${pri_key}',${data},['outUserId','platform','randomNum']))"
    }

    r = self_ref_replace(js, "data", cm, None, False)
    print(r)