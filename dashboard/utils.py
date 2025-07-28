
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.database import DATABASE_URL, EMARData, SessionLocal
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_data
def load_data():
    """Loads data from the database and caches it."""
    try:
        engine = create_engine(DATABASE_URL)
        with SessionLocal(bind=engine) as session:
            reports = session.query(EMARData).all()
            df = pd.DataFrame([report.__dict__ for report in reports])
            if '_sa_instance_state' in df.columns:
                df = df.drop(columns=['_sa_instance_state'])

            # Clean up the 'allergies' column
            if 'allergies' in df.columns:
                df['allergies'] = df['allergies'].apply(
                    lambda x: ', '.join(x) if isinstance(x, list) else str(x)
                )

            return df
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return pd.DataFrame()
