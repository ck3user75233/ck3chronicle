"""Watcher-owned extraction of a captured CK3 playset from VFS emissions."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping

PLAYSET_FILENAME = "playset.json"
PLAYSET_SCHEMA_VERSION = 1
_MOUNTED_DATA = re.compile(
    r"^\[[^\]]+\]\[[^\]]+\]\[virtualfilesystem_physfs\.cpp:\d+\]: Mounted Data: (?P<path>.+)$",
    re.IGNORECASE,
)
_TOKENS = re.compile(r'\s+|#[^\r\n]*|"(?:\\.|[^"\\])*"|[={}]|[^\s={}#"]+')
WarningSink = Callable[[dict[str, object]], None]


@dataclass(frozen=True)
class PlaysetMember:
    load_order: int
    name: str
    path: str
    root_ID: str | None
    stable_id: str | None
    descriptor_path: str | None


@dataclass(frozen=True)
class PlaysetTemplate:
    error_log_sha256: str
    debug_log_sha256: str
    captured_at: str
    members: tuple[PlaysetMember, ...]

    @property
    def log_pair_id(self) -> str:
        return f"sha256:{self.error_log_sha256}:{self.debug_log_sha256}"

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": PLAYSET_SCHEMA_VERSION,
            "error_log_sha256": self.error_log_sha256,
            "debug_log_sha256": self.debug_log_sha256,
            "log_pair_id": self.log_pair_id,
            "captured_at": self.captured_at,
            "members": [asdict(member) for member in self.members],
        }


def iter_mounted_paths(lines: Iterable[str]) -> Iterable[str]:
    """Yield exactly the emitted VFS paths in their original order."""
    for line in lines:
        match = _MOUNTED_DATA.match(line.rstrip("\r\n"))
        if match:
            yield match.group("path")


def _root_id(path: Path, roots: Mapping[str, Path]) -> str | None:
    # Prefer the most specific configured root if roots are nested.
    matches = [
        (len(Path(root).parts), key)
        for key, root in roots.items()
        if path.is_relative_to(root)
    ]
    return max(matches)[1] if matches else None


def _read_descriptor_fields(path: Path) -> dict[str, str]:
    """Read top-level scalar metadata, ignoring nested Paradox script blocks."""
    source = path.read_text(encoding="utf-8-sig")
    tokens: list[str] = []
    position = 0
    for match in _TOKENS.finditer(source):
        if match.start() != position:
            raise ValueError(f"malformed descriptor at character {position}")
        position = match.end()
        token = match.group()
        if not token.isspace() and not token.startswith("#"):
            tokens.append(token)
    if position != len(source):
        raise ValueError(f"malformed descriptor at character {position}")
    fields: dict[str, str] = {}
    depth = 0
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "{":
            depth += 1
        elif token == "}":
            depth -= 1
            if depth < 0:
                raise ValueError("unbalanced descriptor braces")
        elif depth == 0 and index + 2 < len(tokens) and tokens[index + 1] == "=":
            value = tokens[index + 2]
            if value not in {"{", "}", "="}:
                if value.startswith('"'):
                    value = re.sub(r'\\(["\\])', r'\1', value[1:-1])
                if token in {"name", "path", "remote_file_id", "pops_id"}:
                    if token in fields and fields[token] != value:
                        raise ValueError(f"conflicting descriptor field: {token}")
                    fields[token] = value
                index += 2
        index += 1
    if depth:
        raise ValueError("unbalanced descriptor braces")
    return fields


def _descriptor_mount(raw_path: str, roots: Mapping[str, Path]) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = roots["ROOT_LOCAL_MODS"].parent / path
    return path


def _find_descriptor(
    mount_path: Path, root_id: str | None, roots: Mapping[str, Path]
) -> Iterable[tuple[Path, bool]]:
    """Yield candidates and whether their declared path must match the mount."""
    yield mount_path / "descriptor.mod", False
    if root_id == "ROOT_GAME":
        for descriptor in sorted(mount_path.glob("*.dlc")):
            yield descriptor, False
    local = roots["ROOT_LOCAL_MODS"]
    preferred = local / f"ugc_{mount_path.name}.mod"
    if root_id == "ROOT_STEAM":
        yield preferred, True
    for descriptor in sorted(local.glob("*.mod")):
        if root_id != "ROOT_STEAM" or descriptor != preferred:
            yield descriptor, True


def _resolve_member(
    path: str, load_order: int, roots: Mapping[str, Path], on_warning: WarningSink
) -> PlaysetMember:
    mount = Path(path)
    root_id = _root_id(mount, roots)
    stable_id = None
    if root_id == "ROOT_STEAM":
        relative_parts = mount.relative_to(roots[root_id]).parts
        workshop_id = relative_parts[0] if relative_parts else ""
        if workshop_id.isdecimal():
            stable_id = f"steam_workshop:{workshop_id}"

    def warn(reason: str, message: str, descriptor: Path | None = None) -> None:
        on_warning({
            "load_order": load_order, "path": path,
            "descriptor_path": str(descriptor) if descriptor else None,
            "reason_code": reason, "message": message,
        })

    try:
        if not mount.is_dir():
            warn("mounted_path_unavailable", "Mounted path is missing or is not a directory")
    except OSError as exc:
        warn("mounted_path_unavailable", str(exc))
    selected = None
    fields: dict[str, str] = {}
    try:
        for candidate, requires_path in _find_descriptor(mount, root_id, roots):
            if not candidate.is_file():
                continue
            try:
                candidate_fields = _read_descriptor_fields(candidate)
            except (OSError, UnicodeError, ValueError) as exc:
                warn("descriptor_unreadable", str(exc), candidate)
                continue
            if requires_path:
                declared_path = candidate_fields.get("path")
                if not declared_path or _descriptor_mount(declared_path, roots) != mount:
                    if candidate.name == f"ugc_{mount.name}.mod":
                        warn("descriptor_path_mismatch", "Associated descriptor path differs from mount", candidate)
                    continue
            if candidate.suffix.casefold() == ".dlc" and candidate_fields.get("path"):
                if roots["ROOT_GAME"] / candidate_fields["path"] != mount:
                    warn("descriptor_path_mismatch", "Packaged DLC descriptor path differs from mount", candidate)
                    continue
            selected, fields = candidate, candidate_fields
            break
    except OSError as exc:
        warn("descriptor_search_failed", str(exc))
    if selected is None:
        warn("descriptor_missing", "No usable root or associated descriptor found", mount / "descriptor.mod")
    elif not fields.get("name", "").strip():
        warn("descriptor_name_missing", "Descriptor has no nonempty top-level name", selected)
    remote_id = fields.get("remote_file_id")
    if remote_id:
        descriptor_id = f"steam_workshop:{remote_id}"
        if stable_id and stable_id != descriptor_id:
            warn("descriptor_id_mismatch", "Descriptor remote_file_id differs from Workshop path ID", selected)
        elif not stable_id:
            stable_id = descriptor_id
    if selected and selected.suffix.casefold() == ".dlc":
        stable_id = f"pops:{fields['pops_id']}" if fields.get("pops_id") else None
    return PlaysetMember(
        load_order, fields.get("name", "").strip() or "UNKNOWN", path,
        root_id, stable_id, str(selected) if selected else None,
    )


def extract_playset(
    debug_path: Path, *, roots: Mapping[str, Path], on_warning: WarningSink
) -> tuple[PlaysetMember, ...]:
    """Extract one protected log; descriptors only supply member metadata."""
    game = roots["ROOT_GAME"]
    game_error = None
    try:
        if not game.is_dir():
            game_error = "Configured base game path is missing or is not a directory"
    except OSError as exc:
        game_error = str(exc)
    if game_error:
        on_warning({
            "load_order": 0, "path": str(game), "descriptor_path": None,
            "reason_code": "mounted_path_unavailable",
            "message": game_error,
        })
    members = [PlaysetMember(0, "CK3 Game Files", str(game), "ROOT_GAME", "ck3:1158310", None)]
    with Path(debug_path).open(encoding="utf-8-sig") as stream:
        for order, path in enumerate(iter_mounted_paths(stream), start=1):
            members.append(_resolve_member(path, order, roots, on_warning))
    if len(members) == 1:
        on_warning({
            "load_order": None, "path": str(debug_path), "descriptor_path": None,
            "reason_code": "no_mount_emissions", "message": "Debug log contains no VFS Mounted Data emissions",
        })
    return tuple(members)
