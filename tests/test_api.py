from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

VALID_SESSION = {
    "Administrative": 0, "Administrative_Duration": 0.0,
    "Informational": 0, "Informational_Duration": 0.0,
    "ProductRelated": 1, "ProductRelated_Duration": 0.0,
    "BounceRates": 0.2, "ExitRates": 0.2,
    "PageValues": 0.0, "SpecialDay": 0.0,
    "Month": "Feb",
    "OperatingSystems": 1, "Browser": 1, "Region": 1, "TrafficType": 1,
    "VisitorType": "Returning_Visitor", "Weekend": False,
}

INVALID_SESSION = {
    **VALID_SESSION, "Month" : "X"
}

def test_predict_valid():
    response = client.post("/predict", json = VALID_SESSION)
    assert response.status_code == 200
    assert 0<= response.json()["score"] <=1

def test_predict_invalid():
    response = client.post("/predict", json = INVALID_SESSION)
    assert response.status_code == 422