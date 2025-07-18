
from fastapi.testclient import TestClient
import sys
import os

# Add the api directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app

client = TestClient(app)

def test_ingest_data_low_risk():
    """Tests the /ingest endpoint with data that should be low risk."""
    response = client.post("/ingest", json={"medication": "Metformin", "dose": "20mg"})
    assert response.status_code == 200
    assert response.json()["predicted_risk"] == "Low"

def test_ingest_data_high_risk():
    """Tests the /ingest endpoint with data that should be high risk."""
    response = client.post("/ingest", json={"medication": "Lisinopril", "dose": "10mg"})
    assert response.status_code == 200
    assert response.json()["predicted_risk"] == "High"

def test_ingest_data_unknown_medication():
    """Tests the /ingest endpoint with an unknown medication."""
    response = client.post("/ingest", json={"medication": "Aspirin", "dose": "100mg"})
    assert response.status_code == 200
    assert response.json()["error"] == "Unknown medication"
