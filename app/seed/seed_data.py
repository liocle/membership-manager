# ./app/seed/seed_data.py


import sys
from pathlib import Path

# Add parent directory (/app) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from database import SessionLocal
from models import Member, Membership
from sqlalchemy.orm import Session

# Create a new database session
db: Session = SessionLocal()

# === Seed Members and Memberships Together ===
seed_data = [
    {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice@example.com",
        "phone": "123456789",
        "city": "Helsinki",
        "postal_code": "00100",
        "no_postal_mail": False,
        "notes": "VIP Member",
        "memberships": [
            {"year": 2022, "amount": 25, "discounted": False},
            {"year": 2023, "amount": 25, "discounted": False},
            {"year": 2024, "amount": 25, "discounted": False},
            {"year": 2025, "amount": 25, "discounted": False},
        ],
    },
    {
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob@example.com",
        "phone": "987654321",
        "city": "Espoo",
        "postal_code": "02100",
        "no_postal_mail": True,
        "notes": "Prefers email communication",
        "memberships": [
            {"year": 2022, "amount": 25, "discounted": False},
            {"year": 2024, "amount": 17, "discounted": True},
        ],
    },
    {
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie@example.com",
        "phone": "555555555",
        "city": "Vantaa",
        "postal_code": "01300",
        "no_postal_mail": False,
        "notes": "Long-time supporter",
        "memberships": [
            {"year": 2023, "amount": 25, "discounted": False},
        ],
    },
    {
        "first_name": "Diana",
        "last_name": "Example",
        "email": "diana@example.com",
        "phone": "0400000000",
        "street_address": "Satamakatu 5 A",
        "city": "Tampere",
        "postal_code": "33100",
        "no_postal_mail": False,
        "notes": "New member with unpaid membership",
        "memberships": [
            {"year": 2025, "amount": 0, "discounted": False},  # Unpaid
        ],
    },
    {
        "first_name": "Erkki",
        "last_name": "Legacy",
        "email": "erkki@example.com",
        "phone": "0401234567",
        "street_address": "Aurantie 5 A",
        "city": "Turku",
        "postal_code": "20100",
        "no_postal_mail": False,
        "notes": "Has 2024 membership, 2025 unpaid",
        "memberships": [
            {"year": 2024, "amount": 25, "discounted": False},  # Paid
            {"year": 2025, "amount": 0, "discounted": False},  # Unpaid
        ],
    },
]

# Insert members with nested memberships
for entry in seed_data:
    if db.query(Member).filter_by(email=entry["email"]).first():
        continue  # Skip if already exists

    memberships_data = entry.pop("memberships", [])
    member = Member(**entry)

    for m in memberships_data:
        member.memberships.append(
            Membership(
                year=m["year"],
                amount=m["amount"],
                discounted=m["discounted"],
                is_paid=m["amount"] > 0,  # Paid if amount > 0
            )
        )

    db.add(member)
    db.flush()  # Flush to get the member ID for memberships
    print(
        f"📊 Inserted {len(member.memberships)} memberships for {member.first_name} {member.last_name}"
    )

db.commit()
db.close()
print("✅ Seeded members and their membership history successfully!")
