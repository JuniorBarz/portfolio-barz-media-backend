from __future__ import annotations

from fastapi import FastAPI, HTTPException, status

from app.models import AcceptedResponse, PlaybackEvent, PlaylistResponse, ScreenStatus
from app.store import DemoStore


def create_app() -> FastAPI:
    store = DemoStore()
    api = FastAPI(
        title="Barz Media API — Portfolio",
        description="Synthetic API demonstrating playlist delivery and playback telemetry.",
        version="1.0.0",
    )

    @api.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @api.get("/api/screens/{screen_id}/playlist", response_model=PlaylistResponse)
    def playlist(screen_id: str) -> PlaylistResponse:
        result = store.playlist_for(screen_id)
        if result is None:
            raise HTTPException(status_code=404, detail="screen not found")
        return result

    @api.post(
        "/api/screens/{screen_id}/status",
        response_model=AcceptedResponse,
        status_code=status.HTTP_202_ACCEPTED,
    )
    def update_status(screen_id: str, payload: ScreenStatus) -> AcceptedResponse:
        if not store.update_status(screen_id, payload):
            raise HTTPException(status_code=404, detail="screen not found")
        return AcceptedResponse()

    @api.post(
        "/api/screens/{screen_id}/playback",
        response_model=AcceptedResponse,
        status_code=status.HTTP_202_ACCEPTED,
    )
    def playback(screen_id: str, payload: PlaybackEvent) -> AcceptedResponse:
        if not store.record_playback(screen_id, payload):
            raise HTTPException(status_code=404, detail="screen not found")
        return AcceptedResponse()

    @api.get("/api/admin/overview")
    def overview() -> dict[str, object]:
        return store.overview()

    return api


app = create_app()
