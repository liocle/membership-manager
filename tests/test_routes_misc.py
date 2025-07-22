# tests/test_routes_misc.py
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/misc/", {"status": "ok", "message": "API is running"}),
        ("/misc/health", {"status": "ok", "message": "API is healthy"}),
        ("/misc/version", {"status": "ok", "message": "API version 0.0.1"}),
        (
            "/misc/info",
            {
                "status": "ok",
                "message": "This is a simple API for managing memberships and members.",
            },
        ),
        (
            "/misc/docs",
            {
                "status": "ok",
                "message": "API documentation is available at /docs or /redoc.",
            },
        ),
    ],
)
def test_misc_endpoints(path, expected):
    resp = client.get(path)
    assert resp.status_code == 200
    assert resp.json() == expected
