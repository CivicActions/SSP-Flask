import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app(config_name="testing")
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def app_context(app):
    with app.app_context() as ctx:
        yield ctx
