from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

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



from edms import routes

