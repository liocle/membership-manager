# app/schemas.py

from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Optional

from pydantic import BaseModel, EmailStr, Field, field_serializer


class MembershipResponse(BaseModel):
    year: Optional[int] = Field(default_factory=lambda: datetime.now().year)
    amount: Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)] = Decimal(
        "0.00"
    )
    is_paid: bool
    discounted: bool

    @field_serializer("amount")
    def _ser_amount(self, v: Decimal) -> float:
        return float(v)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "year": 2024,
                "amount": 25.00,
                "is_paid": True,
                "discounted": False,
            }
        },
    }


class MembershipCreate(BaseModel):
    year: Optional[int] = Field(default_factory=lambda: datetime.now().year)
    amount: int = Field(
        default=0, ge=0, description="Membership amount in euros (default: 0 = unpaid)"
    )

    @field_serializer("amount")
    def _ser_amount(self, v: Decimal) -> float:
        return float(v)


class MemberBase(BaseModel):
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    city: Annotated[str, Field(min_length=1, max_length=100)]
    email: Optional[EmailStr] = None
    street_address: Optional[str] = None
    postal_code: Optional[Annotated[str, Field(pattern=r"^\d{3,10}$")]] = None
    phone: Optional[Annotated[str, Field(pattern=r"^\+?\d[\d\s]*$")]] = None
    notes: Optional[str] = None
    organization: Optional[str] = None
    no_postal_mail: Optional[bool] = False

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "First name",
                    "last_name": "Last name",
                    "organization": "Example Organization",
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
    organization: Optional[str] = None
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
    memberships: List[MembershipResponse] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 3,
                "first_name": "First name",
                "last_name": "Last name",
                "organization": "Example Organization",
                "email": "firstname.lastname@example.com",
                "city": "City Name",
                "postal_code": "00100",
                "reference_number": 2000000003,
                "no_postal_mail": False,
                "memberships": [
                    {
                        "year": 2024,
                        "amount": 25.00,
                        "is_paid": True,
                        "discounted": False,
                    }
                ],
            }
        },
    }


class MemberWithMessage(BaseModel):
    message: str
    member: MemberResponse


class MemberSearchResponse(BaseModel):
    total: int
    results: List[MemberResponse]
