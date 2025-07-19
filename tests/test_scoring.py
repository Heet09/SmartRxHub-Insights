
import pandas as pd
import sys
import os

# Add the scripts directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.emar_risk_scoring import score_risk

def get_sample_emar_data_df(medication="Metformin", dose="20mg", patient_id="patient_1", allergies=[], primary_diagnosis="diabetes", medication_category="antidiabetic", route="oral", frequency="daily", is_prn=False, prescribing_doctor_id="doctor_1", administering_nurse_id="nurse_1", patient_location="general ward", administration_time_of_day="morning"):
    data = {
        "patient_id": [patient_id],
        "age": [60],
        "sex": ["female"],
        "weight": [70],
        "allergies": [allergies],
        "primary_diagnosis": [primary_diagnosis],
        "medication": [medication],
        "medication_category": [medication_category],
        "dose": [dose],
        "route": [route],
        "frequency": [frequency],
        "is_prn": [is_prn],
        "prescribing_doctor_id": [prescribing_doctor_id],
        "administering_nurse_id": [administering_nurse_id],
        "patient_location": [patient_location],
        "administration_time_of_day": [administration_time_of_day],
        "timestamp": [1678886400.0]
    }
    return pd.DataFrame(data)

def test_score_risk_low_risk():
    """Tests the score_risk function with data that should be low risk."""
    df = get_sample_emar_data_df()
    df_scored = score_risk(df)
    assert df_scored['predicted_risk'].iloc[0] == 'Low'

def test_score_risk_high_risk():
    """Tests the score_risk function with data that should be high risk."""
    # Example of high risk: antibiotic with penicillin allergy
    df = get_sample_emar_data_df(medication="Azithromycin", dose="250mg", medication_category="antibiotic", allergies=["penicillin"])
    df_scored = score_risk(df)
    assert df_scored['predicted_risk'].iloc[0] == 'High'
