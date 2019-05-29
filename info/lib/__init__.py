# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-27 11:55
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : __init__.py.py
@Software: PyCharm
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

db = SQLAlchemy(app)