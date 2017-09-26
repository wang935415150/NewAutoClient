#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.client import AutoAgent
from src.client import AutoSSH
from src.client import AutoSalt
from lib.config.conf import settings



def client():
    if settings.MODE == 'AGENT':
        cli = AutoAgent()
    elif settings.MODE == 'SSH':
        cli = AutoSSH()
    elif settings.MODE == 'SALT':
        cli = AutoSalt()
    else:
        raise Exception('请配置资产采集模式，如：ssh、agent、salt')
    cli.process()