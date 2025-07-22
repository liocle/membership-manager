# tests/conftest.py
import os

os.environ["ENV_FILE"] = ".env.test"

import uuid
import pytest
from config import settings
from models import Member

import tests.setup_test_db  # noqa: F401

_ = tests.setup_test_db  # Prevent ruff from removing the import


@pytest.fixture(scope="session", autouse=True)
def initialize_test_database():
    yield


@pytest.fixture
def db_session():
    """
    Provides a clean SQLAlchemy session for each test function.
    Rolls back any changes when the test is over.
    """
    from database import SessionLocal

    session = SessionLocal()
    try:
        yield session
        session.rollback()
    finally:
        session.close()


@pytest.fixture
def make_member(db_session):
    """
    Factory to create & persist a Member with sane defaults.
    You can override any field by passing it as a keyword.
    """

    def _make_member(**overrides):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"test_{uuid.uuid4().hex}@example.com",
        }
        data.update(overrides)

        # Build, persist, refresh, and return
        m = Member(**data)
        db_session.add(m)
        db_session.commit()
        db_session.refresh(m)
        return m

    return _make_member


@pytest.fixture
def make_membership(db_session, make_member):
    """
    Factory to create & persist a Membership for a Member.
    You can override any field by passing it as a keyword.
    """
    from models import Membership

    def _make_membership(member=None, **overrides):
        if member is None:
            member = make_member()

        data = {
            "member_id": member.id,
            "year": 2025,
            "amount": 0,  # Default amount
        }
        data.update(overrides)

        membership = Membership(**data)
        db_session.add(membership)
        db_session.commit()
        db_session.refresh(membership)
        return membership

    return _make_membership
