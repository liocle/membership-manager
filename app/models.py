# app/models.py

# model.py defines the database models for the application as a class.

from config import settings
from database import Base
from sqlalchemy import (
    DDL,
    BigInteger,
    Boolean,
    Column,
    Computed,
    Date,
    ForeignKey,
    Integer,
    Sequence,
    String,
    event,
    func,
)
from sqlalchemy.orm import relationship, validates

# Define the sequence for reference_number, starting at 2_000_000_000
reference_number_seq = Sequence("reference_number_seq", start=2000000000, increment=1)
# Explicitly create sequence before tables
event.listen(
    Base.metadata,
    "before_create",
    DDL(
        "CREATE SEQUENCE IF NOT EXISTS reference_number_seq START WITH 2000000000 INCREMENT BY 1 OWNED BY NONE;"
    ),
)


class Member(Base):
    __tablename__ = "members"

    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    city = Column(String(100), index=True)
    street_address = Column(String(200), nullable=True)
    postal_code = Column(String(20), index=True)
    email = Column(String(320), unique=True, index=True, nullable=True)
    phone = Column(String(20), nullable=True)
    no_postal_mail = Column(Boolean, default=False)
    notes = Column(String(2000), nullable=True)
    created_at = Column(Date, nullable=False, server_default=func.now())
    organization = Column(String(200), nullable=True)
    modified_at = Column(
        Date, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    reference_number = Column(
        BigInteger,
        unique=True,
        nullable=False,
        server_default=reference_number_seq.next_value(),
    )

    full_name = Column(
        String,
        Computed("first_name || ' ' || last_name", persisted=True),
        nullable=False,
        index=True,
    )

    memberships = relationship(
        "Membership", back_populates="member", cascade="all, delete-orphan"
    )


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(BigInteger, primary_key=True, index=True)
    member_id = Column(BigInteger, ForeignKey("members.id"), nullable=False, index=True)
    year = Column(Integer, index=True)
    amount = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=False)
    discounted = Column(Boolean, default=False)

    member = relationship("Member", back_populates="memberships")

    @validates("amount")
    def _compute_payment_flags(self, _: str, value: int) -> int:
        """
        Whenever `amount` is set on a Membership, auto-compute:
          - is_paid: True if amount > UNPAID_MEMBERSHIP
          - discounted: True if in (UNPAID_MEMBERSHIP, STANDARD_MEMBERSHIP_FEE)
        """
        # note: value is the new amount
        self.is_paid = value > settings.UNPAID_MEMBERSHIP
        print(f"[DEBUG] _compute_payment_flags: amount={value}, is_paid={self.is_paid}")
        print(
            f"[DEBUG] _compute_payment_flags: UNPAID_MEMBERSHIP={settings.UNPAID_MEMBERSHIP}, "
            f"STANDARD_MEMBERSHIP_FEE={settings.STANDARD_MEMBERSHIP_FEE}"
        )
        self.discounted = (
            settings.UNPAID_MEMBERSHIP < value < settings.STANDARD_MEMBERSHIP_FEE
        )
        print(
            f"[DEBUG] _compute_payment_flags: discounted={self.discounted}, STANDARD_MEMBERSHIP_FEE={settings.STANDARD_MEMBERSHIP_FEE} "
        )
        return value
