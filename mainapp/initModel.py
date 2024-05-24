import bcrypt

from mainapp import db, create_app
from mainapp.models import User
from mainapp.models import Collection
from mainapp.models import Forms
with create_app().app_context():
    db.create_all()


    #db.session.add(User(username='admin2', email='admi211@example.com', password=bcrypt.generate_password_hash('p@ss4App').decode('utf-8')
#))

    db.session.add(Forms(user_id='adad', title='Form 3', form='''
    {
        "fields": [
            {"name": "title", "type": "StringField", "label": "Title 1666", "validators": ["DataRequired"]},
            {"name": "content", "type": "TextAreaField", "label": "Content1666", "validators": ["DataRequired"]},
            {"name": "content2", "type": "TextAreaField", "label": "Content2666", "validators": ["DataRequired"]},
            {"name": "content3", "type": "TextAreaField", "label": "Content3666", "validators": ["DataRequired"]}
        ],
        "submit": {"label": "Add +"}
    }
    '''
     ))
    db.session.commit()


    users = User.query.all()
    coll = Collection.query.all()
    print(coll)