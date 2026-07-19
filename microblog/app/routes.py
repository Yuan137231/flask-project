from flask import render_template, redirect, url_for, flash

from app import app
from app.forms import loginForm,RegistrationForm
# from forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
@login_required
def index():
    # user={'username':'ysx'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title='Home',posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    from app.models import User
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=loginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or  not user.check_password(form.password.data):
            flash('Invalid username or password')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='login in',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    from app.models import User
    from app import db
    # 如果用户已经登录，直接跳首页，禁止重复注册
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 实例化注册表单
    form = RegistrationForm()
    # 判断表单是否提交并全部校验通过
    if form.validate_on_submit():
        # 创建用户对象，填入用户名、邮箱
        user = User(username=form.username.data, email=form.email.data)
        # 加密设置密码，不存储明文
        user.set_password(form.password.data)
        # 添加到数据库会话
        db.session.add(user)
        # 提交事务，真正存入数据库
        db.session.commit()
        # 弹出成功提示消息
        flash('Congratulations, you are now a registered user!')
        # 注册成功跳转登录页
        return redirect(url_for('login'))
    # GET访问 / 校验失败：重新渲染注册页面，把表单传给前端
    return render_template('register.html', title='Register', form=form)