import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY']= '4af1676bcc923bbdd62b174e858f53e7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#TODO
#app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_SERVER'] = 'smtp.o2.pl'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

mail = Mail(app)

from mainapp import routes