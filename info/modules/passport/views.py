# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-26 21:37
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : views.py
@Software: PyCharm
'''
from flask import request, current_app, jsonify, make_response

from info import redis_store, constants
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
    name,text,image = captcha.generate_captcha()
    try:
    # 保存当前生成的图片验证码内容
        redis_store.setex('ImageCode_' + code_id,
                          constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify(errno = RET.DATAERR,errmsg = '保存图片验证码失败'))

    resp = make_response(image)

#     设置响应内容
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


