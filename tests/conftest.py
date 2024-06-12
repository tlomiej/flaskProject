import pytest
from mainapp import create_app, db
from playwright.sync_api import sync_playwright



@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False  # Wyłącz CSRF dla celów testowych
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

# @pytest.fixture(scope="module")
# def browser():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         yield browser
#         browser.close()
#
