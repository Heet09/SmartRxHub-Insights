import csv
from src.database import SessionLocal, engine, Base, RiskReport

def migrate_csv_to_db(csv_file_path: str):
    Base.metadata.create_all(bind=engine)  # Create tables if they don't exist

    session = SessionLocal()
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Clean up keys by stripping whitespace and converting to lowercase
            cleaned_row = {k.strip().lower(): v for k, v in row.items()}

            # Create a new RiskReport object
            report = RiskReport(
                patient_id=cleaned_row['patient_id'],
                medication=cleaned_row.get('medication'),
                dose=cleaned_row.get('dose'),
                condition=cleaned_row.get('condition'),
                allergy=cleaned_row.get('allergy'),
                predicted_risk=cleaned_row.get('predicted_risk')
            )
            session.add(report)
    session.commit()
    session.close()
    print(f"Data from {csv_file_path} migrated to database successfully.")

if __name__ == "__main__":
    csv_path = "reports/emar_risk_report.csv"
    migrate_csv_to_db(csv_path)
