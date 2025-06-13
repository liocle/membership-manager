# File: app/api/routes_member.py

"""
Routes for member-related search and query operations.
"""

from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Member, Membership
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

    return {
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
    }


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
    return {"results": members}


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
    return {"results": members}


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
    return {"results": members}


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
    return {"results": members}


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
    return member
