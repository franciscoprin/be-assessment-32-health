import os
from sqlmodel import create_engine, Session, SQLModel

# Fetch database credentials from environment variables
DATABASE_USER = os.getenv("POSTGRES_USER", "user")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DATABASE_NAME = os.getenv("POSTGRES_DB", "dbname")
DATABASE_HOST = os.getenv("POSTGRES_HOST", "db")  # Default to the service name in Docker Compose

# Construct the database URL
DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

# Create the engine
engine = create_engine(DATABASE_URL)

def init_db():
    """Initialize the database by creating all tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provide a session for interacting with the database."""
    with Session(engine) as session:
        yield session
