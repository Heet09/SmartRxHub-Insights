from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector

DATABASE_URL = "postgresql://heet09:heet123@localhost:5432/smartrxhub"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EMARData(Base):
    __tablename__ = "emar_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    age = Column(Integer)
    sex = Column(String)
    weight = Column(Integer)
    allergies = Column(JSON)
    primary_diagnosis = Column(String)
    medication = Column(String)
    medication_category = Column(String)
    dose = Column(String)
    route = Column(String)
    frequency = Column(String)
    is_prn = Column(Boolean)
    prescribing_doctor_id = Column(String)
    administering_nurse_id = Column(String)
    patient_location = Column(String)
    administration_time_of_day = Column(String)
    timestamp = Column(Float)
    predicted_risk = Column(String)

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  # e.g., the name of the CSV file or table
    content = Column(Text)
    embedding = Column(Vector(384))  # Assuming 'all-MiniLM-L6-v2' which has 384 dimensions

def init_db():
    Base.metadata.create_all(bind=engine)
