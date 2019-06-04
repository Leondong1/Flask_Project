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

# 初始化数据库，在flask很多的扩展里面，咱们可以先初始化扩展的对象，然后再调用 init_app 去初始化
from info.utils.common import do_index_class

db = SQLAlchemy()
redis_store = None  # type: redis.StrictRedis


# (pyhton3.6 之后这样注释会显示提示,主要是用于全局变量，咱们在后面使用的时候希望有提示，可以使用标识变量的类型)

# 注意外界的导入不能导入局部变量
# 整个操作的目的是为了咱们的信息加载是从外界传递的，因为咱们的info目录上线后一般不做修改
def create_app(config_name):
    # 配置项目日志  并且根据传入的配置知道自己使用的是哪一个日志等级
    setup_log(config_name)

    app = Flask(__name__)

    # 通过名字加载指定的配置信息
    app.config.from_object(config[config_name])

    # app初始化
    db.init_app(app)

    # 数据库的迁移
    Migrate(app, db)

    global redis_store

    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST,
                                    port=config[config_name].REDIS_PORT, )
    # redis_store.set('123456', 'leon')
    # 开启当前项目的 CSRF 保护，只做服务器的验证功能
    # 帮我们做了：从cookie中随机取出随机值，从表单中取出随机值，然后进行校验，并且返回校验结果
    # 而我们的登录与注册不是使用的表单，是ajax请求，所以我们需要在ajax请求的时候带上咱们的csrf_token
    CSRFProtect(app)

    Session(app)

    app.add_template_filter(do_index_class,"index_class")

    @app.after_request
    def after_request(response):
        # 在返回响应的时候，生成一个随机的csrf_token 的值
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token", csrf_token)
        return response

    # 注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    return app


# 日志的配置信息仍然与咱们的业务逻辑相关，因此，放在info里面
def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限（相当于一个备份）
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
