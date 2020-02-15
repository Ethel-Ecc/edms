from flask import render_template, url_for, flash, redirect, request
from edms import app, db, bcrypt
from edms.forms import NewUserRegistrationForm, UserLoginForm, UserUpdateAccount, AddDataset
from edms.models import User, Dataset
from flask_login import login_user, current_user, logout_user, login_required
from ckan_wit.src import wit_main



dataset_test = [
    {
        'owner': 'Ethelbert Obinna',
        'name_or_title':'Dataset 1',
        'distribution_license': 'MIT',
        'format': 'PDF',
        'description': 'A population dataset for county X, NRW',
        'download_url': 'https://ckan-wit-documentation.readthedocs.io/_/downloads/en/latest/pdf/',
        'date_added': '23 February, 2020'
    },
    {
        'owner': 'Markus Lindner',
        'name_or_title': 'Dataset 2',
        'distribution_license': 'Open Source',
        'format': 'HTML',
        'description': 'Dataset for students experiments, Göttingen',
        'download_url': 'https://ckan-wit-documentation.readthedocs.io/en/latest',
        'date_added': '20 August, 2020'
    },
    {
        'owner': 'Sven Bingert',
        'name_or_title': 'Dataset 3',
        'distribution_license': 'Python Package',
        'format': 'PyPI',
        'description': 'CKAN-WIT: An API Wrapper for CKAN Open Data Portals',
        'download_url': 'https://test.pypi.org/project/ckan-wit/',
        'date_added': '12 April, 2020'
    },
]

"""
    This route and method handles the contents of the landing/homepage
    :returns The homepage using the contents from the home page templates
"""
@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('pages/homepage.html', dataset_test=dataset_test)


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


@app.route('/user_account', methods=['GET', 'POST'])
@login_required
def user_account():
    form = UserUpdateAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account successfully updated!', 'success')
        return redirect(url_for('user_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    user_avatar = url_for('static', filename='img/' + current_user.user_avatar)
    return render_template('pages/user_account.html',
                           title='user account',
                           user_avatar=user_avatar,
                           form=form
                           )

# the add dataset routes
@app.route('/add_dataset', methods=['GET', 'POST'])
def add_dataset():
    form = AddDataset()
    return render_template('pages/add_dataset.html', title='Add Dataset', form=form)



# CKAN-WIT methods
"""
    This route and method handles the contents of the europe page
    :returns The ckan-wit web page for each continent
"""
@app.route('/ckan-wit/europe')
def europe():
    continent = "Europe's Dataset"
    wit_europe = wit_main.verify_acquire()
    return render_template('pages/ckan-wit/europe.html', title=f'{continent}', wit_europe=wit_europe)


"""
    This route and method handles the contents of the America page
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

