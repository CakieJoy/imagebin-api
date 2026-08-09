from fastapi.testclient import TestClient

from main import app

client = TestClient(app)



def test_change_api_key_perm_success(new_key):
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post(f"/api/v2/update-permissions?entry_key={new_key}&new_permissions=rw", headers=header)
    assert response.status_code == 200

def test_change_api_key_perm_without_api_key(new_key):
    response = client.post(f"/api/v2/update-permissions?entry_key={new_key}&new_permissions=rw")
    assert response.status_code == 401

def test_change_api_key_perm_with_invalid_key(new_key):
    header = {"x-api-key": "727.invalid_key_btw"}
    response = client.post(f"/api/v2/update-permissions?entry_key={new_key}&new_permissions=rw", headers=header)
    assert response.status_code == 401

def test_change_api_key_perm_lost_queries():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/update-permissions", headers=header)
    assert response.status_code == 422

def test_change_api_key_perm_with_wrong_queries():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/update-permissions?entry_key=727.whenyouseeit&new_permissions=rw", headers=header)
    assert response.status_code == 404
