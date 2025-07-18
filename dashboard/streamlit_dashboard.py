import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="SmartRxHub-Insights: eMAR Risk Dashboard",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load Data ---
@st.cache_data
def load_data():
    report_path = os.path.join("reports", "emar_risk_report.csv")
    if os.path.exists(report_path):
        df = pd.read_csv(report_path)
        # Assuming 'timestamp' column exists and is in a readable format
        # If not, you might need to adjust the following line
        # df['Timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df
    return pd.DataFrame()

df = load_data()

# --- Sidebar ---
st.sidebar.title("Filters")
if not df.empty:
    patient_id = st.sidebar.multiselect(
        "Select Patient ID:",
        options=df["Patient_ID"].unique(),
        default=df["Patient_ID"].unique(),
    )

    alert_level = st.sidebar.multiselect(
        "Select Alert Level:",
        options=df["Alert"].unique(),
        default=df["Alert"].unique(),
    )

    df_selection = df.query(
        "Patient_ID == @patient_id & Alert == @alert_level"
    )
else:
    st.sidebar.warning("No data available. Please run the risk scoring script.")
    df_selection = pd.DataFrame()


# --- Main Page ---
st.title("⚕️ SmartRxHub-Insights: eMAR Risk Dashboard")
st.markdown("##")

if not df_selection.empty:
    # --- Key Metrics ---
    total_patients = df_selection["Patient_ID"].nunique()
    total_alerts = len(df_selection)
    high_risk_alerts = len(df_selection[df_selection["Alert"] != "✅ No critical risk"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Patients", value=total_patients)
    with col2:
        st.metric(label="Total Alerts", value=total_alerts)
    with col3:
        st.metric(label="High-Risk Alerts", value=high_risk_alerts)

    st.markdown("---")

    # --- Charts ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Alerts per Patient")
        alerts_per_patient = df_selection.groupby("Patient_ID")["Alert"].count().sort_values(ascending=False)
        st.bar_chart(alerts_per_patient)

    with col2:
        st.subheader("Alert Level Distribution")
        alert_distribution = df_selection["Alert"].value_counts()
        st.bar_chart(alert_distribution)


    # --- Data Table ---
    st.subheader("Filtered Data")
    st.dataframe(df_selection)

else:
    st.warning("No data to display based on the current filters.")
print("No data available to display. Please run the risk scoring script to generate data.")