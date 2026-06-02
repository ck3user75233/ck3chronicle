from __future__ import annotations

from pathlib import Path

GAME_RELATIVE_MARKERS = (
    "common/",
    "events/",
    "decisions/",
    "history/",
    "localization/",
    "gfx/",
    "gui/",
    "map_data/",
    "on_action/",
    "scripted_effects/",
    "scripted_triggers/",
    "cultures/",
    "religions/",
    "characters/",
    "dynasties/",
)


def to_game_relative_path(path: str | None) -> str | None:
    """Return the game-relative portion of a CK3 file path."""

    if not path:
        return None
    p = str(path).replace("\\", "/")
    for marker in GAME_RELATIVE_MARKERS:
        idx = p.find(marker)
        if idx != -1:
            return p[idx:]

    parts = [part for part in p.split("/") if part]
    return "/".join(parts[-2:]) if len(parts) >= 2 else p


def safe_read_lines(path: Path) -> list[str]:
    try:
        return path.read_bytes().decode("utf-8-sig", errors="replace").splitlines()
    except Exception:
        return []
