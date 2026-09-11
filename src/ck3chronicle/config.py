"""Project-local, fail-closed filesystem path authority for ck3chronicle.

Operational code imports the module-level ``ROOT_*`` constants defined here.
These configured machine and writable roots come only from the repository-root
``config.toml`` and have no OS/user-profile fallback. Other bounded path
inference that remains outside this module is documented as closure debt.
"""
from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ImportError:  # Python < 3.11 fallback (should not occur; requires >=3.11)
    import tomli as tomllib  # type: ignore[no-redef]


class ConfigurationError(RuntimeError):
    """The project-local path configuration is absent or invalid."""


# This is an exact project contract, not a search path. Commands are run from
# the canonical repository root, as required by AGENTS.md.
CONFIG_FILE_PATH = Path("config.toml").resolve()

_REQUIRED_PATH_KEYS = (
    "root_game",
    "root_steam",
    "root_local_mods",
    "root_logs",
    "root_crashes",
    "root_wip",
    "root_ck3chronicle",
    "root_learner_state",
)


def default_config_path() -> Path:
    """Return the one configured project file; no fallback search is allowed."""
    return CONFIG_FILE_PATH


def load_config(path: Path | None = None) -> dict[str, object]:
    """Load a complete project-local configuration without creating defaults."""
    cfg_path = Path(path) if path is not None else CONFIG_FILE_PATH
    if not cfg_path.is_file():
        raise ConfigurationError(
            f"required project configuration is missing: {cfg_path}"
        )
    try:
        with cfg_path.open("rb") as stream:
            document = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(
            f"cannot load project configuration: {cfg_path}"
        ) from exc
    if not isinstance(document, dict):
        raise ConfigurationError("project configuration must be a TOML table")
    return document


def _configured_path(
    config_data: dict[str, object],
    key: str,
    *,
    config_path: Path,
) -> Path:
    paths = config_data.get("paths")
    if not isinstance(paths, dict):
        raise ConfigurationError("project configuration requires a [paths] table")
    raw_value = paths.get(key)
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise ConfigurationError(f"project configuration path is missing: paths.{key}")
    configured = Path(raw_value)
    if not configured.is_absolute():
        configured = config_path.parent / configured
    return configured.resolve()


def require_strict_descendant(
    path: Path,
    parent: Path,
    *,
    path_name: str,
    parent_name: str,
) -> Path:
    """Return a resolved path only when it is strictly contained by its parent."""
    resolved_path = Path(path).resolve()
    resolved_parent = Path(parent).resolve()
    try:
        relative = resolved_path.relative_to(resolved_parent)
    except ValueError as exc:
        raise ConfigurationError(
            f"{path_name} must be a strict descendant of {parent_name}: "
            f"{resolved_path} is outside {resolved_parent}"
        ) from exc
    if not relative.parts:
        raise ConfigurationError(
            f"{path_name} must be a strict descendant of {parent_name}: "
            f"both resolve to {resolved_parent}"
        )
    return resolved_path


def validate_project_containment(
    *,
    config_path: Path,
    root_wip: Path,
    root_ck3chronicle: Path,
    root_learner_state: Path,
) -> None:
    """Fail closed unless every writable project root has one unambiguous owner."""
    project_root = Path(config_path).resolve().parent
    resolved_wip = require_strict_descendant(
        root_wip,
        project_root,
        path_name="paths.root_wip",
        parent_name="the project configuration directory",
    )
    resolved_runtime = require_strict_descendant(
        root_ck3chronicle,
        resolved_wip,
        path_name="paths.root_ck3chronicle",
        parent_name="paths.root_wip",
    )
    resolved_learner = require_strict_descendant(
        root_learner_state,
        resolved_wip,
        path_name="paths.root_learner_state",
        parent_name="paths.root_wip",
    )
    if (
        resolved_runtime == resolved_learner
        or resolved_runtime in resolved_learner.parents
        or resolved_learner in resolved_runtime.parents
    ):
        raise ConfigurationError(
            "paths.root_ck3chronicle and paths.root_learner_state must be "
            "separate, non-overlapping trees"
        )


_cfg = load_config(CONFIG_FILE_PATH)
for _required_key in _REQUIRED_PATH_KEYS:
    _configured_path(_cfg, _required_key, config_path=CONFIG_FILE_PATH)

ROOT_GAME = _configured_path(_cfg, "root_game", config_path=CONFIG_FILE_PATH)
ROOT_STEAM = _configured_path(_cfg, "root_steam", config_path=CONFIG_FILE_PATH)
ROOT_LOCAL_MODS = _configured_path(
    _cfg, "root_local_mods", config_path=CONFIG_FILE_PATH
)
ROOT_LOGS = _configured_path(_cfg, "root_logs", config_path=CONFIG_FILE_PATH)
ROOT_CRASHES = _configured_path(_cfg, "root_crashes", config_path=CONFIG_FILE_PATH)
ROOT_WIP = _configured_path(_cfg, "root_wip", config_path=CONFIG_FILE_PATH)
ROOT_CK3CHRONICLE = _configured_path(
    _cfg, "root_ck3chronicle", config_path=CONFIG_FILE_PATH
)
ROOT_LEARNER_STATE = _configured_path(
    _cfg, "root_learner_state", config_path=CONFIG_FILE_PATH
)
validate_project_containment(
    config_path=CONFIG_FILE_PATH,
    root_wip=ROOT_WIP,
    root_ck3chronicle=ROOT_CK3CHRONICLE,
    root_learner_state=ROOT_LEARNER_STATE,
)
