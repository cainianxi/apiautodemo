#!/usr/local/python3

from copy import deepcopy

from autotest.analyzers.collect_fixtures import collect_api, collect_setup, collect_teardown, collect_var, collect_assert
from autotest.utils import str_eval_with_none, variable_replace

api_fields = ["var", "setup", "teardown", "test_case"]


class TestInfo:
    def __init__(self, _setup, _teardown, _api, _assert, _var, keywords_mod):
        self.setup = _setup
        self.teardown = _teardown
        self.api = _api
        self.assert_ = _assert
        self.var = _var
        self.keywords_mod = keywords_mod

    def __str__(self):
        _str = ["<" + self.__class__.__name__ + ">"]
        for k, v in self.__dict__.items():
            _str.append("\t" + k + ": " + str(v))
        return "\n".join(_str)


class CaseInfo:
    def __init__(self, values_dict, var_mod, other_conf, config):
        if isinstance(self, Scenario):
            self.var = values_dict.pop("var", None)
            self.scenario = values_dict
            self.fixed = other_conf
        elif isinstance(self, Api):
            self.set_fields(values_dict)

        self.collect_info(var_mod, other_conf, config)

    def set_fields(self, values_dict):
        for field in api_fields:
            setattr(self, field, values_dict.get(field.replace("_", "-")))

    def collect_info(self, var_mod, other_conf, config):
        if isinstance(self, Api):
            self._collect_api(var_mod, other_conf, config)
        elif isinstance(self, Scenario):
            self._collect_scenario(var_mod, other_conf, config)

    def _collect_api(self, var_mod, api_name, config):
        chain_map = getattr(var_mod, "get_value")(api_name)
        var = collect_var(self.var, chain_map, config)

        self.setup = setup = collect_setup(self.setup, var, config)
        self.teardown = teardown = collect_teardown(self.teardown, var, config)

        for name, value in self.test_case.items():
            varx = collect_var(value.pop("var", None), var, config)  # add1
            _setup = collect_setup(value.pop("setup", None), varx, config) or setup
            _teardown = collect_teardown(value.pop("teardown", None), varx, config) or teardown
            _assert = collect_assert(value.pop("assert", None), config)
            _api = collect_api({name: value}, api_name, config, varx)
            if _api:
                _api = _api[0]
                self.test_ids.append(name)
                self.test_list.append(TestInfo(_setup, _teardown, _api, _assert, varx, config.keywords_mod))

    def _collect_scenario(self, var_mod, fixed, config):
        
        for name, info in self.scenario.items():
            if info:
                self.scenario_name = name
                # chain_map = getattr(var_mod, "get_value")(name) var_mod.get(name)
                chain_map = var_mod.get(name)
                self.var = var = collect_var(self.var, chain_map, config)
                for apis in info:
                    if isinstance(apis, str):
                        api_params = apis.split("|", 1)
                        apis = api_params[0].strip()
                        _fix = fixed and fixed.get(apis)  # 先去group取

                        if _fix and len(api_params) == 2:
                            params = variable_replace(str_eval_with_none(api_params[1].strip()), var)
                            if isinstance(params, dict):
                                _fix = deepcopy(_fix)
                                _fix = variable_replace(_fix, params)
                            else:
                                raise Exception("group 引用参数格式错误: {}".format(params))
                        elif not _fix:  # group没取到，假定为接口名
                            _fix = {apis: config.api_config.get(apis)}
                            _fix = deepcopy(_fix)
                        else:  # 没有参数替换
                            _fix = deepcopy(_fix)

                        # _fix = deepcopy(_fix)

                        if _fix and isinstance(_fix, list):
                            for f in _fix:
                                if isinstance(f, str):
                                    f = {f: config.api_config.get(f)}
                                self._get_step_info(f, var, config)
                        elif _fix and isinstance(_fix, dict):
                            self._get_step_info(_fix, var, config)
                        else:
                            raise Exception("group/api配置错误")

                    elif isinstance(apis, dict):
                        self._get_step_info(apis, var, config)

    def _get_step_info(self, obj, chain_map, config):
        for step_name, step_value in obj.items():
            chain_map = collect_var(step_value.pop("var", None), chain_map, config)  # add2
            _assert = collect_assert(step_value.pop("assert", None), config)
            _setup = collect_setup(step_value.pop("setup", None), chain_map, config)
            _teardown = collect_teardown(step_value.pop("teardown", None), chain_map, config)
            _api = collect_api({step_name: step_value}, None, config, chain_map)
            if _api:
                _api = _api[0]
                _step = {step_name: TestInfo(_setup, _teardown, _api, _assert, chain_map, config.keywords_mod)}
                self.test_list.append(_step)

    def __str__(self):
        _str = ["<" + self.__class__.__name__ + ">"]
        for k, v in self.__dict__.items():
            _str.append("\t" + k + ": " + str(v))
        return "\n".join(_str)


class Api(CaseInfo):
    def __init__(self, content, var_mod, api_name, config):
        self.test_ids = []
        self.test_list = []
        super().__init__(content, var_mod, api_name, config)


class Scenario(CaseInfo):
    def __init__(self, content, var_mode, fixed, config):
        self.scenario_name = None
        self.test_list = []
        super().__init__(content, var_mode, fixed, config)
