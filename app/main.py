"""
Main entrypoint for the Membership Manager API.

This module creates the FastAPI application instance and includes routers
for different functional domains (members, miscellaneous).
"""

from api.routes_member import router as member_router
from api.routes_misc import router as misc_router
from fastapi import FastAPI

app = FastAPI(
    title="Membership Manager API",
    description="A simple API for managing memberships and members.",
    version="0.0.1",
    contact={"name": "Lionel", "email": "email@toto.com"},
)

# Include API routers
app.include_router(misc_router)
app.include_router(member_router)
