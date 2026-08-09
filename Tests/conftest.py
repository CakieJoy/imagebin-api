import pytest
from fastapi.testclient import TestClient

from main import app, limiter

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

@pytest.fixture()
def new_key():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/create-api-key/?new_key_permissions=rwa", headers=header)
    new_key = response.json()["api_key"]
    yield new_key
