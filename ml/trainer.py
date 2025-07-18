import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json

# This is a placeholder for a real dataset with more features.
DATA = {
    'patient_id': [i for i in range(100)],
    'medication': ['Lisinopril', 'Metformin', 'Simvastatin', 'Amlodipine'] * 25,
    'dose_mg': [10, 20, 40, 50] * 25,
    'condition': ['Hypertension', 'Diabetes', 'High Cholesterol', 'Hypertension'] * 25,
    'allergy': ['None', 'None', 'Sulfa', 'None'] * 25,
    # 1 for high risk, 0 for low risk (example logic)
    'risk_level': [1, 0, 1, 0, 1, 1, 0, 0, 1, 0] * 10 
}

def train_model():
    """Trains a random forest classifier on the enhanced dataset."""
    df = pd.DataFrame(DATA)

    # --- Feature Engineering ---
    # One-hot encode categorical features
    df_encoded = pd.get_dummies(df, columns=['medication', 'condition', 'allergy'], drop_first=True)

    # Define features (X) and target (y)
    features = [col for col in df_encoded.columns if col not in ['patient_id', 'risk_level']]
    X = df_encoded[features]
    y = df_encoded['risk_level']

    # --- Model Training ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"Model Accuracy on new features: {accuracy_score(y_test, y_pred)}")

    # --- Save Model and Features ---
    # Save the trained model
    joblib.dump(model, 'ml/emar_risk_model.joblib')
    print("Model saved to ml/emar_risk_model.joblib")

    # Save the list of feature columns for consistent use in prediction
    with open('ml/model_features.json', 'w') as f:
        json.dump(features, f)
    print("Model features saved to ml/model_features.json")

if __name__ == "__main__":
    train_model()