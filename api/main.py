from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load the model at startup
model = joblib.load('ml/emar_risk_model.joblib')

@app.post("/ingest")
async def ingest_data(data: dict):
    """
    This endpoint receives eMAR data, predicts the risk, 
    and returns the prediction.
    """
    try:
        # Prepare the data for the model
        medication_map = {'Lisinopril': 0, 'Metformin': 1, 'Simvastatin': 2, 'Amlodipine': 3}
        dose_mg = int(data['dose'].replace('mg', ''))
        medication_code = medication_map.get(data['medication'], -1)

        if medication_code == -1:
            return {"error": "Unknown medication"}

        # Create a DataFrame for the model
        df = pd.DataFrame([{'medication': medication_code, 'dose_mg': dose_mg}])

        # Predict the risk
        prediction = model.predict(df)
        risk_level = "High" if prediction[0] == 1 else "Low"

        print(f"Received data: {data}, Predicted Risk: {risk_level}")
        return {"status": "success", "data_received": data, "predicted_risk": risk_level}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "SmartRxHub-Insights API is running with ML model."}