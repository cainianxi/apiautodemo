from enum import Enum
from io import StringIO
import json
import re

from autotest.utils.utils import is_number, str_eval
from autotest.utils.obj_dict import ObjDict, ObjDict4Assert


class ObjDictUtils:
    TYPE_MAP = {dict: "(object)", list: "(array)", float: "(number)", int: "(number)", str: "(string)",
                bool: "(boolean)", ObjDict: "(object)"}
    None_MAP = {dict: "{}", list: "[]", float: "0.0", int: "0", str: "", bool: "false", ObjDict: "{}"}

    KEY_TYPE = Enum("KEY_TYPE", ("DICT", "LIST"))
    CONN_STR = {"update": " ==> ", "create": " --> ", "delete": " ++> "}

    _INDENT = 4
    _file = None

    class Missing:
        pass

    _mis = Missing()

    SMART_ITEM = [int, float, str]
    SMART_OBJ = [list, dict, ObjDict]

    # part表示是否全量比较,默认为部分比较(只要期望值在实际值中存在并且相等即成功),传True即可完成Schema的校验
    # str2number 表示是否将代表数字的字符串转成数字和目标数字比较
    def diff(self, real, expect, str2number=True, part=True, smart=False):
        if smart:
            real, expect = self._smart_value(real, expect)
        return self.format(self._diff(real, expect, str2number, part))

    @classmethod
    def _smart_value(cls, real, expect):
        if type(real) in cls.SMART_ITEM and type(expect) in cls.SMART_OBJ:
            if expect:
                if isinstance(expect, list):
                    if len(expect) == 1 and isinstance(expect[0], (dict, ObjDict)) and len(expect[0]) == 1:
                        expect = list(expect[0].values())[0]
                elif len(expect) == 1:
                    expect = list(expect.values())[0]

        if type(expect) in cls.SMART_ITEM and type(real) in cls.SMART_OBJ:
            if real:
                if isinstance(real, list):
                    if len(real) == 1 and isinstance(real[0], (dict, ObjDict)) and len(real[0]) == 1:
                        real = list(real[0].values())[0]
                elif len(real) == 1:
                    real = list(real.values())[0]

        if type(real) in cls.SMART_OBJ and type(expect) in cls.SMART_OBJ:
            if isinstance(real, list) and not isinstance(expect, list):
                if len(real) == 1 and isinstance(real[0], (dict, ObjDict)):
                    real = real[0]
            if isinstance(expect, list) and not isinstance(real, list):
                if len(expect) == 1 and isinstance(expect[0], (dict, ObjDict)):
                    expect = expect[0]

        return real, expect

    def _print(self, *args, **kwargs):
        print(*args, **kwargs, file=self._file)

    def _line_inner_output(self, *args, **kwargs):
        print(*args, **kwargs, file=self._file, end="")

    @classmethod
    def _true_msg(cls, value):
        _value = value
        if isinstance(value, bool):
            _value = "true"
        return str(_value) + cls.TYPE_MAP[type(value)]

    @classmethod
    def _false_msg(cls, value):
        _false_exp = "(object)" if value is None else cls.None_MAP[type(value)] + cls.TYPE_MAP[type(value)]
        return _false_exp

    @classmethod
    def _real_expect_msg(cls, real_value, expect_value):
        real_exp = cls._true_msg(real_value) if real_value else cls._false_msg(real_value)
        expect_exp = cls._true_msg(expect_value) if expect_value else cls._false_msg(expect_value)
        return real_exp, expect_exp

    @classmethod
    def _value_msg_create(cls, real, expect):
        real_exp, expect_exp = cls._real_expect_msg(real, expect)
        return real_exp + cls.CONN_STR["update"] + expect_exp

    @classmethod
    def _list_msg_create(cls, index, real_value, expect_value):
        real_exp, expect_exp = cls._real_expect_msg(real_value, expect_value)
        return str(index) + ": " + real_exp + cls.CONN_STR["update"] + expect_exp

    @classmethod
    def _dict_msg_create(cls, key, real_value, expect_value):
        real_exp, expect_exp = cls._real_expect_msg(real_value, expect_value)
        return {key: real_exp + cls.CONN_STR["update"] + expect_exp}

    @classmethod
    def _missing_msg_create(cls, real_value, expect_value, k=None, k_type=None):
        conn_str = cls.CONN_STR["update"]

        if isinstance(real_value, cls.Missing):
            real_exp = ""
            conn_str = cls.CONN_STR["create"].lstrip()
        elif real_value is None:
            real_exp = "None(object)"
        else:
            real_exp = cls._true_msg(real_value)

        if isinstance(expect_value, cls.Missing):
            expect_exp = ""
            conn_str = cls.CONN_STR["delete"].rstrip()
        elif expect_value is None:
            expect_exp = "None(object)"
        else:
            expect_exp = cls._true_msg(expect_value)

        if k_type == cls.KEY_TYPE.DICT:
            return {k: real_exp + conn_str + expect_exp}
        elif k_type == cls.KEY_TYPE.LIST:
            return str(k) + ": " + real_exp + conn_str + expect_exp

    @classmethod
    def _single_element_compare(cls, real_value, expect_value, k=None, k_type=None, str2number=True):
        msg = None

        if str2number:
            if is_number(real_value) and is_number(expect_value):
                if float(real_value) != float(expect_value):
                    if k_type == cls.KEY_TYPE.DICT:
                        msg = cls._dict_msg_create(k, real_value, expect_value)
                    elif k_type == cls.KEY_TYPE.LIST:
                        msg = cls._list_msg_create(k, real_value, expect_value)
                    else:
                        msg = cls._value_msg_create(real_value, expect_value)
            elif real_value != expect_value:
                if k_type == cls.KEY_TYPE.DICT:
                    msg = cls._dict_msg_create(k, real_value, expect_value)
                elif k_type == cls.KEY_TYPE.LIST:
                    msg = cls._list_msg_create(k, real_value, expect_value)
                else:
                    msg = cls._value_msg_create(real_value, expect_value)
        elif real_value != expect_value:
            if k_type == cls.KEY_TYPE.DICT:
                msg = cls._dict_msg_create(k, real_value, expect_value)
            elif k_type == cls.KEY_TYPE.LIST:
                msg = cls._list_msg_create(k, real_value, expect_value)
            else:
                msg = cls._value_msg_create(real_value, expect_value)
        return msg

    @classmethod
    def _diff_list(cls, real, expect, str2number, part):
        msg = []

        real_len = len(real)
        expect_len = len(expect)
        _intersection = real_len if real_len <= expect_len else expect_len

        for i in range(_intersection):
            if isinstance(real[i], list) and isinstance(expect[i], list):
                _msg = cls._diff_list(real[i], expect[i], str2number, part)
                if _msg:
                    msg.append(str(i) + ": " + str(_msg))
            elif isinstance(real[i], dict) and isinstance(expect[i], dict):
                _msg = cls._diff_dict(real[i], expect[i], str2number, part)
                if _msg:
                    msg.append(str(i) + ": " + str(_msg))
            else:
                _msg = cls._single_element_compare(real[i], expect[i], i, cls.KEY_TYPE.LIST, str2number)
                if _msg:
                    msg.append(_msg)

        diff_obj, idx_low, idx_high = (expect, real_len, expect_len) if real_len < expect_len else (
            real, expect_len, real_len)

        for i in range(idx_low, idx_high):  # 列表长度不相等的情况下，列出多余或缺失的项
            if real_len < expect_len:
                msg.append(cls._missing_msg_create(cls._mis, diff_obj[i], i, cls.KEY_TYPE.LIST))
            else:
                msg.append(cls._missing_msg_create(diff_obj[i], cls._mis, i, cls.KEY_TYPE.LIST))

        return msg

    @classmethod
    def _diff_dict(cls, real, expect, str2number, part):
        msg = {}

        real = ObjDict4Assert(real)
        expect = ObjDict4Assert(expect)
        _intersection = set(real) & set(expect)
        _diff_real = set(real) - set(expect)
        _diff_expect = set(expect) - set(real)

        for k in _intersection:  # 处理key的交集部分
            if isinstance(real[k], list) and isinstance(expect[k], list):
                _msg = cls._diff_list(real[k], expect[k], str2number, part)
                if _msg:
                    msg[k] = _msg
            elif isinstance(real[k], dict) and isinstance(expect[k], dict):
                _msg = cls._diff_dict(real[k], expect[k], str2number, part)
                if _msg:
                    msg[k] = _msg
            else:
                _msg = cls._single_element_compare(real[k], expect[k], k, cls.KEY_TYPE.DICT, str2number)
                if _msg:
                    msg.update(_msg)

        for k in _diff_expect:  # 处理新增的部分
            _msg = cls._missing_msg_create(cls._mis, expect[k], k, cls.KEY_TYPE.DICT)
            msg.update(_msg)

        if part:
            return msg

        for k in _diff_real:  # 处理删除的部分
            _msg = cls._missing_msg_create(real[k], cls._mis, k, cls.KEY_TYPE.DICT)
            msg.update(_msg)

        return msg

    @classmethod
    def _diff(cls, real, expect, str2number, part):
        if isinstance(real, dict) and isinstance(expect, dict):
            return cls._diff_dict(real, expect, str2number, part)
        elif isinstance(real, list) and isinstance(expect, list):
            return cls._diff_list(real, expect, str2number, part)
        else:
            return cls._single_element_compare(real, expect, str2number=str2number)

    def _print_single(self, value):
        output = self._line_inner_output

        if isinstance(value, str):
            for flag in self.CONN_STR.values():
                _flag = flag.strip()
                idx = value.find(_flag)
                if idx >= 0:
                    _left = value[:idx]
                    _right = value[idx + len(_flag):]
                    for f1 in set(self.TYPE_MAP.values()):
                        idx_left = _left.find(f1)
                        if idx_left >= 0:
                            _data_left = _left[:idx_left]
                            self._print_single(str_eval(_data_left))
                            output(f1)
                            break
                    else:
                        output(_left)

                    if _left and _right:  # 处理多余的空格
                        output(flag)
                    elif _left:
                        output(flag.rstrip())
                    elif _right:
                        output(flag.lstrip())
                    else:
                        output(flag.strip())

                    for f2 in set(self.TYPE_MAP.values()):
                        idx_right = _right.find(f2)
                        if idx_right >= 0:
                            _data_right = _right[:idx_right]
                            self._print_single(str_eval(_data_right))
                            output(f2)
                            break
                    else:
                        output(_right)

                    break
            else:
                output(value)

        # 注释部分实现行内值的裸输出
        # elif isinstance(value, list):
        #     output("[")
        #     count = 0
        #
        #     for v in value:
        #         count += 1
        #         if isinstance(v, (list, dict)):
        #             self._print_single(v)
        #         else:
        #             output(v)
        #
        #         if count < len(value):
        #             output(", ")
        #
        #     output("]")
        # elif isinstance(value, dict):
        #     output("{")
        #     count = 0
        #
        #     for k, v in value.items():
        #         output(k, ": ", sep="")
        #         count += 1
        #         if isinstance(v, (list, dict)):
        #             self._print_single(v)
        #         else:
        #             output(v)
        #
        #         if count < len(value):
        #             output(", ")
        #
        #     output("}")

        else:
            s = json.dumps(value, ensure_ascii=False)
            s = re.sub(r"(\\)(.)", r'\2', s, flags=re.DOTALL)  # 去掉字符串内的转义字符
            output(s)

    def _print_list(self, lst, indent_num):
        _print = self._print
        _space = " " * (self._INDENT * indent_num)
        _print("[")

        for i, v in enumerate(lst):
            idx = v.find(": ")
            _i = v[:idx]
            _v = str_eval(v[idx + 1:])

            _print(_space, _i, ": ", sep="", end="")

            if isinstance(_v, list):
                self._print_list(_v, indent_num + 1)
            elif isinstance(_v, dict):
                self._print_dict(_v, indent_num + 1)
            else:
                self._print_single(_v)

            if i + 1 < len(lst):
                _print(",")
            else:
                _print()

        if indent_num == 1:
            _print("]")
        else:
            _print(" " * self._INDENT * (indent_num - 1), "]", sep="", end="")

    def _print_dict(self, dic, indent_num):
        _print = self._print
        _space = " " * (self._INDENT * indent_num)
        count = 0

        _print("{")

        for k, v in dic.items():
            count += 1
            _print(_space, k, ": ", sep="", end="")

            if isinstance(v, dict):
                self._print_dict(v, indent_num + 1)
            elif isinstance(v, list):
                self._print_list(v, indent_num + 1)
            else:
                self._print_single(v)

            if count < len(dic):
                _print(",")
            else:
                _print()

        if indent_num == 1:
            _print("}")
        else:
            _print(" " * self._INDENT * (indent_num - 1), "}", sep="", end="")

    def format(self, obj):
        self._file = StringIO()
        if obj:
            if isinstance(obj, dict):
                self._print_dict(obj, indent_num=1)
            elif isinstance(obj, list):
                self._print_list(obj, indent_num=1)
            else:
                self._print_single(obj)
        else:
            return ""

        msg = self._file.getvalue()
        self._file = None

        return msg


if __name__ == "__main__":
    diff = ObjDictUtils().diff
    
    # old =
    # new =
    # print(diff(old, new,  True, True, True))
