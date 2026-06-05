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

