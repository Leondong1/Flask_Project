# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 22:20
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : views.py
@Software: PyCharm
'''
from flask import render_template

from . import index_blu

@index_blu.route('/index')
def index():
    return render_template('news/index.html')

