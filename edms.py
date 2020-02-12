from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import NewUserRegistrationForm, UserLoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3b540e068213b34df30c333454d0b31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

"""
    A dataset list of doctionaries, where each dictionary represents a single dataset
"""

datasets = [
    {
        'owner': 'Ethelbert obinna',
        'name_or_title': 'Dataset 1',
        'distribution_license': 'MIT',
        'format': 'XLSX',
        'description': 'A population dataset for county X, NRW',
        'download_url': 'https://ckan-wit-documentation.readthedocs.io/_/downloads/en/latest/pdf/',
        'date_added': '21 April, 2020',
    },
    {
        'owner': 'Sven Bingert',
        'name_or_title': 'Dataset 2',
        'distribution_license': 'Open Source',
        'format': 'PDF',
        'description': 'Dataset for students experiments, Göttingen',
        'download_url': 'https://ckan-wit-documentation.readthedocs.io/_/downloads/en/latest/pdf/',
        'date_added': '23 July, 2020',
    }

]

"""
    This route and method handles the contents of the landing/homepage
    :returns The homepage using the contents from the home page templates
"""
@app.route('/')
@app.route('/homepage')
def homepage():
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
    form = NewUserRegistrationForm()
    if form.validate_on_submit():
        flash(f'Account successfully created for {form.username.data}.', 'success')
        return redirect(url_for('homepage'))
    return render_template('pages/new_user_registration.html', title='New User Registration', form=form)


"""
    This route and method handles the UserLoginForm
    :returns The user_login.html page, using the contents from forms.py
"""
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@dataset.com' and form.password.data == '123456':
            flash(f'{form.email.data} is successfully logged in.', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Login was Unsuccessful. Please recheck your username and password', 'danger')

    return render_template('pages/user_login.html', title='User Login', form=form)


"""
    This route and method handles the contents of the europe page
    :returns The ckan-wit web page for each continent
"""
@app.route('/ckan-wit/europe')
def ckan_wit(continent):
    return render_template('pages/ckan-wit/europe.html', title='ckan-wit/<continent>')


if __name__ == '__main__':
    app.run(debug=True)
