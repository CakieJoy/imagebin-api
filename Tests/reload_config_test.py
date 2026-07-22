from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_reload_config_success():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/reload_config", headers=header)
    assert response.status_code == 200

def test_reload_config_without_api_key():
    response = client.post("/api/v2/reload_config")
    assert response.status_code == 401

def test_reload_config_with_invalid_api_key():
    header = {"x-api-key": "im_not_a_api_key_iam_a_teapot"}
    response = client.post("/api/v2/reload_config", headers=header)
    assert response.status_code == 403