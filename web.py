from flask import Flask,render_template,request,flash,redirect,url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms.widgets import HTMLString, html_params
from wtforms import Field
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from sql_all import *

#登陆界面的表单
class loginForm(FlaskForm):
    username=StringField('account',validators=[DataRequired()])
    password=StringField('password',validators=[DataRequired()])
    submit=SubmitField('Submit')

#注册页面的表单
class registerForm(FlaskForm):
    name=StringField('real name',validators=[DataRequired()])
    gender=StringField('male or female?',validators=[DataRequired()])
    id=StringField('your student number',validators=[DataRequired()])
    major=StringField('your major',validators=[DataRequired()])
    username = StringField('account', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    sign_up = SubmitField('Sign up')

#搜索学生的表单
class searchStu(FlaskForm):
    player_id=StringField('成员学号',validators=[DataRequired()])
    search=SubmitField('Search')

#增加选手的表单
class addStu(FlaskForm):
    name=StringField('选手姓名', validators=[DataRequired()])
    gender=StringField('选手性别', validators=[DataRequired()])
    id=StringField('选手学号', validators=[DataRequired()])
    major=StringField('选手专业', validators=[DataRequired()])
    isteacher=StringField('选手指导老师', validators=[DataRequired()])
    player_num=StringField('选手账号', validators=[DataRequired()])
    add_stu=SubmitField('Add_Student')

#添加题目的表单
class Add_que(FlaskForm):
    que_id=StringField('题目ID', validators=[DataRequired()])
    que_content=StringField('题目内容', validators=[DataRequired()])
    add_que=SubmitField('Add_Questions')

def del_queBy(del_id):
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="ctfmanagement",
        charset="utf8"
    )
    cursor=conn.cursor()
    sql="delete from questions where id=%s;"
    try:
        cursor.execute(sql,[del_id])
        conn.commit()
        return 1
    except Exception as e:
        conn.rollback()
        return -1
    cursor.close()
    conn.close()

def add_queBy(add_id,add_content):
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="ctfmanagement",
        charset="utf8"
    )
    cursor=conn.cursor()
    sql="insert into questions VALUES (%s,%s);"
    try:
        cursor.execute(sql,[add_id,add_content])
        conn.commit()
        return 1
    except Exception as e:
        conn.rollback()
        return -1
    cursor.close()
    conn.close()

#删除指定ID题目
class Del_ID_que(FlaskForm):
    que_id=StringField('题目ID', validators=[DataRequired()])
    del_que = SubmitField('删除该题')

def delete_que_by_id(del_id):
    try:
        deled_quetion=Question.query.filter_by(id=del_id).first()
        db.session.delete(deled_quetion)
        db.session.commit()
    except Exception as error:
        db.session.rollback()

@app.route('/login/',methods=['GET','POST'])
def login():
    error=None
    username=None
    password=None
    form=loginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        form.username.data=''
        form.password.data=''
    if username:
        user = Admin.query.filter_by(admin_num=username,admin_pwd=password).first()
        if user is not None:
            return redirect(url_for('index',username=username))
        else:
            return render_template('auth/login.html', form=form,error='用户名或者密码错误！')
    return render_template('auth/login.html',form=form,username=username,password=password)

@app.route('/register',methods=['GET','POST'])
def register():
    loginform=loginForm()
    registerform=registerForm()
    name=None
    gender=None
    id=None
    major=None
    username=None
    password=None
    if registerform.validate_on_submit():
        stu = Student(name=registerform.name.data,
                      gender=registerform.gender.data,
                      id=registerform.id.data,
                      major=registerform.major.data)
        admin=Admin(stu_id=registerform.id.data,
                    admin_num=registerform.username.data,
                    admin_pwd=registerform.password.data)
        db.session.add(stu)
        db.session.add(admin)
        db.session.commit()
        return  redirect('/login')
    return render_template('auth/register.html',form=registerform)

@app.route('/index/<username>',methods=['GET','POST'])
def index(username):
    return render_template('index.html',username=username)

@app.route('/playerAu',methods=['GET','POST'])
def playerAu():
    searchform=searchStu()
    s_id=None
    s_stu=None
    s_player=None
    if searchform.validate_on_submit():
        s_id=searchform.player_id.data
        s_player=Player.query.filter_by(stu_id=s_id).first()
        s_stu=Student.query.filter_by(id=s_id).first()
    all_players=Player.query.all()
    return render_template('auth/playerAu.html',all_players=all_players,s_player=s_player,s_stu=s_stu,form=searchform)

@app.route('/add',methods=['GET','POST'])
def add_stu():
    addform=addStu()
    if addform.validate_on_submit():
       added_stu = Student(name=addform.name.data,
                           gender=addform.gender.data,
                           id=addform.id.data,
                           major=addform.major.data)
       added_player = Player(stu_id=addform.id.data,
                             guiding_teacher_name=addform.isteacher.data,
                             player_num=addform.player_num.data)
       this_teacher_name=addform.isteacher.data
       this_teacher=Teacher.query.filter_by(name=this_teacher_name).first()
       if this_teacher is None:
           new_teacher=Teacher(name=this_teacher_name)
           db.session.add(new_teacher)
           db.session.commit()
       db.session.add(added_stu)
       db.session.add(added_player)
       try:
           db.session.commit()
           return redirect('/playerAu')
       except Exception as e:
           db.session.rollback()
           return render_template('auth/add.html',form=addform,error="重复输入或者该成员已是管理员！")
    return render_template('auth/add.html',form=addform,error=None)

@app.route('/del_player/<player_id>',methods=['GET','POST'])
def del_player(player_id):
    deled_player=Player.query.filter_by(stu_id=player_id).first()
    deled_stu=Student.query.filter_by(id=player_id).first()
    db.session.delete(deled_player)
    db.session.delete(deled_stu)
    db.session.commit()
    return redirect('/playerAu')

@app.route('/edit_player',methods=['GET','POST'])
def edit_player():
    return render_template('auth/edit_player.html')

@app.route('/queAu',methods=['GET','POST'])
def queAu():
    all_ques=Question.query.all()
    del_id_queform=Del_ID_que()
    if del_id_queform.validate_on_submit():
        flag=del_queBy(del_id_queform.que_id.data)
        if flag==1:
            return redirect('/queAu')
    return render_template('auth/queAu.html',error="题目管理",all_ques=all_ques,form=del_id_queform)

@app.route('/add_que',methods=['GET','POST'])
def add_ques():
    error=None
    addform=Add_que()
    if addform.validate_on_submit():
        flag=add_queBy(addform.que_id.data,addform.que_content.data)
        if flag==1:
            return redirect(url_for('queAu',error=None))
        else:
            return render_template('auth/add_que.html',form=addform,error="重复添加题目！")
    return render_template('auth/add_que.html',form=addform,error=error)

@app.route('/del_que/<que_id>',methods=['GET','POST'])
def del_ques(que_id):
    delete_que_by_id(que_id)
    return redirect('/queAu')

class editQue(FlaskForm):
    ID = StringField('题目ID', validators=[DataRequired()])
    content = StringField('题目内容', validators=[DataRequired()])
    edit = SubmitField('修改该题内容')

def edit_queBy(edit_id,edit_content):
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="ctfmanagement",
        charset="utf8"
    )
    cursor=conn.cursor()
    sql="update questions set content=%s where id=%s;"
    try:
        flag=cursor.execute(sql,[edit_content,edit_id])
        conn.commit()
        return flag
    except Exception as e:
        conn.rollback()
        return 0
    cursor.close()
    conn.close()


@app.route('/edit_que',methods=['GET','POST'])
def edit_ques():
    editform=editQue()
    if editform.validate_on_submit():
        flag=edit_queBy(editform.ID.data,editform.content.data)
        #print(flag)
        if flag==1:
            return redirect("/queAu")
        else:
            return render_template('auth/edit_que.html',form=editform,error="不存在该题或者没有更新内容！")
    return render_template('auth/edit_que.html',form=editform,error=None)

class solve_solutions(FlaskForm):
    que_id = StringField('题目ID', validators=[DataRequired()])
    player_id = StringField('选手ID', validators=[DataRequired()])
    solve_yes = SubmitField('该选手已回答该题')

@app.route('/solve_solution',methods=['GET','POST'])
def sol_solution():
    sol_form=solve_solutions()
    all_player=Player.query.all()
    if sol_form.validate_on_submit():
        if Player.query.filter_by(stu_id=sol_form.player_id.data).first() and Question.query.filter_by(id=sol_form.que_id.data).first():
            solved=Solve(player_id=sol_form.player_id.data,
                         que_id=sol_form.que_id.data
                         )
            db.session.add(solved)
            db.session.commit()
            return redirect('/solve_solution')
        else:
            return render_template('auth/solve_solution.html', form=sol_form, error="选手或者题目ID错误！",all_players=all_player)
    return render_template('auth/solve_solution.html',form=sol_form,error=None,all_players=all_player)