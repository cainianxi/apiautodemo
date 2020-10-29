#!/user/local/python

"""
pytest 收集测试用例 以及配置的相关信息
"""

import os
import json
import pytest
import allure
from importlib import import_module

from autotest.samples import YamlSampler
from autotest.analyzers import api_config, Api, Config, collect_session_fixture, collect_case_fixture, collect_var, Scenario, TestInfo

from autotest.runner.run_api import fixture_executor, case_run
from autotest.runner.run_ui import run_case_, fixtur_executor_ui
from autotest.utils import ObjDict
from autotest.utils.Log import Log
import autotest.utils.globaval as gl


"""
ui 自动化: 采取的就是 模块运行方式，
app 默认启动 放置在 全局中 进行启动
如果fixture中配置模块的前置条件 运行前置 条件
未配置: 则不运行 前置条件 
运行完成后 停止app

"""


# 初始化 全局变量 gl
api_conf_filename_key = ("api", "fixture.api", "fixture.session", )
app_conf_filename_key = ("runconf", "fixture")

gl._init()


try:
    keywords_mod = import_module("autotest.keywords")
except Exception:
    keywords_mod = None
    print("项目keywords文件不存在或有语法错误")


def pytest_addoption(parser):
    group = parser.getgroup("collect")
    group.addoption(
        "--path",
        default=os.getcwd(),
        dest="path",
        help="api配置信息"
    )

    group.addoption(
        "--runtype",
        default=os.getcwd(),
        dest="runtype",
        help="运行类型"
    )

    group.addoption(
        "--casenames",
        dest="casenames",
        help="运行指定的用例"
    )

    group.addoption("--cmdopt", action="store", default="",
        help="my option: ip, devices")


def pytest_configure(config):
    #  获取 命令行参数 进行 基础数据的收集
    gl.set_value("runtype", config.getoption("runtype").lower())
    print( config.getoption("cmdopt").lower())
    if gl.get_value("runtype") == "api":
        print("api 相关配置信息 ==> {}".format(config.getoption("path")))
        for key in ("api", "fixture.api", "fixture.session", "runconf"):
            _setGlobValue(config.getoption("path"), key)
    
        # api 配置信息
        datafile = gl.get_value("runconf").data
        runconfile = os.path.join(config.getoption("path"), "runconf.yaml")
        api_config_ = api_config(gl.get_value("api"), datafile)
        os.path.join(config.getoption("path"), "runconf")
        # 获取 db 配置信息
        run_conf = YamlSampler.read_yaml(runconfile)
        if run_conf.db:
            for key, value in run_conf.db.items():
                if value.get("default") is True:
                    default_db_conn = value
                    default_db_conn["pool_name"] = key
                    default_db_conn.pop("default")
        else:
            default_db_conn = None
    
        # config 配置信息
    
        config_obj = Config(api_config_, keywords_mod, default_db_conn,
                            datafile, runconfile)
        gl.set_value("config_obj", config_obj)
        log = Log(logpath=gl.get_value("runconf").logpath)
        gl.set_value("log", log)
        # 获取session 的配置信息
        if gl.get_value("fixture.session"):
            session_fixture_obj = gl.delete_dict("fixture.session")
        else:
            session_fixture_obj = None
        # 解析出 session 的结构数据 var =全局变量  setup = 前置, teardown = 后置
        session_var, session_setup, session_teardown = collect_session_fixture(session_fixture_obj,
                                                                               config_obj, None)
        # 获取 api fixture_var
        if gl.get_value("fixture.api"):
            api_fixture_obj = gl.delete_dict("fixture.api")
        else:
            api_fixture_obj = None
    
        gl.get_value("log").getlog().info("开始收集 api 层的 前置条件")
        
        api_var, api_fixture = collect_case_fixture(api_fixture_obj, session_var, gl.get_value("config_obj"))
        gl.get_value("log").getlog().info("api fixture收集成功:{}".format(json.dumps(api_fixture, ensure_ascii=False, indent=4)))
        gl.get_value("log").getlog().info("执行前全局变量: {}".format(session_var))
        gl.set_value("session_var", session_var if session_var else {})
        gl.set_value("session_setup", session_setup)
        gl.set_value("session_teardown", session_teardown)
        gl.set_value("__apivar__", api_var if api_var else {})
        gl.set_value("__apifixture__", api_fixture)
        
        '''to do 缺少 场景的收集信息'''
        # 暂时不做 场景的前置的条件，全部放在 group 中处理
    
    elif gl.get_value("runtype") == "ui":

        for key in ("pageobject", "fixture.ui", "fixture.session","runconf",):
            _setGlobValue(config.getoption("path"), key)

        log = Log(logpath=gl.get_value("runconf").logpath)
        gl.set_value("log", log)
        # 收集手机设备信息
        gl.set_value("device", config.getoption("cmdopt"))

def pytest_sessionstart(session):
    # 对变量中的参数进行 执行替换
    # print(dir(session))
    if gl.get_value("runtype") == "api":
        gl.get_value("log").getlog().info("开始执行 session setup :{}".format(json.dumps(gl.get_value("session_setup"), ensure_ascii=False, indent=4)
                                                                          if gl.get_value("session_setup") else "None"))
        
        session_var = fixture_executor(gl.get_value("session_setup"),
                                       gl.get_value("session_var"),
                                       gl.get_value("config_obj").keywords_mod)
        
        gl.get_value("log").getlog().info("执行 session setup 结束, session_var:{}".format(session_var))
    
        # api接口 变量
        gl.set_value("__apivar__", collect_var(dict(session_var) if dict(session_var) else {}, gl.get_value("__apivar__"),
                                               ObjDict({"keywords_mod": gl.get_value("config_obj")})))
        
        gl.get_value("log").getlog().info("与API var 变量合并后全局变量: {}".
                                          format(gl.get_value("__apivar__")))
        
        # 场景 变量
    
        gl.set_value("__scenariovar__", collect_var(dict(session_var) if dict(session_var) else {}, {},
                                               ObjDict({"keywords_mod": gl.get_value("config_obj")})))
    
        gl.get_value("log").getlog().info("与scenario var 变量合并后全局变量: {}".
                                          format(gl.get_value("__scenariovar__")))
    
        gl.delete_dict("session_var")
        gl.delete_dict("session_setup")

    elif gl.get_value("runtype") == "ui":
        # 运行前置条件
        # print(gl.get_value("fixture.session").setup)
        fixtur_executor_ui(gl.get_value("fixture.session").setup if gl.get_value("fixture.session") else None)

def pytest_sessionfinish(session, exitstatus):
    if gl.get_value("runtype") == "api":
        fixture_executor(gl.get_value("session_teardown"),
                         gl.get_value("__apivar__"),
                         gl.get_value("config_obj").keywords_mod)

    elif gl.get_value("runtype") == "ui":

        fixtur_executor_ui(gl.get_value("fixture.session").teardown if gl.get_value("fixture.session") else None, False)
    
def pytest_collect_file(path, parent):
    # 收集传入路径下的 api 配置信息与用例
    config = parent.config
    run_name = config.getoption("casenames")  # 运行的用例名称  或者 场景名称
    gl.set_value("run_case_name", run_name.split(",") if run_name else run_name)

    if path.ext in (".yml", ".yaml") and path.basename not in ("api.yaml", "api.yml",
                                                               "fixture.api.yaml", "fixture.api.yml",
                                                               "fixture.session.yml", "fixture.session.yaml",
                                                               "runconf.yml", "runconf.yaml", "fixture.yml", "fixture.yaml",
                                                               "pageobject.yaml", "pageobject.yml"):
        gl.get_value("log").getlog().info("收集测试用例文件: {}".format(path))
        return YamlFile(path, parent)


class YamlFile(pytest.File):
    def __init__(self, path, parent):
        super(YamlFile, self).__init__(path, parent)
        if gl.get_value("runtype") == "api":
            self.api_name = os.path.basename(self.fspath).split(".")[0]
            self.api_fixture = gl.get_value("__apifixture__")
        elif gl.get_value("runtype") == "ui":
            self.mode_name = os.path.basename(self.fspath).split(".")[0]
            self.ui_fixture = gl.get_value("fixture.ui")
        
    def setup(self):
        # 运行接口层级的 api
        if gl.get_value("runtype") == "api":
            if self.api_fixture.get(self.api_name):
                gl.get_value("log").getlog().info(
                    "开始执行api层级的 fixture setup: {}".format(json.dumps(self.api_fixture.get(self.api_name).setup,
                                                                     ensure_ascii=False, indent=4)))
    
                var = fixture_executor(self.api_fixture.get(self.api_name).setup, gl.get_value("__apivar__"),
                                       gl.get_value("config_obj").keywords_mod)
                
                # 执行完前置条件后，生成新变量
                gl.set_value(self.api_name, collect_var(dict(var), gl.get_value(self.api_name),
                                                        ObjDict({"keywords_mod": gl.get_value("config_obj")})))
                
                gl.get_value("log").getlog().info("api 层级的fixture setup 执行完成")
        elif gl.get_value("runtype") == "ui":
            if self.ui_fixture.get(self.mode_name):
                gl.get_value("log").getlog().info(
                    "开始执行模块层级UI的 fixture setup: {}".format(json.dumps(self.ui_fixture.get(self.mode_name).setup,
                                                                     ensure_ascii=False, indent=4)))
    
                var = fixture_executor(self.ui_fixture.get(self.mode_name).setup)

                
                gl.get_value("log").getlog().info("模块层级UI的fixture setup 执行完成")


    def teardown(self):
        if gl.get_value("runtype") == "api":
            if self.api_fixture.get(self.api_name):
                gl.get_value("log").getlog().info(
                    "开始执行api层级的 fixture teardown: {}".format(json.dumps(self.api_fixture.get(self.api_name).setup,
                                                                        ensure_ascii=False, indent=4)))
                fixture_executor(self.api_fixture.get(self.api_name).teardown, gl.get_value("__apivar__"),
                                 gl.get_value("config_obj").keywords_mod)
    
                gl.get_value("log").getlog().info("api 层级的fixture teardown 执行完成")

        elif gl.get_value("runtype") == "ui":

            if self.ui_fixture.get(self.mode_name):
                gl.get_value("log").getlog().info(
                    "开始执行模块层级UI的 fixture teardown: {}".format(json.dumps(self.ui_fixture.get(self.mode_name).teardown,
                                                                     ensure_ascii=False, indent=4)))
                var = fixture_executor(self.ui_fixture.get(self.mode_name).teardown)
                
                gl.get_value("log").getlog().info("模块层级UI的fixture teardown 执行完成")


    def collect(self):
        # 收集每个文件下测试用例 : 区分单用例， 多用例
        raw = YamlSampler.read_yaml(self.fspath)
        if ".scenario.yaml" in self.name or ".scenario.yml" in self.name:
            gl.set_value("__nowruntype__", "场景")
            gl.set_value("__runfile__", self.api_name)
            fixed = raw.get("group")
            scenario_test_list = dict()
            scenario = raw.get("scenario")
            if raw.get("var"):
                gl.set_value(self.api_name, collect_var(dict(raw.var), gl.get_value("__scenariovar__"),
                                                        ObjDict({"keywords_mod": gl.get_value("config_obj")})))
            else:
                gl.set_value(self.api_name, collect_var(dict(), gl.get_value("__scenariovar__"),
                                                        ObjDict({"keywords_mod": gl.get_value("config_obj")})))
            for name, info in scenario.items():
                if info:
                    single = {"var": raw.get("var"), name: info}
                    scenario_test_list[name] = Scenario(single, gl.get_value(self.api_name), fixed, gl.get_value("config_obj"))
            for name, value in scenario_test_list.items():
                if gl.get_value("run_case_name"):
                    if name in gl.get_value("run_case_name"):
                        yield YamlTestItem(self.api_name, name, self, value)  # 生成器逐一的 运行用例
                else:
                    yield YamlTestItem(self.api_name, name, self, value)
        
        elif ".api.yaml" in self.name or ".api.yml" in self.name:
            gl.set_value("__nowruntype__", "接口")
            gl.set_value("__runfile__", self.api_name)
            self.api_ = Api(raw, gl, self.api_name, gl.get_value("config_obj"))
            
        # 用例级别的变量与 高级别（api， session） 的变量 合并
            if self.api_.var:
                gl.set_value(self.api_name, collect_var(dict(self.api_.var), gl.get_value("__apivar__"),
                                                        ObjDict({"keywords_mod": gl.get_value("config_obj")})))
            else:
                gl.set_value(self.api_name, collect_var(dict(), gl.get_value("__apivar__"),
                                                        ObjDict({"keywords_mod": gl.get_value("config_obj")})))
        
            for name, value in zip(self.api_.test_ids, self.api_.test_list):
                if gl.get_value("run_case_name"):
                    if name in gl.get_value("run_case_name"):
                        yield YamlTestItem(self.api_name, name, self, value)  # 生成器逐一的 运行用例
                else:
                    yield YamlTestItem(self.api_name, name, self, value)

        elif ".app.yaml" in self.name or ".app.yml" in self.name:
            for key, cases in raw.items():
                # key 用例标题,cases 用例步骤
                yield YamlTestItem(key, key, self, cases)

class YamlTestItem(pytest.Item):
    def __init__(self, apiname, name, parent, spec):
        super(YamlTestItem, self).__init__(name, parent)
        if gl.get_value("runtype") == "api":
            self.caseName = name
            self.api_name = apiname
            self.api_value = spec

        elif gl.get_value("runtype") == "ui":
            self.caseName = name
            self.keyMode = apiname
            self.caseInfo = spec
        
    def runtest(self):
        if gl.get_value("runtype") == "api":
            if isinstance(self.api_value, Scenario):
                scenarios = self.api_value.test_list
                for api in scenarios:
                    for name, value in api.items():
                        with pytest.allure.step(name):
                            _var = case_run(name, self.api_name, value)
            
            elif isinstance(self.api_value, TestInfo):
                with pytest.allure.step(self.caseName):
                    _var = case_run(self.caseName, self.api_name, self.api_value)

        elif gl.get_value("runtype") == "ui":
            with pytest.allure.step(self.caseName):
                run_case_(gl.get_value("pageobject"), self.caseInfo, gl.get_value("runconf").type, self.caseName)

    def repr_faile(self, excinfo):
        if isinstance(excinfo.value, Exception):
            return '测试用例名称：{} \n' \
                   '输入参数：{} \n' \
                   '错误信息：{}'.format(self.caseName, self.caseInfo, excinfo.value.args)


def _setGlobValue(path, key=None):
    # 获取当前目录
    dirandfile = list(os.walk(path))
    for filename in dirandfile[0][-1]:
        if key + ".yml" == filename or key + '.yaml' == filename:
            gl.set_value(key, YamlSampler.read_yaml(os.path.join(dirandfile[0][0], filename)))
            return
    _setGlobValue(os.path.dirname(path), key)


# if __name__ == "__main__":
# # #     #"./Demo/场景/直播.scenario.yaml"  "./Demo/直播/关注的主播列表.api.yaml",
# # #     pytest.main(["./Demo/case/demo.app.yaml", "--runtype", "ui", "--cmdopt", "CLB0219807000456",
# # #      "--path", "./Demo", "--alluredir", "./Demo/reports", "-s", "--capture=no"])
#     pytest.main(["/Users/rudolf_han/Documents/rela-testcase/场景", "--runtype", "api",
#      "--path", "/Users/rudolf_han/Documents/rela-testcase", "--alluredir", "/Users/rudolf_han/Documents/rela-testcase/reports", "-s", "--capture=no"])

