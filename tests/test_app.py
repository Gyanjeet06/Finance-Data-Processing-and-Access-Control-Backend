from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Finance Backend is running"}


def test_auth_token_requires_credentials():
    response = client.post("/api/v1/auth/token", data={})
    assert response.status_code == 422
