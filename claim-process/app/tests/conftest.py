import pytest
from ..database import get_session, engine
from sqlmodel import SQLModel
from ..models import Claim

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

# Test setup to insert sample data
@pytest.fixture
def insert_sample_data(session):
    # Prepare some sample data with at least 13 claims, including duplicate provider_npi
    sample_claims = [
        {"provider_npi": "1234567890", "net_fee": 5000.0, "provider_fees": 1000.0, "allowed_fees": 2000.0, "member_coinsurance": 100.0, "member_copay": 50.0},
        {"provider_npi": "2345678901", "net_fee": 4500.0, "provider_fees": 1200.0, "allowed_fees": 1800.0, "member_coinsurance": 150.0, "member_copay": 75.0},
        {"provider_npi": "3456789012", "net_fee": 4000.0, "provider_fees": 1100.0, "allowed_fees": 1700.0, "member_coinsurance": 120.0, "member_copay": 80.0},
        {"provider_npi": "4567890123", "net_fee": 3500.0, "provider_fees": 1300.0, "allowed_fees": 1600.0, "member_coinsurance": 90.0, "member_copay": 60.0},
        {"provider_npi": "5678901234", "net_fee": 3000.0, "provider_fees": 1000.0, "allowed_fees": 1500.0, "member_coinsurance": 80.0, "member_copay": 50.0},
        {"provider_npi": "6789012345", "net_fee": 2500.0, "provider_fees": 900.0, "allowed_fees": 1400.0, "member_coinsurance": 70.0, "member_copay": 40.0},
        {"provider_npi": "7890123456", "net_fee": 2000.0, "provider_fees": 800.0, "allowed_fees": 1300.0, "member_coinsurance": 60.0, "member_copay": 30.0},
        {"provider_npi": "8901234567", "net_fee": 1500.0, "provider_fees": 700.0, "allowed_fees": 1200.0, "member_coinsurance": 50.0, "member_copay": 25.0},
        {"provider_npi": "9012345678", "net_fee": 1000.0, "provider_fees": 600.0, "allowed_fees": 1100.0, "member_coinsurance": 40.0, "member_copay": 20.0},
        {"provider_npi": "0123456789", "net_fee": 500.0, "provider_fees": 500.0, "allowed_fees": 1000.0, "member_coinsurance": 30.0, "member_copay": 10.0},
        {"provider_npi": "2233445566", "net_fee": 4700.0, "provider_fees": 1500.0, "allowed_fees": 2500.0, "member_coinsurance": 130.0, "member_copay": 70.0},
        {"provider_npi": "3344556677", "net_fee": 3900.0, "provider_fees": 1400.0, "allowed_fees": 2200.0, "member_coinsurance": 110.0, "member_copay": 60.0},
        {"provider_npi": "4455667788", "net_fee": 3200.0, "provider_fees": 1300.0, "allowed_fees": 2100.0, "member_coinsurance": 100.0, "member_copay": 55.0},
        # Duplicates for verification of summation
        {"provider_npi": "1234567890", "net_fee": 2000.0, "provider_fees": 900.0, "allowed_fees": 1800.0, "member_coinsurance": 50.0, "member_copay": 25.0},
        {"provider_npi": "2345678901", "net_fee": 1000.0, "provider_fees": 1100.0, "allowed_fees": 1500.0, "member_coinsurance": 60.0, "member_copay": 30.0}
    ]
    
    # Insert claims into the database
    for claim_data in sample_claims:
        claim = Claim(
            provider_npi=claim_data["provider_npi"],
            net_fee=claim_data["net_fee"],
            service_date="2025-01-01",
            submitted_procedure="procedure_code",
            quadrant="A",
            plan_group="group1",
            subscriber="subscriber1",
            provider_fees=claim_data["provider_fees"],
            allowed_fees=claim_data["allowed_fees"],
            member_coinsurance=claim_data["member_coinsurance"],
            member_copay=claim_data["member_copay"]
        )
        session.add(claim)
    session.commit()

