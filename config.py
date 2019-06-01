# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 19:51
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : config.py
@Software: PyCharm
'''
import redis
import logging


class Config(object):
    """工程的配置信息"""
    DEBUG = True

    SECRET_KEY = "abcdefghij"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:dongjie931207@127.0.0.1:3306/news_information"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis 配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # flask_session 的配置信息
    SESSION_TYPE = "redis"
    # 开启session签名，使得咱们的session 更加严密，具有保护功能
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,
                                      port=REDIS_PORT)
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2  # session 的有效期，单位是秒  此时代表两天

    # 设置日志等级
    LOG_LEVEL = logging.DEBUG


class DevelopementConfig(Config):
    """开发模式下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境下的配置"""
    LOG_LEVEL = logging.ERROR


class DevelopementConfig(Config):
    """单元测试环境下的配置"""
    DEBUG = True
    Testing = True


# 通过咱们的字典形式保存咱们的配置信息
config = {
    "development": DevelopementConfig,
    "production": ProductionConfig
}
