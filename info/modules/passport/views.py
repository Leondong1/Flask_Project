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

from flask import request, current_app, jsonify, make_response

from info import redis_store, constants
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


@passport_blu.route('/smscode')
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
        return jsonify(error = RET.DBERR,errmsg = "获取图片验证码失败")

    if not real_image_code:
        return jsonify(errno = RET.NODATA,errmsg = "验证码已过期")

    if image_code.lower() != real_image_code.lower():
        return jsonify(errno = RET.DATAERR,errmsg = '验证码输入错误')

    try:
        user = User.query.filter_by(mobile).first()
    except Exception as e:
        user = None
        current_app.logger.error(e)

    if user:

        return jsonify(errno = RET.DATAEXIST,errmsg = "该手机已经被注册")

    # 5.生成短信的内容并发送短信
    result = random.randint(0,999999)
    sms_code = "%06d" % result
    current_app.logger.debug('短信验证码的内容：%s'% sms_code)
    result = CCP().send_template_sms(mobile,[sms_code,
                                             constants.SMS_CODE_REDIS_EXPIRES / 60],"1")
    if result != 0:
        return jsonify(errno = RET.THIRDERR,errmsg = '发送短信失败')

    try:
        redis_store.set("SMS_" + mobile,sms_code,
                        constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR , errmsg = "保存短信验证码失败")

    return jsonify(errno = RET.OK ,errmsg = "发送成功")


