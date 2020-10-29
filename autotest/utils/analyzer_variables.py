import re
import string
import builtins
from ast import literal_eval
from copy import deepcopy

import regex
from autotest import keywords as inner_mod

function_regexp_compile = re.compile(r"\$\([\w\.]+\(.*?\)\)", re.DOTALL)  # 不支持函数嵌套

# function_regexp_compile_nest = regex.compile(
# r"(?<func>\$\([\w\.]+\((?:(?:(?!\$\().)*?|(?:(?!\$\().)*((?&func))?.*?)*\)\))")
function_regexp_compile_nest = regex.compile(r"(?<func>\$\([\w\.]+\((.*?((?&func))*.*?)*\){2})", re.DOTALL)

object_path_dict_regexp_compile = regex.compile(r"\$\{(?<obj>\{(?:[^{}]+|(?&obj))*\})(.*?)\}")
object_path_list_regexp_compile = regex.compile(r"\$\{(?<obj>\[(?:[^[\]]+|(?&obj))*\])(.*?)\}")


def analyzer_expression(obj, chain_map, keywords_mod):
    return function_replace(object_access(variable_replace(obj, chain_map)), keywords_mod)


def variable_replace(obj, chain_map, parse_none_str=False):
    if parse_none_str and obj == "None":
        return None

    if not chain_map:
        return obj

    if isinstance(obj, str) and chain_map:
        if obj.startswith("${") and obj.endswith("}") and obj[2:-1].find("$") == -1:
            try:
                return chain_map[obj[2:-1]]
            except:
                return obj
        elif obj.startswith("$") and obj[1:].find("$") == -1:
            try:
                return chain_map[obj[1:]]
            except:
                return obj
        else:
            obj = string.Template(obj).safe_substitute(chain_map)  # \d\s\d?
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            if v and not isinstance(v, (int, float, bool)):
                obj[i] = variable_replace(v, chain_map, parse_none_str)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if value and not isinstance(value, (int, float, bool)):
                obj[key] = variable_replace(value, chain_map, parse_none_str)

    return obj


def object_access(obj):
    if isinstance(obj, str):
        obj_path_list = extract_object_path(obj)
        if len(obj_path_list) == 0:
            return obj
        elif len(obj_path_list) == 1 and obj[2:-1] == obj_path_list[0][0] + obj_path_list[0][1]:
            try:
                return eval(obj[2:-1])
            except Exception:
                print("对象属性引用出错: {}{}".format(obj_path_list[0][0], obj_path_list[0][1]))
                return obj
        else:
            for _obj, path in obj_path_list:
                try:
                    obj_value = eval(_obj + path)
                    _s = ["${", _obj, path, "}"]
                    obj = obj.replace("".join(_s), str(obj_value), 1)
                except Exception:
                    print("对象属性引用出错: {}{}".format(_obj, path))

    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            if v and not isinstance(v, (int, float, bool)):
                obj[i] = object_access(v)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if value and not isinstance(value, (int, float, bool)):
                obj[key] = object_access(value)
    return obj


def function_replace(obj, keywords_mod):
    if isinstance(obj, str):
        functions_list = extract_functions(obj)
        if len(functions_list) == 0:
            return obj
        elif len(functions_list) == 1 and obj[2:-1] == functions_list[0]:
            return execute_function(functions_list[0], keywords_mod)
        else:
            for func in functions_list:
                func_value = execute_function(func, keywords_mod)
                obj = obj.replace("$({})".format(func), str(func_value), 1)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            if v and not isinstance(v, (int, float, bool)):
                obj[i] = function_replace(v, keywords_mod)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if value and not isinstance(value, (int, float, bool)):
                obj[key] = function_replace(value, keywords_mod)
    return obj


def function_replace_nest(obj, keywords_mod, r):
    if not r:
        return function_replace(obj, keywords_mod)

    if isinstance(obj, str):
        functions_list = extract_functions_nest(obj)
        if len(functions_list) == 0:
            return obj
        elif len(functions_list) == 1 and obj == functions_list[0][-1]:
            return execute_function_nest(functions_list[0], keywords_mod)
        else:
            for func in functions_list:
                func_value = execute_function_nest(func, keywords_mod)
                obj = obj.replace(func[-1], str(func_value), 1)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            if v and not isinstance(v, (int, float, bool)):
                obj[i] = function_replace_nest(v, keywords_mod, r)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if value and not isinstance(value, (int, float, bool)):
                obj[key] = function_replace_nest(value, keywords_mod, r)

    return obj


def execute_function_nest(functions_list, keywords_mod):
    if len(functions_list) == 1:
        return execute_function(functions_list[-1][2:-1], keywords_mod)
    else:
        r_ = []
        for i, f in enumerate(functions_list[:-1]):
            if i and (functions_list[i - 1] in functions_list[i]) and (
                    functions_list[i - 1] != functions_list[i]):
                r_[-1] = (
                    i, execute_function(f[2:-1].replace(functions_list[i - 1], str(r_[-1][-1]), 1), keywords_mod))
            else:
                r_.append((i, execute_function(f[2:-1], keywords_mod)))

        ret = deepcopy(functions_list[-1])
        for x in r_:
            ret = ret.replace(functions_list[x[0]], str(x[1]), 1)

        return execute_function(ret[2:-1], keywords_mod)


def execute_function(function_string, keywords_mod):  # func ->　"mod.func(x, y)"
    idx = function_string.find("(")
    func_param = function_string[idx + 1:-1]
    mod_func = function_string[:idx]

    mod_func = mod_func.rsplit(".", 1)
    func_name = mod_func[-1]
    func_mod = mod_func[0] if len(mod_func) > 1 else ""
    func_obj = None

    if func_mod:
        import importlib
        try:
            func_mod = importlib.import_module(func_mod)
        except Exception:
            raise Exception("模块导入异常: {}".format(func_mod))

    if func_name:
        if func_mod:
            try:
                func_obj = getattr(func_mod, func_name)
            except Exception:
                raise Exception("函数导入异常: {}.{}".format(func_mod, func_name))
        else:
            try:
                func_obj = getattr(keywords_mod, func_name)
            except Exception:
                try:
                    func_obj = getattr(inner_mod, func_name)
                except Exception:
                    try:
                        func_obj = getattr(builtins, func_name)
                    except Exception:
                        raise Exception("函数没有找到: {}".format(func_name))
    else:
        raise Exception("函数引用异常: {}".format(function_string))

    try:
        func_param = literal_eval(func_param)
    except Exception:
        pass

    try:
        if isinstance(func_param, (list, tuple)):
            return func_obj(*func_param)
        else:
            return func_obj(func_param) if func_param else func_obj()
    except Exception as e:
        print(e)
        raise Exception("函数调用异常：{}".format(function_string))


def extract_functions(expression):
    functions_list = function_regexp_compile.findall(expression)
    return [exp[2:-1] for exp in functions_list]


def extract_functions_nest(expression):
    result = regex.search(function_regexp_compile_nest, expression)
    ret = []

    while result:
        span = result.span()
        ret.append(result.captures('func'))
        expression = expression[span[1]:]
        result = regex.search(function_regexp_compile_nest, expression)

    return ret


def extract_object_path(expression):
    ret_dict = object_path_dict_regexp_compile.findall(expression)
    if ret_dict:
        return ret_dict
    else:
        ret_list = object_path_list_regexp_compile.findall(expression)
        return ret_list



