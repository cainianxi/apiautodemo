#!/usr/bin/python
# -*- coding: utf-8 -*-
# 这个是全局变量


def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


def delete_dict(key):
    return _global_dict.pop(key)
