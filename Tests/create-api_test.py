from fastapi.testclient import TestClient

from main import app

client = TestClient(app)



def test_create_api_key_success():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/create-api-key/?new_key_permissions=rwa", headers=header)
    assert response.status_code == 200


def test_create_api_key_without_queries():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/create-api-key/", headers=header)
    assert response.status_code == 422


def test_create_api_key_without_api_key():
    response = client.post("/api/v2/create-api-key/?new_key_permissions=rwa")
    assert response.status_code == 401


def test_create_api_key_with_invalid_key():
    header = {"x-api-key": "1.adsadsadsadsadsad"}
    response = client.post("/api/v2/create-api-key/?new_key_permissions=rwa", headers=header)
    assert response.status_code == 401