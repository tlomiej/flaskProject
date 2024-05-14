from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY']= '4af1676bcc923bbdd62b174e858f53e7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'
db = SQLAlchemy(app)

from mainapp import routes