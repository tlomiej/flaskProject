import bcrypt

from mainapp import db, create_app
from mainapp.models import User
from mainapp.models import Collection
from mainapp.models import Forms
with create_app().app_context():
    db.create_all()

    #db.session.add(User(username='admin2', email='admi211@example.com', password=bcrypt.generate_password_hash('p@ss4App').decode('utf-8')
#))


    #db.session.commit()


    users = User.query.all()
    coll = Collection.query.all()
    print(coll)