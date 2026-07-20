from Tests.upload_test import test_upload_image_success, test_upload_image_with_invalid_api_key, test_upload_image_without_api_key, test_upload_image_without_image
from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

@pytest.fixture
def upload_image_id():
    files = {'image': ('test_image.jpg', b"Example data", 'image/jpeg')}
    header = {"x-api-key": "my_very_very_secret_api_key"}
    response = client.post("/v1/upload", headers=header, files=files)
    img_id = response.json()["image_id"]
    yield img_id

def test_upload_image():
    header = {"x-api-key": "my_very_very_secret_api_key"}
    files = {'image': ('test_image.jpg', b"Example data", 'image/jpeg')}

    response = client.post("/v1/upload", headers=header, files=files)

    assert response.status_code == 200

def test_delete_image(upload_image_id):
    header = {"x-api-key": "my_very_very_secret_api_key"}
    response = client.delete(f"/v1/delete/?image_id={upload_image_id}", headers=header)
    assert response.status_code == 200

def test_reload_config():
    header = {"x-api-key": "my_very_very_secret_api_key"}
    response = client.post("/v1/reload_config", headers=header)
    assert response.status_code == 200

def test_get_images():
    header = {"x-api-key": "my_very_very_secret_api_key"}
    response = client.get("/v1/get-images", headers=header)
    assert response.status_code == 200



# * AuthV2 Tests
def test_get_images_authv2():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.get("/api/v2/get-images", headers=header)
    assert response.status_code == 200

test_upload_image_success()

test_upload_image_without_image()

test_upload_image_without_api_key()

test_upload_image_with_invalid_api_key()

def test_delete_image(upload_image_id):
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.delete(f"/api/v2/delete/?image_id={upload_image_id}", headers=header)
    assert response.status_code == 200

def test_reload_config():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/reload_config", headers=header)
    assert response.status_code == 200