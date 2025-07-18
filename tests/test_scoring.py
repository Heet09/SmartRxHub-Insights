
import pandas as pd
import sys
import os

# Add the scripts directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.emar_risk_scoring import score_risk

def test_score_risk_low_risk():
    """Tests the score_risk function with data that should be low risk."""
    data = {
        'patient_id': ['P001'],
        'medication': ['Metformin'],
        'dose': ['20mg'],
        'condition': ['Diabetes'],
        'allergy': ['None']
    }
    df = pd.DataFrame(data)
    df_scored = score_risk(df)
    assert df_scored['Predicted_Risk'].iloc[0] == 'Low'

def test_score_risk_high_risk():
    """Tests the score_risk function with data that should be high risk."""
    data = {
        'patient_id': ['P002'],
        'medication': ['Lisinopril'],
        'dose': ['10mg'],
        'condition': ['Hypertension'],
        'allergy': ['None']
    }
    df = pd.DataFrame(data)
    df_scored = score_risk(df)
    assert df_scored['Predicted_Risk'].iloc[0] == 'High'
