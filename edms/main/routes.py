from flask import Blueprint, render_template, request
from edms.models import Dataset


main = Blueprint('main', __name__)


"""
    This route and method handles the contents of the landing/homepage
    :returns The homepage using the contents from the home page templates
"""
@main.route('/')
@main.route('/homepage')
def homepage():
    page = request.args.get('page', 1, type=int)
    datasets = Dataset.query.order_by(Dataset.date_added.desc()).paginate(page=page, per_page=3)
    return render_template('pages/homepage.html', datasets=datasets)


"""
    This route and method handles the contents of the about page
    :returns The about page, using the contents from the about page templates
"""
@main.route('/about')
def about():
    return render_template('pages/about.html', title='About')