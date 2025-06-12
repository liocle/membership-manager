# ./app/api/routes_misc.py
# API routes for miscellaneous operations

from fastapi import APIRouter

router = APIRouter(prefix="/misc", tags=["misc"])


@router.get("/")
def root():
    """
    Root endpoint to verify the API is running.

    Returns:
        dict: A simple message indicating the API is running.
    """
    return {"status": "ok", "message": "API is running"}


@router.get("/health")
def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
        dict: A simple message indicating the API is healthy.
    """
    return {"status": "ok", "message": "API is healthy"}


@router.get("/version")
def get_version():
    """
    Version endpoint to return the API version.

    Returns:
        dict: A message with the current API version.
    """
    return {"status": "ok", "message": "API version 0.0.1"}


@router.get("/info")
def get_info():
    """
    Information endpoint to provide details about the API.

    Returns:
        dict: A message with basic information about the API.
    """
    return {
        "status": "ok",
        "message": "This is a simple API for managing memberships and members.",
    }


@router.get("/docs")
def get_docs():
    """
    Documentation endpoint to provide API documentation.

    Returns:
        dict: A message indicating where to find the API documentation.
    """
    return {
        "status": "ok",
        "message": "API documentation is available at /docs or /redoc.",
    }

