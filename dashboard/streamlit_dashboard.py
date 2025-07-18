import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.database import DATABASE_URL, RiskReport, SessionLocal

st.set_page_config(
    page_title="SmartRxHub-Insights: eMAR Risk Dashboard",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load Data ---
@st.cache_data
def load_data():
    engine = create_engine(DATABASE_URL)
    try:
        with SessionLocal() as session:
            # Query all risk reports and convert to DataFrame
            reports = session.query(RiskReport).all()
            df = pd.DataFrame([report.__dict__ for report in reports])
            # Drop the SQLAlchemy internal state object
            if '_sa_instance_state' in df.columns:
                df = df.drop(columns=['_sa_instance_state'])
            return df
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return pd.DataFrame()

df = load_data()

# --- Sidebar ---
st.sidebar.title("Filters")
if not df.empty:
    patient_id = st.sidebar.multiselect(
        "Select Patient ID:",
        options=df["patient_id"].unique(),
        default=df["patient_id"].unique(),
    )

    alert_level = st.sidebar.multiselect(
        "Select Alert Level:",
        options=df["predicted_risk"].unique(),
        default=df["predicted_risk"].unique(),
    )

    df_selection = df.query(
        "patient_id == @patient_id & predicted_risk == @alert_level"
    )
else:
    st.sidebar.warning("No data available. Please run the risk scoring script.")
    df_selection = pd.DataFrame()


# --- Main Page ---
st.title("⚕️ SmartRxHub-Insights: eMAR Risk Dashboard")
st.markdown("##")

if not df_selection.empty:
    # --- Key Metrics ---
    total_patients = df_selection["patient_id"].nunique()
    total_alerts = len(df_selection)
    high_risk_alerts = len(df_selection[df_selection["predicted_risk"] == "High"])

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
        alerts_per_patient = df_selection.groupby("patient_id")["predicted_risk"].count().sort_values(ascending=False)
        st.bar_chart(alerts_per_patient)

    with col2:
        st.subheader("Alert Level Distribution")
        alert_distribution = df_selection["predicted_risk"].value_counts()
        st.bar_chart(alert_distribution)


    # --- Data Table ---
    st.subheader("Filtered Data")
    st.dataframe(df_selection)

else:
    st.warning("No data to display based on the current filters.")
print("No data available to display. Please run the risk scoring script to generate data.")