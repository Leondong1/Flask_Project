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
from config import config

db = SQLAlchemy()
redis_store = None

def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)



    Migrate(app,db)

    global redis_store

    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST,
                                    port=config[config_name].REDIS_PORT)
    # redis_store.set('123456', 'leon')

    CSRFProtect(app)

    Session(app)

    return app