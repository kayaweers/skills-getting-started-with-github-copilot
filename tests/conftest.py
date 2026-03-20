import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(scope="function", autouse=True)
def fresh_activities():
    """Reset in-memory activities after each test to avoid cross-test contamination."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app_module.app)
