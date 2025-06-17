# tests/test_models.py

import uuid
from datetime import date

import pytest
from database import SessionLocal
from models import Member


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()


def test_member_creation(db):
    member = Member(
        first_name="Alice",
        last_name="Johnson",
        email=f"{uuid.uuid4().hex}@example.com",
        phone="123456789",
        city="Helsinki",
        postal_code="00100",
        no_postal_mail=False,
        notes="VIP Member",
        created_at=date.today(),
        modified_at=date.today(),
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    assert member.reference_number is not None
    assert str(member.full_name) == "Alice Johnson"
    assert member.created_at is not None
    assert member.modified_at is not None
