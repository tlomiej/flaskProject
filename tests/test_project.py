# from mainapp.models import User
#
# from flask import url_for
#
# from playwright.sync_api import Page, expect
# import re
#
#
# def test_home(client):
#     response = client.get("/")
#     assert b"<title>Document</title>" in response.data
#
#
# def test_registration(client, app):
#     email = "test@test.com"
#     password = "Pa$$4App"
#     username = "testUser123"
#
#     response = client.post("/register", data={"email": email,
#                                               "password": password,
#                                               "confirm_password": password,
#                                               "username": username,
#                                               'submit': 'Sign Up'})
#
#
#     #form = RegistrationForm()
#     #assert form.validate_on_submit() == True
#
#     user = User.query.filter_by(username=username).first()
#     assert user is not None, "User was not created."
#     assert user.username == username
#     assert user.email == email
