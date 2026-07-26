

from flask import render_template, redirect, url_for, flash

from app import app
from app.email import send_password_reset_email
from app.forms import loginForm, RegistrationForm, ResetPasswordForm
# from forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

from datetime import datetime

# ...

@app.before_request
def before_request():
    from app import db
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
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


@app.route('/user/<username>')
@login_required
def user(username):
    from app.models import User
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body':'Test post #1'},
        {'author': user, 'body':'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

from app.forms import EditProfileForm
# ...

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    from app.models import User
    from app import db
    form = EditProfileForm()
    from flask import request
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

#关注用户
@app.route('/follow/<username>')
@login_required
def follow(username):
    from app.models import User
    from app import db
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

# 取消用户关注
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    from app.models import User
    from app import db
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email

@app.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    from app.models import User
    from app import db
    # 如果用户已经登录，直接重定向到主页，不需要重置密码
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 创建表单实例
    form = ResetPasswordRequestForm()
    # 判断：POST提交 + 表单校验通过
    if form.validate_on_submit():
        # 根据邮箱查询用户
        user = User.query.filter_by(email=form.email.data).first()
        # 如果该邮箱存在对应的用户
        if user:
            # 发送重置密码邮件
            send_password_reset_email(user)
        # 无论邮箱是否存在，都给出相同提示（安全，防止攻击者探测邮箱）
        flash('Check your email for the instructions to reset your password')
        # 跳转到登录页面
        return redirect(url_for('login'))
    # GET请求 / 表单校验失败：渲染重置密码请求页面
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    from app.models import User
    from app import db
    # 如果用户已经登录，直接跳主页，无需重置密码
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 校验token，获取用户对象
    user = User.verify_reset_password_token(token)
    # token无效/过期，跳转首页
    if not user:
        return redirect(url_for('index'))
    # 实例化重置密码表单
    form = ResetPasswordForm()
    # POST提交表单验证
    if form.validate_on_submit():
        # 设置新密码（内部自动哈希加密）
        user.set_password(form.password.data)
        db.session.commit()
        # 闪现提示
        flash('Your password has been reset.')
        # 修改完成跳转登录页面
        return redirect(url_for('login'))
    # GET请求：渲染重置密码页面，展示输入新密码表单
    return render_template('reset_password.html', form=form)