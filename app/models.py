# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship
from database import Base

class Member(Base):
	__tablename__ = "members"

	id = Column(Integer, primary_key=True, index=True)
	first_name = Column(String, index=True)
	last_name = Column(String, index=True)
	email = Column(String, unique=True, index=True, nullable=True)
	phone = Column(String, nullable=True)
	city = Column(String, index=True)
	postal_code = Column(String, index=True)
	reference_number = Column(String, unique=True, nullable=False)
	no_postal_mail = Column(Boolean, default=False)
	notes = Column(String, nullable=True)

	# computed column generated from first_name and last_name
	full_name = Column(String, Computed("first_name || ' ' || last_name", persisted=True), nullable=False, index=True)

	memberships = relationship("Membership", back_populates="member")

class Membership(Base):
	__tablename__ = "memberships"

	id = Column(Integer, primary_key=True, index=True)
	member_id = Column(Integer, ForeignKey("members.id"))
	year = Column(Integer, index=True)
	amount = Column(Integer, nullable=False)
	is_paid = Column(Boolean, default=False)
	discounted = Column(Boolean, default=False)

	member = relationship("Member", back_populates="memberships")
