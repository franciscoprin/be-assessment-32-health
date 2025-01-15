from fastapi.testclient import TestClient
from ..main import app
from ..models import Claim
from sqlmodel import select


client = TestClient(app=app)

# Define a test case for valid data
def test_process_claim_valid(session):
    payload = {
        "service_date": "2025-01-15",
        "submitted_procedure": "D0180",
        "quadrant": "Upper",
        "plan_group": "GRP-1000",
        "subscriber": "3730189502",
        "provider_npi": "1497775530",
        "provider_fees": 100.00,
        "allowed_fees": 100.00,
        "member_coinsurance": 0.00,
        "member_copay": 0.00
    }

    response = client.post("/claims/", json=payload)

    assert response.status_code == 200
    data = response.json()
    
    assert data["service_date"] == payload["service_date"]
    assert data["submitted_procedure"] == payload["submitted_procedure"]
    assert data["quadrant"] == payload["quadrant"]
    assert data["plan_group"] == payload["plan_group"]
    assert data["subscriber"] == payload["subscriber"]
    assert data["provider_npi"] == payload["provider_npi"]
    assert data["provider_fees"] == payload["provider_fees"]
    assert data["allowed_fees"] == payload["allowed_fees"]
    assert data["member_coinsurance"] == payload["member_coinsurance"]
    assert data["member_copay"] == payload["member_copay"]
    assert data["net_fee"] == 0.00  # since provider_fees + member_coinsurance + member_copay - allowed_fees = 0.00

    # Check if the claim was added to the database
    stmt = select(Claim).where(Claim.id == data["id"])
    db_claim = session.exec(stmt).first()
    assert db_claim is not None  # Ensure the claim exists in the database
    assert db_claim.service_date == payload["service_date"]
    assert db_claim.submitted_procedure == payload["submitted_procedure"]
    assert db_claim.quadrant == payload["quadrant"]
    assert db_claim.plan_group == payload["plan_group"]
    assert db_claim.subscriber == payload["subscriber"]
    assert db_claim.provider_npi == payload["provider_npi"]
    assert db_claim.provider_fees == payload["provider_fees"]
    assert db_claim.allowed_fees == payload["allowed_fees"]
    assert db_claim.member_coinsurance == payload["member_coinsurance"]
    assert db_claim.member_copay == payload["member_copay"]
    assert db_claim.net_fee == 0.00  # same calculation for net_fee

    # Assert that only one claim exists in the database
    stmt = select(Claim)
    results = session.exec(stmt).all()
    total_claims = len(results)

    assert total_claims == 1  # Check that only one claim has been inserted

# Test when 'submitted_procedure' does not start with 'D'
def test_process_claim_invalid_procedure(session):
    payload = {
        "service_date": "2025-01-15",
        "submitted_procedure": "A0180",  # Invalid, does not start with 'D'
        "quadrant": "Upper",
        "plan_group": "GRP-1000",
        "subscriber": "3730189502",
        "provider_npi": "1497775530",
        "provider_fees": 100.00,
        "allowed_fees": 100.00,
        "member_coinsurance": 0.00,
        "member_copay": 0.00
    }

    response = client.post("/claims/", json=payload)
    data = response.json()

    assert data == {
        'detail': [{
            'type': 'value_error',
            'loc': ['body', 'submitted_procedure'],
            'msg': 'Value error, Submitted procedure must start with "D"',
            'input': 'A0180', 'ctx': {'error': {}}
        }]
    }

    assert response.status_code == 422

    # Assert that only non claims exist in the database
    stmt = select(Claim)
    results = session.exec(stmt).all()
    total_claims = len(results)

    assert total_claims == 0


# Test when 'provider_npi' is not a 10-digit number
def test_process_claim_invalid_npi(session):
    payload = {
        "service_date": "2025-01-15",
        "submitted_procedure": "D0180",
        "quadrant": "Upper",
        "plan_group": "GRP-1000",
        "subscriber": "3730189502",
        "provider_npi": "14977",  # Invalid, not 10 digits
        "provider_fees": 100.00,
        "allowed_fees": 100.00,
        "member_coinsurance": 0.00,
        "member_copay": 0.00
    }

    response = client.post("/claims/", json=payload)
    data = response.json()

    assert data == {
        'detail': [{
            'type': 'value_error',
            'loc': ['body', 'provider_npi'],
            'msg': 'Value error, Provider NPI must be a 10-digit number',
            'input': '14977',
            'ctx': {'error': {}}
        }
    ]}

    assert response.status_code == 422

    # Assert that only non claims exist in the database
    stmt = select(Claim)
    results = session.exec(stmt).all()
    total_claims = len(results)

    assert total_claims == 0

# Test missing required fields
def test_process_claim_missing_fields(session):
    payload = {}
    # Notice that quadrant is not a required field
    expected_require_fields = [
        'service_date',
        'submitted_procedure',
        'plan_group',
        'subscriber',
        'provider_npi',
        'provider_fees',
        'allowed_fees',
        'member_coinsurance',
        'member_copay',
    ]

    response = client.post("/claims/", json=payload)
    data = response.json()

    assert data == {
        'detail': [
            {
                'type': 'missing',
                'loc': ['body', field],
                'msg': 'Field required',
                'input': {}
            } for field in expected_require_fields
        ]
    }

    assert response.status_code == 422

    # Assert that only non claims exist in the database
    stmt = select(Claim)
    results = session.exec(stmt).all()
    total_claims = len(results)

    assert total_claims == 0

# Test function for the get_top_providers endpoint
def test_get_top_providers_with_duplicate_providers(insert_sample_data, session):

    # Send GET request to the /top-providers/ endpoint
    response = client.get("/top-providers/")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON contains the correct data structure
    data = response.json()
    assert "top_providers" in data
    assert len(data["top_providers"]) == 10  # Ensure 10 providers are returned

    # Check that the first provider has the highest net fee (including duplicated NPI)
    assert data["top_providers"][0]["provider_npi"] == "1234567890"
    assert data["top_providers"][0]["total_net_fee"] == 7000.0  # Sum of 5000.0 + 2000.0

    # Check that the second provider is the one with the next highest net fee (including duplicated NPI)
    assert data["top_providers"][1]["provider_npi"] == "2345678901"
    assert data["top_providers"][1]["total_net_fee"] == 5500.0  # Sum of 4500.0 + 1000.0

    # Check that the last provider has the lowest net fee
    assert data["top_providers"][-1]["provider_npi"] == "7890123456"
    assert data["top_providers"][-1]["total_net_fee"] == 2000
