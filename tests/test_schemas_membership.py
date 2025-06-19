# tests/test_schemas_membership.py
from datetime import datetime

import pytest
from pydantic import ValidationError
from schemas import MembershipCreate, MembershipResponse


def test_membership_create_defaults_year_and_amount():
    m = MembershipCreate()
    assert m.year == datetime.now().year
    assert m.amount == 0


def test_membership_create_negative_amount_rejected():
    with pytest.raises(ValidationError):
        MembershipCreate(amount=-1)


def test_membership_response_model():
    class Dummy:
        year = 2023
        amount = 50
        is_paid = True
        discounted = False

    resp = MembershipResponse.model_validate(Dummy())
    assert resp.year == 2023
    assert resp.is_paid
    assert resp.discounted is False
