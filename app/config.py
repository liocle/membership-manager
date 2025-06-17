# app/config.py

import os
import sys
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Which environment we’re running in: development, test, or production
    ENV: Literal["development", "test", "production"] = "development"

    # Full connection string—overridden by ENV_FILE
    DATABASE_URL: str = "postgresql://admin:changeme@localhost:5432/members_db"

    # Business logic defaults
    STANDARD_MEMBERSHIP_FEE: int = 25
    UNPAID_MEMBERSHIP: int = 0

    # Tell Pydantic which file to load
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        extra="ignore",
    )


# Singleton instance, import this everywhere
settings = Settings()
# DEBUG: show exactly what got loaded

print(
    f"[CONFIG] sys.argv={sys.argv[:1]}, "
    f"ENV_FILE={os.getenv('ENV_FILE')!r}, "
    f"settings.ENV={settings.ENV!r}, "
    f"settings.DATABASE_URL={settings.DATABASE_URL!r}",
    file=sys.stderr,
)
