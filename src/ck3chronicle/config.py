"""ck3chronicle.config — single source of truth for all filesystem paths.

All other modules import ROOT_* from here.  No other module may call
Path.home(), os.environ, or hardcode CK3/Steam/Paradox path literals.
"""
from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # Python < 3.11 fallback (should not occur; requires >=3.11)
    import tomli as tomllib  # type: ignore[no-redef]

# ---------------------------------------------------------------------------
# OS-default discovery
# ---------------------------------------------------------------------------

_DEFAULT_CONFIG_TOML = """\
# ck3chronicle user configuration
# Edit any path below to override its OS default.
# Leave a value as the empty string "" to fall back to the OS default.

[paths]
root_game         = ""
root_steam        = ""
root_local_mods   = ""
root_logs         = ""
root_wip          = ""
root_ck3chronicle = ""
"""

_CONFIG_KEY_TO_ROOT: dict[str, str] = {
    "root_game": "ROOT_GAME",
    "root_steam": "ROOT_STEAM",
    "root_local_mods": "ROOT_LOCAL_MODS",
    "root_logs": "ROOT_LOGS",
    "root_wip": "ROOT_WIP",
    "root_ck3chronicle": "ROOT_CK3CHRONICLE",
}


def default_root(name: str) -> Path:
    """Return the OS-default Path for the named ROOT_* constant.

    Calls platform.system() at call time so tests can mock it.
    """
    is_windows = platform.system() == "Windows"

    if name == "ROOT_GAME":
        if is_windows:
            return Path(r"C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game")
        return Path.home() / ".steam/steam/steamapps/common/Crusader Kings III/game"

    if name == "ROOT_STEAM":
        if is_windows:
            return Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1158310")
        return Path.home() / ".steam/steam/steamapps/workshop/content/1158310"

    if name == "ROOT_LOCAL_MODS":
        if is_windows:
            userprofile = os.environ.get("USERPROFILE", str(Path.home()))
            return Path(userprofile) / "Documents" / "Paradox Interactive" / "Crusader Kings III" / "mod"
        return Path.home() / ".local/share/Paradox Interactive/Crusader Kings III/mod"

    if name == "ROOT_LOGS":
        if is_windows:
            userprofile = os.environ.get("USERPROFILE", str(Path.home()))
            return Path(userprofile) / "Documents" / "Paradox Interactive" / "Crusader Kings III" / "logs"
        return Path.home() / ".local/share/Paradox Interactive/Crusader Kings III/logs"

    if name == "ROOT_CK3CHRONICLE":
        if is_windows:
            localappdata = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
            return Path(localappdata) / "ck3chronicle"
        return Path.home() / ".local/share/ck3chronicle"

    if name == "ROOT_WIP":
        return default_root("ROOT_CK3CHRONICLE") / "wip"

    if name == "CONFIG_FILE_PATH":
        return default_root("ROOT_CK3CHRONICLE") / "config.toml"

    raise ValueError(f"Unknown root name: {name!r}")


def default_config_path() -> Path:
    """Return the OS-default path for config.toml."""
    return default_root("CONFIG_FILE_PATH")


# ---------------------------------------------------------------------------
# Config file I/O
# ---------------------------------------------------------------------------


def load_config(path: Path | None = None) -> dict:
    """Load (and create with defaults if absent) the user config file.

    Args:
        path: Override the config file path.  Defaults to default_config_path().

    Returns:
        Parsed TOML dict.
    """
    cfg_path = path if path is not None else default_config_path()

    if not cfg_path.exists():
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text(_DEFAULT_CONFIG_TOML, encoding="utf-8")

    with cfg_path.open("rb") as f:
        return tomllib.load(f)


def _read_config_silent(path: Path) -> dict:
    """Read config if it exists; return empty dict on any error."""
    try:
        if path.exists():
            with path.open("rb") as f:
                return tomllib.load(f)
    except Exception:
        pass
    return {}


def _resolve_root(name: str, config_data: dict) -> Path:
    """Resolve a ROOT_* constant: check config override, fall back to OS default."""
    for cfg_key, root_name in _CONFIG_KEY_TO_ROOT.items():
        if root_name == name:
            override = config_data.get("paths", {}).get(cfg_key, "")
            if override:
                return Path(override)
            break
    return default_root(name)


# ---------------------------------------------------------------------------
# Module-level constants — resolved once at import time
# ---------------------------------------------------------------------------

_cfg = _read_config_silent(default_config_path())

ROOT_GAME: Path = _resolve_root("ROOT_GAME", _cfg)
ROOT_STEAM: Path = _resolve_root("ROOT_STEAM", _cfg)
ROOT_LOCAL_MODS: Path = _resolve_root("ROOT_LOCAL_MODS", _cfg)
ROOT_LOGS: Path = _resolve_root("ROOT_LOGS", _cfg)
ROOT_CK3CHRONICLE: Path = _resolve_root("ROOT_CK3CHRONICLE", _cfg)
ROOT_WIP: Path = _resolve_root("ROOT_WIP", _cfg)
CONFIG_FILE_PATH: Path = default_config_path()
