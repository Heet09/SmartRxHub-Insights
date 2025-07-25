import sys
import os
from sentence_transformers import SentenceTransformer

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import SessionLocal, EMARData, KnowledgeBase

def generate_and_store_embeddings():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    session = SessionLocal()

    try:
        emar_data_entries = session.query(EMARData).all()
        for entry in emar_data_entries:
            # Combine relevant fields into a single string for embedding
            content_text = f"Patient ID: {entry.patient_id}. Primary Diagnosis: {entry.primary_diagnosis}. Medication: {entry.medication}. Dose: {entry.dose}. Allergies: {entry.allergies}. Predicted Risk: {entry.predicted_risk}."

            # Generate embedding
            embedding = model.encode(content_text).tolist()

            # Store in KnowledgeBase
            knowledge_entry = KnowledgeBase(
                source="emar_data",
                content=content_text,
                embedding=embedding
            )
            session.add(knowledge_entry)
        session.commit()
        print(f"Successfully generated and stored embeddings for {len(emar_data_entries)} entries.")

    except Exception as e:
        session.rollback()
        print(f"Error generating or storing embeddings: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    generate_and_store_embeddings()
