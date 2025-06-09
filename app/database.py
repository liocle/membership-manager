# api/database.py

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Require environment variables to be set
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Detect if we are running inside Docker
DB_HOST = (
    os.getenv("POSTGRES_HOST", "postgres")
    if os.getenv("RUNNING_IN_DOCKER")
    else "localhost"
)

# Construct DATABASE_URL using the assigned variables
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create the SQLAlchemy engine - It takes the DATABASE_URL as an argument which contains the connection details (string) 
# The engine is used to connect to the database and execute queries
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class - Configure the session class to be used with the engine for the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our models to inherit from
Base = declarative_base()


# Dependency to get the database session - This function will return a new session to the database
# After the request is finished, the session will be closed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
