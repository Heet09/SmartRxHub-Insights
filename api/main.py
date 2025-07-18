
from fastapi import FastAPI
import joblib
import pandas as pd
import json

app = FastAPI()

# --- Load Model and Features at Startup ---
model = joblib.load('ml/emar_risk_model.joblib')
with open('ml/model_features.json', 'r') as f:
    model_features = json.load(f)

@app.post("/ingest")
async def ingest_data(data: dict):
    """
    This endpoint receives eMAR data with patient conditions and allergies,
    predicts the risk using the enhanced model, and returns the prediction.
    """
    try:
        # --- Prepare Data for Prediction ---
        # Create a DataFrame from the incoming data
        input_df = pd.DataFrame([data])

        # Feature Engineering (must match the training script)
        input_df['dose_mg'] = input_df['dose'].str.replace('mg', '').astype(int)
        input_df = input_df.drop(columns=['dose'])

        # One-hot encode categorical features
        input_encoded = pd.get_dummies(input_df)

        # Align columns with the model's features
        # This adds missing columns (if any) and fills them with 0
        # and ensures the order is identical to the training data.
        input_aligned = input_encoded.reindex(columns=model_features, fill_value=0)

        # --- Predict Risk ---
        prediction = model.predict(input_aligned)
        risk_level = "High" if prediction[0] == 1 else "Low"

        print(f"Received data: {data}, Predicted Risk: {risk_level}")
        return {"status": "success", "data_received": data, "predicted_risk": risk_level}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "SmartRxHub-Insights API is running with the enhanced ML model."}
