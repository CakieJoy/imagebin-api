from Tests.upload_test import test_upload_image_success, test_upload_image_with_invalid_api_key, test_upload_image_without_api_key, test_upload_image_without_image
from fastapi.testclient import TestClient
import pytest
from main import app
from main import limiter

client = TestClient(app)




@pytest.fixture(autouse=True)
def clear_rate_limit():
    limiter._storage.reset()
    yield

@pytest.fixture()
def img_id():
    files = {'image': ('test_image.jpg', b"Example data", 'image/jpeg')}
    header = {"x-api-key": "my_very_very_secret_api_key"}
    response = client.post("/v1/upload", headers=header, files=files)
    img_id = response.json()["image_id"]
    yield img_id


# * AuthV2 Tests


test_upload_image_success()

test_upload_image_without_image()

test_upload_image_without_api_key()

test_upload_image_with_invalid_api_key()

def test_get_images_authv2():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.get("/api/v2/get-images", headers=header)
    assert response.status_code == 200


def test_reload_config():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/reload_config", headers=header)
    assert response.status_code == 200