# File: app/api/routes_member.py

"""
Routes for member-related search and query operations.
"""

from datetime import datetime

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import Member, Membership
from schemas import MemberCreate, MemberResponse, MemberUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/search/{reference_number}")
def get_member_by_reference(reference_number: str, db: Session = Depends(get_db)):
    """
    Fetch a member and their memberships by reference number.

    Args:
        reference_number (str): Unique reference number of the member.
        db (Session): SQLAlchemy DB session (injected).

    Returns:
        dict: Member details including memberships.

    Raises:
        HTTPException: If no member is found.
    """
    member = (
        db.query(Member).filter(Member.reference_number == reference_number).first()
    )

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    memberships = db.query(Membership).filter(Membership.member_id == member.id).all()

    return JSONResponse(
        status_code=200,
        content={
            "message": f"Member {reference_number} and their memberships fetched successfully.",
            "member": {
                "id": member.id,
                "first_name": member.first_name,
                "last_name": member.last_name,
                "email": member.email,
                "city": member.city,
                "postal_code": member.postal_code,
                "notes": member.notes,
                "reference_number": member.reference_number,
                "no_postal_mail": member.no_postal_mail,
                "memberships": [
                    {
                        "year": m.year,
                        "amount": m.amount,
                        "is_paid": m.is_paid,
                        "discounted": m.discounted,
                    }
                    for m in memberships
                ],
            },
        },
    )


@router.get("/search/full_name/{name}")
def search_by_full_name(name: str, db: Session = Depends(get_db)):
    """
    Search members by partial or full name.

    Args:
        name (str): Full or partial name string.

    Returns:
        dict: List of matching members.
    """
    members = db.query(Member).filter(Member.full_name.ilike(f"%{name}%")).all()
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Found {len(members)} member(s) matching full name '{name}'.",
            "results": [MemberResponse.model_validate(m).model_dump() for m in members],
        },
    )


@router.get("/search/name/{name}")
def search_by_name(name: str, db: Session = Depends(get_db)):
    """
    Search members by first or last name.

    Args:
        name (str): Name string to match.

    Returns:
        dict: List of matching members.
    """
    members = (
        db.query(Member)
        .filter(
            (Member.first_name.ilike(f"%{name}%"))
            | (Member.last_name.ilike(f"%{name}%"))
        )
        .all()
    )
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Found {len(members)} member(s) matching name '{name}'.",
            "results": [MemberResponse.model_validate(m).model_dump() for m in members],
        },
    )


@router.get("/search/city/{city}")
def search_by_city(city: str, db: Session = Depends(get_db)):
    """
    Search members by city name.

    Args:
        city (str): City name.

    Returns:
        dict: List of members in the specified city.
    """
    members = db.query(Member).filter(Member.city.ilike(f"%{city}%")).all()
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Found {len(members)} member(s) in city '{city}'.",
            "results": [MemberResponse.model_validate(m).model_dump() for m in members],
        },
    )


@router.get("/search/postal/{postal_code}")
def search_by_postal(postal_code: str, db: Session = Depends(get_db)):
    """
    Search members by postal code.

    Args:
        postal_code (str): Postal code to match.

    Returns:
        dict: List of members with that postal code.
    """
    members = db.query(Member).filter(Member.postal_code == postal_code).all()
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Found {len(members)} member(s) with postal code {postal_code}.",
            "results": [MemberResponse.model_validate(m).model_dump() for m in members],
        },
    )


@router.get("/search/reference/{reference_number}")
def search_by_reference(reference_number: str, db: Session = Depends(get_db)):
    """
    Search a member by reference number (exact match).

    Args:
        reference_number (str): Member's unique reference number.

    Returns:
        dict or HTTPException: The matched member or 404.
    """
    member = (
        db.query(Member).filter(Member.reference_number == reference_number).first()
    )
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Member with reference number {reference_number} found.",
            "member": MemberResponse.model_validate(member).model_dump(),
        },
    )


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member_in: MemberCreate, db: Session = Depends(get_db)):
    """
    Create a new member (admin-initiated, no membership auto-created).

    Args:
        member_in (MemberCreate): Input data for creating a new member.
        db (Session): SQLAlchemy DB session (injected).

    Returns:
        JSONResponse: Success message and created member data.
    """
    member = Member(**member_in.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Member created successfully.",
            "member": MemberResponse.model_validate(member).model_dump(),
        },
    )


@router.put("/{id}", response_model=MemberResponse)
def update_member(id: int, updates: MemberUpdate, db: Session = Depends(get_db)):
    """
    Update an existing member by ID.

    Args:
        id (int): ID of the member to update.
        updates (MemberUpdate): Fields to update.
        db (Session): SQLAlchemy DB session (injected).

    Returns:
        JSONResponse: Confirmation message and updated data.
    """
    member = db.query(Member).filter(Member.id == id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)

    return JSONResponse(
        status_code=200,
        content={
            "message": f"Member {member.id} updated successfully.",
            "member": MemberResponse.model_validate(member).model_dump(),
        },
    )


@router.post(
    "/new_member", response_model=MemberResponse, status_code=status.HTTP_201_CREATED
)
def register_new_member(member_in: MemberCreate, db: Session = Depends(get_db)):
    """
    Register a new member and automatically create an unpaid membership.

    This is the primary intake endpoint (e.g., from email form).
    """
    # Create the member
    member = Member(**member_in.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)

    # Create default unpaid membership for current year
    membership = Membership(
        member_id=member.id,
        year=datetime.now().year,
        amount=0,
        is_paid=False,
        discounted=False,
    )
    db.add(membership)
    db.commit()

    db.refresh(member)
    return JSONResponse(
        status_code=201,
        content={
            "message": "Member created successfully.",
            "member": MemberResponse.model_validate(member).model_dump(),
        },
    )


@router.delete("/members/{member_id}", status_code=200)
def delete_member(member_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a member by ID and return a confirmation message.

    Args:
        member_id (int): ID of the member to delete.
        db (Session): SQLAlchemy DB session.

    Raises:
        HTTPException: If member not found.

    Returns:
        dict: JSON message with deletion confirmation.
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()

    return {"message": f"Member with ID {member_id} was deleted successfully."}
