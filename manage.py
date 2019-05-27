# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-23 19:59
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : manage.py.py
@Software: PyCharm
'''

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from info import db, create_app
import pymysql
from info import models



# create_app 就类似于工厂方法
app = create_app('development')

from config import config

# 添加扩展命令行

manager = Manager(app)

# 数据库的迁移
Migrate(app,db)
manager.add_command('db',MigrateCommand)
pymysql.install_as_MySQLdb()


# 与以上的方法一致 +pymysql
# import pymysql
# pymysql.install_as_MySQLdb()
# db.create_all()



if __name__ == '__main__':
    # print(app.url_map)
    manager.run()
