import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from ckan_wit.src import wit_main


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3b540e068213b34df30c333454d0b31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edms.db'  # The /// are a relative path from this current file.
# It means the edms.db file should be created along side this python module we are currently in.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # this creates an SQLAlchemy database instance.
bcrypt = Bcrypt(app)  # used for user authentication
login_manager = LoginManager(app)  # this is used to handle user login session
login_manager.login_view = 'user_login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'ethel.christos@gmail.com'
app.config['MAIL_PASSWORD'] = '!!!Excellence2019AMEN...'
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)
wit_res = wit_main.ckan_wit_main()

from edms import routes

