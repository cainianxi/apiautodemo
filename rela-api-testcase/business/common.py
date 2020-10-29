#!/usr/bin/python3

from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import SchemaError, ValidationError


def assert_schema(request, schema):
    msg_ = []
    try:
        validate(instance=request, schema=schema, format_checker=draft7_format_checker)
    except SchemaError as e:
        msg_.append("验证模式schema出错：\n出错位置：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
    except ValidationError as e:
        msg_.append("json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
    else:
        print("验证成功！")
    finally:
        return msg_