import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json
import numpy as np

# Import the data generator from our simulator script
from scripts.data_simulator import generate_emar_data

def create_dataset(num_records=1000):
    """Creates a dataset using the enhanced data simulator."""
    data = [generate_emar_data() for _ in range(num_records)]
    return pd.DataFrame(data)

def train_model():
    """Trains a random forest classifier on the enhanced dataset."""
    df = create_dataset()

    # --- Feature Engineering ---
    # Convert dose to a numerical format
    df['dose_numeric'] = df['dose'].str.extract('(\d+\.?\d*)').astype(float)
    df.drop(['dose'], axis=1, inplace=True)

    # Define risk based on a combination of factors
    # This is a more realistic way to define risk for training purposes
    conditions = (
        (df['medication_category'] == 'antibiotic') & (df['allergies'].apply(lambda x: 'penicillin' in x)),
        (df['primary_diagnosis'] == 'diabetes') & (df['medication_category'] != 'antidiabetic'),
        (df['age'] > 75) & (df['medication_category'] == 'antihypertensive'),
        (df['weight'] > 90) & (df['dose_numeric'] > 500)
    )
    risk_levels = [1, 1, 1, 1] # High risk
    df['risk_level'] = np.select(conditions, risk_levels, default=0) # Low risk

    # One-hot encode categorical features
    categorical_cols = ['sex', 'primary_diagnosis', 'medication', 'medication_category', 'route', 'frequency', 'patient_location', 'administration_time_of_day']
    df_encoded = pd.get_dummies(df, columns=categorical_cols)

    # Define features (X) and target (y)
    features = [col for col in df_encoded.columns if col not in ['patient_id', 'risk_level', 'allergies', 'timestamp', 'prescribing_doctor_id', 'administering_nurse_id']]
    X = df_encoded[features]
    y = df_encoded['risk_level']

    # --- Model Training ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"Model Accuracy on new features: {accuracy_score(y_test, y_pred)}")

    # --- Save Model and Features ---
    joblib.dump(model, 'ml/emar_risk_model.joblib')
    print("Model saved to ml/emar_risk_model.joblib")

    with open('ml/model_features.json', 'w') as f:
        json.dump(features, f)
    print("Model features saved to ml/model_features.json")

if __name__ == "__main__":
    train_model()