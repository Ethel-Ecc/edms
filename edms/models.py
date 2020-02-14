from datetime import datetime
from edms import db, login_manager
from flask_login import UserMixin


# decorated function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
    A dataset list of dictionaries, where each dictionary represents a single dataset
"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_avatar = db.Column(db.String(30), nullable=False, default='default.jpg')
    password = db.Column(db.String(70), nullable=False)
    datasets = db.relationship('Dataset', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_avatar}')"


# user_1 = User(username='user1', email='user1@user1.com', password='user1user1')
# user_2 = User(username='user2', email='user2@user2.com', password='user2user2')
# user_3 = User(username='user3', email='user3@user3.com', password='user3user3')


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_or_title = db.Column(db.String(120), nullable=False)
    distribution_license = db.Column(db.String(30), nullable=False)
    format = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    download_url = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Dataset('{self.name_or_title}', '{self.distribution_license}', '{self.format}', '{self.download_url}', '{self.date_added}')"

# dataset_1 = Dataset(name_or_title='Dataset 1', distribution_license='MIT', format='PDF', description='A population dataset for county X, NRW',
#                     download_url='https://ckan-wit-documentation.readthedocs.io/_/downloads/en/latest/pdf/')
# dataset_2 = Dataset(name_or_title='Dataset 2', distribution_license='Open Source', format='HTML', description='Dataset for students experiments, Göttingen',
#                     download_url='https://ckan-wit-documentation.readthedocs.io/en/latest/')
# dataset_3 = Dataset(name_or_title='Dataset 3', distribution_license='PythonPackage', format='PyPI', description='CKAN-WIT: An API Wrapper for CKAN Open Data Portals',
#                     download_url='https://test.pypi.org/project/ckan-wit/')
