"""
@Author: 600490
@Email: xianrong.song@resvent.com
@FileName: decorators.py
@DataTime: 2023/01/17 14:12
"""
from functools import wraps
from flask import redirect, url_for, g


def login_required(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner


# @login_required
# def public_question(question_id):
#     pass
# # 上面三行等价于下面一行
# login_required(public_question)(question_id)

