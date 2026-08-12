from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_info_endpoint():
    response = client.get("/api/v2/info")
    assert response.status_code == 200