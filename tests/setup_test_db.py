# tests/setup_test_db.py

import os
import sys

from config import settings
from database import Base, engine
from models import Member, Membership  # noqa: F401
from sqlalchemy_utils import create_database, database_exists, drop_database

# prevent Member/Membership imports from looking unused and having ruff formatter removing the imports
_ = (Member, Membership)

# 1. Force test mode so we load .env.test
settings.ENV = "test"

# 2. Drop & recreate the database according to settings.DATABASE_URL
if database_exists(settings.DATABASE_URL):
    drop_database(settings.DATABASE_URL)
create_database(settings.DATABASE_URL)

# 3. Build your tables
Base.metadata.create_all(bind=engine)

print("✅ Test database created:", settings.DATABASE_URL)

print(
    f"[TEST_SETUP] sys.argv={sys.argv[:1]}, "
    f"ENV_FILE={os.getenv('ENV_FILE')!r}, "
    f"settings.ENV={settings.ENV!r}, "
    f"settings.DATABASE_URL={settings.DATABASE_URL!r}",
    file=sys.stderr,
)
