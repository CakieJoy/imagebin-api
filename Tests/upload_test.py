from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_upload_image_success():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    files = {'image': ('test_image.jpg', b"Example data", 'image/jpeg')}

    response = client.post("/api/v2/upload", headers=header, files=files)

    assert response.status_code == 200

def test_upload_image_without_image():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    files = {}

    response = client.post("/api/v2/upload", headers=header, files=files)

    assert response.status_code == 422

def test_upload_image_without_api_key():
    header = {}
    files = {'image': ('test_image.jpg', b"Example data", 'image/jpeg')}

    response = client.post("/api/v2/upload", headers=header, files=files)

    assert response.status_code == 401

def test_upload_image_with_invalid_api_key():
    header = {"x-api-key": "im_not_a_api_key_iam_a_teapot"}
    files = {'image': ('test_image.jpg', b"Example data", 'image/jpeg')}

    response = client.post("/api/v2/upload", headers=header, files=files)

    assert response.status_code == 403

