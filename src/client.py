#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from config import settings
from src.plugins import PluginManager
from concurrent.futures import ThreadPoolExecutor


class AutoBase(object):
    def __init__(self):
        self.asset_api = settings.ASSET_API

    def get_asset(self):
        """
        get方式向获取未采集的资产
        :return: {"data": [{"hostname": "c1.com"}, {"hostname": "c2.com"}], "error": null, "message": null, "status": true}
        """
        response = requests.get(url=self.asset_api)
        return response.json()

    def post_asset(self, msg):
        """
        post方式向街口提交资产信息
        :param msg:
        :return:
        """
        requests.post(url=self.asset_api, json=msg)
        # print(msg)

    def process(self):
        """
        派生类需要继承此方法，用于处理请求的入口
        :return:
        """
        raise NotImplementedError('you must implement process method')


class AutoAgent(AutoBase):
    def process(self):
        """
        获取当前资产信息
        :return:
        """
        server_info = PluginManager().exec_plugin()
        self.post_asset(server_info)


class AutoSSH(AutoBase):
    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        """
        task = self.get_asset()
        if not task['status']:
            return

        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run, hostname)
        pool.shutdown(wait=True)

    def run(self, hostname):
        server_info = PluginManager(hostname).exec_plugin()
        self.post_asset(server_info)


class AutoSalt(AutoBase):
    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        """
        task = self.get_asset()
        if not task['status']:
            return
        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run, hostname)
        pool.shutdown(wait=True)

    def run(self, hostname):
        server_info = PluginManager(hostname).exec_plugin()
        self.post_asset(server_info)
