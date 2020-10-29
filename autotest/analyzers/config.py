#!/usr/local/python3


class Config:
    def __init__(self, _api_config, _keywords_mod=None, _default_conn=None, _datadir=None, _confile=None):
        self.api_config = _api_config
        self.keywords_mod = _keywords_mod
        self.default_db_conn = _default_conn
        self.datapath = _datadir
        self.confile = _confile
