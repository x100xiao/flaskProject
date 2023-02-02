"""
@Author: 600490
@Email: xianrong.song@resvent.com
@FileName: models.py
@DataTime: 2023/01/10 19:47
"""
from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, comment="账号")    # 账号
    password = db.Column(db.String(200), nullable=False, comment="密码")    # 密码
    email = db.Column(db.String(100), nullable=False, unique=True, comment="邮箱唯一")  # 邮箱唯一
    join_time = db.Column(db.DateTime, default=datetime.now, comment="添加时间")    # 添加时间


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, comment="邮箱")
    captcha = db.Column(db.String(100), nullable=False, comment="验证码")


class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="id主键")
    title = db.Column(db.String(100), nullable=False, comment="标题")
    content = db.Column(db.Text, nullable=False, comment="内容")
    create_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), comment="发布者外键")
    # 关系
    author = db.relationship(UserModel, backref="questions")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="id主键")
    content = db.Column(db.Text, nullable=False, comment="评论内容")
    create_time = db.Column(db.DateTime, default=datetime.now, comment="评论创建时间")

    # 外键
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), comment="问题外键")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), comment="评论者外键")
    # 关系
    question = db.relationship(QuestionModel, backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="answers")

