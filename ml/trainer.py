
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# This is a placeholder for a real dataset.
# In a real-world scenario, this would be a large, labeled dataset of eMAR records.
DATA = {
    'patient_id': [i for i in range(100)],
    'medication': ['Lisinopril', 'Metformin', 'Simvastatin', 'Amlodipine'] * 25,
    'dose_mg': [10, 20, 40, 50] * 25,
    # 1 for high risk, 0 for low risk
    'risk_level': [1, 0, 1, 0, 1, 1, 0, 0, 1, 0] * 10 
}

def train_model():
    """Trains a random forest classifier on the sample data."""
    df = pd.DataFrame(DATA)

    # Feature Engineering (simple example)
    df['medication'] = df['medication'].astype('category').cat.codes

    X = df[['medication', 'dose_mg']]
    y = df['risk_level']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred)}")

    # Save the trained model
    joblib.dump(model, 'ml/emar_risk_model.joblib')
    print("Model saved to ml/emar_risk_model.joblib")

if __name__ == "__main__":
    train_model()
