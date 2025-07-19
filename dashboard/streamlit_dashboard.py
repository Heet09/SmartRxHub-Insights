import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.database import DATABASE_URL, EMARData, SessionLocal

st.set_page_config(
    page_title="SmartRxHub-Insights: Real-Time eMAR Risk Dashboard",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        engine = create_engine(DATABASE_URL)
        with SessionLocal(bind=engine) as session:
            reports = session.query(EMARData).all()
            df = pd.DataFrame([report.__dict__ for report in reports])
            if '_sa_instance_state' in df.columns:
                df = df.drop(columns=['_sa_instance_state'])
            return df
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return pd.DataFrame()

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("Filters")
if not df.empty:
    patient_id = st.sidebar.multiselect(
        "Select Patient ID:",
        options=df["patient_id"].unique(),
        default=df["patient_id"].unique(),
    )

    risk_level = st.sidebar.multiselect(
        "Select Risk Level:",
        options=df["predicted_risk"].unique(),
        default=df["predicted_risk"].unique(),
    )

    medication_category = st.sidebar.multiselect(
        "Select Medication Category:",
        options=df["medication_category"].unique(),
        default=df["medication_category"].unique(),
    )

    df_selection = df.query(
        "patient_id == @patient_id & predicted_risk == @risk_level & medication_category == @medication_category"
    )
else:
    st.sidebar.warning("No data available. Please run the risk scoring script.")
    df_selection = pd.DataFrame()

# --- Main Page ---
st.title("⚕️ SmartRxHub-Insights: Real-Time eMAR Risk Dashboard")
st.markdown("##")

if not df_selection.empty:
    # --- Key Metrics ---
    total_patients = df_selection["patient_id"].nunique()
    total_records = len(df_selection)
    high_risk_alerts = len(df_selection[df_selection["predicted_risk"] == "High"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Patients", value=total_patients)
    with col2:
        st.metric(label="Total Records", value=total_records)
    with col3:
        st.metric(label="High-Risk Alerts", value=high_risk_alerts)

    st.markdown("---")

    # --- Patient-Centric View ---
    st.subheader("Patient-Centric View")
    selected_patient = st.selectbox("Select a patient to view details:", df_selection["patient_id"].unique())

    patient_data = df_selection[df_selection["patient_id"] == selected_patient]
    st.dataframe(patient_data)

    # --- Actionable Recommendations ---
    st.subheader("Actionable Recommendations")
    high_risk_patient_data = patient_data[patient_data["predicted_risk"] == "High"]
    if not high_risk_patient_data.empty:
        for index, row in high_risk_patient_data.iterrows():
            st.warning(f"**High Risk Alert for {row['patient_id']}:** Administering **{row['medication']}** ({row['dose']}) for **{row['primary_diagnosis']}**. ")
            st.info("**Recommendation:** Review patient's allergies and current medications for potential interactions. Verify dosage with the prescribing doctor.")
    else:
        st.success("No high-risk alerts for the selected patient.")

    st.markdown("---")

    # --- Charts ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Risk Level Distribution")
        risk_distribution = df_selection["predicted_risk"].value_counts()
        st.bar_chart(risk_distribution)

    with col2:
        st.subheader("Medication Categories by Risk")
        risk_by_category = df_selection.groupby("medication_category")["predicted_risk"].apply(lambda x: (x == 'High').sum()).sort_values(ascending=False)
        st.bar_chart(risk_by_category)

else:
    st.warning("No data to display based on the current filters.")
