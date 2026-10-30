from __future__ import annotations

from threading import Lock

from app.models import MediaItem, PlaybackEvent, PlaylistResponse, ScreenStatus


class DemoStore:
    """Process-local state containing only deterministic demonstration data."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._playlist = PlaylistResponse(
            screen_id="screen-demo",
            revision=1,
            items=[
                MediaItem(
                    id="welcome-image",
                    kind="image",
                    url="https://cdn.example.test/media/welcome.webp",
                    duration_seconds=12,
                ),
                MediaItem(
                    id="product-loop",
                    kind="video",
                    url="https://cdn.example.test/media/product-loop.mp4",
                    duration_seconds=30,
                ),
            ],
        )
        self._status = {
            "screen-demo": {
                "screen_id": "screen-demo",
                "state": "offline",
                "current_media_id": None,
                "free_storage_mb": None,
                "app_version": None,
            }
        }
        self._playback = {"completed": 0, "failed": 0, "total_played_ms": 0}

    def playlist_for(self, screen_id: str) -> PlaylistResponse | None:
        if screen_id != self._playlist.screen_id:
            return None
        return self._playlist.model_copy(deep=True)

    def update_status(self, screen_id: str, status: ScreenStatus) -> bool:
        if screen_id not in self._status:
            return False
        with self._lock:
            self._status[screen_id] = {
                "screen_id": screen_id,
                **status.model_dump(),
            }
        return True

    def record_playback(self, screen_id: str, event: PlaybackEvent) -> bool:
        if screen_id not in self._status:
            return False
        with self._lock:
            if event.result in {"completed", "failed"}:
                self._playback[event.result] += 1
            self._playback["total_played_ms"] += event.played_ms
        return True

    def overview(self) -> dict[str, object]:
        with self._lock:
            return {
                "screens": [dict(self._status[key]) for key in sorted(self._status)],
                "playback": dict(self._playback),
            }
