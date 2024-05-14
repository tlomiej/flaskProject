from mainapp import app, db
from mainapp.models import User

with app.app_context():
    db.create_all()
    print('')

    db.session.add(User(username='admin1', email='admi111@example.com', password='pass'))

    db.session.commit()


    users = User.query.all()
    print(users)