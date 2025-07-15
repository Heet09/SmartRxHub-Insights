
import requests
import time
import random

API_URL = "http://127.0.0.1:8000/ingest"

def generate_emar_data():
    """Generates a random eMAR data record."""
    return {
        "patient_id": f"patient_{random.randint(1, 100)}",
        "medication": random.choice(["Lisinopril", "Metformin", "Simvastatin", "Amlodipine"]),
        "dose": f"{random.choice([10, 20, 40, 50])}mg",
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
