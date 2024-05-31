from datetime import datetime
#from itsdangerous import URLSafeTimedSerializer as Serializer
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mainapp import db, login_manager
from flask_login import UserMixin
from flask import current_app
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='defaultUser.svg')
    password = db.Column(db.String(60), nullable=False)

    collection = db.relationship('Collection', backref='author', lazy=True)
    forms = db.relationship('Forms', backref='author', lazy=True)
    formsdata = db.relationship('Formsdata', backref='author', lazy=True)

    #def get_reset_token(self, expires_sec=1800):
        #s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        #return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        #s = Serializer(current_app.config['SECRET_KEY'])
        #try:
           # user_id = s.loads(token)['user_id']
        #except:
        #    return None
       # return User.query.get(user_id)
        return None
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Collection(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    title = db.Column(db.String(180), nullable=False)
    content = db.Column(db.String(180), nullable=False)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='nodata.svg')

    def __repr__(self):
        return f"Data('{self.user_id}', '{self.title}', '{self.image_file}')"


class Forms(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(1800))
    form = db.Column(db.String(6000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #formsdata = db.relationship('Formsdata', backref='form', lazy=True)



class Formsdata(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    form_id = db.Column(db.Integer, nullable=False)
    data = db.Column(db.String(8000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"Data('{self.form_id}, {self.data}')"

