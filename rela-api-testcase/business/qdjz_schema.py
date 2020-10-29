#!/usr/bin/python3
from common import assert_schema


def config_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "配置接口返回体格式验证",
        "description": "配置接口返回体格式验证",
        "type": "object",
        "properties": {
            "code": {
                # "description": "The unique identifier for a book",
                "type": "integer",
                "minimum": 0
            },
            "data": {
                # "description": "book name",
                "type": "object",
                # "minLength": 3,
                # "maxLength": 30
                "properties": {
                    "app_init_adv": {
                        "type": "object",
                    },
                    "default_jump_page": {
                        "type": "string",
                        "default": "recommend"
                    },
                    "moment_detail_recommend_switch": {
                        "type": "string",
                    },
                    "nearby_ai_default_switch": {
                        "type": "string",
                    },
                    "roam_world_hot_city": {
                        "type": "string",
                    },
                    "withdrawHiddenVersions": {
                        "type": "string",
                    }
                },
                "required": [
                    "app_init_adv", "withdrawHiddenVersions", "roam_world_hot_city", "moment_detail_recommend_switch",
                    "default_jump_page"
                ]
            }
        },
        "required": [
            "code", "data"
        ]
    }
    return assert_schema(request, schema)


def init_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "初始化数据",
        "description": "初始化数据",
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
                # "minLength": 3,
                # "maxLength": 30
                "properties": {
                    "IMServer": {
                        "type": "array",
                        "maxItems": 2
                    },
                    "audit": {
                        "type": "integer",
                        "default": 0
                    },
                    # "autoSubscribe": {
                    #     "type": "integer",
                    #     "default": 0
                    # },
                    # "defaultFollowCount": {
                    #     "type": "integer",
                    #     "default": 10
                    # },
                    # "enablePubLive": {
                    #     "type": "integer",
                    #     "minimum": 1
                    # },
                    # "freshMan": {
                    #     "type": "integer",
                    #     "minimum": 0
                    # },
                    #
                    # "httpsSwitch": {
                    #     "type": "integer",
                    #     "minimum": 0
                    # },

                    "level": {
                        "type": "integer",
                        "minimum": 0
                    },
                    "permApplyUrl": {
                        "type": "string",
                        "format": 'uri'
                    },
                    "topLink": {
                        "type": "string",
                        "format": 'uri'
                    },
                    "rtmpUrls": {
                        "type": "array",
                        "maxItems": 1
                    },

                    "flvInfos": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "bucket": {
                                        "type": "string",
                                        "default": "rela-live",
                                    },
                                    "host": {
                                        "type": "string",
                                        "default": "pili-live-hdl.rela.me",
                                    },
                                    "suffix": {
                                        "type": "string",
                                        "default": "",
                                    },
                                    "type": {
                                        "type": "string",
                                    }
                                },
                                "required": [
                                    "bucket", "host", "suffix", "type"
                                ]
                            }
                        ]
                    },
                    "multiFlvInfos": {
                        "type": "array",
                        "items": [{
                            "properties": {
                                "bucket": {
                                    "type": "string",
                                    "default": "live",
                                },
                                "host": {
                                    "type": "string",
                                    "default": "flv.pili-pull-baidu.rela.me",
                                },
                                "suffix": {
                                    "type": "string",
                                    "default": "",
                                },
                                "type": {
                                    "type": "string",
                                    "default": "qiniu",
                                }
                            },
                            "required": [
                                "bucket", "host", "suffix", "type"
                            ]
                        }]
                    }
                },
                "required": [
                    "IMServer", "audit", "rtmpUrls", "topLink", "permApplyUrl", "level",
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


def myinfo_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "我的信息",
        "description": "我的信息",
        "type": "object",
        "properties": {
            "code": {
                # "description": "The unique identifier for a book",
                "type": "integer",
                "default": 0
            },
            "data": {
                # "description": "book name",
                "type": "object",
                # "minLength": 3,
                # "maxLength": 30
                "properties": {
                    "badges": {
                        "type": "array",
                        "maxItems": 0
                    },
                    "nearByUsers": {
                        "type": "array",
                        "maxItems": 0
                    },
                    "age": {
                        "type": "string",
                    },
                    "userName": {
                        "type": "string",
                    },
                    "picUrl": {
                        "type": "string",
                        "format": 'uri'
                    },
                    "avatar": {
                        "type": "string",
                        "format": 'uri'
                    },
                    "bgImage": {
                        "type": "string",
                        "format": 'uri'
                    },
                    "birthday": {
                        "type": "string",
                        "format": 'date'
                    },
                    "gold": {
                        "type": "integer",
                        "default": 0
                    },
                    "userLevel": {
                        "type": "integer",
                        "default": 0
                    },
                    "id": {
                        "type": "integer",
                        "minimum": 0
                    },
                    "intro": {
                        "type": "string",
                    },
                    "match": {
                        "type": "object",
                        "properties": {
                            "likeCount": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "notReplyMeCount": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "recentLikeMeCount": {
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": [
                            "likeCount", "notReplyMeCount", "recentLikeMeCount"
                        ]
                    }
                },
                "required": [
                    "badges", "match", "intro", "id", "userLevel", "gold", "birthday",
                    "bgImage", "avatar", "picUrl", "userName", "age", "nearByUsers"
                ]
            }
        },
        "required": [
                "code", "data"
            ]
    }
    return assert_schema(request, schema)


def moments_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "推荐日志",
        "description": "推荐日志",
        "type": "object",
        "properties": {
            "code": {
                # "description": "The unique identifier for a book",
                "type": "integer",
                "minimum": 0
            },
            "data": {
                # "description": "book name",
                "type": "object",
                # "minLength": 3,
                # "maxLength": 30
                "properties": {
                    "cursor": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 20
                    },
                    "haveNextPage": {
                        "type": "boolean",
                    },
                    "momentsList": {
                        "type": "array",
                        "maxItems": 20,
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "winkUserList": {
                                        "type": "array",
                                        "minItems": 0,
                                    },
                                    "momentsId": {
                                        "type": "number"
                                    },
                                    "momentsId_str": {
                                        "type": "string"
                                    },
                                    "momentsText": {
                                        "type": "string"
                                    },
                                    "nickname": {
                                        "type": "string"
                                    },
                                    "userId": {
                                        "type": "number"
                                    },
                                    "atUserList": {
                                        "type": "array",
                                        "default": []
                                    }
                                },
                                "required": [
                                    "winkUserList", "momentsId", "momentsId_str", "momentsText",
                                    "nickname", "userId"
                                ]
                            }
                        ]
                    }
                },
                "required": [
                    "cursor", "haveNextPage", "momentsList"
                ]
            }
        },
        "required": [
            "code", "data"
        ]
    }
    return assert_schema(request, schema)


def zy_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "资源配置接口",
        "description": "资源配置接口",
        "type": "object",
        "properties": {
            "code": {
                # "description": "The unique identifier for a book",
                "type": "integer",
                "default": 0,
                "minimum": 0
            },
            "data": {
                # "description": "book name",
                "type": "object",
                # "minLength": 3,
                # "maxLength": 30
                "properties": {
                    "list": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "advertTitle": {
                                        "type": "string"
                                    },
                                    "avatar": {
                                        "type": "string",
                                        "format": "uri"
                                    },
                                    "nickName": {
                                        "type": "string",
                                    },
                                    "type": {
                                        "type": "string",
                                    },
                                    "userId": {
                                        "type": "string",
                                        "default": "0"
                                    }
                                },
                                "required": [
                                    "advertTitle", "avatar", "nickName", "type", "userId"
                                ]
                            }
                        ]
                    }
                },
                "required": [
                    "list"
                ]
            }
        },
        "required": ["code", "data"]
    }
    return assert_schema(request, schema)


def theme_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "推荐日志",
        "description": "推荐日志",
        "type": "object",
        "properties": {
            "code": {
                "type": "integer",
                "minimum": 0
            },
            "data": {
                "type": "object",
                "properties": {
                    "cursor": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 20
                    },
                    "haveNextPage": {
                        "type": "boolean",
                    },
                    "list": {
                        "type": "array",
                        "maxItems": 20,
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "video": {
                                        "type": "object",
                                    },
                                    "id": {
                                        "type": "number"
                                    },
                                    "idStr": {
                                        "type": "string"
                                    },
                                    "text": {
                                        "type": "string",

                                    },
                                    "type": {
                                        "type": "string",
                                        "default": "theme"
                                    },
                                    "simpleReply": {
                                        "type": "object"
                                    },
                                    "authorAvatar": {
                                        "type": "string",
                                        "format": "uri",
                                        "default": ""
                                    },
                                    "image": {
                                        "type": "string",
                                        "format": "uri",
                                        "default": ""
                                    },
                                },
                                "required": [
                                    "video", "id", "idStr", "text",
                                    "type", "simpleReply", "authorAvatar", "image"
                                ]
                            }
                        ]
                    }
                },
                "required": [
                    "cursor", "haveNextPage", "list"
                ]
            }
        },
        "required": [
            "code", "data"
        ]
    }
    return assert_schema(request, schema)


def recommend_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "推荐用户",
        "description": "推荐用户",
        "type": "object",
        "properties": {
            "code": {
                "type": "integer",
                "minimum": 0
            },
            "data": {
                "type": "object",
                "properties": {
                    "cursor": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 60
                    },
                    "haveNextPage": {
                        "type": "boolean",
                    },
                    "list": {
                        "type": "array",
                        "maxItems": 60,
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "nickName": {
                                        "type": "string"
                                    },
                                    "userId": {
                                        "type": "number"
                                    },
                                    "userName": {
                                        "type": "string",

                                    },
                                    "avatar": {
                                        "type": "string",
                                        "format": "uri",
                                        "default": ""
                                    },
                                    "picList": {
                                        "type": "array",
                                        "maxItems": 9,
                                        "items": [
                                            {
                                                "type": "object",
                                                "properties": {
                                                    "longThumbnailUrl": {
                                                        "type": "string",
                                                        "format": "uri"
                                                    },
                                                    "picUrl": {
                                                        "type": "string",
                                                        "format": "uri"
                                                    },
                                                    "picId": {
                                                        "type": "number",
                                                    },
                                                    "picHeight": {
                                                        "type": "number",
                                                    },
                                                    "picWidth": {
                                                        "type": "number",
                                                    },

                                                },
                                                "required": [
                                                    "longThumbnailUrl", "picUrl", "picId", "picHeight",
                                                    "picWidth"
                                                ]
                                            }
                                        ]
                                    },
                                },
                                "required": [
                                    "nickName", "userId", "userName", "avatar"
                                ]
                            }
                        ]
                    }
                },
                "required": [
                    "cursor", "haveNextPage", "list"
                ]
            }
        },
        "required": [
            "code", "data"
        ]
    }
    return assert_schema(request, schema)


def arlist_api(request):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "ar礼物列表",
        "description": "ar礼物列表",
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "default": "1"
            },
            "data": {
                "type": "object",
                "properties": {
                    "arGiftMasterKey": {
                        "type": "string",
                    },
                    "list": {
                        "type": "array",
                        "minItems": 0,
                        "default": [],
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "arGiftId": {
                                        "type": "integer"
                                    },
                                    "arResource": {
                                        "type": "string",
                                        "default": "",
                                        "format": "uri",
                                    },
                                    "title": {
                                        "type": "string",
                                    },
                                    "id": {
                                        "type": "number",
                                    },
                                },
                                "required": [
                                    "arGiftId", "arResource", "title", "id"
                                ]
                            }
                        ]
                    }
                },
                "required": [
                    "arGiftMasterKey", "list"
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


def black_api(request):
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
                    "blackList": {
                        "type": "array",
                        "minItems": 0,
                        "default": []
                    },
                    "blackMeList": {
                        "type": "array",
                        "minItems": 0,
                        "default": []
                    }
                },
                "required": [
                    "blackList", "blackMeList"
                ]
            }
        },
        "required": [
            "result", "data"
        ]
    }
    return assert_schema(request, schema)


