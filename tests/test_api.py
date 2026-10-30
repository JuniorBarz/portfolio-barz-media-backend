from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def client() -> TestClient:
    return TestClient(create_app())


def test_health_is_minimal_and_ready() -> None:
    response = client().get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "database" not in response.text.lower()


def test_playlist_contract_uses_only_synthetic_public_media() -> None:
    response = client().get("/api/screens/screen-demo/playlist")

    assert response.status_code == 200
    body = response.json()
    assert body["screen_id"] == "screen-demo"
    assert body["revision"] == 1
    assert [item["kind"] for item in body["items"]] == ["image", "video"]
    assert all("example.test" in item["url"] for item in body["items"])
    assert all(item["duration_seconds"] > 0 for item in body["items"])


def test_unknown_screen_returns_a_generic_not_found_response() -> None:
    response = client().get("/api/screens/unknown/playlist")

    assert response.status_code == 404
    assert response.json() == {"detail": "screen not found"}


def test_status_update_is_validated_and_reflected_in_overview() -> None:
    api = client()
    response = api.post(
        "/api/screens/screen-demo/status",
        json={
            "state": "playing",
            "current_media_id": "welcome-image",
            "free_storage_mb": 2048,
            "app_version": "portfolio-1.0.0",
        },
    )

    assert response.status_code == 202
    assert response.json() == {"accepted": True}
    overview = api.get("/api/admin/overview").json()
    assert overview["screens"][0]["state"] == "playing"
    assert overview["screens"][0]["current_media_id"] == "welcome-image"


def test_invalid_status_is_rejected_without_mutating_state() -> None:
    api = client()
    response = api.post(
        "/api/screens/screen-demo/status",
        json={"state": "secret-state", "free_storage_mb": -1, "app_version": "x"},
    )

    assert response.status_code == 422
    assert api.get("/api/admin/overview").json()["screens"][0]["state"] == "offline"


def test_playback_events_are_aggregated_without_storing_private_payloads() -> None:
    api = client()
    first = api.post(
        "/api/screens/screen-demo/playback",
        json={"media_id": "welcome-image", "result": "completed", "played_ms": 12000},
    )
    second = api.post(
        "/api/screens/screen-demo/playback",
        json={"media_id": "product-loop", "result": "failed", "played_ms": 3500},
    )

    assert first.status_code == 202
    assert second.status_code == 202
    metrics = api.get("/api/admin/overview").json()["playback"]
    assert metrics == {"completed": 1, "failed": 1, "total_played_ms": 15500}


def test_documentation_is_available_for_portfolio_review() -> None:
    response = client().get("/docs")

    assert response.status_code == 200
    assert "Swagger UI" in response.text
