# ./create_tables.py

# === Standard lib
import os

# === Local
from database import Base, engine

# === Third-party
from dotenv import load_dotenv
from models import Member, Membership  # noqa: F401
from sqlalchemy.orm import Session

# Load .env vars
load_dotenv()
print(f"📡 DATABASE_URL = '{os.getenv('DATABASE_URL')}'")

# Debug vars
print("Environment variables check:")
for var in [
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "DATABASE_URL",
]:
    print(f"\t{var}: {os.getenv(var)}")
print(" Environment variables check complete!")
print(
    "________________________________________________________________________________"
)

# Drop & recreate tables
print("🔄 Dropping and recreating database tables in:", engine.url)
Base.metadata.drop_all(bind=engine)
print("✅ Dropped existing tables (if any)...")
Base.metadata.create_all(bind=engine)

session = Session(engine)
session.commit()
print("✅ Database tables created successfully!")
