"""
@Author: 600490
@Email: xianrong.song@resvent.com
@FileName: auth.py
@DataTime: 2023/01/10 19:43
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginFrom
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginFrom(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("用户不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):

                session['user_id'] = user.id
                # return "ok"
                return redirect("/")
            else:
                print("密码错误！")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/loginout")
def loginout():
    session.clear()
    return redirect("/")


@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits*4
    captcha = random.sample(source, 4)
    print(captcha)
    captcha = "".join(captcha)
    # I/O: Input/Output 耗时
    message = Message(subject='flask注册验证码', recipients=[email], body=f'您的验证码是：{captcha}')
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code": 200, "message": "", "data": None})


# @bp.route("/mail/test")
# def mail_test():
#     msg = Message(subject='cs', recipients=["1002567463@qq.com"], body='zhegeshi sfds')
#     mail.send(msg)
#     return "ok"

