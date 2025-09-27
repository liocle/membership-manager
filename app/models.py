# app/models.py

# model.py defines the database models for the application as a class.

import logging
from decimal import Decimal

from config import settings
from database import Base
from sqlalchemy import (
    DDL,
    BigInteger,
    Boolean,
    Column,
    Computed,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    Sequence,
    String,
    UniqueConstraint,
    event,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

logger = logging.getLogger(__name__)

# Define the sequence for reference_number, starting at 2_000_000_000
reference_number_seq = Sequence("reference_number_seq", start=2000000000, increment=1)
# Create the sequence BEFORE tables (so server_default can reference it)
event.listen(
    Base.metadata,
    "before_create",
    DDL(
        "CREATE SEQUENCE IF NOT EXISTS reference_number_seq "
        "START WITH 2000000000 INCREMENT BY 1 OWNED BY NONE;"
    ),
)

# After tables exist, attach ownership to members.reference_number
event.listen(
    Base.metadata,
    "after_create",
    DDL("ALTER SEQUENCE reference_number_seq OWNED BY members.reference_number;"),
)


class Member(Base):
    __tablename__ = "members"

    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    city = Column(String(100), index=True)
    street_address = Column(String(200), nullable=True)
    postal_code = Column(String(20), index=True)
    email = Column(String(320), unique=True, index=True, nullable=True)
    phone = Column(String(20), nullable=True)
    no_postal_mail = Column(Boolean, default=False)
    notes = Column(String(2000), nullable=True)
    organization = Column(String(200), nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    modified_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
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
    __table_args__ = (UniqueConstraint("member_id", "year", name="uq_member_year"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("members.id"), nullable=False, index=True
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_paid: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    discounted: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

    member = relationship("Member", back_populates="memberships")

    @validates("amount")
    def _compute_payment_flags(self, _: str, value: Decimal) -> Decimal:
        """
        Whenever `amount` is set on a Membership, auto-compute:
          - is_paid: True if amount > UNPAID_MEMBERSHIP
          - discounted: True if in (UNPAID_MEMBERSHIP, STANDARD_MEMBERSHIP_FEE)
        """
        unpaid = Decimal(str(settings.UNPAID_MEMBERSHIP))
        standard = Decimal(str(settings.STANDARD_MEMBERSHIP_FEE))

        self.is_paid = value > unpaid
        logger.debug("amount=%s is_paid=%s", value, self.is_paid)

        self.discounted = unpaid < value < standard
        logger.debug(
            "discounted=%s (unpaid=%s standard=%s)", self.discounted, unpaid, standard
        )

        return value
