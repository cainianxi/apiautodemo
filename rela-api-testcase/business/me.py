#!/usr/bin/python3
import json
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import SchemaError, ValidationError


def aa(aa):
    msg_ = []
    try:
        assert aa.get("code") == 0
    except AssertionError as E:
        print(E.message())
        msg_ = ["断言结果:", " {0} ==> {1}".format(aa.get("code"), 0)]

    return msg_


def json_schema(json_data):
    msg_ = []
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "book info",
        "description": "some information about book",
        "type": "object",
        "properties": {
            "id": {
                "description": "The unique identifier for a book",
                "type": "integer",
                "minimum": 1
            },
            "name": {
                "description": "book name",
                "type": "string",
                "minLength": 3,
                "maxLength": 30
            },
            "info": {
                "description": "simple information about book",
                "type": "string",
                "minLength": 10,
                "maxLength": 60
            },
            "price": {
                "description": "book price",
                "type": "number",
                "multipleOf": 0.5,
                # 这里没有取等，5.0<price<99999.0
                "minimum": 5.0,
                "maximum": 99999.0,
                # 若使用下面这两个关键字则 5.0<=price<=99999.0
                # "exclusiveMinimum": 5.0,
                # "exclusiveMaximum": 99999.0
            },
            "tags": {
                "type": "array",
                "items": [
                    {
                        "type": "string",
                        "minLength": 2,
                        "macLength": 8
                    },
                    {
                        "type": "number",
                        "minimum": 1.0
                    }
                ],
                "additonalItems": {
                    "type": "string",
                    "miniLength": 2
                },
                "miniItems": 1,
                "maxItems": 5,
                "uniqueItems": True
            },
            "date": {
                "description": "书籍出版日期",
                "type": "string",
                "format": "date",
            },
            "bookcoding": {
                "description": "书籍编码",
                "type": "string",
                "pattern": "^[A-Z]+[a-zA-Z0-9]{12}$"
            },
            "other": {
                "description": "其他信息",
                "type": "object",
                "properties": {
                    "info1": {
                        "type": "string"
                    },
                    "info2": {
                        "type": "string"
                    }
                }
            }
        },
        "minProperties": 3,
        "maxProperties": 7,
        "required": [
            "id", "name", "info", "price"
        ]
    }

    # json_data = {
    #     "id": 1,
    #     "name": "jarvis手册",
    #     "info": "贾维斯平台使用手册1",
    #     "price": 5.5,
    #     "tags": ["jar"],
    #     "date": "2019-5-25",
    #     "other": {
    #         "info1": "1111",
    #         "info2": "222"
    #     }
    # }

    try:
        validate(instance=json_data, schema=schema, format_checker=draft7_format_checker)
    except SchemaError as e:
        msg_.append("验证模式schema出错：\n出错位置：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
    except ValidationError as e:
        msg_.append("json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
    else:
        print("验证成功！")

    finally:
        return msg_
