
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
print(f"DEBUG: model_features loaded: {model_features}")

@app.post("/ingest")
async def ingest_data(data: EMARData):
    try:
        data_dict = data.model_dump()
        # Normalize keys used in one-hot encoding
        data_dict["medication_category"] = data_dict["medication_category"].strip().replace(" ", "_").lower()
        data_dict["patient_location"] = data_dict["patient_location"].strip().replace(" ", "_").lower()
        data_dict["route"] = data_dict["route"].strip().replace(" ", "_").lower()
        data_dict["frequency"] = data_dict["frequency"].strip().replace(" ", "_").lower()
        data_dict["primary_diagnosis"] = data_dict["primary_diagnosis"].strip().replace(" ", "_").lower()
        data_dict["medication"] = data_dict["medication"].strip().replace(" ", "_").lower()
        data_dict["administration_time_of_day"] = data_dict["administration_time_of_day"].strip().replace(" ", "_").lower()
        data_dict["sex"] = data_dict["sex"].strip().lower()


        input_df = pd.DataFrame([data_dict])

        input_df['dose_numeric'] = input_df['dose'].str.extract(r'(\d+\.?\d*)').astype(float)
        input_df.drop(['dose'], axis=1, inplace=True)

        categorical_cols = ['sex', 'primary_diagnosis', 'medication', 'medication_category',
                            'route', 'frequency', 'patient_location', 'administration_time_of_day']
        input_encoded = pd.get_dummies(input_df, columns=categorical_cols)

        input_aligned = input_encoded.reindex(columns=model_features, fill_value=0)

        # --- Medication & Category validation BEFORE prediction ---
        known_medications = {f.replace('medication_', '').strip() for f in model_features if f.startswith('medication_')}
        known_med_categories = {f.replace('medication_category_', '').strip() for f in model_features if f.startswith('medication_category_')}

        print(f"DEBUG: Incoming medication_category: {data_dict['medication_category']}")
        print(f"DEBUG: Known medication categories: {known_med_categories}")

        if data.medication.strip() not in known_medications:
            return {"error": f"Unknown medication: '{data.medication}'"}

        if data_dict["medication_category"] not in known_med_categories:
            return {"error": f"Unknown medication category: '{data_dict['medication_category']}'"}

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
