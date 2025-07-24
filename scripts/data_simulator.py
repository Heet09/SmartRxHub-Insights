
import requests
import time
import random

API_URL = "http://127.0.0.1:8000/ingest"

def generate_emar_data():
    """Generates a random eMAR data record with expanded fields."""
    medications = {
        "Lisinopril": {"category": "antihypertensive", "routes": ["oral"], "doses": ["10mg", "20mg", "40mg"]},
        "Metformin": {"category": "antidiabetic", "routes": ["oral"], "doses": ["500mg", "850mg", "1000mg"]},
        "Simvastatin": {"category": "statin", "routes": ["oral"], "doses": ["20mg", "40mg", "80mg"]},
        "Amlodipine": {"category": "antihypertensive", "routes": ["oral"], "doses": ["5mg", "10mg"]},
        "Levothyroxine": {"category": "thyroid_hormone", "routes": ["oral", "IV"], "doses": ["25mcg", "50mcg", "100mcg"]},
        "Azithromycin": {"category": "antibiotic", "routes": ["oral", "IV"], "doses": ["250mg", "500mg"]},
    }
    
    medication_name = random.choice(list(medications.keys()))
    medication_info = medications[medication_name]

    return {
        "patient_id": f"patient_{random.randint(1, 100)}",
        "age": random.randint(18, 90),
        "sex": random.choice(["male", "female"]),
        "weight": random.randint(50, 100),
        "allergies": random.choice([[], ["penicillin"], ["sulfa"], ["nuts"]]),
        "primary_diagnosis": random.choice(["hypertension", "diabetes", "hyperlipidemia", "hypothyroidism", "infection"]),
        "medication": medication_name,
        "medication_category": medication_info["category"],
        "dose": random.choice(medication_info["doses"]),
        "route": random.choice(medication_info["routes"]),
        "frequency": random.choice(["daily", "BID", "TID", "QID"]),
        "is_prn": random.choice([True, False]),
        "prescribing_doctor_id": f"doctor_{random.randint(1, 20)}",
        "administering_nurse_id": f"nurse_{random.randint(1, 50)}",
        "patient_location": random.choice(["ICU", "general ward", "cardiac unit", "oncology ward"]),
        "administration_time_of_day": random.choice(["morning", "afternoon", "evening", "night"]),
        "timestamp": time.time()
    }

def main():
    """Sends eMAR data to the API every few seconds."""
    while True:
        data = generate_emar_data()
        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
            print(f"Sent data: {data}")
            print(f"Received response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")
        
        time.sleep(random.randint(2, 5))

if __name__ == "__main__":
    main()
