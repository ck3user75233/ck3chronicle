"""One explicit configuration authority; importing it requires no configuration."""
from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
import os
from copy import deepcopy

try:
    import tomllib
except ImportError:  # Python < 3.11 fallback (should not occur; requires >=3.11)
    import tomli as tomllib  # type: ignore[no-redef]


class ConfigurationError(RuntimeError):
    """The project-local path configuration is absent or invalid."""


@dataclass(frozen=True)
class WatcherSettings:
    database: Path
    ingest_enabled: bool = True
    retention_enabled: bool = True
    maintenance_hours: int = 24
    retention_days: int = 30


def watcher_settings() -> WatcherSettings:
    """Use the existing configuration authority; no runtime path discovery."""
    values = load_config().get("watcher", {})
    if not isinstance(values, dict):
        raise ConfigurationError("watcher configuration must be a table")
    database = values.get("database")
    if not isinstance(database, str) or not database.strip():
        raise ConfigurationError("watcher.database must name the initialized SQLite database file")
    path = Path(database)
    if not path.is_absolute():
        path = default_config_path().parent / path
    options = {}
    for key in ("ingest_enabled", "retention_enabled"):
        value = values.get(key, True)
        if type(value) is not bool:
            raise ConfigurationError(f"watcher.{key} must be boolean")
        options[key] = value
    for key, default in (("maintenance_hours", 24), ("retention_days", 30)):
        value = values.get(key, default)
        if type(value) is not int or value <= 0:
            raise ConfigurationError(f"watcher.{key} must be a positive integer")
        options[key] = value
    return WatcherSettings(database=path.resolve(), **options)


_selected_path = None
_document = None


def configure(path=None):
    """Select before runtime imports. Library callers must do this once at entry."""
    global _selected_path, _document
    _selected_path = Path(path).resolve() if path is not None else None
    _document = None
    return default_config_path()

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
    """Return the selected exact file or the single fixed Windows bootstrap."""
    if _selected_path is not None:
        return _selected_path
    local = os.environ.get('LOCALAPPDATA')
    if not local or not Path(local).is_absolute():
        raise ConfigurationError('LocalAppData unavailable; specify --config PATH')
    return (Path(local) / 'ck3chronicle' / 'paths.toml').resolve()


def load_config(path: Path | None = None) -> dict[str, object]:
    """Load a complete project-local configuration without creating defaults."""
    global _document
    if path is None and _document is not None:
        return deepcopy(_document)
    cfg_path = Path(path).resolve() if path is not None else default_config_path()
    if not cfg_path.is_file():
        raise ConfigurationError(
            f"configuration is missing: {cfg_path}; use ck3chronicle --config PATH setup"
        )
    try:
        with cfg_path.open("rb") as stream:
            document = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(
            f"cannot load configuration {cfg_path}: {exc}"
        ) from exc
    if not isinstance(document, dict):
        raise ConfigurationError("project configuration must be a TOML table")
    if path is None:
        _document = deepcopy(document)
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
    resolved_wip = Path(root_wip).resolve()
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


def paths_for(document, config_path):
    roots = {key: _configured_path(document, key, config_path=config_path)
             for key in _REQUIRED_PATH_KEYS}
    validate_project_containment(config_path=config_path,
        **{key: roots[key] for key in ('root_wip', 'root_ck3chronicle', 'root_learner_state')})
    # Installed package bytes and all external evidence are read-only owners.
    import sys
    from .pipeline.catalog import selected_models_root
    protected = [Path(__file__).resolve().parent, selected_models_root().resolve(),
                 Path(sys.prefix).resolve(),
                 *[roots[key] for key in _REQUIRED_PATH_KEYS[:5]]]
    data = roots['root_wip']
    for other in protected:
        if data == other or data in other.parents or other in data.parents:
            raise ConfigurationError(f'writable data root overlaps read-only files: {data} / {other}')
        if Path(config_path).resolve().is_relative_to(other):
            raise ConfigurationError(f'configuration destination is inside read-only files: {config_path} / {other}')
    return roots


def __getattr__(name):
    if name == 'CONFIG_FILE_PATH':
        return default_config_path()
    if name.lower() in _REQUIRED_PATH_KEYS:
        return paths_for(load_config(), default_config_path())[name.lower()]
    raise AttributeError(name)
