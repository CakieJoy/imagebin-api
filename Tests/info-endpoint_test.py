from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_info_endpoint():
    response = client.get("/api/info")
    assert response.status_code == 200