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


def test_reload_config():
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.post("/api/v2/reload_config", headers=header)
    assert response.status_code == 200