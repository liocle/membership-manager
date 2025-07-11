# tests/test_schemas_member.py
import pytest
from pydantic import ValidationError
from schemas import MemberCreate, MemberResponse, MembershipResponse, MemberUpdate

# pyright: reportGeneralTypeIssues=false, reportCallIssue=false, reportArgumentType=false


def test_member_create_requires_mandatory_fields():
    # Missing all three required fields should fail
    with pytest.raises(ValidationError):
        MemberCreate()

    # Supplying only first_name still fails
    with pytest.raises(ValidationError):
        MemberCreate(first_name="A")

    # Supplying first_name+last_name still fails
    with pytest.raises(ValidationError):
        MemberCreate(first_name="A", last_name="B")


def test_member_create_optional_fields_default():
    # Provide the three required, omit everything else
    m = MemberCreate(
        first_name="Foo",
        last_name="Bar",
        city="TestCity",
    )
    # Optional fields default correctly
    assert m.email is None
    assert m.street_address is None
    assert m.postal_code is None
    assert m.phone is None
    assert m.notes is None
    # no_postal_mail is Optional[bool]=False
    assert m.no_postal_mail is False


def test_member_create_invalid_patterns():
    # Bad postal_code
    with pytest.raises(ValidationError):
        MemberCreate(first_name="X", last_name="Y", city="Z", postal_code="12AB")
    # Bad phone
    with pytest.raises(ValidationError):
        MemberCreate(first_name="X", last_name="Y", city="Z", phone="123-abc")


def test_member_update_partial_and_none():
    # You may supply only some fields
    upd = MemberUpdate(email="me@example.com")
    assert upd.first_name is None
    assert upd.email == "me@example.com"

    # Or explicitly null out a boolean
    upd2 = MemberUpdate(no_postal_mail=None)
    assert hasattr(upd2, "no_postal_mail") and upd2.no_postal_mail is None


def test_member_response_roundtrip():
    """
    MemberResponse exposes exactly the fields declared in the schema:
    id, reference_number, first_name, last_name, city, optional attrs,
    and memberships: List[MembershipResponse].
    """
    # Build one nested MembershipResponse dict to feed into MemberResponse
    mship_dict = {
        "year": 2024,
        "amount": 25,
        "is_paid": True,
        "discounted": False,
    }
    # Assemble the full dict for MemberResponse
    data = {
        "id": 42,
        "reference_number": 2000000042,
        "first_name": "Anna",
        "last_name": "Korhonen",
        "city": "Helsinki",
        # optional ones:
        "email": "anna@example.com",
        "street_address": "Street 1",
        "postal_code": "00100",
        "phone": "+358401234567",
        "notes": "VIP",
        "no_postal_mail": True,
        # list of dicts matching MembershipResponse
        "memberships": [mship_dict],
    }

    resp = MemberResponse(**data)
    # Top‐level fields
    assert resp.id == 42
    assert resp.reference_number == 2000000042
    assert resp.first_name == "Anna"
    assert resp.city == "Helsinki"
    assert resp.no_postal_mail is True

    # Nested memberships
    assert isinstance(resp.memberships, list)
    assert len(resp.memberships) == 1
    m0 = resp.memberships[0]
    assert isinstance(m0, MembershipResponse)
    assert m0.year == 2024
    assert m0.amount == 25
    assert m0.is_paid
    assert not m0.discounted


def test_member_create_invalid_email():
    with pytest.raises(ValidationError):
        MemberCreate(
            first_name="A",
            last_name="B",
            city="C",
            email="not-an-email",
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("first_name", ""),
        ("last_name", ""),
        ("city", ""),
        ("first_name", "x" * 101),
        ("last_name", "x" * 101),
        ("city", "y" * 101),
    ],
)
def test_member_create_name_city_length_bounds(field, value):
    kwargs = {"first_name": "A", "last_name": "B", "city": "C"}
    kwargs[field] = value
    with pytest.raises(ValidationError):
        MemberCreate(**kwargs)


# 3) Omitting a required field on MemberResponse should raise
@pytest.mark.parametrize(
    "missing",
    [
        "id",
        "reference_number",
        "first_name",
        "last_name",
        "city",
    ],
)
def test_member_response_missing_required_field_raises(missing):
    # Build up a “complete” payload
    payload = {
        "id": 1,
        "reference_number": 2000000001,
        "first_name": "Anna",
        "last_name": "Korhonen",
        "city": "Helsinki",
        "email": "anna@example.com",
        "street_address": "Foo 1",
        "postal_code": "00100",
        "phone": "+123456789",
        "notes": "Test",
        "no_postal_mail": False,
        "memberships": [],
    }
    # Remove the required key
    payload.pop(missing)
    with pytest.raises(ValidationError):
        MemberResponse(**payload)


# 4) MemberUpdate pattern checks on partial updates
def test_member_update_invalid_postal_and_phone():
    # invalid postal_code
    with pytest.raises(ValidationError):
        MemberUpdate(postal_code="12-345")
    # invalid phone
    with pytest.raises(ValidationError):
        MemberUpdate(phone="(123)456")
