"""
membership-manager/app/main.py

This module sets up a basic FastAPI application with a single route.
The root URL ("/") returns a welcome message.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Member, Membership


app = FastAPI()


# Simple route to return a STATIC welcome message
# Requires a FastAPI app instance, does not require database access
@app.get("/")
def read_root():
    return {"message": "Welcome to the Membership Manager API!"}


# Dependency to get a database session for each request
# SQLAlchemy requires a session to interact with the database
# How It Works in FastAPI:
# When FastAPI receives a request, it calls get_db().
# SessionLocal() creates a database session.
# The function returns the session to the endpoint function.
# When FastAPI finishes processing, it automatically closes the session (finally: db.close()).
# This prevents memory leaks and ensures every API request gets a fresh database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/members/search/{reference_number}")
def get_member_by_reference(reference_number: str, db: Session = Depends(get_db)):
    # FastAPI calls get_db() to get a database session
    # SQLAlchemy fetches the member by reference number
    member = (
        db.query(Member).filter(Member.reference_number == reference_number).first()
    )

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Fetch all their membership payments
    memberships = db.query(Membership).filter(Membership.member_id == member.id).all()

    # Format the response
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


# Search by full name (supports partial search)
@app.get("/members/search/full_name/{name}")
def search_by_full_name(name: str, db: Session = Depends(get_db)):
    members = db.query(Member).filter(Member.full_name.ilike(f"%{name}%")).all()
    return {"results": members}


# Search by first name OR last name
@app.get("/members/search/name/{name}")
def search_by_name(name: str, db: Session = Depends(get_db)):
    members = (
        db.query(Member)
        .filter(
            (Member.first_name.ilike(f"%{name}%"))
            | (Member.last_name.ilike(f"%{name}%"))
        )
        .all()
    )
    return {"results": members}


# Search by city
@app.get("/members/search/city/{city}")
def search_by_city(city: str, db: Session = Depends(get_db)):
    members = db.query(Member).filter(Member.city.ilike(f"%{city}%")).all()
    return {"results": members}


# Search by postal code
@app.get("/members/search/postal/{postal_code}")
def search_by_postal(postal_code: str, db: Session = Depends(get_db)):
    members = db.query(Member).filter(Member.postal_code == postal_code).all()
    return {"results": members}


# Search by reference number (exact match)
@app.get("/members/search/reference/{reference_number}")
def search_by_reference(reference_number: str, db: Session = Depends(get_db)):
    member = (
        db.query(Member).filter(Member.reference_number == reference_number).first()
    )
