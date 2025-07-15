
import pandas as pd
from datetime import datetime
import os

# Simulated patient condition data
data = {
    'Patient_ID': ['P001', 'P002', 'P003'],
    'Condition': ['Asthma', 'Diabetes', 'Kidney Disease'],
    'Allergy': ['NSAIDs', 'None', 'Penicillin']
}

df = pd.DataFrame(data)

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

print(f"✔️ EMAR Risk Report saved at: {report_path}")
