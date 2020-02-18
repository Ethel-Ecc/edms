from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from edms.cfg import Config
from ckan_wit.src import wit_main as m


db = SQLAlchemy()  # this creates an SQLAlchemy database instance.
bcrypt = Bcrypt()  # used for user authentication

login_manager = LoginManager()  # this is used to handle user login session
login_manager.login_view = 'users.user_login'
login_manager.login_message_category = 'info'

mail = Mail()
wit_res = m.ckan_wit_main()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.__init__(app)
    bcrypt.__init__(app)
    login_manager.__init__(app)
    login_manager.__init__(app)
    login_manager.__init__(app)
    mail.__init__(app)

    from edms.users.routes import users
    from edms.datasets.routes import datasets
    from edms.main.routes import main
    from edms.wit.routes import wit
    from edms.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(datasets)
    app.register_blueprint(main)
    app.register_blueprint(wit)
    app.register_blueprint(errors)

    return app