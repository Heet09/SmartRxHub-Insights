import streamlit as st
import pandas as pd
import os

# File path to the report
report_path = os.path.join("..", "reports", "emar_risk_report.csv")

st.set_page_config(page_title="EMAR Risk Alert Dashboard", layout="centered")

st.title("📊 EMAR Risk Alert Dashboard")
st.markdown("Get real-time alerts for high-risk patients.")

# Load report
if os.path.exists(report_path):
    df = pd.read_csv(report_path)
    st.success("Risk report loaded successfully.")
    
    # Show all data
    st.subheader("🩺 Patient Risk Summary")
    st.dataframe(df, use_container_width=True)

    # Filter by Alert Type
    st.subheader("🔍 Filter by Alert Type")
    alert_type = st.selectbox("Choose alert filter", ["All", "⚠️ Avoid NSAIDs", "⚠️ Use kidney-safe medication", "✅ No critical risk"])
    
    if alert_type != "All":
        filtered = df[df['Alert'] == alert_type]
        st.dataframe(filtered, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
else:
    st.error("Risk report not found. Please run emar_risk_scoring.py first.")
