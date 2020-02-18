from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo

from edms.models import User


class NewUserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        new_user = User.query.filter_by(username=username.data).first()
        if new_user:
            raise ValidationError('The username already exists. please choose a different username')

    def validate_email(self, email):
        new_user = User.query.filter_by(email=email.data).first()
        if new_user:
            raise ValidationError('The email already exists. Please choose a different email')


class UserLoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


# User Account Edit form
class UserUpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Info')

    def validate_username(self, username):
        if username.data != current_user.username:
            new_user = User.query.filter_by(username=username.data).first()
            if new_user:
                raise ValidationError('The username already exists. please choose a different username')

    def validate_email(self, email):
        if email.data != current_user.email:
            new_user = User.query.filter_by(email=email.data).first()
            if new_user:
                raise ValidationError('The email already exists. Please choose a different email')


class RequestPasswordResetForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

