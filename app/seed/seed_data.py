import sys
from pathlib import Path

# Add parent directory (i.e., /app/) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from database import SessionLocal
from models import Member
from sqlalchemy.orm import Session

# Create a new database session
db: Session = SessionLocal()

# Sample test members
test_members = [
    Member(
        first_name="Alice",
        last_name="Johnson",
        email="alice@example.com",
        phone="123456789",
        city="Helsinki",
        postal_code="00100",
        no_postal_mail=False,
        notes="VIP Member",
    ),
    Member(
        first_name="Bob",
        last_name="Smith",
        email="bob@example.com",
        phone="987654321",
        city="Espoo",
        postal_code="02100",
        no_postal_mail=True,
        notes="Prefers email communication",
    ),
    Member(
        first_name="Charlie",
        last_name="Brown",
        email="charlie@example.com",
        phone="555555555",
        city="Vantaa",
        postal_code="01300",
        no_postal_mail=False,
        notes="Long-time supporter",
    ),
]


# Insert only if the email doesn't already exist
inserted = 0
for member in test_members:
    if not db.query(Member).filter_by(email=member.email).first():
        db.add(member)
        inserted += 1

db.commit()
db.close()

print("✅ Test data inserted successfully!")
