# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-26 21:37
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : __init__.py.py
@Software: PyCharm
'''
from flask import Blueprint

passport_blu = Blueprint("passport",__name__,
                         url_prefix='/passport')

from . import views