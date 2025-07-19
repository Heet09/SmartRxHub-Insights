
from fastapi.testclient import TestClient
import sys
import os

# Add the api directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app

client = TestClient(app)

def get_sample_emar_data(medication="Metformin", dose="20mg", patient_id="patient_1", allergies=[], primary_diagnosis="diabetes", medication_category="antidiabetic", route="oral", frequency="daily", is_prn=False, prescribing_doctor_id="doctor_1", administering_nurse_id="nurse_1", patient_location="general ward", administration_time_of_day="morning"):
    return {
        "patient_id": patient_id,
        "age": 60,
        "sex": "female",
        "weight": 70,
        "allergies": allergies,
        "primary_diagnosis": primary_diagnosis,
        "medication": medication,
        "medication_category": medication_category,
        "dose": dose,
        "route": route,
        "frequency": frequency,
        "is_prn": is_prn,
        "prescribing_doctor_id": prescribing_doctor_id,
        "administering_nurse_id": administering_nurse_id,
        "patient_location": patient_location,
        "administration_time_of_day": administration_time_of_day,
        "timestamp": 1678886400.0
    }

def test_ingest_data_low_risk():
    """Tests the /ingest endpoint with data that should be low risk."""
    data = get_sample_emar_data(medication="Metformin", medication_category="antidiabetic")
    response = client.post("/ingest", json=data)
    assert response.status_code == 200
    assert response.json()["predicted_risk"] == "Low"

def test_ingest_data_high_risk():
    """Tests the /ingest endpoint with data that should be high risk."""
    # Example of high risk: antibiotic with penicillin allergy
    data = get_sample_emar_data(medication="Lisinopril", dose="40mg", medication_category="antihypertensive")
    response = client.post("/ingest", json=data)
    assert response.status_code == 200
    assert response.json()["predicted_risk"] == "High"

def test_ingest_data_unknown_medication():
    """Tests the /ingest endpoint with an unknown medication."""
    data = get_sample_emar_data(medication="UnknownDrug", medication_category="unknown")
    response = client.post("/ingest", json=data)
    assert response.status_code == 200
    assert response.json()["error"] == "Unknown medication: 'UnknownDrug'"
