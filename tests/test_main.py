# tests/test_main.py

from fastapi.testclient import TestClient

from app.main import app  # Import your FastAPI app

client = TestClient(app)


def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Membership Manager API!"}


def test_invalid_route():
    """Test a non-existing route"""
    response = client.get("/invalid")
    assert response.status_code == 404
