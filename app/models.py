from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class MediaItem(BaseModel):
    id: str = Field(min_length=1, max_length=100)
    kind: Literal["image", "video"]
    url: HttpUrl
    duration_seconds: int = Field(ge=1, le=3600)


class PlaylistResponse(BaseModel):
    screen_id: str
    revision: int = Field(ge=1)
    items: list[MediaItem]


class ScreenStatus(BaseModel):
    state: Literal["offline", "syncing", "playing", "error"]
    current_media_id: str | None = Field(default=None, max_length=100)
    free_storage_mb: int = Field(ge=0, le=10_000_000)
    app_version: str = Field(min_length=1, max_length=50)


class PlaybackEvent(BaseModel):
    media_id: str = Field(min_length=1, max_length=100)
    result: Literal["completed", "failed", "skipped"]
    played_ms: int = Field(ge=0, le=86_400_000)


class AcceptedResponse(BaseModel):
    accepted: bool = True
