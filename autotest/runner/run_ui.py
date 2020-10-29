#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools
import inspect
import pytest
import allure
import time
import sys
from string import Template
import json


import autotest.utils.globaval as gl
from .runapp import APPRun
# from .runweb import WebRun
import uiautomator2 as u2
# from selenium import webdriver


# def autocase(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         def run(case_list):
#             # var 中加载了 各个 页面的 page
#             log.info("==========================开始运行用例部分==========================")
#             run_case_(gl.get_value("page_object"), case_list, gl.get_value("conf_file").get("runtype"))
#             log.info("==========================用例部分运行结束==========================")
#         func_args = inspect.getcallargs(func, *args, **kwargs)
#         case_info = func_args.get("test_list")
#         # var_ = func_args.get("var_main")
#         run(case_info)
#         # , var_
#     return wrapper


def run_case_(objpage, casesteps, run_type, case_name,fixture=False):
    gl.get_value("log").getlog().info("==========================开始执行用例==========================")

    if run_type.lower() == "app":
        run_ = APPRun(gl.get_value("d"))
    elif run_type.lower() == "web":
        run_ = WebRun(gl.get_value("d"))

    gl.get_value("log").getlog().info("加载页面对象数据:{}".format(json.dumps(objpage, ensure_ascii=False, indent=4)))
    gl.get_value("log").getlog().info("加载用例数据:{}".format(json.dumps(casesteps, ensure_ascii=False, indent=4)))

    for case_ in casesteps:
        # print("开始执行用例: ", case_)
        page_name = list(case_.keys())[0]
        if page_name not in objpage:
            gl.get_value("log").getlog().error("页面对象未定义:{}".format(page_name))
            assert False
        else:
            # 获取用例对应的 执行步骤
            case_step = objpage.get(page_name)
            #  重组页面步骤 组装成 exec 可执行的 string （valid= true, false == keyword 是否定义 ）
            print(11111111111111111111, case_)
            if case_.get(page_name):
                case_params = dict(case_.get(page_name).get("data", {}),
                                   **case_.get(page_name).get("assert", {}))
                gl.get_value("log").getlog().info("参数与断言组合值:{}".format(json.dumps(case_params, ensure_ascii=False, indent=4)))
            else:
                case_params = {}
            # 连接相关信息
            # case_params["conn_info"] = {"conn_obj": var.connect_obj}

            if not fixture:
                with pytest.allure.step(page_name):
                    for step in case_step:
                        step = Template(step).safe_substitute(case_params)
                        kw = step.split("|")[0].strip()
                        selector_value = step.split("|")[1].strip()
                        desc = step.split("|")[-1].strip()
                        gl.get_value("log").getlog().info("重新处理后的步骤:{}".format(step))
                        with pytest.allure.step(step.split("|")[-1].strip()):
                            run_.run_step(kw, selector_value, desc)
            else:
                for step in case_step:
                    step = Template(step).safe_substitute(case_params)
                    kw = step.split("|")[0].strip()
                    selector_value = step.split("|")[1].strip()
                    desc = step.split("|")[-1].strip()
                    gl.get_value("log").getlog().info("重新处理后的步骤:{}".format(step))
                    run_.run_step(kw, selector_value, desc)        

    gl.get_value("log").getlog().info("==========================用例执行结束==========================")


# 执行前置stup, teardown
def fixtur_executor_ui(steps,is_setup=True):
    run_type = gl.get_value("runconf").get("type")
    if is_setup:
        gl.get_value("log").getlog().info("--------- 执行 {} 端项目--------- ".format(run_type))
        gl.get_value("log").getlog().info("==========开始执行setup=============")
        start_time = time.time()
        if run_type == "app":
            # 连接设备 
            # 此判断是 为了多设备并行运行时，使用脚本传入 设备号
            if not gl.get_value("device"):
                gl.get_value("log").getlog().error("=========未设置设备号=======")
                sys.exit()
            try:
                u = u2.connect(addr=gl.get_value("device"))
                d = u.session(gl.get_value("runconf").get("devices").get("apkname"))
                gl.set_value("d", d)
                start_done = time.time()
            except Exception as e:
                gl.get_value("log").getlog().error("初始化链接失败启动失败, 失败原因：".format(str(e)))
                d.close()
            # 解锁屏幕 并启动 uiautomator服务
            conn_time = time.time()
            # d.healthcheck()

        elif run_type == "web":
            if gl.get_value("address").lower() == "chrome":
                conn_time = time.time()
                try:
                    d = webdriver.Chrome(gl.get_value("conf_file").get("devices").
                                         get("device").get(gl.get_value("address").lower()))
                    start_done = time.time()
                except Exception as e:
                    gl.get_value("log").getlog().error("初始化启动失败, 失败原因：".format(str(e)))
                    d.quit()
        gl.get_value("log").getlog().info("记录启动过程中耗时, 链接设备耗时：{} , 启动耗时： {}".format(str(start_done-start_time),
                                                          str(conn_time-start_done)))
        # 接收前置步骤

        if steps:

            run_case_(gl.get_value("pageobject"), steps, run_type, "", True)

        gl.get_value("log").getlog().info("========== setup执行结束 =============")
    else:


        gl.get_value("log").getlog().info("========== 开始执行teardown =============")
        if run_type == "app":
            if steps:
                run_case_(gl.get_value("pageobject"), steps, run_type, "", True)
            gl.get_value("d").close()
        else:
            gl.get_value("d").quit()
        gl.get_value("log").getlog().info("========== teardown执行结束 =============")

