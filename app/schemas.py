# app/schemas.py

from typing import List, Optional

from pydantic import BaseModel


class MembershipResponse(BaseModel):
    year: int
    amount: int
    is_paid: bool
    discounted: bool

    class Config:
        orm_mode = True


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    notes: Optional[str] = None
    phone: Optional[str] = None
    no_postal_mail: Optional[bool] = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "you@example.com",
                    "street_address": "Main Street 12 A",
                    "city": "Helsinki",
                    "postal_code": "00100",
                    "notes": "Prefers email contact",
                    "phone": "0401234567",
                    "no_postal_mail": False,
                }
            ]
        }
    }


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    notes: Optional[str] = None
    no_postal_mail: Optional[bool] = None


class MemberResponse(MemberBase):
    id: int
    reference_number: int
    memberships: List[MembershipResponse] = []

    class Config:
        orm_mode = True
