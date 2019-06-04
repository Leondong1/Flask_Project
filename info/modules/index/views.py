# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-25 22:20
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : views.py
@Software: PyCharm
'''
from flask import render_template, current_app, session

from info import constants, redis_store
from info.models import User, News, Category
from . import index_blu

@index_blu.route('/')
def index():
    # 显示用户是否登录的逻辑
    # 获取到当前登录用户的id
    user_id = session.get("user_id",None)
    # 通过id获取用户信息
    # 加上这句的含义是 因为即使后面 没有查到user,也不影响咱们的程序正常执行
    user =None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 右侧新闻排行的逻辑
    new_list = None
    # 该语句查询出来的是一个模型，及对应一个对象
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    # 定义一个空的字典列表，里面装的就是字典
    click_new_list = []
    # 遍历对象列表，将对象的字典添加到字典列表中
    for news in news_list if news_list else []:
        click_new_list.append(news.to_basic_dict())

    categories = Category.query.all()
    categories_dicts = []
    for category in categories:
        categories_dicts.append(category.to_dict())

    return render_template('news/index.html',data = {"user_info":user.to_dict() if user else None,
                                                     "click_new_list":click_new_list,
                                                     "categories":categories_dicts})


# 在打开网页的时候，浏览器会默认去请求根路径 +favicon.ico作网站标签的小图标
# send_static_file 是flask 去查找指定的静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')



