from fastapi.testclient import TestClient
from v2_api.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_add_vitals_and_fetch():
    vitals_payload = {
        "patient_name": "Test Patient",
        "dob": "01/01/00",
        "vitals": {
            "blood_pressure": {"systolic": 120, "diastolic": 80},
            "heart_rate": 75,
            "respiratory_rate": 18,
            "temperature": 37.0,
            "oxygen_saturations": 98,
            "consciousness": "Yes"
        }
    }
    response = client.post("/add_vitals/", json=vitals_payload)
    assert response.status_code == 200
    data = response.json()
    assert "patient_id" in data
    assert "total_news2_score" in data

    patient_id = data["patient_id"]
    response = client.get(f"/patient/{patient_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)