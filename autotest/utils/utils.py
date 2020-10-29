import json
from ast import literal_eval
from collections import ChainMap

SCALAR_ITEM = [int, float, str, bool]


def merge_obj(target, source):
    if type(target) in SCALAR_ITEM or type(source) in SCALAR_ITEM:
        return source

    if target is None or source is None:
        return source

    if isinstance(source, list) and isinstance(target, list):
        if not source:
            return target

        if not isinstance(source[-1], list):
            return source

        if target:
            if source[:-1]:
                for ii, it in enumerate(source[-1]):
                    try:
                        target[it] = merge_obj(target[it], source[ii])
                    except:
                        pass  # 索引错误越界忽略
            else:
                target = []
        else:
            target = source[:-1]
        return target

    elif isinstance(source, dict) and isinstance(target, dict):
        for k, v in source.items():
            target[k] = merge_obj(target[k], v)
        return target

    else:
        return source


def merge_dict(target, source):
    if not target:
        return ChainMap(source)
    if not source:
        return ChainMap(target)

    for k, v in source.items():
        if isinstance(v, dict) and isinstance(target.get(k), dict):
            target[k] = merge_dict(target[k], v)
        else:
            target[k] = v

    return ChainMap(target)


def merge_body(target, source):
    if not target:
        return source
    if not source:
        return target

    for k, v in source.items():
        if isinstance(v, dict) and isinstance(target.get(k), dict):
            target[k] = merge_body(target[k], v)
        else:
            target[k] = v

    return target


def str_eval_with_none(obj_str):
    if not obj_str or isinstance(obj_str, (int, float, bool)):
        return obj_str

    ret = None
    try:
        ret = literal_eval(str(obj_str))
        if isinstance(ret, (int, float, bool)):  # 解决str转换问题
            ret = obj_str
    except Exception as e:
        return obj_str.strip() if isinstance(obj_str, str) else obj_str

    if isinstance(ret, dict):
        for key, value in ret.items():
            if value and not isinstance(value, (int, float, bool)):
                ret[key] = str_eval_with_none(value)
    elif isinstance(ret, list):
        for i, v in enumerate(ret):
            if v and not isinstance(v, (int, float, bool)):
                ret[i] = str_eval_with_none(v)

    return ret


def str_eval(obj_str):
    if isinstance(obj_str, str):
        try:
            r = literal_eval(obj_str)
            if isinstance(r, (int, float, bool)):
                return obj_str
            else:
                return r
        except Exception:
            return obj_str.strip()
    else:
        return obj_str


def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False


def json_dumps(dic):
    return json.dumps(dic, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == "__main__":
    # cm = {
    #     'status': '1030',
    #     'child_status': None
    # }
    #
    # fix = [{
    #     '查询进件': {
    #         'assert': {
    #             'sql-json': {
    #                 'sql': "SELECT STATUS, child_status FROM  t_apply_msg  where id = '10000003931'",
    #                 'json': {
    #                     'status': '${status}',
    #                     'child_status': '${child_status}'
    #                 }
    #             }
    #         }
    #     }
    # }]
    # import string
    # # fix = string.Template(str(fix)).safe_substitute(cm)
    # o = string.Template(str(fix)).safe_substitute(cm)
    # fix = str_eval_with_none(o)
    # print(json_dumps(fix))

    target = {"a": 123, "b": [1, 2], "c": {"d": 123, "e": {"f": 123, "g": "abc"}}, "h": {"i": [1, 2]}}
    source = {"a": 12, "b": [1, 2, {"s": 222}], "c": {"e": {"f": "aaa"}}, "d": 123456789}
    # ro = merge_dict(target, source)
    ro = merge_body(target, source)

    # target = {"a": 123, "b": [1, 2, {'qa': "test"}], "h": [[1, 2]]}
    # source = {"b": [{'qa': "test-update"}, [2]], "h": [[123, [1]], [0]]}
    #
    # ro = merge_obj(target, source)
    # print(json_dumps(ro))

    s = "{'a': 'None'}"
    s2 = '{"level":1,"parent_id":0,"category_status":1}'
    print(str_eval_with_none(s))
    import string

    s2 = str_eval(string.Template(s2).safe_substitute(None))
    print(s2)

    d = {"channel_id": "${channel_id}", "level": "${level}", "parent_id": "${parent_id}"}
    print(string.Template(str(d)).safe_substitute(s2))
    d = str_eval_with_none(string.Template(str(d)).safe_substitute(s2))
    print(d)
