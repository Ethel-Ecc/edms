from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
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
        new_user = User.query.filter_by(email=email.data).first()
        if new_user is None:
            raise ValidationError('There is no account with that email. Please register.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')




# add new dataset
class AddDatasetForm(FlaskForm):
    name_or_title = StringField('Name/Title', validators=[DataRequired(), Length(min=5)])
    distribution_license = SelectField('License',
                                       choices=[
                                            ('MIT License', 'MIT'),
                                            ('Apache License 2.0', 'Apache2.0'),
                                            ('BSD 3', 'BSD 3-Clause License (Revised)'),
                                            ('GPL v3', 'GNU General Public License v3'),
                                            ('LGPL v3', 'GNU Lesser General Public License v3 (LGPL-3.0)'),
                                                ],
                                       validators=[DataRequired()]
                                       )
    format = SelectField('Format',
                         choices=[
                             ('PDF', 'PDF'),
                             ('XML', 'XML'),
                             ('XLXS', 'XLXS'),
                             ('DOC', 'DOC'),
                             ('DOCX', 'DOCX'),
                             ('TEX', 'TEX'),
                         ],
                         validators=[DataRequired()])
    description = TextAreaField('Short Description', validators=[DataRequired(), Length(min=10)])
    download_url = StringField('Resource URL', validators=[DataRequired()])
    # download_url = FileField('Upload Resource', validators=[FileAllowed(['pdf', 'xlxs', 'doc', 'tex', 'docx', 'xml'])])
    submit = SubmitField('Save Dataset')
