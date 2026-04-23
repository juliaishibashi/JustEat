import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, "/app")

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def get_token():
    def _get_token(client, username: str, password: str) -> str:
        response = client.post(
            "/auth/login",
            data={
                "username": username,
                "password": password,
            },
        )
        assert response.status_code == 200
        return response.json()["access_token"]

    return _get_token
