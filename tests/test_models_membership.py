# tests/test_models_membership.py
# pyright: reportGeneralTypeIssues=false

from config import settings
from models import Membership


def test_membership_default_flags():
    """
    When Membership is instantiated without ever flushing to the DB,
    the default booleans should be False.
    """
    m = Membership(amount=0, year=2025)
    assert m.is_paid is False
    assert m.discounted is False


def test_membership_flag_logic():
    """
    The @validates('amount') hook should set:
      - is_paid  True if amount > UNPAID_MEMBERSHIP
      - discounted True if UNPAID_MEMBERSHIP < amount < STANDARD_MEMBERSHIP_FEE
    """
    # unpaid
    m0 = Membership(amount=0, year=2025)
    assert not m0.is_paid
    assert not m0.discounted

    # paid & discounted
    m1 = Membership(amount=settings.UNPAID_MEMBERSHIP + 1, year=2025)
    assert m1.is_paid
    assert m1.discounted

    # paid only
    m2 = Membership(amount=settings.STANDARD_MEMBERSHIP_FEE, year=2025)
    assert m2.is_paid
    assert not m2.discounted
