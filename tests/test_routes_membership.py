# tests/test_routes_membership.py
import pytest
from fastapi.testclient import TestClient

from app.main import app
from database import get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def _override_db(db_session):
    app.dependency_overrides[get_db] = lambda: db_session


def test_create_membership_success(make_member):
    m = make_member()
    payload = {"year": 2025, "amount": 10}
    resp = client.post(f"/members/{m.id}/memberships", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["membership"]["year"] == 2025
    assert data["membership"]["is_paid"] is True


def test_create_membership_member_not_found():
    resp = client.post("/members/999999/memberships", json={"amount": 5})
    assert resp.status_code == 404
    assert "Member not found" in resp.json()["detail"]
