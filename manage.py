# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-23 19:59
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : manage.py.py
@Software: PyCharm
'''
import redis
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_session import Session
from config import Config

app = Flask(__name__)

manager = Manager(app)




app.config.from_object(Config)
db = SQLAlchemy(app)


Migrate(app,db)
manager.add_command('db',MigrateCommand)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST,
                                port=Config.REDIS_PORT)
redis_store.set('123456', 'leon')

CSRFProtect(app)

Session(app)





# 与以上的方法一致 +pymysql
# import pymysql
# pymysql.install_as_MySQLdb()
# db.create_all()


@app.route('/index')
def index():
    return 'hello,leon'


if __name__ == '__main__':
    manager.run()
