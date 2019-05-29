# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 20:03
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : __init__.py.py
@Software: PyCharm
'''
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_wtf.csrf import generate_csrf

from config import config

db = SQLAlchemy()
redis_store = None

def create_app(config_name):

    # 配置项目日志
    setup_log(config_name)

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)

    Migrate(app,db)

    global redis_store

    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST,
                                    port=config[config_name].REDIS_PORT,)
    # redis_store.set('123456', 'leon')

    CSRFProtect(app)

    Session(app)

    @app.after_request
    def after_request(response):
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token",csrf_token)
        return response


    # 注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    return app

def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)