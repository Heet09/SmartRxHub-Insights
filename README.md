# 💊 SmartRxHub Insights: EMAR Risk Alert Engine

A real-time risk scoring engine and dashboard built for SmartRxHub to identify and alert healthcare providers about high-risk medication conditions using patient data.

---

## 🚀 Project Overview

This project is part of a proposed analytics pipeline for SmartRxHub’s EMAR system. It leverages Python, pandas, and Streamlit to:

- 🔍 Analyze patient diagnoses and allergy records
- ⚠️ Generate medication risk alerts (e.g., avoid NSAIDs in asthmatic patients)
- 📈 Display risk reports in an interactive dashboard
- 🔁 Automatically update the report daily via CI/CD (GitHub Actions)

---

## 🏗️ Project Structure

SmartRxHub-Insights/
├── scripts/
│ └── emar_risk_scoring.py # Rule-based scoring logic
├── dashboard/
│ └── streamlit_dashboard.py # Streamlit UI for visualizing alerts
├── reports/
│ └── emar_risk_report.csv # Auto-generated daily report
├── .github/
│ └── workflows/
│ └── emar_risk_engine.yml # CI/CD pipeline
├── requirements.txt
├── README.md



---

## 📊 Dashboard Preview

Launch the dashboard locally:

```bash
cd dashboard
streamlit run streamlit_dashboard.py
```

🔁 Make sure emar_risk_report.csv exists (run the scoring script first).

🔄 CI/CD Pipeline
- A GitHub Actions workflow is configured to:

- Auto-run emar_risk_scoring.py daily at 2 AM UTC

- Push updated emar_risk_report.csv to the reports/ folder

- Trigger on both main branch pushes and schedule


📦 Tech Stack
- Python 3.10

- Pandas for data manipulation

- Streamlit for visualization

- GitHub Actions for automation (CI/CD)

