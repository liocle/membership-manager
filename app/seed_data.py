from sqlalchemy.orm import Session
from database import SessionLocal
from models import Member, Membership

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
        reference_number="REF001",
        no_postal_mail=False,
        notes="VIP Member"
    ),
    Member(
        first_name="Bob",
        last_name="Smith",
        email="bob@example.com",
        phone="987654321",
        city="Espoo",
        postal_code="02100",
        reference_number="REF002",
        no_postal_mail=True,
        notes="Prefers email communication"
    ),
    Member(
        first_name="Charlie",
        last_name="Brown",
        email="charlie@example.com",
        phone="555555555",
        city="Vantaa",
        postal_code="01300",
        reference_number="REF003",
        no_postal_mail=False,
        notes="Long-time supporter"
    ),
    Member(
            first_name="Georgette",
            last_name="Johnson",
            email="georgette@example.com",
            phone="123456789",
            city="Helsinki",
            postal_code="00100",
            reference_number="REF004",
            no_postal_mail=False,
            notes="VIP Member"
        ),
]

# Add members to database
db.add_all(test_members)
db.commit()

# Close session
db.close()

print("✅ Test data inserted successfully!")
