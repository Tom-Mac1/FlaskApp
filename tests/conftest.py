import pytest
import os
import sys 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
from run import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret",
    )
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_client(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["access"] = 1
    return client


@pytest.fixture
def user_client(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 2
        sess["access"] = 0
    return client
