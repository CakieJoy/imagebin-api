from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



def test_delete_api_key_success(new_key):
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.delete(f"/api/v2/delete-api-key?entry_key={new_key}", headers=header)
    assert response.status_code == 200

def test_delete_api_key_without_key(new_key):
    response = client.delete(f"/api/v2/delete-api-key?entry_key={new_key}")
    assert response.status_code == 401

def test_delete_api_key_without_queries():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.delete(f"/api/v2/delete-api-key", headers=header)
    assert response.status_code == 422

def test_delete_api_key_with_wrong_key(new_key):
    header = {"x-api-key": "aasdadsadsa"}
    response = client.delete(f"/api/v2/delete-api-key?entry_key={new_key}", headers=header)
    assert response.status_code == 400

def test_delete_api_key_with_wrong_query(new_key):
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.delete(f"/api/v2/delete-api-key?entry_key=727.whenyouseeit", headers=header)
    assert response.status_code == 404