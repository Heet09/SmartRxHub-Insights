
import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.utils import load_data

st.set_page_config(
    page_title="SmartRxHub-Insights: Overview",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("Filters")
if not df.empty:
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
        "predicted_risk == @risk_level & medication_category == @medication_category"
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

    # --- Charts ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Risk Level Distribution")
        risk_distribution = df_selection["predicted_risk"].value_counts()
        fig = px.bar(risk_distribution, x=risk_distribution.index, y=risk_distribution.values,
                     labels={'x': 'Risk Level', 'y': 'Number of Patients'},
                     color=risk_distribution.index,
                     color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Medication Categories by Risk")
        risk_by_category = df_selection.groupby("medication_category")["predicted_risk"].apply(lambda x: (x == 'High').sum()).sort_values(ascending=False)
        fig2 = px.bar(risk_by_category, x=risk_by_category.index, y=risk_by_category.values,
                      labels={'x': 'Medication Category', 'y': 'Number of High-Risk Records'})
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("No data to display based on the current filters.")
