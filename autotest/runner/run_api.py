#!/usr/local/python3

"""
api 运行器
"""
from collections import ChainMap
import json
from os.path import splitext, basename
from operator import itemgetter

import pytest
import allure

from autotest.samples import HttpSampler, MysqlSampler
from autotest.utils import execute_function, json_dumps, variable_replace, object_access, str_eval, \
    analyzer_expression, function_replace
from autotest.assertions import diff
from autotest.utils import ObjDict
from autotest.analyzers import self_ref_replace, collect_var, Config
import autotest.utils.globaval as gl

api_sampler = HttpSampler()

file_type = [x for x in dir(allure.attachment_type) if not x.startswith("__")]
self_ref_keys = ("params", "data")


def case_run(caseName, api_name, api_value):
    with pytest.allure.step("Set up"):
        gl.get_value("log").getlog().info("开始执行用例--{} -- 前置条件setup：{}".format(caseName,
                                                                              json.dumps(api_value.setup,
                                                                                         ensure_ascii=False, indent=4)))
        var = fixture_executor(api_value.setup, gl.get_value(api_name),
                               api_value.keywords_mod)
        gl.set_value(api_name, var)
        gl.get_value("log").getlog().info("此时全局变量：{}".format(gl.get_value("__api__var")))

    gl.get_value("log").getlog().info("开始执行用例---{}---".format(caseName))
    gl.get_value("log").getlog().info("此时测参数---{}---".format(gl.get_value(api_name)))
    case_vale = api_value.api.get(caseName)
    gl.get_value("log").getlog().info("用例信息：{}".format(json.dumps(case_vale, ensure_ascii=False, indent=4)))
    result, var, _value = api_run(case_vale, gl.get_value(api_name), api_value.keywords_mod)
    gl.get_value("log").getlog().info("请求的返回体为：{}".format(json.dumps(result.json(), ensure_ascii=False, indent=4)))
    gl.set_value(api_name, var)
    # code = result.status_code()
    # assert code == 200, "HTTP响应码为: {}".format(code)
    msg = assert_run(api_value.assert_, var, result.json(), api_value.keywords_mod)
    gl.get_value("log").getlog().info("断言结果：{}".format("\n".join(msg)))
    
    with pytest.allure.step("Tear down"):
        gl.get_value("log").getlog().info("开始执行用例--{} -- 后置teardown：{}".format(caseName,
                                                                               json.dumps(api_value.setup,
                                                                                          ensure_ascii=False, indent=4)))
        ret_var = fixture_executor(api_value.teardown, gl.get_value("__apivar__"), api_value.keywords_mod)
    
    if msg:
        allure.attach("\n".join(msg), "断言结果")
        assert msg == [], "断言失败"
    return ret_var


def write_file(files):
    if not files:
        return

    def get_name_type(file_obj):
        _name = basename(file_obj.name)
        _ext = splitext(_name)[1].lstrip(".").upper()
        _file_type = None

        if _ext in file_type:
            _file_type = eval("allure.attachment_type." + _ext)
        return _name, _file_type

    def attach_file(obj, _name, _clazz):
        data = obj.seek(0) or obj.read()
        if _clazz:
            allure.attach(data, _name, attachment_type=_clazz, extension=_clazz.extension)
        else:
            allure.attach(data, _name, extension=_clazz.extension)

    if isinstance(files, dict):
        for key, value in files.items():
            if isinstance(value, (list, tuple)):
                value = value[1]
            name, _type = get_name_type(value)
            attach_file(value, name, _type)
    elif isinstance(files, (list, tuple)):
        for item in files:
            if isinstance(item, (list, tuple)):
                if isinstance(item[1], (list, tuple)):
                    item[1] = item[1][1]
                name, _type = get_name_type(item[1])
                attach_file(item[1], name, _type)


def assert_run(assert_obj, chain_map, result, keywords_mod):
    f = assert_obj.pop("function", None)
    if f:
        for v in f:
            func_run(object_access(variable_replace(v, chain_map)), keywords_mod)

    msg = []
    assert_obj = analyzer_expression(assert_obj, chain_map, keywords_mod)

    for key, value in assert_obj.items():
        if value:
            if key == "json-sql":
                for i, assert_ in enumerate(value):
                    obj = assert_.json.obj or result
                    real = ObjDict.accessor(obj, assert_.json.path)
                    if not real:  # 用path作为obj进行二次尝试
                        real = assert_.json.path
                    expect, _ = sql_run(assert_.sql, chain_map, is_assert=True)
                    # 处理index
                    index = assert_.sql.index
                    if index and isinstance(expect, list):
                        try:
                            expect = expect[index]
                        except Exception:
                            expect = None
                    # end
                    real, expect = sort_list_of_dict(real, expect)
                    _msg = diff(real, expect, str2number=True, part=True, smart=True)
                    if _msg:
                        _msg = "\n".join(["实际值:", json_dumps(real), "期望值:", json_dumps(expect), "断言结果:", _msg, "\n"])
                        if i == 0:
                            _msg = "JSON-SQL:\n" + _msg
                        msg.append(_msg)
            elif key == "sql-json":
                for i, assert_ in enumerate(value):
                    obj = assert_.json.obj or result
                    expect = ObjDict.accessor(obj, assert_.json.path)
                    if not expect:  # 用path作为obj进行二次尝试
                        expect = assert_.json.path
                    real, _ = sql_run(assert_.sql, chain_map, is_assert=True)
                    # 处理index
                    index = assert_.sql.index
                    if index and isinstance(real, list):
                        try:
                            real = real[index]
                        except Exception:
                            real = None
                    # end
                    real, expect = sort_list_of_dict(real, expect)
                    _msg = diff(real, expect, str2number=True, part=True, smart=True)
                    if _msg:
                        _msg = "\n".join(["实际值:", json_dumps(real), "期望值:", json_dumps(expect), "断言结果:", _msg, "\n"])
                        if i == 0:
                            _msg = "SQL-JSON:\n" + _msg
                        msg.append(_msg)
            elif key == "json-json":
                for i, assert_ in enumerate(value):
                    _msg = diff(result, assert_, str2number=True, part=True, smart=False)
                    if _msg:
                        _msg = "\n".join(["实际值:", json_dumps(result), "期望值:", json_dumps(assert_), "断言结果:", _msg, "\n"])
                        if i == 0:
                            _msg = "JSON-JSON:\n" + _msg
                        msg.append(_msg)
            # elif key == "log":
            #     for i, assert_ in enumerate(value):
            #         _conn = assert_.conn
            #         log_obj = TomcatLogMonitor(_conn.host, _conn.port, _conn.user, _conn.password)
            #         if assert_.key:
            #             func_list = collect_function(assert_.key, chain_map)
            #             for v in func_list:
            #                 func_run(object_access(variable_replace(v, chain_map), keywords_mod))
            #             _msg = log_obj.has_keywords(_conn.files, assert_.text, seconds=1)
            #         else:
            #             _msg = log_obj.has_keywords(_conn.files, assert_.text)
            #
            #         if _msg:
            #             _msg = "\n".join(["日志文件:", _conn.files, "未找到关键字:", json_dumps(_msg), "\n"])
            #             if i == 0:
            #                 _msg = "Log:\n" + _msg
            #             msg.append(_msg)
            #         log_obj.close()

    return msg


def sort_list_of_dict(real, expect):
    if isinstance(real, list) and isinstance(expect, list):
        if real and isinstance(real[0], dict) and expect and isinstance(expect[0], dict):
            try:
                _intersection = set(real[0]) & set(expect[0])
                real = sorted(real, key=itemgetter(*_intersection))
                expect = sorted(expect, key=itemgetter(*_intersection))
            except Exception:
                print("json/sql 结果排序异常")

    return real, expect


def fixture_executor(fixture_obj, chain_map, keywords_mod, type='api'):
    if not fixture_obj:
        return chain_map

    _var = chain_map
    
    for item in fixture_obj:
        
        for key, value in item.items():
            if key == "sql":
                with pytest.allure.step("SQL"):
                    for i, v in enumerate(value, start=1):
                        with pytest.allure.step("语句_" + str(i)):
                            _, _var = sql_run(v, _var, keywords_mod=keywords_mod)
            if key == "api":
                # with pytest.allure.step("API"):
                for i, v in enumerate(value, start=1):
                    for _, _v in v.items():
                        #with pytest.allure.step("API_" + str(i)):
                            _v.pop("spec", None)
                            _var = collect_var(_v.pop("var", None), _var,
                                                   Config(_api_config=None, _keywords_mod=keywords_mod))
                            _, _var, _ = api_run(_v, _var, keywords_mod, 0)
            elif key == "function":
                with pytest.allure.step("Function"):
                    for i, v in enumerate(value, start=1):
                        with pytest.allure.step("Function_" + str(i)):
                            func_run(object_access(variable_replace(v, _var)), keywords_mod)
    return _var


def sql_run(sql_obj, chain_map, keywords_mod=None, is_assert=False):
    if sql_obj.conn:
        query = object_access(variable_replace(sql_obj.query, chain_map))
        if keywords_mod:
            query = function_replace(query, keywords_mod)
        _query = query.split(";;")
        _query = [x.strip() for x in _query if x.strip()]

        query2 = []

        for q in _query:
            if q.lower()[:6] in ("select", "insert", "update", "delete") or q.lower()[:4] == "call":
                query2.append([q])
            else:
                if isinstance(query2[-1], list):
                    query2[-1].append(str_eval(q))
                else:
                    raise Exception("SQL 参数化语句不正确")

        result = None
        for item in query2:
            allure.attach(json_dumps(sql_obj.conn), "SQL 连接", allure.attachment_type.TEXT)
            allure.attach(item[0], "SQL 语句", allure.attachment_type.TEXT)

            sql_sample = MysqlSampler(sql_obj.conn)
            if len(item) == 1:
                result = sql_sample.execute(item[0], is_assert)
            else:
                allure.attach(item[1], "SQL 语句参数", allure.attachment_type.TEXT)
                result = sql_sample.execute_many(item[0], item[1])

            allure.attach(json_dumps(result), "SQL 执行结果", allure.attachment_type.TEXT)

        if sql_obj.output:  # 应该放到for语句之外，保存最后一条语句执行结果
            if chain_map:
                chain_map = chain_map.new_child({sql_obj.output: result})
            else:
                chain_map = ChainMap({sql_obj.output: result})

        return result, chain_map
    else:
        raise Exception("Database Connection 沒有配置")


def _get_spec(api_obj, spec):
    r = {}

    for k, v in spec.items():
        if isinstance(v, dict):
            r[k] = _get_spec(api_obj[k], v)
        else:
            r[k] = api_obj[k]

    return r


def api_run(api_obj, chain_map, keywords_mod, type=1):
    r = bool(api_obj["r"])
    for k in self_ref_keys:
        api_obj[k] = self_ref_replace(api_obj[k], k, chain_map, keywords_mod, r)

    api_obj.url = variable_replace(api_obj.url, chain_map)
    api_obj["headers"] = analyzer_expression(api_obj["headers"], chain_map, keywords_mod)

    spec = api_obj.get("spec", {})
    _sks = list(spec)
    for k in _sks:
        if k not in self_ref_keys or spec[k] is None:
            spec.pop(k)

    spec = _get_spec(api_obj, spec)

    if api_obj.method.upper() == "POST":
        result = api_sampler.post(api_obj.url, api_obj.data, api_obj.headers, api_obj.params, api_obj.files)
    elif api_obj.method.upper() == "PUT":
        result = api_sampler.put(api_obj.url, api_obj.data, api_obj.headers, api_obj.params, api_obj.files)
    elif api_obj.method.upper() == "DELETE":
        result = api_sampler.delete(api_obj.url, api_obj.data, api_obj.headers, api_obj.params, api_obj.files)
    elif api_obj.method.upper() == "GET":
        result = api_sampler.get(api_obj.url, api_obj.params, api_obj.headers, api_obj.data)
    else:
        raise Exception("不支持的请求方法")

    output = api_obj.output

    if output:
        if isinstance(output, str):
            chain_map = chain_map.new_child({output: result.json()}) if chain_map else ChainMap({output: result.json()})
        elif isinstance(output, dict):
            for k, v in output.items():
                if k.lower() == "headers":
                    chain_map = chain_map.new_child({v: result.headers()}) if chain_map else ChainMap(
                        {v: result.headers()})
                else:
                    chain_map = chain_map.new_child({v: result.json()}) if chain_map else ChainMap(
                        {v: result.json()})
        else:
            raise Exception("output 配置错误")

    if chain_map:
        chain_map = chain_map.new_child(
            {"context_params": api_obj.params, "context_data": api_obj.data})
    else:
        chain_map = ChainMap({"context_params": api_obj.params, "context_data": api_obj.data})
    ###
    if type:
        allure.attach(result.url(), "请求URL", allure.attachment_type.TEXT)
        allure.attach(api_obj.method, "请求方法", allure.attachment_type.TEXT)
        api_obj.headers and allure.attach(json_dumps(api_obj.headers), "请求头")
        api_obj.params and allure.attach(json_dumps(api_obj.params), "请求参数")
        api_obj.data and allure.attach(json_dumps(api_obj.data), "请求体")

    if spec:
        allure.attach(json_dumps(spec), "测试专属数据")

    write_file(api_obj.files)

    if not isinstance(result.json(), str):
        if type:
            allure.attach(json_dumps(result.json()), "响应结果")
    else:
        if type:
            allure.attach(result.json(), "响应结果")
    ###

    return result, chain_map, api_obj


def func_run(func_obj, keywords_mod):
    allure.attach(func_obj, "function 执行", allure.attachment_type.TEXT)
    return execute_function(func_obj, keywords_mod)