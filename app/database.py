# app/database.py

# app/database.py
import sys

from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# The URL now comes straight from settings.DATABASE_URL
print(
    f"[DB] creating engine with DATABASE_URL={settings.DATABASE_URL!r}", file=sys.stderr
)
engine = create_engine(settings.DATABASE_URL, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

Base = declarative_base()


def get_db():
    """
    Yields a new database session for each request, then closes it.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
