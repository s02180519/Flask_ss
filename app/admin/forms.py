from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('register')


class RegisterUsers(FlaskForm):
    userNumber = StringField('Количество пользователей для добавления', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # password_repeat = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Создать пользователей')
