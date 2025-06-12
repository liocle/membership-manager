# app/models.py

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
from sqlalchemy.orm import relationship

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
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)
    city = Column(String, index=True)
    postal_code = Column(String, index=True)
    no_postal_mail = Column(Boolean, default=False)
    notes = Column(String, nullable=True)
    created_at = Column(Date, nullable=False, server_default=func.now())
    modified_at = Column(
        Date, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Use the defined sequence in the reference_number column
    reference_number = Column(
        BigInteger,
        unique=True,
        nullable=False,
        server_default=reference_number_seq.next_value(),
    )

    # Computed column generated from first_name and last_name
    full_name = Column(
        String,
        Computed("first_name || ' ' || last_name", persisted=True),
        nullable=False,
        index=True,
    )

    memberships = relationship("Membership", back_populates="member")


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(BigInteger, primary_key=True, index=True)
    member_id = Column(BigInteger, ForeignKey("members.id"))
    year = Column(Integer, index=True)
    amount = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=False)
    discounted = Column(Boolean, default=False)

    member = relationship("Member", back_populates="memberships")
