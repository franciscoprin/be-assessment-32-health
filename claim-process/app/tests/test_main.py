import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app=app)

# Define a test case for valid data
def test_process_claim_valid():
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

# Test when 'submitted_procedure' does not start with 'D'
def test_process_claim_invalid_procedure():
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

# Test when 'provider_npi' is not a 10-digit number
def test_process_claim_invalid_npi():
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

# Test missing required fields
def test_process_claim_missing_fields():
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
