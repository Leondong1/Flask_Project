# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 22:20
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : views.py
@Software: PyCharm
'''
from flask import render_template, current_app, session

from info import constants
from info.models import User, News, Category
from . import index_blu

@index_blu.route('/')
def index():
    # 显示用户是否登录的逻辑
    # 获取到当前登录用户的id
    user_id = session.get("user_id",None)
    # 通过id获取用户信息
    user =None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 右侧新闻排行的逻辑
    new_list = None
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    click_new_list = []
    for news in news_list if news_list else []:
        click_new_list.append(news.to_basic_dict())

    categories = Category.query.all()
    categories_dicts = []
    for category in categories:
        categories.append(category.to_dict())

    return render_template('news/index.html',data = {"user_info":user.to_dict() if user else None,
                                                     "click_new_list":click_new_list,
                                                     "categories":categories_dicts})


# 在打开网页的时候，浏览器会默认去请求根路径 +favicon.ico作网站标签的小图标
# send_static_file 是flask 去查找指定的静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')



