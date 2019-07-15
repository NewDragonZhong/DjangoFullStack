# -*- coding: utf-8 -*-

import paramiko



class servers:
    def __init__(self,server_add,server_port,server_username,server_password):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # ssh 面签
        self.add = server_add
        self.port = server_port
        self.username = server_username
        self.password = server_password
        self.result_dic = {}  # 存储返回结果的字典表

    # 将系统调用执行完成的结果返回 给下一个函数进行处理
    def servers_link(self):
        self.ssh.connect(self.add,self.port,self.username,self.password) # 创建实例链接
        self.stdin,self.stdout,self.stderr = self.ssh.exec_command("free") # 执行系统调用
        self._stdin, self._stdout, self._stderr = self.ssh.exec_command("uptime")

        return self.stdout.read().decode('utf-8'),self._stdout.read().decode('utf-8')

    # 信息格式化(处理) 后返回
    def info_dispose(self):
        self.result,self._result = self.servers_link()
        self.list_title = self.result[:80].split(" ")
        self.list_comtent = self.result[84:160].split(" ")
        self._list = self._result.split(" ")

        while '' in self.list_title:
            self.list_title.remove('')
        while '' in self.list_comtent:
            self.list_comtent.remove('')
        while '' in self._list:
            self._list.remove('')

        for (x,y) in zip(self.list_title,self.list_comtent):
            self.result_dic[x] = y

        return self.result_dic,self._list

    # 断开连接
    def server_linke_close(self):

        return  self.ssh.close()
