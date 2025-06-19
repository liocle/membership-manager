# tests/test_db.py

import uuid

from models import Member


def test_member_auto_fields(db_session):
    """
    Verify that reference_number, full_name,
    created_at and modified_at are set automatically.
    """
    member = Member(
        first_name="Alice",
        last_name="Johnson",
        email=f"alice_{uuid.uuid4().hex}@example.com",
        phone="123456789",
        city="Helsinki",
        postal_code="00100",
        no_postal_mail=False,
        notes="VIP Member",
    )
    db_session.add(member)
    db_session.commit()
    db_session.refresh(member)

    # Because of SQLA stubs, Pyright thinks these are ColumnElements;
    # it is known that they are attributes with values.
    assert member.reference_number >= 2_000_000_000  # type: ignore[reportGeneralTypeIssues]
    assert member.full_name == "Alice Johnson"  # type: ignore[reportGeneralTypeIssues]
    assert member.created_at is not None
    assert member.modified_at is not None
