from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import SourceInstance, SourceType


def load_ck3_sdk() -> Any:
    """Load ck3raven's local SDK from ~/.ck3raven/wip/sdk."""

    sdk_dir = Path.home() / ".ck3raven" / "wip" / "sdk"
    sys.path.insert(0, str(sdk_dir))
    import ck3_sdk as ck3_sdk_mod  # type: ignore

    return ck3_sdk_mod.CK3SDK()


class CK3SDKSourceProvider:
    """Source provider backed by ck3raven's CK3SDK.

    This preserves the original script behavior but keeps it outside parsing.
    """

    def __init__(self, sdk: Any):
        self.sdk = sdk

    def iter_instances(self, rel_path: str) -> list[SourceInstance]:
        found: list[SourceInstance] = []

        try:
            game_file = self.sdk.resolve(f"root:game/{rel_path}")
            if game_file and Path(game_file).exists():
                path = Path(game_file)
                found.append(
                    SourceInstance(
                        source_name="Base Game",
                        load_order=-1,
                        path=path,
                        modified_at=datetime.fromtimestamp(path.stat().st_mtime),
                        source_type="base_game",
                    )
                )
        except Exception:
            pass

        for mod in sorted(getattr(self.sdk, "mods", []), key=lambda m: m.load_order):
            try:
                mod_file = self.sdk.resolve(f"mod:{mod.name}/{rel_path}")
                if mod_file and Path(mod_file).exists():
                    path = Path(mod_file)
                    raw_path = str(path).replace("\\", "/")
                    source_type: SourceType = "local_mod" if "/mod/" in raw_path else "workshop_mod"
                    found.append(
                        SourceInstance(
                            source_name=mod.name,
                            load_order=mod.load_order,
                            path=path,
                            modified_at=datetime.fromtimestamp(path.stat().st_mtime),
                            source_type=source_type,
                        )
                    )
            except Exception:
                pass

        return sorted(found, key=lambda i: i.load_order)


def default_log_path_from_sdk(sdk: Any) -> tuple[Path, str]:
    ck3_root = sdk.resolve("root:user_docs")
    override = sdk.wip / ".log_path_override"

    if override.exists():
        log_path = Path(override.read_text(encoding="utf-8").strip())
        override.unlink()
        return log_path, str(log_path)

    return Path(ck3_root) / "logs" / "error.log", "root:user_docs/logs/error.log"
