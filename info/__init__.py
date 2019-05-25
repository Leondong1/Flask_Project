# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 20:03
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : __init__.py.py
@Software: PyCharm
'''
import redis
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_session import Session
from config import Config


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)


Migrate(app,db)


redis_store = redis.StrictRedis(host=Config.REDIS_HOST,
                                port=Config.REDIS_PORT)
# redis_store.set('123456', 'leon')

CSRFProtect(app)

Session(app)