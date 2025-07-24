from src.database import init_db
from sqlalchemy import text
from src.database import engine

# Enable the pgvector extension
with engine.connect() as connection:
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
    connection.commit()

# Create the tables
init_db()

print("Database initialized, pgvector extension enabled, and tables created.")
