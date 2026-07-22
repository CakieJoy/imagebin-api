from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



def test_delete_image_success(img_id):
    header = {"x-api-key": "1.very_secret_key_100_real"}
    response = client.delete(f"/api/v2/delete/?image_id={img_id}", headers=header)
    assert response.status_code == 200