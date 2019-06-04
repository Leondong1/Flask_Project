# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-04 16:07
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : common.py
@Software: PyCharm
'''
# 公用的自定义工具类

def do_index_class(index):
    """返回指定索引所对应的类名"""
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"
    else:
        return ""


