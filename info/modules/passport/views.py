# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-26 21:37
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : views.py
@Software: PyCharm
'''

import random
import re
from datetime import datetime

from flask import request, current_app, jsonify, make_response, session

from info import redis_store, constants, db
from info.lib.yuntongxun.sms import CCP
from info.models import User
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu


@passport_blu.route('/image_code')
def get_image_code():
    """
    获取图片验证码
    :return:
    """
    # 1.获取到当前的图片编号id
    code_id = request.args.get('code_id')
    # 2.生成验证码
    name, text, image = captcha.generate_captcha()
    try:
        # 保存当前生成的图片验证码内容
        redis_store.setex('ImageCode_' + code_id,
                          constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify(errno=RET.DATAERR, errmsg='保存图片验证码失败'))

    resp = make_response(image)

    #     设置响应内容
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


@passport_blu.route('/smscode',methods = ['POST'])
def send_sms():
    """
        1. 接收参数并判断是否有值
        2. 校验手机号是正确
        3. 通过传入的图片编码去redis中查询真实的图片验证码内容
        4. 进行验证码内容的比对
        5. 生成发送短信的内容并发送短信
        6. redis中保存短信验证码内容
        7. 返回发送成功的响应
        :return:
    """
    args_data = request.json
    mobile = args_data.get('mobile')
    image_code = args_data.get('image_code')
    image_code_id = args_data.get('image_code_id')

    if not all([mobile, image_code, image_code_id]):
        #         参数不全
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    if not re.match("^1[3578][0-9]{9}$", mobile):
        return jsonify(errno=RET.DATAERR, errmsg='手机号不正确')

    try:
        real_image_code = redis_store.get("ImageCode_" +
                                          image_code_id)
        if real_image_code:
            real_image_code = real_image_code.decode()
            redis_store.delete("ImageCode_" + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg="获取图片验证码失败")

    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码已过期")

    if image_code.lower() != real_image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg='验证码输入错误')

    try:
        user = User.query.filter_by(mobile).first()
    except Exception as e:
        user = None
        current_app.logger.error(e)

    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg="该手机已经被注册")

    # 5.生成短信的内容并发送短信
    result = random.randint(0, 999999)
    sms_code = "%06d" % result
    current_app.logger.debug('短信验证码的内容：%s' % sms_code)
    result = CCP().send_template_sms(mobile, [sms_code,
                                              constants.SMS_CODE_REDIS_EXPIRES / 60], "1")
    if result != 0:
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信失败')

    try:
        redis_store.set("SMS_" + mobile, sms_code,
                        constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码失败")

    return jsonify(errno=RET.OK, errmsg="发送成功")


@passport_blu.route('/register', methods=["POST"])
def register():
    """
       1. 获取参数和判断是否有值
       2. 从redis中获取指定手机号对应的短信验证码的
       3. 校验验证码
       4. 初始化 user 模型，并设置数据并添加到数据库
       5. 保存当前用户的状态
       6. 返回注册的结果
         :return:
    """
    # 1.获取参数和判断是否有值
    json_data = request.json
    mobile = json_data.get("mobile")
    sms_code = json_data.get("smscode")
    password = json_data.get("password")

    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    # 2.从redis 中获取指定手机号对应的短信验证码
    try:
        real_sms_code = redis_store.get("SMS_" + mobile)
    except Exception as e:
        current_app.logger.error(e)

        return jsonify(errno=RET.DBERR, errmsg="获取本地验证码失败")

    if not real_sms_code:
        #         短信验证码过期
        return jsonify(errno=RET.NODATA, errmsg="短信验证码过期")

    real_sms_code = real_sms_code.decode()

    # 3. 校验验证码
    if sms_code != real_sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

    # 4. 初始化 user 模型，并设置数据并添加到数据库
    user = User()
    user.nick_name = mobile
    user.mobile = mobile
    user.last_login = datetime.now()
    # 对密码进行处理
    user.password = password


    try:
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

        return jsonify(errno=RET.DATAERR, errmsg="数据保存错误")

    #     5. 保存用户登录状态
    session["user_id"] = user.id
    session["nick_name"] = user.nick_name
    session["mobile"] = user.mobile

    #     6.返回注册结果
    return jsonify(errno=RET.OK, errmsg="OK")


@passport_blu.route('/login', methods=['POST'])
def login():


    """
    1. 获取参数和判断是否有值
    2. 从数据库查询出指定的用户
    3. 校验密码
    4. 保存用户登录状态
    5. 返回结果
    :return:
    """
#     1. 获取参数和判断是否有值
    json_data = request.json

    mobile = json_data.get("mobile")
    password = json_data.get("password")

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误")

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户不存在")

    if not user.check_passowrd(password):
        return jsonify(errno=RET.PWDERR, errmsg="密码错误")

    session["user_id"] = user.id
    session["nick_name"] = user.nick_name
    session["mobile"] = user.mobile

    user.last_login = datetime.now()

    try:
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

    return jsonify(errno=RET.OK, errmsg="OK")

@passport_blu.route("/logout",methods = ['POST'])
def logout():
    """
    清除session中的对应登录之后保存的信息
    :return:
    """
    session.pop('user_id',None)
    session.pop('nick_name',None)
    session.pop('mobile',None)

    return jsonify(errno = RET.OK,errmsg = "OK")
