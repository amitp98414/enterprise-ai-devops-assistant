from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.core.security import reset_rate_limit_state
from app.main import app
from app.core.config import settings


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert data["application"] == settings.APP_NAME
    assert data["agent_endpoint"] == "/agent/run"
    assert data["documentation"] == "/docs"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == settings.APP_NAME


def test_agents_endpoint():
    response = client.get("/agent/modes")

    assert response.status_code == 200

def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "python_info" in response.text

def test_chat_requires_api_key(monkeypatch):
    monkeypatch.setattr(settings, "OPSSAGE_API_KEY", "test-secret")

    response = client.post(
        "/chat",
        json={"prompt": "hello"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key."


def test_chat_rejects_wrong_api_key(monkeypatch):
    monkeypatch.setattr(settings, "OPSSAGE_API_KEY", "test-secret")

    response = client.post(
        "/chat",
        headers={"X-API-Key": "wrong-key"},
        json={"prompt": "hello"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key."


def test_chat_accepts_valid_api_key(monkeypatch):
    monkeypatch.setattr(settings, "OPSSAGE_API_KEY", "test-secret")

    with patch("app.main.ask_ai", return_value="mocked response"):
        response = client.post(
            "/chat",
            headers={"X-API-Key": "test-secret"},
            json={"prompt": "hello"},
        )

    assert response.status_code == 200
    assert response.json() == {"response": "mocked response"}


def test_agent_run_accepts_valid_api_key(monkeypatch):
    monkeypatch.setattr(settings, "OPSSAGE_API_KEY", "test-secret")

    with patch(
        "app.api.agent_routes.execute_agent",
        new=AsyncMock(return_value={"result": "mocked agent response"}),
    ):
        response = client.post(
            "/agent/run",
            headers={"X-API-Key": "test-secret"},
            json={"prompt": "hello", "mode": "auto"},
        )

    assert response.status_code == 200
    assert response.json() == {"result": "mocked agent response"}

def test_chat_rate_limit(monkeypatch):
    monkeypatch.setattr(settings, "OPSSAGE_API_KEY", "test-secret")
    monkeypatch.setattr(settings, "RATE_LIMIT_REQUESTS", 2)
    monkeypatch.setattr(settings, "RATE_LIMIT_WINDOW_SECONDS", 60)

    reset_rate_limit_state()

    with patch("app.main.ask_ai", return_value="mocked response"):
        first_response = client.post(
            "/chat",
            headers={"X-API-Key": "test-secret"},
            json={"prompt": "first request"},
        )
        second_response = client.post(
            "/chat",
            headers={"X-API-Key": "test-secret"},
            json={"prompt": "second request"},
        )
        blocked_response = client.post(
            "/chat",
            headers={"X-API-Key": "test-secret"},
            json={"prompt": "third request"},
        )

    reset_rate_limit_state()

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert blocked_response.status_code == 429
    assert blocked_response.json()["detail"] == (
        "Rate limit exceeded. Try again later."
    )
    assert int(blocked_response.headers["Retry-After"]) >= 1
