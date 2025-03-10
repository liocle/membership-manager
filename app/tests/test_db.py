from database import SessionLocal
from models import Member

db = SessionLocal()

# Create a test member (DO NOT set created_at, modified_at)
new_member = Member(
    first_name="Alice",
    last_name="Johnson",
    email="alice@example.com",
    phone="123456789",
    city="Helsinki",
    postal_code="00100",
    no_postal_mail=False,
    notes="VIP Member",
)
db.add(new_member)

db.commit()
db.refresh(new_member)

# ✅ Check if values are generated correctly
print(f"✅ Generated Reference Number: {new_member.reference_number}")
print(f"✅ Full Name: {new_member.full_name}")
print(f"✅ Created At: {new_member.created_at}")  # Should not be None
print(f"✅ Modified At: {new_member.modified_at}")  # Should not be None

db.close()
