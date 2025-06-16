# app/schemas.py

from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, EmailStr, Field


class MembershipResponse(BaseModel):
    year: int
    amount: int
    is_paid: bool
    discounted: bool

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "year": 2024,
                "amount": 25,
                "is_paid": True,
                "discounted": False,
            }
        },
    }


class MemberBase(BaseModel):
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    city: Annotated[str, Field(min_length=1, max_length=100)]
    email: Optional[EmailStr] = None
    street_address: Optional[str] = None
    postal_code: Optional[Annotated[str, Field(pattern=r"^\d{3,10}$")]] = None
    phone: Optional[Annotated[str, Field(pattern=r"^\+?\d[\d\s]*$")]] = None
    notes: Optional[str] = None
    no_postal_mail: Optional[bool] = False

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "you@example.com",
                    "street_address": "Street Address 123",
                    "city": "City Name",
                    "postal_code": "00100",
                    "notes": "Prefers email contact",
                    "phone": "0401234567",
                    "no_postal_mail": False,
                }
            ]
        },
    }


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    first_name: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    last_name: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    city: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None
    email: Optional[EmailStr] = None
    street_address: Optional[str] = None
    postal_code: Optional[Annotated[str, Field(pattern=r"^\d{3,10}$")]] = None
    phone: Optional[Annotated[str, Field(pattern=r"^\+?\d[\d\s]*$")]] = None
    notes: Optional[str] = None
    no_postal_mail: Optional[bool] = None


class MemberResponse(MemberBase):
    id: int
    reference_number: int
    memberships: List[MembershipResponse] = []

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 3,
                "first_name": "Anna",
                "last_name": "Korhonen",
                "email": "anna@example.com",
                "city": "Helsinki",
                "postal_code": "00100",
                "reference_number": 2000000003,
                "no_postal_mail": False,
                "memberships": [
                    {"year": 2024, "amount": 25, "is_paid": True, "discounted": False}
                ],
            }
        },
    }


class MembershipCreate(BaseModel):
    year: Optional[int] = Field(default_factory=lambda: datetime.now().year)
    amount: int = Field(
        default=0, ge=0, description="Membership amount in euros (default: 0 = unpaid)"
    )
