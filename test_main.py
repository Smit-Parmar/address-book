from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_user_address():
    response = client.get("address/1?lat=12.982077&long=78.682568&distance=150")
    assert response.status_code == 200
    assert response.json() == [
        {
            "address_detail": "Bengaluru",
            "lat": 13.18457,
            "long": 77.479279,
            "id": 3
        }
        ]