
import pandas as pd
import sys
import os

# Add the scripts directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.emar_risk_scoring import risk_alert

def test_risk_alert_critical():
    """Tests the 'Avoid NSAIDs' alert."""
    row = pd.Series({'Condition': 'asthma', 'Allergy': 'nsaids'})
    assert risk_alert(row) == '⚠️ Avoid NSAIDs'

def test_risk_alert_kidney():
    """Tests the 'kidney-safe' alert."""
    row = pd.Series({'Condition': 'kidney disease', 'Allergy': 'None'})
    assert risk_alert(row) == '⚠️ Use kidney-safe medication'

def test_risk_alert_no_risk():
    """Tests the 'no critical risk' case."""
    row = pd.Series({'Condition': 'Hypertension', 'Allergy': 'None'})
    assert risk_alert(row) == '✅ No critical risk'
