from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://heet09:heet123@localhost:5432/smartrxhub"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RiskReport(Base):
    __tablename__ = "risk_reports"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    medication = Column(String)
    dose = Column(String)
    condition = Column(String)
    allergy = Column(String)
    predicted_risk = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
