#!/usr/local/python3

"""
主要把json 转换为对象的形式， 可以通过. 进行访问
"""

import objectpath
from ast import literal_eval


class ObjDict4Assert(dict):
    def __init__(self, json):
        _json = {k.lower(): v for k, v in json.items()}
        super().__init__(_json)

        for k, v in json.items():
            if isinstance(v, dict):
                if isinstance(k, str):
                    self[k.lower()] = ObjDict(v)
                else:
                    self[k] = ObjDict(v)
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        if isinstance(k, str):
                            self[k.lower()][i] = ObjDict(item)
                        else:
                            self[k][i] = ObjDict(item)

    def __getattr__(self, key):
        try:
            if isinstance(key, str):
                return self[key.lower()]
            else:
                return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __call__(self, selectors):
        return objectpath.Tree(dict(self)).execute(selectors)

    @staticmethod
    def accessor(obj, path):
        _obj = ObjDict(obj)
        if not isinstance(path, str):
            return None

        _path = None
        _path_op = None
        path = path.strip()

        if path.startswith('$'):
            _path_op = path
        elif path.startswith('[') or path.startswith('.'):
            _path = path
        else:
            _path = '.' + path

        try:
            return str_eval('_obj' + _path) if _path else _obj(_path_op)
        except Exception:
            return None


class ObjDict(dict):
    def __init__(self, json):
        super().__init__(json)
        for k, v in json.items():
            if isinstance(v, dict):
                self[k] = ObjDict(v)
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        self[k][i] = ObjDict(item)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __call__(self, selectors):
        return objectpath.Tree(dict(self)).execute(selectors)

    @staticmethod
    def accessor(obj, path):
        if isinstance(obj, dict):
            _obj = ObjDict(obj)
            if not isinstance(path, str):
                return None

            _path = None
            _path_op = None
            path = path.strip()

            if path.startswith('$'):
                _path_op = path
            elif path.startswith('[') or path.startswith('.'):
                _path = path
            else:
                _path = '.' + path

            try:
                return '_obj' + _path if _path else _obj(_path_op)
            except Exception:
                return None
        elif isinstance(obj, list):
            return objectpath.Tree(obj).execute(path.strip())
        else:
            return obj

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