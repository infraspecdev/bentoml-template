import pytest
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from middlewares.update_response_headers import UpdateResponseHeaders


async def sample_endpoint(request):
    return JSONResponse({"message": "success"})


app = Starlette(routes=[Route("/test", sample_endpoint)])
app.add_middleware(UpdateResponseHeaders)


@pytest.fixture
def client():
    return TestClient(app)


def test_headers_removed(client, monkeypatch):
    response = client.get("/test")
    assert "x-bentoml-request-id" not in response.headers
    assert "server" not in response.headers


def test_headers_added_in_production(client, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    response = client.get("/test")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "deny"
    assert response.headers["Content-Security-Policy"] == "default-src 'none'"


def test_headers_not_added_in_non_production(client, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "development")
    response = client.get("/test")
    assert "X-Content-Type-Options" not in response.headers
    assert "X-Frame-Options" not in response.headers
    assert "Content-Security-Policy" not in response.headers
