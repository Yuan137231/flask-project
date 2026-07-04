import os

from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
print(__name__)
print(app)
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///'+os.path.join(basedir, 'data.sqlite')
db=SQLAlchemy(app)
migrate = Migrate(app, db)

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' %self.name
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    role_id = db.Column(db.String(80), db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' %self.username
with app.app_context():
    db.create_all()
    admin_role = Role(name='Admin')
    mod_role = Role(name='Moderator')
    user_role = Role(name='User')
    user_john = User(username='john', role=admin_role)
    user_susan = User(username='susan', role=user_role)
    user_david = User(username='david', role=user_role)
    db.session.add(admin_role)
    db.session.add(mod_role)
    db.session.add(user_role)
    db.session.add(user_john)
    db.session.add(user_susan)
    db.session.add(user_david)
    db.session.commit()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role}

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user!=None:
            session['known']=True
        else:
            session['known']=False
            user=User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

# def index():
#     name = None
#     form = NameForm()
#
#     if form.validate_on_submit():
#         old_name = session.get('name')
#         if old_name is not None and old_name!=form.name.data:
#             flash("you change your name!")
#         name = form.name.data
#         session['name']=name
#         return redirect(url_for("index"))
#     name=session.get('name')
#     return render_template('index.html', form=form, name=name)

if __name__ == '__main__':
    app.run(debug=False)