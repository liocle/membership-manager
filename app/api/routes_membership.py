# ./app/api/routes_membership.py

from config import settings
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import Member, Membership
from schemas import MembershipCreate, MembershipResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/members", tags=["members"])


@router.post(
    "/{member_id}/memberships",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_membership_for_member(
    member_id: int,
    membership_in: MembershipCreate,
    db: Session = Depends(get_db),
):
    """
    Admin-only: Manually create a new membership for an existing member.

    This endpoint is used for manual corrections or historical data import.
    The user provides 'amount' (default 0) and optionally the 'year'.
    We compute 'is_paid' and 'discounted' based on amount.
    """
    # Lookup member existence
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Determine internal logic flags
    amount = membership_in.amount
    is_paid = amount > settings.UNPAID_MEMBERSHIP_AMOUNT
    is_discounted = (
        settings.UNPAID_MEMBERSHIP_AMOUNT < amount < settings.STANDARD_MEMBERSHIP_FEE
    )

    # Create and persist the Membership
    membership = Membership(
        member_id=member_id,
        year=membership_in.year,
        amount=amount,
        is_paid=is_paid,
        discounted=is_discounted,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)

    return JSONResponse(
        status_code=201,
        content={
            "message": f"Membership for year {membership.year} created for member ID {member_id}.",
            "membership": MembershipResponse.model_validate(membership).model_dump(),
        },
    )
