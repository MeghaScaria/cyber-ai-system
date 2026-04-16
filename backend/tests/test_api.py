import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

def test_analyze_message_skeleton():
    response = client.post(
        "/analyze-message",
        json={"message": "Help me!", "user_id": "user123"}
    )
    assert response.status_code == 200
    assert "is_fraud" in response.json()
