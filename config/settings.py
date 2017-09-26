#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

MODE = "AGENT"  # AGENT、SALT、SSH

SSH_USER = 'root'
SSH_PORT = 22
SSH_PRIVATE_KEY = "/home/auto/.ssh/id_rsa"

PLUGIN_DICT = {
    'basic': 'src.plugins.basic.Basic',
    'memory': 'src.plugins.memory.Memory',
    'cpu': 'src.plugins.cpu.Cpu',
    'disk': 'src.plugins.disk.Disk',
    'nic': 'src.plugins.nic.Nic',
    'board': 'src.plugins.board.Board',
}

# 资产信息API
ASSET_API = "http://127.0.0.1:8000/api/asset.html"
