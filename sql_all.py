# coding=utf-8
from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import pymysql

app=Flask(__name__)
bootstrap=Bootstrap(app)

# 配置数据库的地址URI , 格式 "数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:pwd@localhost/CTFManagement"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY']='yigemima'

db=SQLAlchemy(app)

"""
使用ORM实现数据库
"""

class Student(db.Model):
    __tablename__='students'
    __abstract=True
    name=db.Column(db.String(15),nullable=False)
    gender=db.Column(db.String(5),nullable=True)
    id=db.Column(db.Integer,primary_key=True)
    major=db.Column(db.String(255),nullable=False)
    admins=db.relationship('Admin',backref='stu',uselist=False)
    players=db.relationship('Player',backref='stu',uselist=False)

    def __repr__(self):
        return '<Student %r>' % self.name

class Admin(db.Model):
    __tablename__='admins'
    stu_id=db.Column(db.Integer,db.ForeignKey('students.id'),primary_key=True)
    admin_num=db.Column(db.String(35),nullable=True)
    admin_pwd=db.Column(db.String(35),nullable=True)
    def __repr__(self):
        return '<Admin %r>' % self.admin_num

class Player(db.Model):
    __tablename__='players'
    stu_id=db.Column(db.Integer,db.ForeignKey('students.id'),primary_key=True)
    guiding_teacher_name=db.Column(db.String(15),db.ForeignKey('teachers.name'))
    player_num=db.Column(db.String(35),nullable=True)
    sol_num=db.Column(db.Integer,default=0,nullable=False)
    solve_questions=db.relationship('Solve',backref='ques')
    def __repr__(self):
        return '<Player %r>' % self.player_num

class Question(db.Model):
    __tablename__ ='questions'
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text)
    besolved = db.relationship('Solve', backref='solved')
    def __repr__(self):
        return '<Question %r>' % self.kind

class Teacher(db.Model):
    __tablename__='teachers'
    name=db.Column(db.String(15),primary_key=True)
    guided_players=db.relationship('Player',backref='stus')
    def __repr__(self):
        return '<Teacher %r>' % self.name

class Solve(db.Model):
    __tablename__='solve'
    solve_tag=db.Column(db.Integer,primary_key=True,nullable=True)
    player_id=db.Column(db.Integer,db.ForeignKey('players.stu_id'))
    que_id=db.Column(db.Integer,db.ForeignKey('questions.id'))
    def __repr__(self):
        return '<Solve %r>' % self.que_id

def init():
    db.create_all()
    admin_1=Admin(
        stu_id=123456,
        admin_num="admin",
        admin_pwd="pwd")
    stu_1=Student(
        name="admin",
        gender="male",
        id=123456,
        major="IS"
    )
    db.session.add(admin_1)
    db.session.add(stu_1)
    db.session.commit()