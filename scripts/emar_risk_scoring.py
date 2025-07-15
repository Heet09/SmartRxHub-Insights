
import pandas as pd
from datetime import datetime
import os
import numpy as np

# Function to generate more diverse simulated patient data
def generate_patient_data(num_patients=100):
    patient_ids = [f'P{i:03d}' for i in range(1, num_patients + 1)]
    conditions = np.random.choice(['Asthma', 'Diabetes', 'Kidney Disease', 'Hypertension', 'Arthritis', 'None'], size=num_patients)
    allergies = np.random.choice(['NSAIDs', 'Penicillin', 'Sulfa', 'None', 'Pollen', 'Dust'], size=num_patients)

    data = {
        'Patient_ID': patient_ids,
        'Condition': conditions,
        'Allergy': allergies
    }
    return pd.DataFrame(data)

df = generate_patient_data(num_patients=50) # Generate 50 patients for demonstration

# Define simple rule-based alerts
def risk_alert(row):
    if row['Condition'].lower() == 'asthma' and 'nsaid' in row['Allergy'].lower():
        return '⚠️ Avoid NSAIDs'
    elif row['Condition'].lower() == 'kidney disease':
        return '⚠️ Use kidney-safe medication'
    else:
        return '✅ No critical risk'

df['Alert'] = df.apply(risk_alert, axis=1)

# Save report
timestamp = datetime.now().strftime("%Y-%m-%d")
report_path = os.path.join("reports", "emar_risk_report.csv")
df.to_csv(report_path, index=False)

print(f"EMAR Risk Report saved at: {report_path}")
