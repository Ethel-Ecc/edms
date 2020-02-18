from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required

from edms import bcrypt, db
from edms.models import User, Dataset
from edms.users.forms import NewUserRegistrationForm, UserLoginForm, UserUpdateAccountForm, RequestPasswordResetForm, PasswordResetForm
from edms.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


"""
    This route and method handles the NewUserRegistrationForm
    :returns The new_user_registration.html page, using the contents from forms.py
"""
@users.route('/new_user_registration', methods=['GET', 'POST'])
def new_user_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    form = NewUserRegistrationForm()
    if form.validate_on_submit():
        new_user_hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=new_user_hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account successfully created. You are now able to log in', 'success')
        return redirect(url_for('users.user_login'))

    return render_template('pages/new_user_registration.html', title='New User Registration', form=form)


"""
    This route and method handles the UserLoginForm
    :returns The user_login.html page, using the contents from forms.py
"""


@users.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    form = UserLoginForm()
    if form.validate_on_submit():
        user_info = User.query.filter_by(email=form.email.data).first()
        if user_info and bcrypt.check_password_hash(user_info.password, form.password.data):
            login_user(
                user_info, remember=form.remember_me.data
            )
            next_page = request.args.get('next')
            flash(f'{user_info.username} successfully logged in', 'success')

            return redirect(next_page) if next_page else redirect(url_for('main.homepage'))  # this is ternary conditional

        flash('Login was Unsuccessful. Please recheck your Email and Password', 'danger')

    return render_template('pages/user_login.html', title='User Login', form=form)


@users.route('/user_logout')
def user_logout():
    logout_user()
    return redirect(url_for('main.homepage'))


@users.route('/user_account', methods=['GET', 'POST'])
@login_required
def user_account():
    form = UserUpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.user_avatar = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been successfully updated!', 'success')
        return redirect(url_for('users.user_account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    user_avatar = url_for('static', filename='img/' + current_user.user_avatar)

    return render_template('pages/user_account.html', title='user account', user_avatar=user_avatar, form=form)


# show only user specific post
@users.route('/user/<string:username>')
def user_datasets(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    datasets = Dataset.query.filter_by(owner=user)\
        .order_by(Dataset.date_added.desc())\
        .paginate(page=page, per_page=1)

    return render_template('pages/user_datasets.html', datasets=datasets, user=user)


@users.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RequestPasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.user_login'))

    return render_template('pages/reset_password_request.html', title='Request password reset', form=form)


@users.route('/reset_password_request/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('The token is invalid or expired.', 'warning')
        return redirect(url_for('users.reset_password_request'))

    form = PasswordResetForm()

    if form.validate_on_submit():
        new_hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = new_hashed_password
        db.session.commit()
        flash(f'Password successfully updated. You are now able to log in', 'success')
        return redirect(url_for('users.user_login'))

    return render_template('pages/reset_password.html', title='Reset Password', form=form)
