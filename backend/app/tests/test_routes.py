from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app

client = TestClient(app)


def test_invalid_url_returns_422():
    payload = {"url": "not-a-valid-url"}
    resp = client.post("/audit", json=payload)

    assert resp.status_code == 422

    data = resp.json()
    assert "detail" in data and isinstance(data["detail"], list) and len(data["detail"]) > 0

    # Ensure the validation error is related to the URL field
    assert any(
        ("url" in str(err.get("loc", "")) or "value_error.url" in str(err.get("type", "")))
        for err in data["detail"]
    )


async def _mock_non_html_response(url: str):
    raise HTTPException(
        status_code=415,
        detail="The requested URL does not return an HTML response."
    )


def test_non_html_response_returns_415(monkeypatch):
    # Mock the audit_website used by the route to avoid real HTTP requests
    monkeypatch.setattr("app.routes.audit_website", _mock_non_html_response)

    resp = client.post("/audit", json={"url": "https://example.com"})

    assert resp.status_code == 415
    data = resp.json()
    assert data.get("detail") == "The requested URL does not return an HTML response."
