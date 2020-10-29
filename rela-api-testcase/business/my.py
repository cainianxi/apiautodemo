#!/usr/bin/python3

from common import assert_schema


def level_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "我的等级",
        "description": "我的等级",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "data": {
                "type": "object",
                "properties": {
                    "currentExpPercent": {
                        "type": "number",
                    },
                    "diamond": {
                        "type": "number",
                    },
                    "entrySwitch": {
                        "type": "number",
                    },
                    "exp": {
                        "type": "number",
                    },
                    "isCloaking": {
                        "type": "integer",
                    },
                    "level": {
                        "type": "integer",
                    },
                    "levelIconSwitch": {
                        "type": "integer",
                    },
                    "levelUpRequire": {
                        "type": "integer",
                    },
                    "nextLevelHasGot": {
                        "type": "integer",
                    },
                    "shareCount": {
                        "type": "integer",
                    },
                    "userId": {
                        "type": "integer",
                    },
                    "watchTime": {
                        "type": "number",
                    },

                },
                "required": [
                    "currentExpPercent", "diamond", "entrySwitch", "exp", "isCloaking", "level",
                    "levelIconSwitch", "levelUpRequire", "nextLevelHasGot", "shareCount", "userId",
                    "watchTime"
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


def popularity_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "屏蔽用户",
        "description": "屏蔽用户",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "data": {
                "type": "object",
                "properties": {
                    "cursor": {
                        "type": "integer",
                        "maximum": 20
                    },
                    "haveNextPage": {
                        "type": "boolean"
                    },
                    "totalPopularity": {
                        "type": "integer",
                        "minimum": 0
                    },
                    "winkList": {
                        "type": "array",
                        "minItems": 0,
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "avatar": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "nickName": {
                                        "type": "string",
                                    },
                                    "userId": {
                                        "type": "number",
                                    },
                                    "userName": {
                                        "type": "string",
                                    },
                                    "vipLevel": {
                                        "type": "number",
                                        "default": 0
                                    },
                                    "roleName": {
                                        "type": "string",
                                        "default": "0"
                                    },
                                    "popularity": {
                                        "type": "number",
                                    }
                                },
                                "required": ["avatar", "nickName", "userId", "userName",
                                             "vipLevel", "roleName", "popularity"]
                            }
                        ]
                    }
                },
                "required": [
                    "cursor", "haveNextPage", "totalPopularity", "winkList"
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


def first_change_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "是否守充",
        "description": "是否守充",
        "type": "object",
        "properties": {
            "code": {
                "type": "number",
                "default": 0
            },
            "data": {
                "type": "object",
                "properties": {
                    "isFirstCharge": {
                        "type": "number",
                        "default": 0
                    }
                },
                "required": [
                    "isFirstCharge"
                ]
            }
        },
        "required": [
            "code", "data"
        ]
    }
    return assert_schema(request, schema)


def vip_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "热拉会员",
        "description": "热拉会员",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "data": {
                "type": "object",
                "properties": {
                    "vipSetting": {
                        "type": "object",
                        "properties": {
                            "autoSubscribe": {
                                "type": "number",
                                "default": 0
                            },
                            "expireTime": {
                                "type": "string",
                                "format": "date"
                            },
                            "followRemind": {
                                "type": "number",
                            },
                            "hiding": {
                                "type": "number",
                            },
                            "incognito": {
                                "type": "number",
                            },
                            "level": {
                                "type": "number",
                            },
                            "liveHiding": {
                                "type": "number",
                            },
                            "msgHiding": {
                                "type": "number",
                            },
                            "userId": {
                                "type": "number",
                            },
                            "vipHiding": {
                                "type": "number",
                            },
                        },
                        "required": [
                            "autoSubscribe", "expireTime", "followRemind", "hiding", "incognito",
                            "level", "liveHiding", "userId", "vipHiding"
                        ]
                    }
                },
                "required": [
                    "vipSetting"
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


def look_me_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "谁看过我",
        "description": "谁看过我",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "data": {
                "type": "object",
                "properties": {
                    "map_list": {
                        "type": "array",
                        "minItems": 0,
                        "default": [],
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "Avatar": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "avatar": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "id": {
                                        "type": "number",
                                    },
                                    "userId": {
                                        "type": "number",
                                        "format": "uri"
                                    },
                                    "userName": {
                                        "type": "string",
                                    },
                                    "online": {
                                        "type": "number",
                                    }
                                },
                                "required": [
                                    "Avatar", "avatar", "id", "userId", "userName", "online"
                                ]
                            }
                        ]
                    },
                    "moreGirls": {
                        "type": "array",
                        "minItems": 0,
                        "default": []
                    },
                    "total": {
                        "type": "number"
                    },
                    "viewCount": {
                        "type": "number"
                    },
                },
                "required": [
                    "total", "total", "viewCount", "map_list"
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


def image_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "照片墙",
        "description": "我的等级",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "data": {
                "type": "object",
                "properties": {
                    "total": {
                        "type": "number",
                        "default": 0
                    },
                    "imagesList": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "coverFlag": {
                                        "type": "string",
                                        "default": "0"
                                    },
                                    "isBlcak": {
                                        "type": "number",
                                        "default": "0"
                                    },
                                    "isPrivate": {
                                        "type": "number",
                                        "default": "0"
                                    },
                                    "picHeight": {
                                        "type": "number",
                                        "default": "0"
                                    },
                                    "picId": {
                                        "type": "number",
                                        "default": "0"
                                    },
                                    "picWidth": {
                                        "type": "number",
                                        "default": "0"
                                    },
                                    "longThumbnailUrl": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "picUrl": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                },
                                "required": [
                                    "coverFlag", "isBlcak", "isPrivate", "picHeight", "picId", "picWidth",
                                    "longThumbnailUrl", "picUrl"
                                ]

                            }
                        ]
                    },


                },
                "required": [
                    "total", "imagesList"
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


def my_moment_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "我的日志",
        "description": "我的日志",
        "type": "object",
        "properties": {
            "code": {
                "type": "number",
                "default": 0
            },
            "data": {
                "type": "object",
                "properties": {
                    "momentsNum": {
                        "type": "number",
                        "default": 0
                    },
                    "momentsTotalNum": {
                        "type": "number",
                        "default": 0
                    },
                    "notReadCommentNum": {
                        "type": "number",
                        "default": 0
                    },
                    "viewMyself": {
                        "type": "number",
                        "default": 0
                    },
                    "mainType": {
                        "type": "string",
                        "default": "moments"
                    },
                    "momentsList": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "atUserList": {
                                        "type": "array",
                                        "default": []
                                    },
                                    "momentsId": {
                                        "type": "number",
                                    },
                                    "momentsId_str": {
                                        "type": "string",
                                    },
                                    "userId": {
                                        "type": "number",
                                    },
                                    "userName": {
                                        "type": "string",
                                    }
                                },
                                "required": [
                                    "atUserList", "momentsId", "momentsId_str", "userId",
                                    "userName"
                                ]

                            }
                        ]
                    },
                },
                "required": [
                    "mainType", "momentsList", "viewMyself", "notReadCommentNum", "momentsTotalNum", "momentsNum"
                ]
            }
        },
        "required": [
            "code", "data"
        ]
    }
    return assert_schema(request, schema)


