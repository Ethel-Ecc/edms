import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from edms import app, db, bcrypt, mail
from edms.forms import NewUserRegistrationForm, UserLoginForm, UserUpdateAccountForm, AddDatasetForm, RequestPasswordResetForm, PasswordResetForm
from edms.models import User, Dataset
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from ckan_wit.src import wit_main


"""
    This route and method handles the contents of the landing/homepage
    :returns The homepage using the contents from the home page templates
"""


@app.route('/')
@app.route('/homepage')
def homepage():
    page = request.args.get('page', 1, type=int)
    datasets = Dataset.query.order_by(Dataset.date_added.desc()).paginate(page=page, per_page=1)
    return render_template('pages/homepage.html', datasets=datasets)


"""
    This route and method handles the contents of the about page
    :returns The about page, using the contents from the about page templates
"""


@app.route('/about')
def about():
    return render_template('pages/about.html', title='About')


"""
    This route and method handles the NewUserRegistrationForm
    :returns The new_user_registration.html page, using the contents from forms.py
"""


@app.route('/new_user_registration', methods=['GET', 'POST'])
def new_user_registration():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

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
        return redirect(url_for('user_login'))

    return render_template('pages/new_user_registration.html', title='New User Registration', form=form)


"""
    This route and method handles the UserLoginForm
    :returns The user_login.html page, using the contents from forms.py
"""


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = UserLoginForm()
    if form.validate_on_submit():
        user_info = User.query.filter_by(email=form.email.data).first()
        if user_info and bcrypt.check_password_hash(user_info.password, form.password.data):
            login_user(
                user_info, remember=form.remember_me.data
            )
            next_page = request.args.get('next')
            flash(f'{user_info.username} successfully logged in', 'success')

            return redirect(next_page) if next_page else redirect(url_for('homepage'))  # this is ternary conditional

        flash('Login was Unsuccessful. Please recheck your Email and Password', 'danger')

    return render_template('pages/user_login.html', title='User Login', form=form)


@app.route('/user_logout')
def user_logout():
    logout_user()
    return redirect(url_for('homepage'))


# This allows handling the user profile image.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, pic_file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + pic_file_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_filename)
    image_resize = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(image_resize)
    i.save(picture_path)

    return picture_filename


@app.route('/user_account', methods=['GET', 'POST'])
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
        return redirect(url_for('user_account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    user_avatar = url_for('static', filename='img/' + current_user.user_avatar)

    return render_template('pages/user_account.html', title='user account', user_avatar=user_avatar, form=form)


# This method handles the dataset option
def save_dataset(form_dataset):
    random_hex = secrets.token_hex(8)
    _, dataset_ext = os.path.splitext(form_dataset.filename)
    dataset_filename = random_hex + dataset_ext
    dataset_path = os.path.join(app.root_path, 'static/datasets', dataset_filename)
    form_dataset.save(dataset_path)

    return dataset_filename


# This handles add dataset routes
@app.route('/dataset/add', methods=['GET', 'POST'])
@login_required
def add_dataset():
    form = AddDatasetForm()
    if form.validate_on_submit():
        dataset_new = Dataset(
            name_or_title=form.name_or_title.data,
            distribution_license=form.distribution_license.data,
            format=form.format.data,
            description=form.description.data,
            download_url=form.download_url.data,
            owner=current_user
        )
        db.session.add(dataset_new)
        db.session.commit()

        flash('Dataset added successfully', 'success')

        return redirect(url_for('homepage'))

    return render_template('pages/add_dataset.html',
                           title='Add Dataset',
                           form=form,
                           legend='Add new dataset')


# This handles each dataset via its id
@app.route('/dataset/details/<int:dataset_id>')
def dataset_details(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    return render_template('pages/dataset.html', title=dataset.name_or_title, dataset=dataset)


# This handles each dataset via its id for updating.
@app.route('/dataset/details/<int:dataset_id>/update', methods=['GET', 'POST'])
@login_required
def dataset_update(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    if dataset.owner != current_user:
        abort(403)
    form = AddDatasetForm()

    if form.validate_on_submit():
        dataset.name_or_title = form.name_or_title.data
        dataset.distribution_license = form.distribution_license.data
        dataset.format = form.format.data
        dataset.description = form.description.data
        dataset.download_url = form.download_url.data

        db.session.commit()

        flash('dataset successfully updated', 'success')
        return redirect(url_for('dataset_details', dataset_id=dataset_id))

    elif request.method == 'GET':
        form.name_or_title.data = dataset.name_or_title,
        form.distribution_license.data = dataset.distribution_license,
        form.format.data = dataset.format,
        form.description.data = dataset.description
        form.download_url.data = dataset.download_url

    return render_template('pages/add_dataset.html',
                           title='Update Dataset',
                           form=form,
                           legend='Update Dataset'
                           )


@app.route('/dataset/<int:dataset_id>/delete', methods=['POST'])
@login_required
def delete_dataset(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    if dataset.owner != current_user:
        abort(403)

    db.session.delete(dataset)
    db.session.commit()
    flash('The dataset has been deleted successfully', 'success')
    return redirect(url_for('homepage'))


# show only user specific post
@app.route('/user/<string:username>')
def user_datasets(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    datasets = Dataset.query.filter_by(owner=user)\
        .order_by(Dataset.date_added.desc())\
        .paginate(page=page, per_page=1)

    return render_template('pages/user_datasets.html', datasets=datasets, user=user)


## handles user email and password reset
def send_reset_email(user):
    token = user.get_reset_token(),
    msg = Message('Password Reset Request',
                  sender='noreply@edms.com',
                  recipients=[user.email],
                  )
    msg.body = f''' To reset your password, use this link {url_for('reset_password', token=token, _external=True)}
If you did not make this request, simply ignore this message and no changes will be made
'''
    mail.send(msg)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RequestPasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('user_login'))

    return render_template('pages/reset_password_request.html', title='request password reset', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('The token is invalid or expired.', 'warning')
        return redirect(url_for('reset_password_request'))

    form = PasswordResetForm()

    if form.validate_on_submit():
        new_user_hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = new_user_hashed_password
        db.session.commit()

        flash(f'Password successfully updated. You are now able to log in', 'success')
        return redirect(url_for('user_login'))
    return render_template('pages/reset_password.html', title='Reset password', form=form)






# CKAN-WIT methods
"""
    This route and method handles the contents of the europe page
    :returns The ckan-wit web page for each continent
"""


@app.route('/ckan-wit/europe')
def europe():
    continent = "Europe's Dataset"
    # wit_europe = wit_main.verify_acquire()
    return render_template('pages/ckan-wit/europe.html', title=f'{continent}')


"""
    # This route and method handles the contents of the America page
    :returns The ckan-wit web page for each continent
"""


@app.route('/ckan-wit/americas')
def america():
    continent = "America's Dataset"
    return render_template('pages/ckan-wit/america.html', title=f'{continent}')


"""
    This route and method handles the contents of the Africa page
    :returns The ckan-wit web page for each continent
"""


@app.route('/ckan-wit/africa')
def africa():
    continent = "Africa's Dataset"
    return render_template('pages/ckan-wit/africa.html', title=f'{continent}')


"""
    This route and method handles the contents of the Asia page
    :returns The ckan-wit web page for each continent
"""


@app.route('/ckan-wit/asia')
def asia():
    continent = "Asia's Dataset"
    return render_template('pages/ckan-wit/asia.html', title=f'{continent}')
