import sys

import pytest


sys.path.append("./")

from main import create_app


@pytest.fixture(scope="session")
def client():
    app = create_app("config.TestingConfig")
    yield app.test_client()


@pytest.fixture(scope="function")
def single_use_client():
    app = create_app("config.SingleUseTestingConfig")
    yield app.test_client()
