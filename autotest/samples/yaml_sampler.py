#!/usr/local/python

"""
解析 yaml 文件
"""

import yaml

from autotest.utils.obj_dict import ObjDict


class YamlSampler:
    @classmethod
    def read_yaml(cls, filename):
        with open(filename, encoding='UTF-8') as f:
            doc = yaml.load(f)
        if isinstance(doc, dict):
            return ObjDict(doc)
        else:
            return doc

    @classmethod
    def read_json(cls, filename):
        return cls.read_yaml(filename)
