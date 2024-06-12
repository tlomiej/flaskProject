from mainapp.models import Forms

FORM_TITLE_NAME = 'tEST fORM'


def test_create_form(client):
    data = {
        "title": FORM_TITLE_NAME,
        "description": "Form description",
        "form":
            {
                "fields": [
                    {"name": "title", "type": "StringField", "label": "Title", "validators": ["DataRequired"]},
                    {"name": "content", "type": "TextAreaField", "label": "Content", "validators": ["DataRequired"]},
                    {"name": "x", "type": "TextAreaField", "label": "X", "validators": ["DataRequired"]},
                    {"name": "y", "type": "TextAreaField", "label": "Y", "validators": ["DataRequired"]},
                    {"name": "radio_element", "type": "RadioField", "label": "Radio Field",
                     "validators": ["DataRequired"],
                     "choices": [["M", "Male"], ["F", "Female"]]},
                    {"name": "bool_field", "type": "BooleanField", "label": "Remember me", "validators": []}
                ],
                "submit": {"label": "Add"}
            }

    }

    email = "test11@test.com"
    password = "Pa$$4App111"
    username = "testUser123111"

    client.post("/register", data={"email": email,
                                   "password": password,
                                   "confirm_password": password,
                                   "username": username,
                                   'submit': 'Sign Up'})

    client.post("/login", data={"email": email, "password": password})

    response = client.post('/newform', data=data)

    # print( Forms.query.all())
    form = Forms.query.filter_by(title=FORM_TITLE_NAME).first()

    assert form.title == FORM_TITLE_NAME


def test_list_form(client):
    test_create_form(client)
    response = client.post("/forms")
    assert b'article-title' in response.data


def test_form_view(client):
    test_create_form(client)
    response = client.post("/forms/1")

    assert FORM_TITLE_NAME.encode() in response.data
