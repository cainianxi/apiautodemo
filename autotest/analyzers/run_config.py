#!/usr/local/python3

from os.path import join, splitext
import random

from autotest.samples.yaml_sampler import YamlSampler


def get_log_conn(filename, env=None):
    try:
        log_conf = YamlSampler.read_yaml(filename).log
    except Exception:
        log_conf = None

    try:
        if env:
            return log_conf[env]
        else:
            for k, v in log_conf.items():
                if v.setdefault("default", False):
                    return log_conf[k]
            else:
                if len(log_conf) == 1:
                    k = list(log_conf.keys())[0]
                    return log_conf[k]
    except Exception:
        if env:
            raise Exception("获取log连接配置项失败：{}".format(env))
        else:
            print("获取log连接配置项失败：{}".format("default"))


def get_db_conn(filename, env=None):
    try:
        db_conf = YamlSampler.read_yaml(filename).db
    except Exception:
        db_conf = None

    try:
        if env:
            return dict(db_conf[env], **{"pool_name": env})
        else:
            for k, v in db_conf.items():
                if v.setdefault("default", False):
                    return dict(db_conf[k], **{"pool_name": k})
            else:
                if len(db_conf) == 1:
                    k = list(db_conf.keys())[0]
                    return dict(db_conf[k], **{"pool_name": k})
    except Exception:
        if env:
            raise Exception("获取数据库连接配置项失败：{}".format(env))
        else:
            print("获取数据库连接配置项失败：{}".format("default"))


def get_file_content(filename, datapath=None):
    datafile = join(datapath, filename)

    with open(datafile, encoding="UTF-8") as fp:
        content = fp.read()

    return content


def get_upload_file(filename, datapath=None):
    file_obj = []

    if isinstance(filename, str):
        file_obj.append(_get_upload_file("file", filename, datapath))
    elif isinstance(filename, dict):
        for key, value in filename.items():
            if isinstance(value, str):
                file_obj.append(_get_upload_file(key, value, datapath))
            elif isinstance(value, list):
                for v in value:
                    file_obj.append(_get_upload_file(key, v, datapath))
    elif isinstance(filename, list):
        for name in filename:
            file_obj.extend(get_upload_file(name, datapath))
    else:
        raise Exception("files元素格式不正确")

    return file_obj


def _get_upload_file(key, filename, datapath):
    return [key, (next(_get_random_filename()) + splitext(filename)[1], open(join(datapath, filename), "rb"))]


def _get_random_filename():
    yield "F" + str(random.randint(100000000, 999999999))
