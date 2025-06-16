# app/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application-wide configuration settings.

    This class automatically reads values from environment variables,
    falling back to the defaults defined here if the environment variables are missing.
    It's designed to centralize constants and settings like fees, toggles, or secrets.

    Attributes:
        STANDARD_MEMBERSHIP_FEE (int): Default membership fee (used unless overridden in .env).
        UNPAID_MEMBERSHIP_AMOUNT (int): Default initial amount for unpaid memberships.
    """

    STANDARD_MEMBERSHIP_FEE: int = 25
    UNPAID_MEMBERSHIP_AMOUNT: int = 0

    class Config:
        env_file = ".env"


# Create a singleton settings object that can be imported app-wide
settings = Settings()
