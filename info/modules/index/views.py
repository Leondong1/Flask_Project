# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 22:20
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : views.py
@Software: PyCharm
'''
from flask import render_template, current_app, session

from info.models import User
from . import index_blu

@index_blu.route('/')
def index():
    # 获取到当前登录用户的id
    user_id = session.get("user_id",None)
    # 通过id获取用户信息
    user =None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    return render_template('news/index.html',data = {"user_info":user.to_dict() if user else None})


# 在打开网页的时候，浏览器会默认去请求根路径 +favicon.ico作网站标签的小图标
# send_static_file 是flask 去查找指定的静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')



