#!/usr/bin/python
# -*- coding: utf-8 -*-
from string import Template


class UITestKeyword:
    def __init__(self):

        # self.step = step

        # d.implicitly_wait(10.0)
        # 支持的定位方式
        self.locate_method = ["position", "resourceId", "xpath", "className",
                              "description", "text"]
        self.akwds = ['单击', '双击', '键入', '断言存在', "清除文本", "断言Toast"]

        self.key_template = {
            "单击_xpath": 'd.xpath("$source").click()',
            "单击_position": 'd.click$source',
            "单击": 'd($source).click()',
            "双击_xpath": 'd.xpath("$source").double_click()',
            "双击_position": 'd.double_click$source',
            "双击": 'd($source).double_click()',
            "键入_xpath": 'd.xpath("$source").set_text("${info}")',
            "键入": 'd($source).set_text("$info")',
            "断言存在": 'assert_exit($excepts)',
            "清除文本": 'd($source).clear_text()',
            "断言Toast": 'assert_toast($excepts)'
        }

        # self.akwds = [
        #     {'index': '单击', 'template': 'd($locatemode="$source").click_exists(timeout=2)'},
        #     {'index': '双击', 'template': 'd($locatemode="$source").double_click(timeout=1)'},
        #     {'index': '长按', 'template': 'd($locatemode="$source").long_click(timeout=1)'},
        #     {'index': '等待', 'template': 'd($locatemode="$source").wait(timeout=$info)'},
        #     {'index': '截图', 'template': 'd.screenshot("$image")'},
        #     {'index': '键入', 'template': 'd($locatemode="$source").set_text("$info")'},
        #     {'index': '滑动', 'template': 'd($locatemode="$source").swipe("$info", steps=${info1})'},
        #     {'index': '关闭APP', 'template': 'd.app_stop("$apk")'},
        #     {'index': '拖拽', 'template': 'd($locatemode="$source").drag_to($info, $info, duration=0.5)'},
        #     {'index': '检验文本', 'template': 'assert_text("$locatemode", "$source", "$info")'},
        # ]

    def get_templat(self, step):
        kw = step.split("|")[0].strip()  # 关键字
        desc = step.split("|")[-1].strip()  # 描述
        loacl_info = step.split("|")[1].strip()  # 定位方式
        # 判断关键字是否存在， 存在开始 判断是否支持定位方式 否则 返回
        step_new = {}
        if kw in self.akwds:
            step_new["info"] = self.convertor_templat(kw, loacl_info)
            step_new["desc"] = desc
            return step_new
        else:
            return step_new

    def convertor_templat(self, kw, local_):
        # 先拆分参数部分
        params_ = {}
        loacl_info = local_
        # 定位 与 参数 已 @@ 区分
        if '@@' in local_:
            params = local_.split("@@")[1].strip()
            loacl_info = local_.split("@@")[0].strip()
            user_par_info = params.split(',')
            i = 0
            for user_par_ in user_par_info:
                i += 1
                if i == 1:
                    params_["info"] = user_par_.strip()
                else:
                    params_["info" + str(i)] = user_par_.strip()
        # 判断是否使用多定位方式定位 ,多定位方式 不能 根据位置，或者 xpath
        if "&&" in loacl_info:
            str_list_ = []
            locals_ = loacl_info.split("@@")  # 多个定位方式
            for local_ in locals_:
                locatemode = local_.split("=", 1)[0].strip()
                if locatemode in ["position", "xpath"]:
                    return
                source = local_.split("=", 1)[1].strip()
                str_list_.append(locatemode + "='"+source+"'")
            params_["source"] = ','.join(str_list_)
            return Template(self.key_template.get(kw)).safe_substitute(params_)
        elif "->" in loacl_info:  # 父子定位方式 ,暂不支持
            pass

        else:
            if kw in ["断言存在", "断言Toast"]:
                return Template(self.key_template.get(kw)).safe_substitute({"excepts": loacl_info})
            locatemode = loacl_info.split("=", 1)[0].strip()
            source = loacl_info.split("=", 1)[1].strip()
            if locatemode not in ('xpath', "position"):
                params_["source"] = locatemode + "='"+source+"'"
            else:
                params_["source"] = source
            if '_'.join([kw, locatemode]) in self.key_template:
                return Template(self.key_template.get('_'.join([kw, locatemode]))).safe_substitute(params_)
            return Template(self.key_template.get(kw)).safe_substitute(params_)



# s ='断言存在 | $except | aECGAcquisitor'
# ss = AndroidKeyword().get_templat(s)
# print(ss)

