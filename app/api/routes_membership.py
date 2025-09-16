# ./app/api/routes_membership.py

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import Member, Membership
from pydantic import BaseModel
from schemas import MembershipCreate, MembershipResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/members", tags=["members"])


# TODO Change all HTTP responses to use status codes


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    # Create and persist the Membership
    membership = Membership(
        member_id=member_id,
        year=membership_in.year,
        amount=membership_in.amount,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": f"Membership for year {membership.year} created for member ID {member_id}.",
            "membership": MembershipResponse.model_validate(membership).model_dump(),
        },
    )


class MembershipUpdate(BaseModel):
    amount: int


@router.put("/{member_id}/memberships/{year}", tags=["members"])
def update_membership_for_year(
    member_id: int, year: int, patch: MembershipUpdate, db: Session = Depends(get_db)
):
    m = (
        db.query(Membership)
        .filter(Membership.member_id == member_id, Membership.year == year)
        .first()
    )
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found"
        )

    m.amount = patch.amount  # triggers @validates('amount') to recompute flags
    db.commit()
    db.refresh(m)

    return MembershipResponse.model_validate(m).model_dump()


@router.delete("/{member_id}/memberships/{year}", tags=["members"])
def delete_membership_for_year(
    member_id: int, year: int, db: Session = Depends(get_db)
):
    m = (
        db.query(Membership)
        .filter(Membership.member_id == member_id, Membership.year == year)
        .first()
    )
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found"
        )

    db.delete(m)
    db.commit()
    return {"message": "Membership deleted."}


@router.get("/{member_id}/memberships", tags=["members"])
def list_memberships_for_member(member_id: int, db: Session = Depends(get_db)):
    items = (
        db.query(Membership)
        .filter(Membership.member_id == member_id)
        .order_by(Membership.year.desc())
        .all()
    )
    return [MembershipResponse.model_validate(m).model_dump() for m in items]
