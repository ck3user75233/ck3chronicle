"""Doctor subcommand: health check for ck3chronicle installation."""
from __future__ import annotations

import platform
import sqlite3
import sys
from pathlib import Path

from . import __version__
from . import config


def run_doctor() -> None:
    """Print health check report to stdout."""
    print(f"ck3chronicle {__version__}")
    print(f"Python {sys.version.split()[0]}   SQLite {sqlite3.sqlite_version}")
    print()

    # Config file
    cfg_path = config.CONFIG_FILE_PATH
    if not cfg_path.exists():
        config.load_config(cfg_path)
        print(f"config.toml: {cfg_path}  (created with defaults)")
    else:
        print(f"config.toml: {cfg_path}  (exists)")
    print()

    # ROOT_* paths
    roots = [
        ("ROOT_GAME", config.ROOT_GAME),
        ("ROOT_STEAM", config.ROOT_STEAM),
        ("ROOT_LOCAL_MODS", config.ROOT_LOCAL_MODS),
        ("ROOT_LOGS", config.ROOT_LOGS),
        ("ROOT_WIP", config.ROOT_WIP),
        ("ROOT_CK3CHRONICLE", config.ROOT_CK3CHRONICLE),
    ]
    for name, path in roots:
        status = "exists" if path.exists() else "missing"
        print(f"{name:<20}: {path}  ({status})")
    print()

    # Durable storage status
    durable = config.ROOT_CK3CHRONICLE
    try:
        durable.mkdir(parents=True, exist_ok=True)
        test_file = durable / ".ck3chronicle_write_test"
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink()
        writable = True
    except OSError:
        writable = False

    print(f"durable storage     : {'writable' if writable else 'NOT writable'}")

    # Same-drive check (Windows only)
    if platform.system() == "Windows":
        d_drive = durable.drive.lower() if durable.drive else ""
        l_drive = config.ROOT_LOGS.drive.lower() if config.ROOT_LOGS.drive else ""
        if d_drive and l_drive and d_drive != l_drive:
            print(
                f"  warning: durable storage on {durable.drive}, "
                f"ROOT_LOGS on {config.ROOT_LOGS.drive}"
            )
