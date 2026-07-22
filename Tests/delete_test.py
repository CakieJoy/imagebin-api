from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



def test_delete_image_success(img_id):
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.delete(f"/api/v2/delete/?image_id={img_id}", headers=header)
    assert response.status_code == 200


def test_delete_image_without_image_id():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.delete("/api/v2/delete/", headers=header)
    assert response.status_code == 422


def test_delete_image_without_api_key(img_id):
    response = client.delete(f"/api/v2/delete/?image_id={img_id}")
    assert response.status_code == 401

def test_delete_image_with_invalid_api_key(img_id):
    header = {"x-api-key": "im_not_a_api_key_iam_a_teapot"}
    response = client.delete(f"/api/v2/delete/?image_id={img_id}", headers=header)
    assert response.status_code == 403

def test_delete_image_with_invalid_img_id(img_id):
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.delete(f"/api/v2/delete/?image_id=im-a-teapot-really-silly3", headers=header)
    assert response.status_code == 404