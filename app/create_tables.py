# ./create_tables.py

import os
import sys

from config import settings
from database import Base, engine
from models import Member, Membership
from sqlalchemy.orm import Session

print(f"📡 Creating tables on {settings.DATABASE_URL!r}")

# Drop & recreate tables
print("🔄 Dropping and recreating database tables in:", engine.url)
Base.metadata.drop_all(bind=engine, checkfirst=True)
print("✅ Dropped existing tables (if any)...")
Base.metadata.create_all(bind=engine)

print("__DEBUG:")
print(
    f"[CREATE_TABLES] ENV_FILE={os.getenv('ENV_FILE')!r}, DATABASE_URL={settings.DATABASE_URL!r}",
    file=sys.stderr,
)

session = Session(engine)
session.commit()
print("✅ Database tables created successfully!")
