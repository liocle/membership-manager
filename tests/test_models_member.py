# tests/test_models_member.py
from datetime import date

import pytest
from config import settings
from models import Membership
from sqlalchemy.exc import IntegrityError

# pyright: reportAttributeAccessIssue=false
# pyright: reportGeneralTypeIssues=false


def test_member_default_values(make_member):
    """
    Test that Member defaults are set correctly:
    """
    m = make_member()
    assert isinstance(m.id, int) and m.id > 0
    assert m.street_address is None
    assert m.phone is None
    assert m.notes is None
    assert m.no_postal_mail is False


def test_member_reference_sequence_and_full_name(make_member):
    """
    Two consecutive Member inserts get strictly increasing
    reference_number ≥ 2_000_000_000, and full_name is computed.

    Tests the sequence for reference_number and the computed full_name.
    """
    m1 = make_member(first_name="Alpha", last_name="One")
    m2 = make_member(first_name="Beta", last_name="Two")

    # Sequence bump
    assert m1.reference_number >= 2_000_000_000
    assert m2.reference_number == m1.reference_number + 1

    # Computed full_name
    assert m1.full_name == "Alpha One"
    assert m2.full_name == "Beta Two"


def test_unique_email_constraint(make_member):
    """
    Attempting to insert two Members with the same email should
    raise an IntegrityError.
    """
    email = "dup_@example.test"

    _m1 = make_member(first_name="Dupe", last_name="One", email=email)

    with pytest.raises(IntegrityError):
        _m2 = make_member(first_name="Dupe", last_name="Two", email=email)


def test_two_memberships_and_cascade_delete(make_member, make_membership, db_session):
    """
    Create two memberships for the same member:
      - full‐fee membership (2024) → not discounted
      - small‐fee membership (2025) → discounted
    Then delete the member and assert that both are cascade‐deleted.
    """
    m = make_member()

    full = make_membership(member=m, year=2024, amount=settings.STANDARD_MEMBERSHIP_FEE)
    assert full.is_paid
    assert not full.discounted

    small = make_membership(member=m, year=2025, amount=settings.UNPAID_MEMBERSHIP + 10)
    assert small.is_paid
    assert small.discounted

    db_session.refresh(m)
    assert len(m.memberships) == 2
    assert {ms.year for ms in m.memberships} == {2024, 2025}

    # 5) Now delete the member → both should be gone
    db_session.delete(m)
    db_session.commit()

    assert db_session.get(Membership, full.id) is None
    assert db_session.get(Membership, small.id) is None


def test_full_name_recomputes_on_update(db_session, make_member):
    """
    Because full_name is a Computed column, updating first_name/last_name
    and committing should update full_name in the DB.
    """
    m = make_member(first_name="John", last_name="Doe")
    assert m.full_name == "John Doe"

    m.first_name = "Jane"
    m.last_name = "Smith"
    db_session.commit()
    db_session.refresh(m)
    assert m.full_name == "Jane Smith"


def test_no_postal_mail_flag_default_and_toggle(db_session, make_member):
    """
    no_postal_mail defaults to False, but can be set and persisted.
    """
    m = make_member()
    assert m.no_postal_mail is False

    m.no_postal_mail = True
    db_session.commit()
    db_session.refresh(m)
    assert m.no_postal_mail is True


def test_created_and_modified_dates(make_member):
    """
    created_at and modified_at are non-null dates, and should be
    instances of date.
    """
    m = make_member()
    assert isinstance(m.created_at, date)
    assert isinstance(m.modified_at, date)
    # Within today’s date
    assert m.created_at <= date.today()
    assert m.modified_at <= date.today()
