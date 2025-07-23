# tests/test_routes_member_search.py

import pytest
from database import get_db
from fastapi.testclient import TestClient
from models import Member, Membership

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _override_db(db_session):
    # Ensure all route DB calls use the test session
    app.dependency_overrides[get_db] = lambda: db_session


def create_member_with_two(db_session, make_member):
    """
    Create one member (with a unique email via make_member)
    and two memberships (one paid, one unpaid).
    """
    m = make_member(first_name="Alice", last_name="Wonder", city="TestCity")
    db_session.add_all(
        [
            Membership(member_id=m.id, year=2023, amount=25),  # paid
            Membership(member_id=m.id, year=2024, amount=0),  # unpaid
        ]
    )
    db_session.commit()
    db_session.refresh(m)
    return m


def test_search_by_reference_found(db_session, make_member):
    m = create_member_with_two(db_session, make_member)
    resp = client.get(f"/members/search/{m.reference_number}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["member"]["reference_number"] == m.reference_number
    assert len(data["member"]["memberships"]) == 2


def test_search_by_reference_not_found():
    resp = client.get("/members/search/9999999999")
    assert resp.status_code == 404


@pytest.mark.parametrize(
    "subpath, query_value, expected_count",
    [
        ("full_name", "Alice", 1),
        ("name", "Wonder", 1),
        ("city", "TestCity", 1),
    ],
)
def test_search_variants(db_session, make_member, subpath, query_value, expected_count):
    # clear out all previous data so only our new member exists
    db_session.query(Membership).delete()
    db_session.query(Member).delete()
    db_session.commit()

    m = create_member_with_two(db_session, make_member)
    resp = client.get(f"/members/search/{subpath}/{query_value}")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["message"].startswith("Found")
    assert len(payload.get("results", [])) == expected_count


def test_exact_reference_endpoint(db_session, make_member):
    m = create_member_with_two(db_session, make_member)
    resp = client.get(f"/members/search/reference/{m.reference_number}")
    assert resp.status_code == 200
    assert resp.json()["member"]["id"] == m.id


def test_exact_reference_not_found():
    resp = client.get("/members/search/reference/123456789")
    assert resp.status_code == 404


def test_search_by_postal_code(db_session, make_member):
    # clear out all previous data
    db_session.query(Membership).delete()
    db_session.query(Member).delete()
    db_session.commit()

    # Create two members with postal_code="00100", plus one with a different code
    m1 = make_member(city="A-City", postal_code="00100")
    m2 = make_member(city="B-City", postal_code="00100")
    _ = make_member(city="C-City", postal_code="99999")

    resp = client.get("/members/search/postal/00100")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["message"].startswith("Found")
    assert len(payload.get("results", [])) == 2
