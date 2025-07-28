
import streamlit as st
import pandas as pd
from dashboard.utils import load_data

st.set_page_config(
    page_title="SmartRxHub-Insights: Patient Deep Dive",
    page_icon="👩‍⚕️",
    layout="wide",
)

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("Filters")
if not df.empty:
    patient_id = st.sidebar.selectbox(
        "Select Patient ID:",
        options=df["patient_id"].unique(),
    )

    df_selection = df[df["patient_id"] == patient_id]
else:
    st.sidebar.warning("No data available. Please run the risk scoring script.")
    df_selection = pd.DataFrame()

# --- Main Page ---
st.title("👩‍⚕️ Patient Deep Dive")
st.markdown("##")

if not df_selection.empty:
    st.subheader(f"Showing data for Patient: {patient_id}")
    st.dataframe(df_selection)

    # --- Actionable Recommendations ---
    st.subheader("Actionable Recommendations")
    high_risk_patient_data = df_selection[df_selection["predicted_risk"] == "High"]
    if not high_risk_patient_data.empty:
        for index, row in high_risk_patient_data.iterrows():
            st.warning(f"**High Risk Alert for {row['patient_id']}:** Administering **{row['medication']}** ({row['dose']}) for **{row['primary_diagnosis']}**. ")
            st.info("**Recommendation:** Review patient's allergies and current medications for potential interactions. Verify dosage with the prescribing doctor.")
    else:
        st.success("No high-risk alerts for the selected patient.")
else:
    st.warning("No data to display based on the current filters.")
