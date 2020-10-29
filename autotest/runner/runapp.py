#!/usr/bin/python
# -*- coding: utf-8 -*-
import uiautomator2 as u2
import autotest.utils.globaval as gl
from autotest.runner import ui2base
from operator import methodcaller

import pytest
import allure


class APPRun:
    def __init__(self, driver):
        self.var = None
        self.imgfile = gl.get_value("runconf").imgpath
        self.ub = ui2base.Ui2Base(driver, self.imgfile)
        self.kwd = {"单击": "one_click",
                    "双击": "double_click",
                    "长按": "long_click",
                    "键入": "send_keys",
                    "获取Toast": "get_toast",
                    "获取文本": "get_text",
                    "断言Toast": "assert_toast",
                    "断言存在": "assert_text",
                    "观察": "watcher_click",
                    "滚动": "scroll",
                    "滚动到": "scroll_to",
                    "等待": "wait"
                    }
        self.kw_selector = {"单击", "双击", "长按", "键入", "获取文本"}

    def run_step(self, kw, selector_value, desc):
        # selector 与 参数值 之间 通过 @@ 区分

        gl.get_value("log").getlog().info("开始执行步骤：{} \n 使用关键字：{} \n 选择器以及参数：{}".format(desc, kw, selector_value))
        # with pytest.allure.step(desc):
        if kw not in self.kwd:
            gl.get_value("log").getlog().error("{} -- 关键字未定义, 请检查".format(kw))
            assert False, "{} -- 关键字未定义, 请检查".format(kw)
        if "@@" in selector_value:
            selector__ = selector_value.split("@@")[0].strip()
            value = selector_value.split("@@")[1].strip()
        else:
            value = selector_value
            selector__ = selector_value
        if kw in self.kw_selector:
            gl.get_value("log").getlog().info("关键字{} 的参数中包含选择器, 有选择器的关键字 {}".format(kw, str(self.kw_selector)))
            params_ = list(getattr(self.ub, self.kwd[kw]).__code__.co_varnames)
            params_count = len(params_[1:])
            gl.get_value("log").getlog().info("关键字：{}, 需要传入参数：{}， 传入个数： {}".format(kw, str(params_), str(params_count)))
            try:
                if params_count > 1:
                    #allure.attach("执行步骤--{0}".format(step), "执行步骤")
                    methodcaller(self.kwd[kw], selector__, value)(self.ub)
                    gl.get_value("log").getlog().info("执行步骤：{} 成功".format(desc))
                else:
                    #allure.attach("执行步骤--{0}".format(step), "执行步骤")
                    methodcaller(self.kwd[kw], selector__)(self.ub)
                    gl.get_value("log").getlog().info("执行步骤：{} 成功".format(desc))
            except Exception as E:
                gl.get_value("log").getlog().error("执行步骤{}失败， 失败原因: {}".format(desc, str(E)))
                assert False, "执行步骤{}失败， 失败原因: {}".format(desc, str(E))
        else:
            gl.get_value("log").getlog().info("关键字{} 的参数中不包含选择器, 有选择器的关键字 {}".format(kw, str(self.kw_selector)))
            try:
                #allure.attach("执行步骤--{0}".format(step), "执行步骤")
                methodcaller(self.kwd[kw], selector__)(self.ub)  # ===>self.ub.one_click(selector__)
                gl.get_value("log").getlog().info("执行步骤：{} 成功".format(desc))
            except Exception as E:
                # allure.attach("", "失败截图", allure.attachment_type.JPG)
                gl.get_value("log").getlog().error("执行步骤{}失败， 失败原因: {}".format(desc, str(E)))
                assert False, "执行步骤{}失败， 失败原因: {}".format(desc, str(E))


# aa = [
#     "单击 | 取消 | 跳过激活码",
#     "单击 | com.nl.android.ecgviewer:id/rb_cloud_case_list | 切换至云病例",
#     "键入 | 身份证号 @@ 123456 | 输入身份证号"
# ]
# d = u2.connect("127.0.0.1:21533")
# d.app_start("com.nl.android.ecgviewer")
# ar = APPRun(d)
# for i in aa:
#     ar.run_setup(i)
# import uiautomator2 as u2
# ub.click("取消")
# ub.click("com.nl.android.ecgviewer:id/rb_cloud_case_list")
# ub.send_keys("身份证号", "123456789")
# ub.click("获 取")
# ub.get_toast()
# b = time.time()