import bcrypt

from mainapp import app, db
from mainapp.models import User

with app.app_context():
    db.create_all()


    db.session.add(User(username='admin1', email='admi111@example.com', password=bcrypt.generate_password_hash('p@ss4App').decode('utf-8')
))
    db.session.commit()


    users = User.query.all()
    print(users)