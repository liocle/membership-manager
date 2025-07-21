# app/scripts/generate_letters.py

from pathlib import Path

from database import SessionLocal
from models import Member
from pdf.generate_welcome_letter import generate_pdf

output_dir = Path("output/letters")


def main():
    db = SessionLocal()
    members = db.query(Member).all()
    count = 0

    for member in members:
        for membership in member.memberships:
            if membership.amount == 0 and not membership.is_paid:
                generate_pdf(member, membership, output_dir)
                count += 1

    db.close()
    print(f"✅ Generated {count} welcome letter(s).")


if __name__ == "__main__":
    main()
