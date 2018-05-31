#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: liangzhibang@baidu.com
# Date: 2018-05-29

__author__ = "liangzhibang@baidu.com"
__date__ = '2018/5/29'

import base64
import zlib

from IPython.core import ultratb


def gnucompress(buf):
    return base64.b64encode(zlib.compress(buf))


def random_useragent():
    pass


def try_except(errors=(Exception)):
    def decorate(func):
        def wrappers(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors:
                ipshell = ultratb.FormattedTB(mode='Context', color_scheme='LightBG', call_pdb=1)
                ipshell()

        return wrappers

    return decorate
