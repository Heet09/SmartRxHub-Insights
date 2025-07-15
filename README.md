# SmartRxHub-Insights: AI-Powered eMAR Risk Analysis

![CI/CD Pipeline](https://github.com/Heet09/SmartRxHub-Insights/actions/workflows/emar_risk_engine.yml/badge.svg)

## Overview

SmartRxHub-Insights is a comprehensive platform designed to analyze electronic Medication Administration Records (eMAR) in real-time, identify potential risks, and provide actionable insights to healthcare providers. This project showcases a full-stack approach to building a data-driven application, from data simulation and ingestion to machine learning-based risk scoring and an interactive dashboard for visualization.

This project demonstrates a strong command of:

*   **Software Engineering:** Building robust and scalable applications with Python, including a RESTful API and data simulation scripts.
*   **Machine Learning:** Implementing a machine learning model to predict and flag potential medication risks.
*   **CI/CD and DevOps:** Automating the testing, training, and deployment process using GitHub Actions.
*   **Data Visualization:** Creating an intuitive and interactive dashboard with Streamlit to present complex data in an understandable format.

## Features

*   **Real-time Data Ingestion:** A FastAPI-based API endpoint (`/ingest`) to receive and process eMAR data.
*   **Data Simulation:** A script to generate realistic eMAR data for testing and demonstration purposes.
*   **AI-Powered Risk Scoring:** A machine learning model that analyzes patient and medication data to identify potential risks.
*   **Automated Reporting:** A script that generates a daily CSV report of all risk assessments.
*   **Interactive Dashboard:** A Streamlit dashboard to visualize patient data, medication trends, and risk alerts.
*   **Automated CI/CD Pipeline:** A GitHub Actions workflow that automatically lints the code, trains the model, and prepares it for deployment on every push to the `main` branch.

## Technology Stack

*   **Backend:** Python, FastAPI
*   **Machine Learning:** scikit-learn, pandas
*   **Dashboard:** Streamlit
*   **CI/CD:** GitHub Actions
*   **Linting:** Ruff

## System Architecture

The application consists of the following components:

1.  **Data Simulator (`scripts/data_simulator.py`):** Continuously generates and sends eMAR data to the API.
2.  **API (`api/main.py`):** A FastAPI application that receives data and logs it.
3.  **ML Trainer (`ml/trainer.py`):** A script to train the eMAR risk model.
4.  **Risk Scoring (`scripts/emar_risk_scoring.py`):** A batch process that uses the trained model to score eMAR data and generate a report.
5.  **Dashboard (`dashboard/streamlit_dashboard.py`):** A Streamlit application to visualize the risk report.
6.  **CI/CD Pipeline (`.github/workflows/emar_risk_engine.yml`):** An automated workflow for continuous integration and delivery.

## CI/CD Pipeline

The project includes a robust CI/CD pipeline configured in `.github/workflows/emar_risk_engine.yml`. The pipeline automates the following steps on every push to the `main` branch:

1.  **Code Checkout:** Checks out the latest version of the code.
2.  **Python Setup:** Sets up the specified Python environment.
3.  **Dependency Installation:** Installs all the required libraries from `requirements.txt`.
4.  **Linting:** Runs `ruff check .` to ensure code quality and adherence to best practices.
5.  **Model Training:** Executes the `ml/trainer.py` script to train the machine learning model.
6.  **Artifact Upload:** Uploads the trained model (`emar_risk_model.joblib`) as a build artifact, making it available for deployment.

This automated pipeline ensures that the project is always in a deployable state and that any new changes are automatically tested and integrated.

## Installation and Usage

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Heet09/SmartRxHub-Insights.git
    cd SmartRxHub-Insights
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the API:**
    ```bash
    uvicorn api.main:app --reload
    ```

4.  **Run the data simulator in a separate terminal:**
    ```bash
    python scripts/data_simulator.py
    ```

5.  **Run the risk scoring script:**
    ```bash
    python scripts/emar_risk_scoring.py
    ```

6.  **View the dashboard:**
    ```bash
    streamlit run dashboard/streamlit_dashboard.py
    ```

## Future Improvements

*   **Database Integration:** Replace the CSV-based reporting with a robust database (e.g., PostgreSQL, MongoDB) to store and manage data more efficiently.
*   **User Authentication:** Implement user authentication and authorization for the dashboard and API.
*   **Model Deployment:** Add a deployment stage to the CI/CD pipeline to automatically deploy the model to a cloud service (e.g., AWS SageMaker, Google AI Platform).
*   **Enhanced Visualizations:** Add more advanced visualizations to the dashboard to provide deeper insights into the data.

## Contact

For any questions or feedback, please feel free to reach out:

*   **GitHub:** [Heet09](https://github.com/Heet09)