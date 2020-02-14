from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileStorage
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
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
class UserUpdateAccount(FlaskForm):
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


# add new dataset
class AddDataset(FlaskForm):
    name_or_title = StringField('Name/Title', validators=[DataRequired(), Length(min=5)])
    distribution_license = StringField('License', validators=[DataRequired()])
    format = StringField('Format', validators=[DataRequired()])
    description = StringField('Short Description', validators=[DataRequired(), Length(min=10)])
    download_url = StringField('Resource URL:')
    submit = SubmitField('Save Dataset')
