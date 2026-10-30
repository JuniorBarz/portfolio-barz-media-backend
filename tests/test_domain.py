from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models import PlaybackEvent, ScreenStatus


def test_status_rejects_oversized_identifiers() -> None:
    with pytest.raises(ValidationError):
        ScreenStatus(
            state="playing",
            current_media_id="x" * 101,
            free_storage_mb=100,
            app_version="portfolio-1.0.0",
        )


def test_playback_duration_has_a_safe_upper_bound() -> None:
    with pytest.raises(ValidationError):
        PlaybackEvent(
            media_id="welcome-image",
            result="completed",
            played_ms=86_400_001,
        )
