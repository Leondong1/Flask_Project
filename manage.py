# -*- coding: utf-8 -*-
'''
@Time    : 2019-05-23 19:59
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : manage.py.py
@Software: PyCharm
'''
from flask import Flask


app = Flask(__name__)

@app.route('/index')
def index():
    return 'hello,leon'

if __name__ == '__main__':
    app.run(debug=True)

