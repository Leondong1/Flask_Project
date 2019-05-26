# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 22:20
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : __init__.py.py
@Software: PyCharm
'''
# 导入蓝图
from flask import Blueprint

# 创建蓝图对象
index_blu = Blueprint('index',__name__)


# 从当前包中导入views,目的是为了执行views.py中的代码，让各视图函数绑定到蓝图上
from . import views