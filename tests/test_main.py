"""
Tests for the Churn Prediction API.

Run with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
"""

from litestar.testing import TestClient

from app.model_utils import predict_churn
from main import app

# ---------------------------------------------------------------------------
# Shared sample payload
# ---------------------------------------------------------------------------
SAMPLE_PAYLOAD = {
    "CreditScore": 600.0,
    "Geography": "France",
    "Gender": "Male",
    "Age": 40.0,
    "Tenure": 3.0,
    "Balance": 60000.0,
    "NumOfProducts": 2.0,
    "HasCrCard": 1.0,
    "IsActiveMember": 1.0,
    "EstimatedSalary": 50000.0,
}

# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------


# TODO 1: Write a test that calls predict_churn() directly with sample features
#         and asserts the result is 0 or 1
def test_predict_churn_returns_binary():
    features = [
        600.0,
        "France",
        "Male",
        40.0,
        3.0,
        60000.0,
        2.0,
        1.0,
        1.0,
        50000.0,
    ]
    result = predict_churn(features)
    assert result in (0, 1), f"Expected 0 or 1, got {result}"


# TODO 2 (bonus): Write another function test with edge-case inputs
def test_predict_churn_high_risk_customer():
    """Edge case: very old customer with low balance — typically higher churn risk."""
    features = [
        300.0,
        "Germany",
        "Female",
        60.0,
        1.0,
        0.0,
        1.0,
        0.0,
        0.0,
        10000.0,
    ]
    result = predict_churn(features)
    assert result in (0, 1)


def test_predict_churn_young_active_customer():
    """Edge case: young, active, multi-product customer — lower churn risk."""
    features = [
        750.0,
        "France",
        "Male",
        28.0,
        8.0,
        120000.0,
        2.0,
        1.0,
        1.0,
        80000.0,
    ]
    result = predict_churn(features)
    assert result in (0, 1)


# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------


# TODO 3: Write a test that POSTs to /predict with valid JSON
#         and checks the status code and response body
def test_predict_endpoint_valid():
    with TestClient(app=app) as client:
        response = client.post("/predict", json=SAMPLE_PAYLOAD)
    assert response.status_code == 201, response.text
    body = response.json()
    assert "churn_prediction" in body
    assert body["churn_prediction"] in (0, 1)


# TODO 4: Write a test for GET /health
def test_health_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# TODO 5: Write a test for GET /
def test_home_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "message" in body


# TODO 6 (bonus): Test that invalid input returns status 400
def test_predict_endpoint_invalid_input():
    """Missing required fields should return 400."""
    with TestClient(app=app) as client:
        response = client.post("/predict", json={"CreditScore": "not-a-number"})
        print(response.text)
    assert response.status_code in (400, 422), response.text


def test_predict_endpoint_empty_body():
    """Empty JSON body should return 400/422 (validation error)."""
    with TestClient(app=app) as client:
        response = client.post("/predict", json={})
    assert response.status_code in (400, 422), response.text
