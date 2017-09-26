#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import importlib
from . import global_settings

ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"


class Settings(object):
    def __init__(self):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            raise Exception('环境变量中未设置配置文件路径，os.environ["SETTINGS_MODULE"]="配置文件路径"')
        for name in dir(global_settings):
            if name.isupper():
                setattr(self, name, getattr(global_settings, name))

        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)
        for key in dir(mod):
            if key.isupper():
                value = getattr(mod, key)
                setattr(self, key, value)

    def __getattr__(self, name):
        return getattr(self, name)


settings = Settings()
