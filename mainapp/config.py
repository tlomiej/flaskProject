import os

class Config:
    SECRET_KEY = '4af1676bcc923bbdd62b174e858f53e7'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site2.db'


    MAIL_SERVER = 'smtp.o2.pl'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
