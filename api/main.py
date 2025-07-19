
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import json

# --- Pydantic Model for Input Validation ---
class EMARData(BaseModel):
    patient_id: str
    age: int
    sex: str
    weight: int
    allergies: list
    primary_diagnosis: str
    medication: str
    medication_category: str
    dose: str
    route: str
    frequency: str
    is_prn: bool
    prescribing_doctor_id: str
    administering_nurse_id: str
    patient_location: str
    administration_time_of_day: str
    timestamp: float

app = FastAPI()

# --- Load Model and Features at Startup ---
model = joblib.load('ml/emar_risk_model.joblib')
with open('ml/model_features.json', 'r') as f:
    model_features = json.load(f)

@app.post("/ingest")
async def ingest_data(data: EMARData):
    """
    This endpoint receives eMAR data, validates it, and returns a risk prediction.
    """
    try:
        # --- Convert Pydantic model to dictionary ---
        data_dict = data.dict()

        # --- Prepare Data for Prediction ---
        input_df = pd.DataFrame([data_dict])

        # --- Feature Engineering (must match the training script) ---
        input_df['dose_numeric'] = input_df['dose'].str.extract(r'(\d+\.?\d*)').astype(float)
        input_df.drop(['dose'], axis=1, inplace=True)

        # --- One-hot encode categorical variables ---
        categorical_cols = ['sex', 'primary_diagnosis', 'medication', 'medication_category',
                            'route', 'frequency', 'patient_location', 'administration_time_of_day']
        input_encoded = pd.get_dummies(input_df, columns=categorical_cols)

        # --- Align with model features ---
        input_aligned = input_encoded.reindex(columns=model_features, fill_value=0)

        # --- Prediction ---
        prediction = model.predict(input_aligned)
        risk_level = "High" if prediction[0] == 1 else "Low"

        print(f"Received data: {data_dict}, Predicted Risk: {risk_level}")
        return {
            "status": "success",
            "data_received": data_dict,
            "predicted_risk": risk_level
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def read_root():
    return {"message": "SmartRxHub-Insights API is running. The /ingest endpoint now accepts expanded eMAR data."}
