
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import joblib
import json
from src.database import SessionLocal, EMARData
#import requests

# --- Load Model and Features ---
model = joblib.load('ml/emar_risk_model.joblib')
with open('ml/model_features.json', 'r') as f:
    model_features = json.load(f)

def score_risk(df):
    """Uses the loaded ML model to predict risk for the given data."""
    input_df = df.copy()

    # --- Feature Engineering (must match the training script) ---
    input_df['dose_numeric'] = input_df['dose'].str.extract(r'(\d+\.?\d*)').astype(float)
    input_df.drop(['dose'], axis=1, inplace=True)

    categorical_cols = ['sex', 'primary_diagnosis', 'medication', 'medication_category', 'route', 'frequency', 'patient_location', 'administration_time_of_day']
    input_encoded = pd.get_dummies(input_df, columns=categorical_cols)

    # Align columns with the model's features
    input_aligned = input_encoded.reindex(columns=model_features, fill_value=0)

    # Predict the risk
    predictions = model.predict(input_aligned)
    
    # Add predictions back to the original DataFrame
    df['predicted_risk'] = ["High" if p == 1 else "Low" for p in predictions]
    return df

# --- Main Execution ---
def main():
    """Main function to fetch data, score it, and save to the database."""
    print("Fetching data from the simulator...")
    # This part needs to be adapted based on how we get data in a real-world scenario.
    # For now, we'll assume we have a way to get a batch of data.
    # In a real application, this might be a stream of data from Kafka or a batch job.
    # We will simulate this by calling our own data generator from the simulator script.
    from data_simulator import generate_emar_data
    data = [generate_emar_data() for _ in range(100)]
    df_generated = pd.DataFrame(data)

    print("Scoring data using the AI model...")
    df_scored = score_risk(df_generated)
    
    # Save the report to the database
    session = SessionLocal()
    try:
        for index, row in df_scored.iterrows():
            emar_record = EMARData(**row.to_dict())
            session.add(emar_record)
        session.commit()
        print("EMAR Risk data saved to database successfully.")
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
