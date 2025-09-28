# File: app/api/routes_member.py

"""
Routes for member-related search and query operations.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import Member, Membership
from pdf.generate_welcome_letter import generate_pdf
from schemas import (
    MemberCreate,
    MemberResponse,
    MemberUpdate,
    MemberWithMessage,
    MemberListResponse,
)
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

router = APIRouter(prefix="/members", tags=["members"])


# TODO Change all HTTP responses to use status codes


@router.get(
    "/search/{reference_number}",
    response_model=MemberWithMessage,
    status_code=status.HTTP_200_OK,
)
def get_member_by_reference(reference_number: int, db: Session = Depends(get_db)):
    """
    Fetch a member and their memberships by reference number.

    Args:
        reference_number (int): Unique reference number of the member.
        db (Session): SQLAlchemy DB session (injected).

    Returns:
        dict: Member details including memberships.

    Raises:
        HTTPException: If no member is found.
    """
    member = (
        db.query(Member)
        .options(joinedload(Member.memberships))
        .filter(Member.reference_number == reference_number)
        .first()
    )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )
    memberships = db.query(Membership).filter(Membership.member_id == member.id).all()
    return MemberWithMessage(
        message=f"Member {reference_number} and their memberships fetched successfully.",
        member=member,
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
        status_code=status.HTTP_200_OK,
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
        status_code=status.HTTP_200_OK,
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
        status_code=status.HTTP_200_OK,
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
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Found {len(members)} member(s) with postal code {postal_code}.",
            "results": [MemberResponse.model_validate(m).model_dump() for m in members],
        },
    )


@router.get(
    "/search/reference/{reference_number}",
    response_model=MemberWithMessage,
    status_code=status.HTTP_200_OK,
)
def search_by_reference(
    reference_number: int,
    db: Session = Depends(get_db),
):
    """
    Search a member by reference number (exact match).

    Args:
        reference_number (str): Member's unique reference number.

    Returns:
        dict or HTTPException: The matched member or 404.
    """

    #     reference_number = int(reference_number)
    # except ValueError:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Reference number must be an integer",
    #     )
    member = (
        db.query(Member)
        .options(joinedload(Member.memberships))
        .filter(Member.reference_number == reference_number)
        .first()
    )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )
    return MemberWithMessage(
        message=f"Member with reference number {reference_number} found.",
        member=MemberResponse.model_validate(member),
    )


@router.post("/", response_model=MemberWithMessage, status_code=status.HTTP_201_CREATED)
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

    return MemberWithMessage(
        message=f"Member {member.first_name} {member.last_name} created.",
        member=member,
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Member {member.id} updated successfully.",
            "member": MemberResponse.model_validate(member).model_dump(),
        },
    )


@router.post(
    "/new_member", response_model=MemberWithMessage, status_code=status.HTTP_201_CREATED
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
    return MemberWithMessage(
        message=f"Member {member.first_name} {member.last_name} created.",
        member=member,
    )


@router.delete("/{member_id}", status_code=status.HTTP_200_OK)
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    db.delete(member)
    db.commit()

    return {"message": f"Member with ID {member_id} was deleted successfully."}


@router.post("/{member_id}/generate_welcome_letter")
def generate_letter(member_id: int, db: Session = Depends(get_db)):
    """
    Generate and save a PDF welcome letter for a given member.

    Args:
        member_id (int): ID of the member.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Confirmation message and path to generated file.
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    if not member.memberships:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Member has no memberships"
        )

    membership = sorted(member.memberships, key=lambda m: m.year, reverse=True)[0]

    try:
        filepath = generate_pdf(member, membership, output_dir=Path("output/letters"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {e}",
        )

    return {"message": "PDF generated successfully", "path": str(filepath)}


@router.get("/", response_model=MemberListResponse, tags=["members"])
def list_members(
    q: Optional[str] = None,
    city: Optional[str] = None,
    postal_code: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    List members with basic filtering & pagination.
    """
    query = db.query(Member)

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(Member.full_name.ilike(like), Member.email.ilike(like))
        )
    if city:
        query = query.filter(Member.city.ilike(f"%{city}%"))
    if postal_code:
        query = query.filter(Member.postal_code == postal_code)

    total = query.count()
    rows = query.order_by(Member.id.desc()).offset(offset).limit(limit).all()

    items = [MemberResponse.model_validate(m).model_dump() for m in rows]
    return MemberListResponse(items=items, total=total)


@router.post("/{member_id}/letters")
def generate_welcome_letter(member_id: int, db: Session = Depends(get_db)):
    """
    Generate a welcome letter PDF for the *current year*.
    If the member has no membership for the current year, use an in-memory
    (non-persisted) membership with amount=0.
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )

    current_year = datetime.now().year
    membership = (
        db.query(Membership)
        .filter(Membership.member_id == member_id, Membership.year == current_year)
        .first()
    )

    if not membership:
        # Build a transient Membership object (do not add/commit)
        membership = Membership(
            member_id=member_id,
            year=current_year,
            amount=0,
            is_paid=False,
            discounted=False,
        )

    try:
        filepath = generate_pdf(member, membership, output_dir=Path("output/letters"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {e}",
        )

    return {"message": "PDF generated successfully", "path": str(filepath)}
