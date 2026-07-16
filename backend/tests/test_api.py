from fastapi.testclient import TestClient

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
