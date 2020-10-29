#!/usr/bin/python3

from common import assert_schema


def sendcode_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "发送验证码",
        "description": "发送验证码",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "errcode": {
                "type": "string",
                "default": ""
            },
            "errdesc": {
                "type": "string",
                "default": ""
            },
            "data": {
                "type": "object",
                "default": {},
                "properties": {
                    "smsRequestId": {
                        "type": "string"
                    },
                },
                "required": [
                    "smsRequestId"
                ]
            }
        },
        "required": [
            "result", "data", "errcode", "errdesc"
        ]
    }
    return assert_schema(request, schema)


def sendcode_newformat_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "发送验证码",
        "description": "发送验证码",
        "type": "object",
        "properties": {
            "code": {
                "type": "number",
                "default": 0
            },
            "message": {
                "type": "string",
                "default": ""
            },
            "data": {
                "type": "object",
                "default": {},
                "properties": {
                    "smsRequestId": {
                        "type": "string"
                    },
                },
                "required": [
                    "smsRequestId"
                ]
            }
        },
        "required": [
            "code", "data", "message"
        ]
    }
    return assert_schema(request, schema)


def check_cell_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "发送验证码",
        "description": "发送验证码",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "errcode": {
                "type": "string",
                "default": ""
            },
            "errdesc": {
                "type": "string",
                "default": ""
            },
            "data": {
                "type": "object",
                "default": None,
                "properties": {
                    "exists": {
                        "type": "boolean"
                    },
                },
                "required": [
                    "exists"
                ]
            }
        },
        "required": [
            "result", "data", "errcode", "errdesc"
        ]
    }
    return assert_schema(request, schema)


def rebind_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "重新绑定",
        "description": "重新绑定",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "errcode": {
                "type": "string",
                "default": ""
            },
            "errdesc": {
                "type": "string",
                "default": ""
            },
            "data": {
                "type": "object",
                "default": None,
                "properties": {
                    "exists": {
                        "type": "boolean"
                    },
                },
                "required": [
                    "exists"
                ]
            }
        },
        "required": [
            "result", "data", "errcode", "errdesc"
        ]
    }
    return assert_schema(request, schema)
