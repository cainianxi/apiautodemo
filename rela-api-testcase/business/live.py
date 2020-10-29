#!/usr/bin/python3
from common import assert_schema


def rank_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "榜单",
        "description": "榜单",
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
                "properties": {
                    "topLink": {
                        "type": "string",
                        "format": "uri"
                    },
                    "anchorToday": {
                        "type": "array",
                        "maxItems": 3,
                        "default": [],
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "audioType": {
                                        "type": "string",
                                        "default": ""
                                    },
                                    "avatar": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "isCloaking": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "live": {
                                        "type": "number",
                                        "enum": [0, 1]
                                    },
                                    "liveUsersCount": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "nickName": {
                                        "type": "string",
                                    },
                                    "score": {
                                        "type": "number",
                                    }
                                },
                                "required": [
                                    "audioType", "score", "nickName", "liveUsersCount", "live",
                                    "isCloaking", "id", "avatar"
                                ]
                            }
                        ]
                    },
                    "anchorWeek": {
                        "type": "array",
                        "maxItems": 3,
                        "default": [],
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "audioType": {
                                        "type": "string",
                                        "default": ""
                                    },
                                    "avatar": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "isCloaking": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "live": {
                                        "type": "number",
                                        "enum": [0, 1]
                                    },
                                    "liveUsersCount": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "nickName": {
                                        "type": "string",
                                    },
                                    "score": {
                                        "type": "number",
                                    }
                                },
                                "required": [
                                    "audioType", "score", "nickName", "liveUsersCount", "live",
                                    "isCloaking", "id", "avatar"
                                ]
                            }
                        ]

                    },
                    "guardToday": {
                        "type": "array",
                        "maxItems": 3,
                        "default": [],
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "audioType": {
                                        "type": "string",
                                        "default": ""
                                    },
                                    "avatar": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "isCloaking": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "live": {
                                        "type": "number",
                                        "enum": [0, 1]
                                    },
                                    "liveUsersCount": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "nickName": {
                                        "type": "string",
                                    },
                                    "score": {
                                        "type": "number",
                                    }
                                },
                                "required": [
                                    "audioType", "score", "nickName", "liveUsersCount", "live",
                                    "isCloaking", "id", "avatar"
                                ]
                            }
                        ]
                    },
                    "guardWeek": {
                        "type": "array",
                        "maxItems": 3,
                        "default": [],
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "audioType": {
                                        "type": "string",
                                        "default": ""
                                    },
                                    "avatar": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "isCloaking": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "live": {
                                        "type": "number",
                                        "enum": [0, 1]
                                    },
                                    "liveUsersCount": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "nickName": {
                                        "type": "string",
                                    },
                                    "score": {
                                        "type": "number",
                                    }
                                },
                                "required": [
                                    "audioType", "score", "nickName", "liveUsersCount", "live",
                                    "isCloaking", "id", "avatar"
                                ]
                            }
                        ]
                    }
                },
                "required": [
                    "anchorToday", "anchorWeek", "guardToday", "guardWeek"
                ]
            }
        },
        "required": [
            "result", "data", "errcode", "errdesc"
        ]
    }
    return assert_schema(request, schema)


def living_friend_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "正在直播朋友",
        "description": "正在直播朋友",
        "type": "object",
        "properties": {
            "result": {
                # "description": "The unique identifier for a book",
                "type": "string",
                "default": "1"
            },
            "data": {
                # "description": "book name",
                "type": "object",
                "properties": {
                    "linkMicFailAwaitTime": {
                        "type": "number"
                    },
                    "pkFailAwaitTime": {
                        "type": "number"
                    },
                    "list": {
                        "type": "array",
                        "minItems": 0,
                        "default": []
                    }
                },
                "required": [
                    "linkMicFailAwaitTime", "pkFailAwaitTime", "list"
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


def meta_api(request):
    pass


def perm_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "直播权限",
        "description": "直播权限",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "errcode": {
                "type": "string",
            },
            "errdesc": {
                "type": "string",
            },
            "data": {
                # "description": "book name",
                "type": "object",
                "properties": {
                    "perm": {
                        "type": "number",
                        "enum": [0, 1]
                    }
                },
                "required": [
                    "perm"
                ]
            }
        },
        "required": [
            "result", "data", "errcode", "errdesc"
        ]
    }
    return assert_schema(request, schema)
