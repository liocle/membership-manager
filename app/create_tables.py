import os

from database import Base, engine
from dotenv import load_dotenv
from models import Member, Membership
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()
print(f"📡 DATABASE_URL = '{os.getenv('DATABASE_URL')}'")

# {{{ Debugging environment variable check ######
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
# }}} Debugging environment variable check ######


print("🔄 Dropping and recreating database tables in:", engine.url)

# Drop all tables first (optional, for a clean start)
Base.metadata.drop_all(bind=engine)

print("✅ Dropped existing tables (if any)...")


# Create tables
Base.metadata.create_all(bind=engine)

# Force SQLAlchemy to commit the changes
session = Session(engine)
session.commit()

print("✅ Database tables created successfully!")
