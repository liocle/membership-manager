# tests/test_routes_member.py

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from models import Member, Membership
from database import get_db

client = TestClient(app)


# Override the DB dependency so FastAPI uses our test session
@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override


def create_member_with_membership(db: Session) -> Member:
    member = Member(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        postal_code="00100",
        city="Helsinki",
        reference_number=3000000000,
    )
    db.add(member)
    db.commit()
    db.refresh(member)

    membership = Membership(
        member_id=member.id,
        year=2025,
        amount=0,
        is_paid=False,
        discounted=False,
    )
    db.add(membership)
    db.commit()
    return member


def test_generate_welcome_letter_success(db_session):
    member = create_member_with_membership(db_session)
    response = client.post(f"/members/members/{member.id}/generate_welcome_letter")

    assert response.status_code == 200
    assert "PDF generated successfully" in response.json()["message"]
    output_path = Path(response.json()["path"])
    assert output_path.exists()
    assert output_path.suffix == ".pdf"


def test_generate_letter_member_not_found():
    response = client.post("/members/members/999999/generate_welcome_letter")
    assert response.status_code == 404
    assert "Member not found" in response.text


def test_generate_letter_member_has_no_membership(db_session):
    # Create a member with no memberships
    member = Member(
        first_name="No",
        last_name="Membership",
        email="no@example.com",
        postal_code="00100",
        city="Espoo",
        reference_number=3000000001,
    )
    db_session.add(member)
    db_session.commit()
    db_session.refresh(member)

    response = client.post(f"/members/members/{member.id}/generate_welcome_letter")

    assert response.status_code == 400
    assert "no memberships" in response.text
