from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class loginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password=StringField('password',validators=[DataRequired()])
    remember_me=BooleanField('remember_me')
    submit=SubmitField('sigin_in')

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

# ...

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('repeat_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')