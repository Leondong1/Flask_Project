# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 19:51
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : config.py
@Software: PyCharm
'''
import redis


class Config(object):
    """工程的配置信息"""
    DEBUG = True

    SECRET_KEY = "abcdefghij"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:dongjie931207@127.0.0.1:3306/news_information"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis 配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # flask_session 的配置信息
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,
                                      port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 86400   # session 的有效期，单位是秒

class DevelopementConfig(Config):
    """开发模式下的配置"""

    DEBUG = True

class ProductionConfig(Config):
    """生产环境下的配置"""
    pass


config = {
    "development":DevelopementConfig,
    "production":ProductionConfig
}