from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    fullname = StringField('Full Name', [validators.DataRequired()])
    email = EmailField('ur email', [validators.DataRequired()])
    username = StringField('uzanto', [
        validators.DataRequired(),
        validators.Length(min=4, max=20)
    ])
    password = PasswordField('ur pass', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='password gotta match'),
        validators.Length(min=4, max=40)
    ])
    confirm = PasswordField('repeat pwd')


class LoginForm(FlaskForm):
    username = StringField('username', [
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.Length(min=4, max=40)
    ])