from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from mainapp.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from mainapp import routes
    from mainapp.users.routes import users
    from mainapp.datas.routes import datas
    from mainapp.main.routes import main
    from mainapp.errors.handlers import errors
    from mainapp.forms.routes import forms


    app.register_blueprint(users)
    app.register_blueprint(datas)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(forms)

    return app






