import pytest

from app import create_app
from app.models import db

@pytest.fixture
def app():
    app = create_app("testing")

    yield app


@pytest.fixture(scope="function")
def database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield db