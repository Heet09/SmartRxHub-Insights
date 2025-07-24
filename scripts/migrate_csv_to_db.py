import sys
import os
import csv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import SessionLocal, engine, Base, EMARData

def migrate_csv_to_db(csv_file_path: str):
    Base.metadata.create_all(bind=engine)  # Create tables if they don't exist

    session = SessionLocal()
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Clean up keys by stripping whitespace and converting to lowercase
            cleaned_row = {k.strip().lower(): v for k, v in row.items()}

            # Create a new EMARData object
            report = EMARData(
                patient_id=cleaned_row['patient_id'],
                medication=cleaned_row.get('medication'),
                dose=cleaned_row.get('dose'),
                primary_diagnosis=cleaned_row.get('condition'), # Mapping 'condition' from CSV to 'primary_diagnosis'
                allergies=cleaned_row.get('allergy'), # Mapping 'allergy' from CSV to 'allergies'
                predicted_risk=cleaned_row.get('predicted_risk')
            )
            session.add(report)
    session.commit()
    session.close()
    print(f"Data from {csv_file_path} migrated to database successfully.")

if __name__ == "__main__":
    csv_path = "reports/emar_risk_report.csv"
    migrate_csv_to_db(csv_path)
