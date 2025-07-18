
import pandas as pd
#from datetime import datetime
import os
import joblib
import json
import random

# --- Load Model and Features ---
model = joblib.load('ml/emar_risk_model.joblib')
with open('ml/model_features.json', 'r') as f:
    model_features = json.load(f)

# --- Data Generation ---
def generate_emar_data(num_records=100):
    """Generates simulated eMAR data with conditions and allergies."""
    patient_ids = [f'P{i:03d}' for i in range(1, num_records + 1)]
    medications = ["Lisinopril", "Metformin", "Simvastatin", "Amlodipine"] * (num_records // 4)
    doses = ["10mg", "20mg", "40mg", "50mg"] * (num_records // 4)
    conditions = ["Hypertension", "Diabetes", "High Cholesterol", "Hypertension"] * (num_records // 4)
    allergies = ["None", "None", "Sulfa", "None"] * (num_records // 4)
    
    random.shuffle(medications)
    random.shuffle(doses)
    random.shuffle(conditions)
    random.shuffle(allergies)

    data = {
        'patient_id': patient_ids,
        'medication': medications,
        'dose': doses,
        'condition': conditions,
        'allergy': allergies
    }
    return pd.DataFrame(data)

# --- Risk Scoring ---
def score_risk(df):
    """Uses the loaded ML model to predict risk for the given data."""
    # Prepare data for the model (must match the API and training script)
    input_df = df.copy()
    input_df['dose_mg'] = input_df['dose'].str.replace('mg', '').astype(int)
    input_df = input_df.drop(columns=['dose', 'patient_id'])

    # One-hot encode and align columns
    input_encoded = pd.get_dummies(input_df)
    input_aligned = input_encoded.reindex(columns=model_features, fill_value=0)

    # Predict the risk
    predictions = model.predict(input_aligned)
    
    # Add predictions back to the original DataFrame
    df['Predicted_Risk'] = ["High" if p == 1 else "Low" for p in predictions]
    return df

from src.database import SessionLocal, RiskReport

# --- Main Execution ---
def main():
    """Main function to generate data, score it, and save the report."""
    print("Generating enhanced simulated eMAR data...")
    df_generated = generate_emar_data(num_records=100)
    
    print("Scoring data using the enhanced AI model...")
    df_scored = score_risk(df_generated)
    
    # Save the report to the database
    session = SessionLocal()
    try:
        for index, row in df_scored.iterrows():
            report = RiskReport(
                patient_id=row['patient_id'],
                medication=row['medication'],
                dose=row['dose'],
                condition=row['condition'],
                allergy=row['allergy'],
                predicted_risk=row['Predicted_Risk']
            )
            session.add(report)
        session.commit()
        print("Enhanced EMAR Risk Report saved to database successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error saving to database: {e}")
    finally:
        session.close()
    
    print("--- Report Preview ---")
    print(df_scored.head())
    print("--------------------")

if __name__ == "__main__":
    main()
