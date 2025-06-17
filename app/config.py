# app/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application-wide configuration settings for the Membership Manager.

    This class loads environment variables using Pydantic BaseSettings. Defaults are provided
    for local development, testing, and CI purposes, and can be overridden via a `.env` file
    or OS-level environment variables.

    Centralizes infrastructure, application, database, and business logic settings.

    Attributes:
        APP_NAME (str): Application name.
        APP_NETWORK (str): Docker network name.
        APP_VOLUME (str): Docker volume name.
        API_PORT (int): Port used by the FastAPI app.
        PYTHON_VERSION (str): Python version used in containers or documentation.

        DATABASE_URL (str): Full SQLAlchemy-style database URL.
        POSTGRES_HOST (str): Hostname for the PostgreSQL server.
        POSTGRES_HOST_LOCAL (str): Localhost alias (usually 'localhost').
        POSTGRES_VERSION (str): PostgreSQL version used in Docker.
        POSTGRES_USER (str): Username for the database.
        POSTGRES_PASSWORD (str): Password for the database user.
        POSTGRES_DB (str): Name of the PostgreSQL database.
        POSTGRES_PORT (int): Port used by PostgreSQL.

        PGADMIN_DEFAULT_EMAIL (str): Default login email for pgAdmin.
        PGADMIN_DEFAULT_PASSWORD (str): Default password for pgAdmin.
        PGADMIN_PORT (int): Port pgAdmin should be served on.

        STANDARD_MEMBERSHIP_FEE (int): Standard yearly membership fee in euros.
        UNPAID_MEMBERSHIP (int): Default amount (0) for newly created unpaid memberships.
    """

    # App-level
    APP_NAME: str = "membermgr"
    APP_NETWORK: str = "MemberMGR_Network"
    APP_VOLUME: str = "MemberMGR_Volume"

    API_PORT: int = 8000
    PYTHON_VERSION: str = "3.11"

    # Database
    DATABASE_URL: str = "postgresql://admin:changeme@localhost:5432/members_db"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_HOST_LOCAL: str = "localhost"
    POSTGRES_VERSION: str = "16"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "members_db"
    POSTGRES_PORT: int = 5432

    # PGAdmin
    PGADMIN_DEFAULT_EMAIL: str = "admin@example.com"
    PGADMIN_DEFAULT_PASSWORD: str = "adminpassword"
    PGADMIN_PORT: int = 5050
    STANDARD_MEMBERSHIP_FEE: int = 25
    UNPAID_MEMBERSHIP: int = 0

    class Config:
        env_file = ".env"


# Create a singleton settings object that can be imported app-wide
settings = Settings()
