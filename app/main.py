"""
membership-manager/api/main.py

This module sets up a basic FastAPI application with a single route.
The root URL ("/") returns a welcome message.
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Membership Manager API!"}
