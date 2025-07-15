import streamlit as st
import pandas as pd
import requests
import time
import numpy as np

st.set_page_config(layout="wide")

API_URL = "http://127.0.0.1:8000/ingest"

# --- Functions ---

def get_live_data():
    """Simulates fetching live data from a source."""
    # In a real app, this would connect to a database or message queue
    # For this demo, we'll just call our own API
    data = {
        "patient_id": f"patient_{np.random.randint(1, 100)}",
        "medication": np.random.choice(["Lisinopril", "Metformin", "Simvastatin", "Amlodipine"]),
        "dose": f"{np.random.choice([10, 20, 40, 50])}mg",
        "timestamp": time.time()
    }
    response = requests.post(API_URL, json=data)
    return response.json()

# --- UI Layout ---

st.title("SmartRxHub-Insights: Real-time Risk Dashboard")

# --- Placeholders for live updates ---
placeholder = st.empty()

# --- Data Storage (session state) ---
if 'events' not in st.session_state:
    st.session_state.events = []

# --- Main Loop ---
while True:
    new_event = get_live_data()
    st.session_state.events.append(new_event)

    with placeholder.container():
        # --- High-Risk Events ---
        st.subheader("High-Risk Events")
        high_risk_events = [e for e in st.session_state.events if e.get('predicted_risk') == 'High']
        if high_risk_events:
            high_risk_df = pd.DataFrame(high_risk_events)
            st.dataframe(high_risk_df)
        else:
            st.info("No high-risk events detected.")

        # --- All Events Log ---
        st.subheader("Live Event Log")
        all_events_df = pd.DataFrame(st.session_state.events)
        st.dataframe(all_events_df)

    time.sleep(2) # Simulate a 2-second delay between new events