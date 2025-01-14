import pytest
from ..database import get_session, engine
from sqlmodel import SQLModel

@pytest.fixture(autouse=True, scope="function")
def create_test_database():
    """Fixture to set up and tear down the test database for each test."""
    
    # Drop any existing tables and recreate them to start fresh for tests
    SQLModel.metadata.drop_all(engine)  # Drop all existing tables (clean state)
    SQLModel.metadata.create_all(engine)  # Create the tables for the test

    # Yield control back to the test function
    yield

    # After all tests are done, drop all tables to clean up
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def session():
    """Fixture to provide a fresh database session for each test."""
    
    # Create a new session for each test function
    session = next(get_session())

    # Yield the session for use in the tests
    yield session

    # Rollback session after each test to ensure a clean state
    session.rollback()
    session.close()
