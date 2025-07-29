# app/main.py

"""
Main entrypoint for the Membership Manager API.

This module creates the FastAPI application instance and includes routers
for different functional domains (members, miscellaneous).
"""

from api.routes_member import router as member_router
from api.routes_membership import router as membership_router
from api.routes_misc import router as misc_router
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Membership Manager API",
    description="A simple API for managing memberships and members.",
    version="0.0.1",
    contact={"name": "Lionel", "email": "email@toto.com"},
)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def read_root():
    """
    Root endpoint to verify API is running.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the Membership Manager API!"}


# Include API routers
app.include_router(misc_router)
app.include_router(member_router)
app.include_router(membership_router)
