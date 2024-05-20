from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from mainapp.models import User


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=4, max=32)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

  submit = SubmitField(
      'Sing up'
  )

  def validate_username(self, username):
    user = User.query.filter_by(username= username.data).first()
    if user:
      raise  ValidationError('That username is taken. Pleas choose another')

  def validate_email(self, email):
    user = User.query.filter_by(username= email.data).first()
    if user:
      raise  ValidationError('That email is taken. Pleas choose another')

class UpdateAccountForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=4, max=32)])
  email = StringField('Email', validators=[DataRequired(), Email()])

  picture = FileField("Update profile picture", validators=[FileAllowed(['jpg', 'png', 'svg'])])
  submit = SubmitField(
      'Update'
  )

  def validate_username(self, username):
    if username.data != current_user.username:
      user = User.query.filter_by(username= username.data).first()
      if user:
        raise  ValidationError('That username is taken. Pleas choose another')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(username= email.data).first()
      if user:
        raise  ValidationError('That email is taken. Pleas choose another')



class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')

  submit = SubmitField('Login')

class NewDataForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

    submit = SubmitField('Add')

