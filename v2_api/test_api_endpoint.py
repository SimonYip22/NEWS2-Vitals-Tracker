from fastapi.testclient import TestClient
from v2_api.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_add_vitals_and_fetch():
    vitals_payload = {
        "Blood pressure": {"systolic": 120, "diastolic": 80},
        "Heart rate": 75,
        "Respiratory rate": 18,
        "Temperature": 37.0,
        "Oxygen saturations": 98,
        "Level of consciousness (fully awake and responsive?)": "Yes"
    }

    response = client.post(
        "/add_vitals/?patient_name=Test Patient&dob=01/01/00",
        json=vitals_payload
    )

    assert response.status_code == 200
    data = response.json()
    assert "patient_id" in data
    assert "total_news2_score" in data

    patient_id = data["patient_id"]
    response = client.get(f"/patient/{patient_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)