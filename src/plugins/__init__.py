#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
import importlib
from lib.config.conf import settings


class PluginManager(object):
    def __init__(self, hostname=None):
        self.plugin_dict = settings.PLUGIN_DICT
        self.mode = settings.MODE
        self.debug = settings.DEBUG

        if self.mode == 'SSH':
            self.ssh_user = settings.SSH_USER
            self.ssh_port = settings.SSH_PORT
            self.ssh_private_key = settings.SSH_PRIVATE_KEY

        self.hostname = hostname

    def exec_plugin(self):
        response = {}
        for name, item in self.plugin_dict.items():
            module_path, cls_name = item.rsplit('.', 1)
            cls = getattr(importlib.import_module(module_path), cls_name)

            result = {'status': True, 'data': None}
            try:
                if not hasattr(cls, 'initial'):
                    content = cls().process(self.command, self.debug)
                else:
                    content = cls.initial().process(self.command, self.debug)
                result['data'] = content
            except Exception as e:
                error_msg = "[%s][%s] plugin error: %s" % (
                    self.hostname if self.hostname else 'Agent', cls_name, traceback.format_exc())
                result['status'] = False
                result['data'] = error_msg

            response[name] = result

        return response

    def command(self, cmd):
        if self.mode == 'SALT':
            return self.__salt_cmd(cmd)
        elif self.mode == 'AGENT':
            return self.__agent_cmd(cmd)
        elif self.mode == 'SSH':
            return self.__ssh_cmd(cmd)
        else:
            raise Exception('请配置采集资产的模式，模式选项有：SALT、AGENT、SSH')

    def __salt_cmd(self, cmd):
        import salt.client
        local = salt.client.LocalClient()
        result = local.cmd(self.hostname, 'cmd.run', [cmd])
        return result[self.hostname]

    def __agent_cmd(self, cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def __ssh_cmd(self, cmd):
        import paramiko

        private_key = paramiko.RSAKey.from_private_key_file(self.ssh_private_key)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result
