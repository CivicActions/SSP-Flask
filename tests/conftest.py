"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app(config_name="testing")
    app.config["SERVER_NAME"] = "127.0.0.1:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def app_context(app):
    with app.app_context() as ctx:
        yield ctx
