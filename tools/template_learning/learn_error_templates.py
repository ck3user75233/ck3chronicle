"""Empirical CK3 error-template learning prototype.

This prototype reads only protected ck3chronicle session/pending copies.  It
never reads the live CK3 log directory and never mutates the production parser
or SQLite index.

The model is deliberately conservative:

* source family is a hard partition and remains part of template identity;
* timestamps are removed by the lexical block reader;
* file/path/line/column/position locators are deterministically masked;
* candidate messages are clustered by ordered-token sequence similarity;
* stable ordered tokens form the semantic backbone;
* variable spans become locator, key, closed semantic alternative, value, or
  generic parameter slots based on observations in stable surrounding context;
* distinct archived error.log content hashes are learned once.

This is calibration tooling, not a production classifier.
"""
from __future__ import annotations

import argparse
import base64
import collections
import dataclasses
import difflib
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Iterable, Sequence

from ck3chronicle.parser.log_blocks import TimestampedLogBlock, iter_log_blocks


NORMALIZER_VERSION = "ck3-empirical-template-normalizer-v4.11"
CLUSTERER_VERSION = "ordered-token-clusterer-v4-bounded-script-layers"
HEADER_RE = re.compile(
    r"^\[\d{2}:\d{2}:\d{2}\](?:\[[^\]]+\])?\[[^\]]+\]:\s*"
)
WINDOWS_PATH_RE = re.compile(r"[A-Za-z]:\\[^\r\n\"']+")
QUOTED_PATH_RE = re.compile(
    r"(?P<quote>[\"'])(?:[^\"'\r\n]*[/\\])[^\"'\r\n]+(?P=quote)"
)
RELATIVE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:mod|common|events|history|localization|gfx|gui|"
    r"interface|map_data|game|dlc|music|sound|launcher|workshop)"
    r"[/\\][^\s,;:\)\]\}\"']+",
    re.IGNORECASE,
)
FILENAME_RE = re.compile(
    r"(?<![A-Za-z0-9_])[^\s,;:\(\)\[\]\{\}\"']+\."
    r"(?:txt|yml|yaml|gui|dds|asset|mesh|mod|json|wav|ogg|bank|png|tga)\b",
    re.IGNORECASE,
)
LINE_LOCATOR_RE = re.compile(
    r"\b(?:near\s+)?(?:line|column|position|row)\s*:?\s*\d+"
    r"(?:\s*(?:-|to)\s*\d+)?\b(?:\s+\([^\r\n\)]*\))?",
    re.IGNORECASE,
)
HEADER_TOKEN_RE = re.compile(
    r"<OPTIONAL_KEY>|<LOCATOR>|<TYPE>|<KEY>|<PARAM>|<VALUE>|"
    r"[A-Za-z_][A-Za-z0-9_#@-]*|"
    r"\d+(?:\.\d+)*|[^\s]"
)
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_#@-]*$")
PERSISTENT_WRAPPER_RE = re.compile(
    r'^\s*Error\s*:\s*"(?P<inner>.*)"\s+in\s+file\s*:',
    re.IGNORECASE,
)
ERROR_INTRO_RE = re.compile(r"\bError\s*:\s*", re.IGNORECASE)
QUOTED_VALUE_RE = re.compile(r"(['\"])(?:\\.|(?!\1).)*\1")
PUNCTUATION = frozenset("'\"`()[]{}:;,.=!?/\\")
LOCATOR = "<LOCATOR>"
KEY = "<KEY>"
OPTIONAL_KEY = "<OPTIONAL_KEY>"
TYPE = "<TYPE>"
PARAM = "<PARAM>"
TRUNCATED_REASON = "<TRUNCATED_REASON>"
SCRIPT_LOCATION_TAIL_RE = re.compile(r"\s+Script\s+location\s*:\s*", re.IGNORECASE)
PERSISTENT_CLAUSE_START_RE = re.compile(
    r"(?=(?:Unknown\s+trigger|Failed\s+to\s+read\s+key\s+reference)\s*:)",
    re.IGNORECASE,
)
PERSISTENT_NEAR_LINE_RE = re.compile(
    r"\s*,?\s*near\s+line\s*:\s*\d+(?:\s*(?:-|to)\s*\d+)?",
    re.IGNORECASE,
)
UNKNOWN_TRIGGER_KEY_RE = re.compile(
    r"^(?P<prefix>Unknown\s+trigger\s*:\s*)(?P<key>.*)$", re.IGNORECASE
)
FAILED_KEY_REFERENCE_RE = re.compile(
    r"^(?P<prefix>Failed\s+to\s+read\s+key\s+reference\s*:\s*)"
    r"(?P<left>.*?)\s*:\s*(?P<right>.*)$",
    re.IGNORECASE,
)
TRAVEL_CHARACTER_REFERENCE_RE = re.compile(
    r"(?P<prefix>Removing\s+travel\s+plan\s+from\s+the\s+character\s+)"
    r"(?P<display>.+?)\s+\(\s*Internal\s+ID\s*:?[ \t]*"
    r"(?P<internal>[^\s\)]+)"
    r"(?:\s*-\s*Historical\s+ID\s+(?P<historical>[^\)]+?))?\s*\)"
    r"(?P<suffix>\s+owner\s+when\s+the\s+travel\s+plan\s+is\s+not\s+ending\s+normally\.?)",
    re.IGNORECASE,
)
SCRIPT_SYSTEM_ROLE_RE = re.compile(
    r"^(?P<prefix>Script\s+system\s+error!\s*"
    r"(?:\([^\)]*\)\s*)?Error\s*:\s*)"
    r"(?P<expression>.+?)\s+(?P<role>trigger|effect)"
    r"(?P<suffix>\s*\[.*(?:\]\s*)?)$",
    re.IGNORECASE,
)
SCRIPT_SYSTEM_PREFIX_RE = re.compile(
    r"^Script\s+system\s+error!\s*(?P<context>\([^\)]*\))?\s*Error\s*:\s*",
    re.IGNORECASE,
)
SCRIPT_TRAVEL_NO_DESTINATIONS_RE = re.compile(
    r"^(?P<display>.+?)\s+\(\s*Internal\s+ID\s*:?[ \t]*"
    r"(?P<internal>[^\s\)]+)"
    r"(?:\s*-\s*Historical\s+ID\s*:?[ \t]*(?P<historical>[^\)]+?))?\s*\)"
    r"(?P<possessive>['\u2019]s)\s+travel\s+plan\s+have\s+no\s+valid\s+destinations$",
    re.IGNORECASE,
)
KEY_PATH_NAMESPACE_RE = re.compile(
    r"^(?P<namespace>scope|var|cp|title)\s*:\s*(?P<path>.+)$",
    re.IGNORECASE,
)
KEY_PATH_SEGMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_#@-]*$")
COMPARISON_TYPE_MISMATCH_RE = re.compile(
    r"(?P<prefix>Left\s+side\s+and\s+right\s+side\s+during\s+comparison\s+"
    r"were\s+of\s+different\s+types\s*\(\s*left\s+was\s*)"
    r"(['\"])[^'\"]+\2"
    r"(?P<middle>\s*,\s*right\s+was\s*)"
    r"(['\"])[^'\"]+\4(?P<suffix>\s*\))",
    re.IGNORECASE,
)
TRIGGER_DESCRIPTION_RE = re.compile(
    r"^(?P<key>[A-Za-z_][A-Za-z0-9_#@-]*)\s*:\s*"
    r"(?P<body>Scope\s+dependent\s+values\s+in\s+localization\s+inside\s+an\s+"
    r"any\s+trigger\s*;\s*consider\s+using\s+a\s+custom_tooltip\s*;)\s*"
    r"at\s+file\s*:.*$",
    re.IGNORECASE,
)
FLAVORIZATION_TITLE_RE = re.compile(
    r"^(?P<prefix>Failed\s+to\s+find\s+any\s+valid\s+flavorization\s+for\s+"
    r"title\s*)(?P<key>[^\s]*)\s*$",
    re.IGNORECASE,
)
ACTIVITY_EVENT_REFERENCE_RE = re.compile(
    r"^(?P<prefix>Trying\s+to\s+trigger\s+activity\s+event\s+)"
    r"(['\"])(?P<event>[^'\"]+)\2"
    r"(?P<character_prefix>\s+for\s+character\s+)"
    r"(?P<display>.+?)\s+\(\s*Internal\s+ID\s*:?[ \t]*"
    r"(?P<internal>[^\s\)]+)"
    r"(?:\s*-\s*Historical\s+ID\s*:?[ \t]*(?P<historical>[^\)]+?))?\s*\)"
    r"(?P<suffix>\s*,\s*but\s+the\s+activity\s+is\s+invalid\s*-\s*skipping\.?)$",
    re.IGNORECASE,
)
PDXMESH_SYNC_RE = re.compile(
    r"^(?P<prefix>pdxmesh\s*\[)\s*[^\]\r\n]+"
    r"(?P<middle>\]\s+is\s+out\s+of\s+sync\s+with\s+its\s+meshsettings\.\s*\[)"
    r"\s*[^\]\r\n]+(?P<suffix>\]\s+is\s+not\s+in\s+use\s+in\s+file\s*:.*)$",
    re.IGNORECASE,
)
DECISION_INTERVAL_RE = re.compile(
    r"^(?P<key>[A-Za-z_][A-Za-z0-9_#@.-]*)"
    r"(?P<suffix>\s+has\s+'ai_check_interval'/'ai_check_interval_by_tier'\s+"
    r"that's\s+negative\s+or\s+unset\.\s+Setting\s+to\s+0\s+instead)$",
    re.IGNORECASE,
)
UNRECOGNIZED_LOC_KEY_RE = re.compile(
    r"^(?P<prefix>Unrecognized\s+loc\s+key\s+)(?P<key>.+?)"
    r"(?P<suffix>\.\s+(?:Near\s+)?file\s*:.*)$",
    re.IGNORECASE,
)
EVENT_THEME_KEY_RE = re.compile(
    r"^(?P<prefix>Theme\s+key\s+)(?P<theme>\S+)"
    r"(?P<middle>\s+in\s+event\s+)(?P<event>\S+)"
    r"(?P<suffix>\s+does\s+not\s+exist\s+in\s+the\s+event\s+theme\s+database)$",
    re.IGNORECASE,
)
ORPHAN_EVENT_RE = re.compile(
    r"^(?P<prefix>Event\s+)(?P<event>\S+)(?P<suffix>\s+is\s+orphaned)$",
    re.IGNORECASE,
)
QUEUED_EVENT_RE = re.compile(
    r"^(?P<prefix>Event\s+)(?P<event>\S+)"
    r"(?P<suffix>\s+has\s+been\s+queued\s+twice\s+with\s+the\s+same\s+data\s+"
    r"including\s+delay)$",
    re.IGNORECASE,
)
ARTIFACT_FEATURE_RE = re.compile(
    r"^(?P<prefix>Artifact\s+)'(?P<display>[^']*)'\s+\((?P<identity>[^\)]+)\)"
    r"(?P<middle>\s+has\s+no\s+feature\s+in\s+group\s+)(?P<group>\S+)$",
    re.IGNORECASE,
)
SCRIPTED_EFFECT_SOURCE_RE = re.compile(
    r"^(?:file\s*:\s+.*?\s+line\s*:\s*\d+(?:\s*(?:-|to)\s*\d+)?\s*"
    r"(?:\([^\)]*\))?|file\s*:\s*<LOCATOR>)\s*:\s*",
    re.IGNORECASE,
)
SCRIPTED_EFFECT_KEY_RE = re.compile(
    r"^(?P<effect>[A-Za-z_][A-Za-z0-9_#@-]*)"
    r"(?P<separator>\s*:\s*)(?P<scope>root|target)"
    r"(?P<suffix>\s+cheated\s+on\s+a\s+partner\s+that\s+"
    r"they\s+wouldn't\s+have\b.*)$",
    re.IGNORECASE,
)
RENDERED_CHARACTER_RE = re.compile(
    r"(?P<prefix>\b(?:Cheater|With)\s*:\s*)"
    r"\x15ONCLICK:CHARACTER,\d+\s+\x15TOOLTIP:CHARACTER,\d+.*?"
    r"(?=(?:\bWith\s*:|$))",
    re.IGNORECASE,
)
FAITH_SCOPE_RE = re.compile(
    r"^(?P<prefix>Failed\s+to\s+scope\s+to\s+(?P<kind>faith|religion)\s+)"
    r"(?P<quote>['\"])[^'\"]+(?P=quote)(?P<suffix>\s+at\s+file\s*:.*)$",
    re.IGNORECASE,
)
POSTVALIDATE_EFFECT_RE = re.compile(
    r"^(?P<prefix>PostValidate\s+of\s+effect\s+)(?P<quote>['\"])"
    r"(?P<effect>[^'\"]+)(?P=quote)"
    r"(?P<suffix>\s+returned\s+false\s+at\s+file\s*:.*)$",
    re.IGNORECASE,
)
MATERIAL_SHADER_RE = re.compile(
    r"^(?P<prefix>Failed\s+to\s+create\s+material\s+with\s+shader\s*)"
    r"(?P<shader>.*?)"
    r"(?P<middle>\s*\(\s*in\s+[^\)]+\)\s+for\s+mesh\s*\[)"
    r"(?P<mesh>[^\]]+)(?P<suffix>\]\s+in\s+.+)$",
    re.IGNORECASE,
)
LOCALIZATION_HASH_COLLISION_RE = re.compile(
    r"^(?P<prefix>Localization\s+key\s+hash\s+collision\.\s+Key\s+)"
    r"(?P<q1>['\"])(?P<left>[^'\"]+)(?P=q1)"
    r"(?P<middle>\s+and\s+)(?P<q2>['\"])(?P<right>[^'\"]+)(?P=q2)"
    r"(?P<suffix>\s+have\s+the\s+same\s+hash\s*:\s*)-?\d+(?P<period>\s*\.?)$",
    re.IGNORECASE,
)
AUDIO_EVENT_INFO_RE = re.compile(
    r"^(?P<prefix>PdxAudio2\s*:\s*couldn't\s+get\s+event\s+info\s+)"
    r"(?P<quote>['\"])(?P<event>[^'\"]+)(?P=quote)"
    r"(?P<suffix>\s+\(The\s+requested\s+event\s*,\s*parameter\s*,\s*bus\s+or\s+"
    r"vca\s+could\s+not\s+be\s+found\.\)\.?)$",
    re.IGNORECASE,
)
PERSISTENT_UNEXPECTED_TOKEN_RE = re.compile(
    r"^(?P<prefix>Error\s*:\s*\"Unexpected\s+token\s*:\s*)"
    r"(?P<token>.*?)(?P<middle>\s*,\s*near\s+line\s*:\s*)\d+"
    r"(?P<file>\"\s+in\s+file\s*:\s*\").*?"
    r"(?P<tail>\"\s+near\s+line\s*:\s*)\d+$",
    re.IGNORECASE,
)
TRIBUTARY_REASON_RE = re.compile(
    r"^Tried\s+to\s+make\s+'(?P<first_display>.+?)\s+of\s+"
    r"(?P<first_title>[^\s]+)\s+\(\s*Internal\s+ID\s*:?\s*(?P<first_id>\d+)"
    r"(?:\s*-\s*Historical\s+ID\s*:?\s*(?P<first_history>\d+))?\s*\)'\s+"
    r"a\s+Tributary\s+contract\s+with\s+Suzerain\s+'"
    r"(?P<second_display>.+?)\s+of\s+(?P<second_title>[^\s]+)\s+"
    r"\(\s*Internal\s+ID\s*:?\s*(?P<second_id>\d+)"
    r"(?:\s*-\s*Historical\s+ID\s*:?\s*(?P<second_history>\d+))?\s*\)'\s*,\s*"
    r"but\s+they\s+are\s+already\s+a\s+vassal\s+of\s+"
    r"(?P<third_display>.+?)\s+of\s+(?P<third_title>[^\s]+)\s+"
    r"\(\s*Internal\s+ID\s*:?\s*(?P<third_id>\d+)"
    r"(?:\s*-\s*Historical\s+ID\s*:?\s*(?P<third_history>\d+))?\s*\)\s*\.?$",
    re.IGNORECASE,
)


@dataclasses.dataclass(frozen=True)
class ProtectedLog:
    evidence_id: str
    kind: str
    path: Path
    sha256: str
    bytes: int
    modified_ns: int


@dataclasses.dataclass
class SequenceRecord:
    source_family: str
    tokens: tuple[str, ...]
    semantic_lead: tuple[str, ...]
    occurrences: int = 0
    evidence_ids: set[str] = dataclasses.field(default_factory=set)
    examples: list[str] = dataclasses.field(default_factory=list)
    location_examples: list[str] = dataclasses.field(default_factory=list)
    structured_slot_examples: list[list[dict]] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class TemplateCluster:
    source_family: str
    cluster_number: int
    records: list[SequenceRecord]
    medoid: SequenceRecord | None = None
    template_tokens: tuple[str, ...] = ()
    support_occurrences: int = 0
    support_evidence: set[str] = dataclasses.field(default_factory=set)

    @property
    def cluster_id(self) -> str:
        material = self.source_family + "\0" + " ".join(self.template_tokens)
        return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


@dataclasses.dataclass(frozen=True)
class LayeredClusterMatch:
    """A full-template match or a proven script-system L1-only match.

    ``cluster`` is populated only when the complete reason-specific template
    matched.  ``outer_contract`` is populated for a bracketed script-system
    diagnostic.  ``outer_known`` proves that the same source family and exact
    ordered outer envelope occurred in approved training evidence.
    """

    cluster: TemplateCluster | None
    outer_contract: tuple[str, ...] | None
    outer_known: bool
    reason_contract: tuple[str, ...] | None
    reason_cluster: TemplateCluster | None

    @property
    def assignment_level(self) -> str | None:
        if self.cluster is not None:
            return "L2" if self.outer_contract is not None else "full"
        if self.outer_known and self.reason_cluster is not None:
            return "L1+L2"
        if self.outer_known:
            return "L1"
        return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def protected_error_logs(runtime_root: Path) -> tuple[list[ProtectedLog], list[dict]]:
    """Return distinct protected error logs and duplicate-content evidence."""
    candidates: list[tuple[str, str, Path]] = []
    sessions = runtime_root / "sessions"
    if sessions.is_dir():
        for directory in sorted(sessions.iterdir(), key=lambda item: item.name):
            if not directory.is_dir() or directory.name == ".staging":
                continue
            path = directory / "error.log"
            if path.is_file():
                candidates.append(("session", directory.name, path))
    pending = runtime_root / "pending"
    if pending.is_dir():
        for directory in sorted(pending.iterdir(), key=lambda item: item.name):
            if not directory.is_dir() or directory.name.startswith(".copying-"):
                continue
            path = directory / "error.log"
            if path.is_file():
                candidates.append(("pending", directory.name, path))

    distinct: list[ProtectedLog] = []
    seen: dict[str, ProtectedLog] = {}
    duplicates: list[dict] = []
    for kind, evidence_id, path in candidates:
        stat = path.stat()
        digest = sha256_file(path)
        item = ProtectedLog(
            evidence_id=evidence_id,
            kind=kind,
            path=path,
            sha256=digest,
            bytes=stat.st_size,
            modified_ns=stat.st_mtime_ns,
        )
        prior = seen.get(digest)
        if prior is not None:
            duplicates.append(
                {
                    "sha256": digest,
                    "kept": prior.evidence_id,
                    "skipped": evidence_id,
                }
            )
            continue
        seen[digest] = item
        distinct.append(item)
    distinct.sort(key=lambda item: (item.modified_ns, item.evidence_id))
    return distinct, duplicates


def strip_header(line: str) -> str:
    return HEADER_RE.sub("", line, count=1).strip()


def split_location_evidence(text: str) -> tuple[str, str | None]:
    """Separate CK3's location tail from the semantic diagnostic.

    The complete tail remains evidence but never participates in template
    identity.  This prevents different call-stack paths, frame labels, or
    frame counts from fragmenting one semantic error contract.
    """
    match = SCRIPT_LOCATION_TAIL_RE.search(text)
    if match is None:
        return text.strip(), None
    semantic = text[: match.start()].rstrip()
    location = text[match.end() :].strip()
    return semantic, location or None


def extract_structured_slots(text: str) -> list[dict]:
    """Extract multi-key entity references without affecting template ID."""
    match = TRAVEL_CHARACTER_REFERENCE_RE.search(text)
    if match is None:
        script_match = SCRIPT_SYSTEM_ROLE_RE.match(text)
        if script_match is not None:
            suffix = script_match.group("suffix").strip()
            if suffix.startswith("[") and suffix.endswith("]"):
                match = SCRIPT_TRAVEL_NO_DESTINATIONS_RE.match(
                    suffix[1:-1].strip()
                )
    if match is None:
        return []
    display = re.sub(r"\s+of\s*$", "", match.group("display").strip())
    return [
        {
            "role": "key",
            "name": "character_display",
            "value": display,
            "present": True,
        },
        {
            "role": "key",
            "name": "internal_id",
            "value": match.group("internal").strip(),
            "present": True,
        },
        {
            "role": "optional_key",
            "name": "historical_id",
            "value": (
                match.group("historical").strip()
                if match.group("historical") is not None
                else None
            ),
            "present": match.group("historical") is not None,
        },
    ]


def normalize_key_path(expression: str) -> str:
    """Preserve CK3 key-path grammar while masking each empirical key.

    Namespace markers such as ``scope:`` are grammar, not part of a key slot.
    Periods express relationships between key segments and therefore remain in
    the normalized structure.
    """
    expression = expression.strip()
    if KEY in expression:
        return expression
    namespace = ""
    namespace_match = KEY_PATH_NAMESPACE_RE.match(expression)
    if namespace_match is not None:
        namespace = namespace_match.group("namespace") + ":"
        expression = namespace_match.group("path").strip()
    segments = [segment.strip() for segment in expression.split(".")]
    if not segments or not all(KEY_PATH_SEGMENT_RE.fullmatch(segment) for segment in segments):
        return expression
    return namespace + ".".join(KEY for _ in segments)


def normalize_script_system_role_slots(text: str) -> str:
    """Mask the key path before a literal ``trigger`` or ``effect`` role."""
    match = SCRIPT_SYSTEM_ROLE_RE.match(text)
    if match is None:
        return text
    suffix = match.group("suffix")
    stripped = suffix.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        reason = stripped[1:-1].strip()
        travel = SCRIPT_TRAVEL_NO_DESTINATIONS_RE.match(reason)
        if travel is not None:
            reason = (
                f"{KEY} ( {KEY} {OPTIONAL_KEY} )'s travel plan have no valid "
                "destinations"
            )
        tributary = TRIBUTARY_REASON_RE.match(reason)
        if tributary is not None:
            reason = (
                f"Tried to make '{KEY} of {KEY} ( {KEY} {OPTIONAL_KEY} )' a "
                f"Tributary contract with Suzerain '{KEY} of {KEY} ( {KEY} "
                f"{OPTIONAL_KEY} )', but they are already a vassal of {KEY} of "
                f"{KEY} ( {KEY} {OPTIONAL_KEY} )"
            )
        suffix = f" [ {reason} ]"
    return (
        match.group("prefix")
        + normalize_key_path(match.group("expression"))
        + " "
        + match.group("role")
        + suffix
    )


def normalize_comparison_types(text: str) -> str:
    """Represent runtime comparison categories as contextual type symbols."""

    def replace(match: re.Match[str]) -> str:
        return (
            match.group("prefix")
            + "'"
            + KEY
            + "'"
            + match.group("middle")
            + "'"
            + KEY
            + "'"
            + match.group("suffix")
        )

    return COMPARISON_TYPE_MISMATCH_RE.sub(replace, text)


def normalize_trigger_description(text: str) -> str:
    """Separate the leading trigger key from deterministic location evidence."""
    match = TRIGGER_DESCRIPTION_RE.match(text)
    if match is None:
        return text
    return f"{KEY}: {match.group('body')} at file: {LOCATOR}"


def normalize_flavorization_title(text: str) -> str:
    """Mask the referenced landed-title key, which is not a locator."""
    match = FLAVORIZATION_TITLE_RE.match(text)
    if match is None:
        return text
    return match.group("prefix") + OPTIONAL_KEY


def normalize_activity_event_reference(text: str) -> str:
    """Normalize event and character identity while retaining optional metadata."""
    match = ACTIVITY_EVENT_REFERENCE_RE.match(text)
    if match is None:
        return text
    return (
        match.group("prefix")
        + f"'{KEY}'"
        + match.group("character_prefix")
        + f"{KEY} ( {KEY} {OPTIONAL_KEY} )"
        + match.group("suffix")
    )


def normalize_known_key_grammars(text: str) -> str:
    """Mask identifiers only inside empirically stable CK3 sentence grammars."""

    match = PDXMESH_SYNC_RE.match(text)
    if match is not None:
        return match.group("prefix") + KEY + match.group("middle") + KEY + match.group("suffix")

    match = DECISION_INTERVAL_RE.match(text)
    if match is not None:
        return KEY + match.group("suffix")

    match = UNRECOGNIZED_LOC_KEY_RE.match(text)
    if match is not None:
        return match.group("prefix") + KEY + f". file: {LOCATOR}"

    match = EVENT_THEME_KEY_RE.match(text)
    if match is not None:
        return match.group("prefix") + KEY + match.group("middle") + KEY + match.group("suffix")

    for pattern in (ORPHAN_EVENT_RE, QUEUED_EVENT_RE):
        match = pattern.match(text)
        if match is not None:
            return match.group("prefix") + KEY + match.group("suffix")

    match = ARTIFACT_FEATURE_RE.match(text)
    if match is not None:
        return (
            match.group("prefix")
            + f"'{OPTIONAL_KEY}' ({KEY})"
            + match.group("middle")
            + KEY
        )

    match = FAITH_SCOPE_RE.match(text)
    if match is not None:
        return match.group("prefix") + f"'{KEY}'" + match.group("suffix")
    match = POSTVALIDATE_EFFECT_RE.match(text)
    if match is not None:
        return match.group("prefix") + f"'{KEY}'" + match.group("suffix")
    match = MATERIAL_SHADER_RE.match(text)
    if match is not None:
        return (
            match.group("prefix")
            + OPTIONAL_KEY
            + match.group("middle")
            + KEY
            + match.group("suffix")
        )
    match = LOCALIZATION_HASH_COLLISION_RE.match(text)
    if match is not None:
        return (
            match.group("prefix")
            + f"'{KEY}'"
            + match.group("middle")
            + f"'{KEY}'"
            + match.group("suffix")
            + PARAM
            + match.group("period")
        )
    match = AUDIO_EVENT_INFO_RE.match(text)
    if match is not None:
        return match.group("prefix") + f"'{KEY}'" + match.group("suffix")
    match = PERSISTENT_UNEXPECTED_TOKEN_RE.match(text)
    if match is not None:
        return (
            match.group("prefix")
            + KEY
            + ", "
            + LOCATOR
            + match.group("file")
            + LOCATOR
            + match.group("tail")
            + LOCATOR
        )

    without_source = SCRIPTED_EFFECT_SOURCE_RE.sub(f"{LOCATOR} ", text, count=1)
    rendered = RENDERED_CHARACTER_RE.sub(
        lambda item: item.group("prefix") + KEY + " ", without_source
    ).strip()
    locator_prefix = f"{LOCATOR} " if rendered.startswith(f"{LOCATOR} ") else ""
    body = rendered[len(locator_prefix) :]
    match = SCRIPTED_EFFECT_KEY_RE.match(body)
    if match is not None:
        return (
            locator_prefix
            + KEY
            + match.group("separator")
            + TYPE
            + match.group("suffix")
        )
    return rendered


def normalize_structured_slots(text: str) -> str:
    """Replace contextual entities with stable, grammar-preserving slots."""

    def replace_travel_character(match: re.Match[str]) -> str:
        # The optional placeholder is always present in the canonical pattern;
        # whether a concrete Historical ID exists is extraction data, not a
        # different template.
        return (
            match.group("prefix")
            + f"{KEY} ( {KEY} {OPTIONAL_KEY} )"
            + match.group("suffix")
        )

    normalized = TRAVEL_CHARACTER_REFERENCE_RE.sub(replace_travel_character, text)
    normalized = normalize_activity_event_reference(normalized)
    normalized = normalize_script_system_role_slots(normalized)
    normalized = normalize_comparison_types(normalized)
    normalized = normalize_trigger_description(normalized)
    normalized = normalize_flavorization_title(normalized)
    normalized = normalize_known_key_grammars(normalized)
    return normalized


def normalize_persistent_clause(text: str) -> str:
    """Normalize known key slots inside one persistent-reader clause."""
    clause = PERSISTENT_NEAR_LINE_RE.sub("", text).strip(" ,")
    unknown = UNKNOWN_TRIGGER_KEY_RE.match(clause)
    if unknown is not None:
        return unknown.group("prefix") + KEY
    failed = FAILED_KEY_REFERENCE_RE.match(clause)
    if failed is not None:
        return failed.group("prefix") + f"{KEY} : {KEY}"
    return clause


def semantic_units(source_family: str, message: str) -> list[str]:
    """Return base semantic occurrences represented by one raw log block.

    Persistent-reader blocks can concatenate the same diagnostic clause many
    times.  Each clause is one occurrence of the base template; repetition
    cardinality is not template content.
    """
    if source_family.casefold() == "pdx_persistent_reader.cpp":
        wrapper = PERSISTENT_WRAPPER_RE.match(message)
        if wrapper is not None:
            inner = wrapper.group("inner")
            starts = list(PERSISTENT_CLAUSE_START_RE.finditer(inner))
            if starts:
                units: list[str] = []
                for index, start in enumerate(starts):
                    end = starts[index + 1].start() if index + 1 < len(starts) else len(inner)
                    clause = normalize_persistent_clause(inner[start.start() : end])
                    if clause:
                        units.append(clause)
                if units:
                    return units
    semantic, _ = split_location_evidence(message)
    return [normalize_structured_slots(semantic)] if semantic else []


def mask_locators(text: str) -> str:
    """Mask only deterministic location metadata; preserve semantic values."""
    text = WINDOWS_PATH_RE.sub(LOCATOR, text)
    text = QUOTED_PATH_RE.sub(LOCATOR, text)
    text = RELATIVE_PATH_RE.sub(LOCATOR, text)
    text = FILENAME_RE.sub(LOCATOR, text)
    text = LINE_LOCATOR_RE.sub(LOCATOR, text)
    return text


def block_message(block: TimestampedLogBlock) -> str:
    header = strip_header(block.header_line)
    # A persistent-reader diagnostic can repeat across more than twelve
    # physical lines before its closing `" in file: ...` wrapper.  Truncating
    # here changes the semantic parse: the same base clause is then treated as
    # one opaque message.  The parser has already bounded the block at the next
    # timestamp, so retain the complete block and let ``semantic_units`` turn
    # repetition into occurrence cardinality.
    continuations = [line.strip() for line in block.continuation_lines if line.strip()]
    joined = " ".join([header, *continuations])
    return re.sub(r"\s+", " ", joined).strip()


def tokenize(text: str) -> tuple[str, ...]:
    semantic, _ = split_location_evidence(text)
    masked = mask_locators(normalize_structured_slots(semantic))
    tokens = HEADER_TOKEN_RE.findall(masked)
    collapsed: list[str] = []
    for token in tokens[:384]:
        if token == LOCATOR and collapsed and collapsed[-1] == LOCATOR:
            continue
        collapsed.append(token)
    return tuple(collapsed)


def script_system_layer_tokens(
    tokens: Sequence[str],
) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    """Split a normalized script-system contract into outer and reason layers.

    The square brackets are an empirical structural delimiter.  The ordered
    tokens before ``[`` form L1 (source-specific outer envelope); the tokens
    inside the brackets form the reason-specific L2 contract.  A malformed or
    non-script-system sequence has no layered representation.
    """
    if len(tokens) < 8:
        return None
    if tuple(token.casefold() for token in tokens[:3]) != (
        "script",
        "system",
        "error",
    ):
        return None
    try:
        open_index = tokens.index("[")
    except ValueError:
        return None
    try:
        close_index = len(tokens) - 1 - tuple(reversed(tokens)).index("]")
        complete = True
    except ValueError:
        # Tokenization is deliberately bounded.  Preserve a provable L1 outer
        # envelope when an exceptionally long reason loses its closing bracket,
        # but make the partial L2 impossible to treat as a learned full reason.
        close_index = len(tokens)
        complete = False
    if close_index <= open_index + 1 or open_index == 0:
        return None
    outer = tuple(tokens[:open_index])
    if not outer or outer[-1].casefold() not in {"trigger", "effect"}:
        return None
    reason = tuple(tokens[open_index + 1 : close_index])
    if not complete:
        reason = (*reason, TRUNCATED_REASON)
    return outer, reason


def reason_semantic_lead(tokens: Sequence[str]) -> tuple[str, ...]:
    """Return the first ordered semantic words of one L2 reason contract."""
    words = [
        token.casefold()
        for token in tokens
        if token not in PUNCTUATION
        and token
        not in {
            KEY,
            OPTIONAL_KEY,
            LOCATOR,
            TYPE,
            "<VALUE>",
            "<PARAM>",
            TRUNCATED_REASON,
        }
    ]
    return tuple(words[:2])


def template_fixed_semantics_are_ordered(
    template_tokens: Sequence[str], candidate_tokens: Sequence[str]
) -> bool:
    """Require every learned fixed semantic token in candidate order.

    Slot markers and punctuation are deliberately ignored.  This rejects a
    superficially similar reason subtype whose learned template contains a
    conflicting literal such as ``domicile`` or ``null``.
    """
    slots = {
        KEY,
        OPTIONAL_KEY,
        LOCATOR,
        TYPE,
        "<VALUE>",
        "<PARAM>",
        TRUNCATED_REASON,
    }

    def semantic(tokens: Sequence[str], *, remove_slots: bool) -> list[str]:
        return [
            token.casefold()
            for token in tokens
            if token not in PUNCTUATION
            and (not remove_slots or token not in slots)
            and re.search(r"[A-Za-z0-9]", token)
        ]

    fixed = semantic(template_tokens, remove_slots=True)
    candidate = semantic(candidate_tokens, remove_slots=False)
    if not fixed:
        return False
    position = 0
    for token in candidate:
        if token == fixed[position]:
            position += 1
            if position == len(fixed):
                return True
    return False


def diagnostic_lead(text: str) -> tuple[str, ...]:
    """Return the ordered semantic phrase immediately introducing the detail.

    This is deliberately part of cluster identity.  The engine source prefix
    alone is not sufficient: one C++ source routinely emits several distinct
    diagnostic contracts.  Quoted values are removed before selecting the
    first two words, while a persistent-reader outer quote is unwrapped first.
    """
    semantic, _ = split_location_evidence(text)
    masked = mask_locators(normalize_structured_slots(semantic))
    faith_scope = FAITH_SCOPE_RE.match(masked)
    if faith_scope is not None:
        return ("failed", "to", "scope", "to", faith_scope.group("kind").casefold())
    prefix_match = SCRIPT_SYSTEM_PREFIX_RE.match(masked)
    prefix_contract: str | None = None
    if prefix_match is not None:
        context = prefix_match.group("context") or ""
        prefix_words = [
            word.casefold()
            for word in re.findall(r"[A-Za-z_][A-Za-z0-9_#@-]*", context)
        ]
        prefix_contract = "prefix:" + (
            "_".join(prefix_words) if prefix_words else "plain"
        )
    script_role = SCRIPT_SYSTEM_ROLE_RE.match(masked)
    if script_role is not None:
        assert prefix_contract is not None
        expression = script_role.group("expression").strip()
        namespace_match = KEY_PATH_NAMESPACE_RE.match(expression)
        namespace = (
            namespace_match.group("namespace").casefold()
            if namespace_match is not None
            else "plain"
        )
        key_count = expression.count(KEY)
        shape = namespace + ":" + ".".join("key" for _ in range(key_count))
        reason_words = [
            word.casefold()
            for word in re.findall(
                r"[A-Za-z_][A-Za-z0-9_#@-]*", script_role.group("suffix")
            )
            if word.casefold() not in {"key", "optional_key", "locator", "type"}
        ]
        return (
            prefix_contract,
            script_role.group("role").casefold(),
            shape,
            *reason_words[:2],
        )
    wrapper = PERSISTENT_WRAPPER_RE.match(masked)
    if wrapper is not None:
        focus = wrapper.group("inner")
    else:
        introductions = list(ERROR_INTRO_RE.finditer(masked))
        focus = masked[introductions[-1].end() :] if introductions else masked
        focus = QUOTED_VALUE_RE.sub(" <KEY> ", focus)
    words = [
        token.casefold()
        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_#@-]*", focus)
        if token.casefold() not in {"key", "optional_key", "locator", "type"}
    ]
    lead = tuple(words[:2])
    return (prefix_contract, *lead) if prefix_contract is not None else lead


def constant_tokens(tokens: Sequence[str]) -> tuple[str, ...]:
    return tuple(token for token in tokens if token != LOCATOR)


def sequence_similarity(left: Sequence[str], right: Sequence[str]) -> float:
    """Ordered-token similarity with a length penalty and no autojunk."""
    if not left or not right:
        return 0.0
    matcher = difflib.SequenceMatcher(None, left, right, autojunk=False)
    matched = sum(block.size for block in matcher.get_matching_blocks())
    precision = matched / max(len(left), len(right))
    coverage = matched / min(len(left), len(right))
    length_ratio = min(len(left), len(right)) / max(len(left), len(right))
    return (0.55 * precision + 0.35 * coverage + 0.10 * length_ratio)


def has_ordered_anchor_overlap(left: Sequence[str], right: Sequence[str]) -> bool:
    """Reject merges without a repeated ordered semantic phrase."""
    left_semantic = [
        token.casefold()
        for token in left
        if token != LOCATOR and token not in PUNCTUATION
    ]
    right_semantic = [
        token.casefold()
        for token in right
        if token != LOCATOR and token not in PUNCTUATION
    ]
    if min(len(left_semantic), len(right_semantic)) <= 2:
        return bool(set(left_semantic) & set(right_semantic))
    left_bigrams = set(zip(left_semantic, left_semantic[1:]))
    right_bigrams = set(zip(right_semantic, right_semantic[1:]))
    return bool(left_bigrams & right_bigrams)


def matching_pairs(reference: Sequence[str], candidate: Sequence[str]) -> dict[int, int]:
    matcher = difflib.SequenceMatcher(None, reference, candidate, autojunk=False)
    pairs: dict[int, int] = {}
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            pairs[block.a + offset] = block.b + offset
    return pairs


def choose_medoid(records: Sequence[SequenceRecord]) -> SequenceRecord:
    if len(records) == 1:
        return records[0]
    candidates = sorted(records, key=lambda record: (-record.occurrences, record.tokens))[:40]
    comparison = sorted(records, key=lambda record: (-record.occurrences, record.tokens))[:100]
    best: tuple[float, int, tuple[str, ...], SequenceRecord] | None = None
    total_weight = sum(record.occurrences for record in comparison) or 1
    for candidate in candidates:
        score = sum(
            sequence_similarity(candidate.tokens, other.tokens) * other.occurrences
            for other in comparison
        ) / total_weight
        rank = (score, candidate.occurrences, tuple(reversed(candidate.tokens)), candidate)
        if best is None or rank[:2] > best[:2]:
            best = rank
    assert best is not None
    return best[3]


def _meaningful(span: Sequence[str]) -> list[str]:
    return [token for token in span if token not in PUNCTUATION and token != LOCATOR]


def infer_slot(spans: Sequence[tuple[str, ...]]) -> str | None:
    nonempty = [span for span in spans if span]
    if not nonempty:
        return None
    flattened = [token for span in nonempty for token in span]
    if flattened and all(token == LOCATOR or token in PUNCTUATION for token in flattened):
        return "<LOCATOR>"

    values = [tuple(_meaningful(span)) for span in nonempty]
    values = [value for value in values if value]
    if not values:
        return "<LOCATOR>"
    distinct = sorted(set(values))
    if len(distinct) == 1:
        return " ".join(distinct[0])

    if all(
        len(value) == 1
        and value[0].islower()
        and value[0].isalpha()
        and len(value[0]) <= 16
        for value in distinct
    ) and len(distinct) <= 4:
        return "<ALT:" + "|".join(value[0] for value in distinct) + ">"

    key_like = 0
    for value in distinct:
        if all(IDENTIFIER_RE.match(token) for token in value):
            if any(
                "_" in token
                or "." in token
                or any(char.isdigit() for char in token)
                or (token[:1].isupper() and token[1:].islower())
                for token in value
            ):
                key_like += 1
            elif len(value) <= 4:
                key_like += 1
    if key_like == len(distinct):
        return "<KEY>"
    if all(all(token.replace(".", "", 1).isdigit() for token in value) for value in distinct):
        return "<VALUE>"
    return "<PARAM>"


def derive_template(cluster: TemplateCluster, stable_ratio: float = 0.80) -> None:
    records = cluster.records
    medoid = choose_medoid(records)
    cluster.medoid = medoid
    reference = medoid.tokens
    mappings = [matching_pairs(reference, record.tokens) for record in records]
    required = max(2, math.ceil(len(records) * stable_ratio)) if len(records) > 1 else 1
    stable_positions = [
        index
        for index, token in enumerate(reference)
        if token == LOCATOR
        or sum(1 for mapping in mappings if index in mapping) >= required
    ]

    parts: list[str] = []
    boundaries = [-1, *stable_positions, len(reference)]
    for boundary_index in range(len(boundaries) - 1):
        left = boundaries[boundary_index]
        right = boundaries[boundary_index + 1]
        spans: list[tuple[str, ...]] = []
        for record, mapping in zip(records, mappings):
            left_target = mapping.get(left, -1) if left >= 0 else -1
            right_target = mapping.get(right, len(record.tokens)) if right < len(reference) else len(record.tokens)
            if right_target < left_target:
                spans.append(())
            else:
                spans.append(tuple(record.tokens[left_target + 1 : right_target]))
        slot = infer_slot(spans)
        if slot and (not parts or parts[-1] != slot):
            parts.append(slot)
        if right < len(reference):
            token = reference[right]
            if token == LOCATOR:
                token = "<LOCATOR>"
            if not parts or parts[-1] != token:
                parts.append(token)

    cluster.template_tokens = tuple(parts)
    cluster.support_occurrences = sum(record.occurrences for record in records)
    cluster.support_evidence = set().union(*(record.evidence_ids for record in records))


def cluster_source_records(
    source_family: str,
    records: Sequence[SequenceRecord],
    threshold: float,
) -> list[TemplateCluster]:
    clusters: list[TemplateCluster] = []
    ordered = sorted(records, key=lambda record: (-record.occurrences, record.tokens))
    for record in ordered:
        best: tuple[float, TemplateCluster] | None = None
        for cluster in clusters:
            assert cluster.medoid is not None
            if cluster.medoid.semantic_lead != record.semantic_lead:
                continue
            if not has_ordered_anchor_overlap(cluster.medoid.tokens, record.tokens):
                continue
            score = sequence_similarity(cluster.medoid.tokens, record.tokens)
            if score < threshold:
                continue
            if best is None or score > best[0]:
                best = (score, cluster)
        if best is None:
            cluster = TemplateCluster(
                source_family=source_family,
                cluster_number=len(clusters) + 1,
                records=[record],
                medoid=record,
            )
            clusters.append(cluster)
        else:
            best[1].records.append(record)
    for cluster in clusters:
        derive_template(cluster)
    clusters.sort(key=lambda item: (-item.support_occurrences, item.template_tokens))
    return clusters


def collect_records(logs: Sequence[ProtectedLog]) -> tuple[dict[str, list[SequenceRecord]], dict]:
    records: dict[tuple[str, tuple[str, ...]], SequenceRecord] = {}
    evidence_stats: dict[str, dict] = {}
    for evidence in logs:
        block_count = 0
        eligible_count = 0
        for block in iter_log_blocks(evidence.path, log_relpath="error.log"):
            if block.timestamp is None:
                continue
            block_count += 1
            message = block_message(block)
            if not message:
                continue
            _, location_evidence = split_location_evidence(message)
            structured_slots = extract_structured_slots(message)
            for unit in semantic_units(block.source_family, message):
                tokens = tokenize(unit)
                if not tokens:
                    continue
                eligible_count += 1
                key = (block.source_family, tokens)
                record = records.get(key)
                if record is None:
                    record = SequenceRecord(
                        block.source_family,
                        tokens,
                        diagnostic_lead(unit),
                    )
                    records[key] = record
                record.occurrences += 1
                record.evidence_ids.add(evidence.evidence_id)
                if len(record.examples) < 3 and unit not in record.examples:
                    record.examples.append(unit[:500])
                if (
                    location_evidence
                    and len(record.location_examples) < 3
                    and location_evidence not in record.location_examples
                ):
                    record.location_examples.append(location_evidence[:1000])
                if (
                    structured_slots
                    and len(record.structured_slot_examples) < 3
                    and structured_slots not in record.structured_slot_examples
                ):
                    record.structured_slot_examples.append(structured_slots)
        evidence_stats[evidence.evidence_id] = {
            "kind": evidence.kind,
            "path": str(evidence.path),
            "sha256": evidence.sha256,
            "bytes": evidence.bytes,
            "timestamped_blocks": block_count,
            "eligible_messages": eligible_count,
        }

    by_source: dict[str, list[SequenceRecord]] = collections.defaultdict(list)
    for record in records.values():
        by_source[record.source_family].append(record)
    return dict(by_source), evidence_stats


def best_cluster(
    clusters_by_source: dict[str, list[TemplateCluster]],
    source_family: str,
    tokens: tuple[str, ...],
    semantic_lead: tuple[str, ...],
    threshold: float,
) -> TemplateCluster | None:
    best: tuple[float, TemplateCluster] | None = None
    for cluster in clusters_by_source.get(source_family, []):
        assert cluster.medoid is not None
        if cluster.medoid.semantic_lead != semantic_lead:
            continue
        if not has_ordered_anchor_overlap(cluster.medoid.tokens, tokens):
            continue
        score = sequence_similarity(cluster.medoid.tokens, tokens)
        if score < threshold:
            continue
        if best is None or score > best[0]:
            best = (score, cluster)
    return best[1] if best is not None else None


def best_layered_cluster(
    clusters_by_source: dict[str, list[TemplateCluster]],
    source_family: str,
    tokens: tuple[str, ...],
    semantic_lead: tuple[str, ...],
    threshold: float,
) -> LayeredClusterMatch:
    """Match the full contract, then independently prove a known L1 envelope.

    Novel bracket reasons are not force-fit to a trained reason cluster.  They
    can still receive an L1 assignment when the exact normalized outer grammar
    is present in approved training for the same source family.
    """
    cluster = best_cluster(
        clusters_by_source,
        source_family,
        tokens,
        semantic_lead,
        threshold,
    )
    layers = script_system_layer_tokens(tokens)
    outer_contract = layers[0] if layers is not None else None
    reason_contract = layers[1] if layers is not None else None
    if cluster is not None:
        return LayeredClusterMatch(
            cluster,
            outer_contract,
            outer_contract is not None,
            reason_contract,
            cluster if reason_contract is not None else None,
        )
    if outer_contract is None:
        return LayeredClusterMatch(None, None, False, None, None)
    outer_known = any(
        cluster.medoid is not None
        and (candidate_layers := script_system_layer_tokens(cluster.medoid.tokens))
        is not None
        and candidate_layers[0] == outer_contract
        for cluster in clusters_by_source.get(source_family, [])
    )
    assert reason_contract is not None
    reason_lead = reason_semantic_lead(reason_contract)
    if TRUNCATED_REASON in reason_contract:
        return LayeredClusterMatch(
            None,
            outer_contract,
            outer_known,
            reason_contract,
            None,
        )
    best_reason: tuple[float, TemplateCluster] | None = None
    for candidate in clusters_by_source.get(source_family, []):
        assert candidate.medoid is not None
        candidate_layers = script_system_layer_tokens(candidate.medoid.tokens)
        template_layers = script_system_layer_tokens(candidate.template_tokens)
        if candidate_layers is None or template_layers is None:
            continue
        candidate_reason = candidate_layers[1]
        if reason_semantic_lead(candidate_reason) != reason_lead:
            continue
        if not has_ordered_anchor_overlap(candidate_reason, reason_contract):
            continue
        if not template_fixed_semantics_are_ordered(
            template_layers[1], reason_contract
        ):
            continue
        score = sequence_similarity(candidate_reason, reason_contract)
        if score < threshold:
            continue
        if best_reason is None or score > best_reason[0]:
            best_reason = (score, candidate)
    return LayeredClusterMatch(
        None,
        outer_contract,
        outer_known,
        reason_contract,
        best_reason[1] if best_reason is not None else None,
    )


def layered_contract_id(
    source_family: str,
    outer_contract: Sequence[str],
    reason_contract: Sequence[str],
) -> str:
    """Return a stable ID for a composed, not-yet-observed L1/L2 pairing."""
    material = (
        source_family
        + "\0L1\0"
        + " ".join(outer_contract)
        + "\0L2\0"
        + " ".join(reason_contract)
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def mutate_key(message: str, values: Iterable[str]) -> str:
    mutated = message
    for index, value in enumerate(sorted(set(values), key=len, reverse=True), start=1):
        if value:
            mutated = mutated.replace(value, f"SYNTHETIC_KEY_{index}_ZZZ")
    return mutated


def mutate_locators(message: str) -> str:
    """Change locator values while preserving their lexical locator shapes."""
    protected: list[tuple[str, str]] = []

    def protect(pattern: re.Pattern[str], replacement: str, text: str) -> str:
        def substitute(match: re.Match[str]) -> str:
            marker = f"ZZZLOCATORMARKER{len(protected)}ZZZ"
            protected.append((marker, replacement))
            return marker

        return pattern.sub(substitute, text)

    mutated = protect(
        QUOTED_PATH_RE,
        "'file: common/synthetic/example.txt line: 987654 (synthetic_scope)'",
        message,
    )
    mutated = protect(
        WINDOWS_PATH_RE,
        r"Z:\synthetic\path\sample.txt",
        mutated,
    )
    mutated = protect(
        RELATIVE_PATH_RE,
        "common/synthetic/example.txt",
        mutated,
    )
    mutated = protect(
        FILENAME_RE,
        "synthetic_example.txt",
        mutated,
    )
    mutated = LINE_LOCATOR_RE.sub("line: 987654", mutated)
    for marker, replacement in protected:
        mutated = mutated.replace(marker, replacement)
    return mutated


def evaluate_frozen_oracle(
    clusters_by_source: dict[str, list[TemplateCluster]],
    oracle_root: Path,
    threshold: float,
) -> dict:
    candidate_path = oracle_root / "SEMANTIC_CALIBRATION_SAMPLE_CANDIDATE.json"
    oracle_path = oracle_root / "SEMANTIC_LABELS_ADJUDICATED.json"
    if not candidate_path.is_file() or not oracle_path.is_file():
        return {"status": "not_available"}
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    samples = {sample["sample_id"]: sample for sample in candidate["samples"]}
    assignments: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    counts = collections.Counter()
    mutation_examples: list[dict] = []
    locator_examples: list[dict] = []
    unassigned_examples: list[dict] = []

    for annotation in oracle["annotations"]:
        sample = samples[annotation["sample_id"]]
        raw = base64.b64decode(sample["raw_block_base64"])
        text = raw.decode("utf-8", errors="replace")
        lines = text.splitlines()
        block = TimestampedLogBlock(
            timestamp=sample["timestamp"],
            level=sample["level"],
            source_tag=sample["source_tag"],
            source_family=sample["source_family"],
            header_line=lines[0] if lines else "",
            continuation_lines=lines[1:],
            raw_block=text,
            line_number=sample["start_line"],
            end_line=sample["end_line"],
        )
        message = block_message(block)
        units = semantic_units(sample["source_family"], message)
        if not units:
            counts["samples"] += 1
            counts["unassigned"] += 1
            continue
        unit = units[0]
        original_tokens = tokenize(unit)
        cluster = best_cluster(
            clusters_by_source,
            sample["source_family"],
            original_tokens,
            diagnostic_lead(unit),
            threshold,
        )
        counts["samples"] += 1
        if cluster is None:
            counts["unassigned"] += 1
            if len(unassigned_examples) < 20:
                unassigned_examples.append(
                    {
                        "sample_id": sample["sample_id"],
                        "source_family": sample["source_family"],
                        "message": sample["header_message"],
                    }
                )
            continue
        counts["assigned"] += 1
        expected = annotation["issues"][0]
        label = (expected["category"], expected["error_type"])
        assignments[cluster.cluster_id].append(label)

        locator_message = mutate_locators(message)
        locator_units = semantic_units(sample["source_family"], locator_message)
        locator_unit = locator_units[0] if locator_units else locator_message
        locator_tokens = tokenize(locator_unit)
        locator_cluster = best_cluster(
            clusters_by_source,
            sample["source_family"],
            locator_tokens,
            diagnostic_lead(locator_unit),
            threshold,
        )
        counts["locator_mutations"] += 1
        if locator_cluster and locator_cluster.cluster_id == cluster.cluster_id:
            counts["locator_stable"] += 1
        elif len(locator_examples) < 20:
            locator_examples.append(
                {
                    "sample_id": sample["sample_id"],
                    "source_family": sample["source_family"],
                    "cluster_id": cluster.cluster_id,
                    "mutated_cluster_id": (
                        locator_cluster.cluster_id if locator_cluster else None
                    ),
                    "original_tokens": list(original_tokens),
                    "mutated_tokens": list(locator_tokens),
                    "message": message[:400],
                }
            )

        values = [
            *expected.get("referenced_symbols", []),
            *expected.get("referenced_objects", []),
        ]
        if values:
            mutated = mutate_key(unit, values)
            if mutated != unit:
                counts["key_mutations"] += 1
                key_cluster = best_cluster(
                    clusters_by_source,
                    sample["source_family"],
                    tokenize(mutated),
                    diagnostic_lead(mutated),
                    threshold,
                )
                if key_cluster and key_cluster.cluster_id == cluster.cluster_id:
                    counts["key_stable"] += 1
                elif len(mutation_examples) < 20:
                    mutation_examples.append(
                        {
                            "sample_id": sample["sample_id"],
                            "source_family": sample["source_family"],
                            "cluster_id": cluster.cluster_id,
                            "mutated_cluster_id": (
                                key_cluster.cluster_id if key_cluster else None
                            ),
                            "values": values,
                            "message": message[:400],
                        }
                    )

    pure_samples = 0
    mixed_clusters: list[dict] = []
    for cluster_id, labels in assignments.items():
        distribution = collections.Counter(labels)
        majority = distribution.most_common(1)[0][1]
        pure_samples += majority
        if len(distribution) > 1:
            mixed_clusters.append(
                {
                    "cluster_id": cluster_id,
                    "samples": len(labels),
                    "labels": [
                        {"category": key[0], "error_type": key[1], "count": value}
                        for key, value in distribution.most_common()
                    ],
                }
            )
    assigned = counts["assigned"]
    return {
        "status": "calibration_only_not_holdout",
        "counts": dict(counts),
        "assignment_rate": assigned / counts["samples"] if counts["samples"] else 0.0,
        "weighted_label_purity": pure_samples / assigned if assigned else 0.0,
        "mixed_cluster_count": len(mixed_clusters),
        "mixed_clusters": sorted(
            mixed_clusters, key=lambda item: (-item["samples"], item["cluster_id"])
        )[:30],
        "unassigned_examples": unassigned_examples,
        "locator_mutation_failures": locator_examples,
        "identifier_mutation_heuristic_failures": mutation_examples,
    }


def serializable_cluster(cluster: TemplateCluster) -> dict:
    assert cluster.medoid is not None
    layers = script_system_layer_tokens(cluster.template_tokens)
    return {
        "cluster_id": cluster.cluster_id,
        "source_family": cluster.source_family,
        "template": " ".join(cluster.template_tokens),
        "semantic_lead": list(cluster.medoid.semantic_lead),
        "template_tokens": list(cluster.template_tokens),
        "support_occurrences": cluster.support_occurrences,
        "support_evidence_count": len(cluster.support_evidence),
        "support_evidence_ids": sorted(cluster.support_evidence),
        "unique_sequences": len(cluster.records),
        "medoid": " ".join(cluster.medoid.tokens),
        "examples": [
            example
            for record in sorted(
                cluster.records, key=lambda item: (-item.occurrences, item.tokens)
            )[:3]
            for example in record.examples[:1]
        ][:3],
        "location_evidence_examples": [
            example
            for record in sorted(
                cluster.records, key=lambda item: (-item.occurrences, item.tokens)
            )
            for example in record.location_examples
        ][:3],
        "structured_slot_examples": [
            slots
            for record in sorted(
                cluster.records, key=lambda item: (-item.occurrences, item.tokens)
            )
            for slots in record.structured_slot_examples
        ][:3],
        "layer_contracts": (
            {
                "l1_outer_template": " ".join(layers[0]),
                "l1_outer_tokens": list(layers[0]),
                "l2_reason_template": " ".join(layers[1]),
                "l2_reason_tokens": list(layers[1]),
            }
            if layers is not None
            else None
        ),
    }


def write_report(model: dict, path: Path) -> None:
    evaluation = model["evaluation"]
    lines = [
        "# Empirical CK3 error-template learner calibration",
        "",
        f"- Distinct protected error logs: **{model['summary']['distinct_error_logs']}**",
        f"- Duplicate protected copies skipped: **{model['summary']['duplicate_copies_skipped']}**",
        f"- Timestamped blocks: **{model['summary']['timestamped_blocks']:,}**",
        f"- Source families: **{model['summary']['source_families']:,}**",
        f"- Learned candidate templates: **{model['summary']['clusters']:,}**",
        "",
        "## Frozen-oracle calibration (not a holdout claim)",
        "",
    ]
    if evaluation.get("status") != "not_available":
        counts = evaluation["counts"]
        lines.extend(
            [
                f"- Assigned: **{counts.get('assigned', 0)}/{counts.get('samples', 0)}**",
                f"- Weighted category/type purity: **{evaluation['weighted_label_purity']:.2%}**",
                f"- Mixed-label clusters: **{evaluation['mixed_cluster_count']}**",
                f"- Locator mutation stability: **{counts.get('locator_stable', 0)}/{counts.get('locator_mutations', 0)}**",
                f"- Key/object mutation stability: **{counts.get('key_stable', 0)}/{counts.get('key_mutations', 0)}**",
                "",
            ]
        )
    lines.extend(["## Highest-support candidate templates", ""])
    for cluster in model["clusters"][:100]:
        lines.extend(
            [
                f"### `{cluster['source_family']}` / `{cluster['cluster_id']}`",
                "",
                f"- Support: {cluster['support_occurrences']:,} occurrences across {cluster['support_evidence_count']} evidence bundles",
                f"- Template: `{cluster['template'][:500]}`",
                f"- Example: `{cluster['examples'][0][:500] if cluster['examples'] else ''}`",
                "",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runtime-root",
        type=Path,
        default=Path.home() / "AppData" / "Local" / "ck3chronicle",
    )
    parser.add_argument(
        "--oracle-root",
        type=Path,
        required=True,
        help="Directory containing the explicitly supplied calibration oracle files.",
    )
    parser.add_argument("--threshold", type=float, default=0.72)
    parser.add_argument(
        "--exclude-sha256",
        action="append",
        default=[],
        help="Exclude a complete protected error.log hash from training.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logs, duplicates = protected_error_logs(args.runtime_root)
    excluded_hashes = {value.casefold() for value in args.exclude_sha256}
    excluded_logs = [item for item in logs if item.sha256.casefold() in excluded_hashes]
    logs = [item for item in logs if item.sha256.casefold() not in excluded_hashes]
    if not logs:
        raise SystemExit("no protected error.log copies found")
    records_by_source, evidence_stats = collect_records(logs)
    clusters_by_source: dict[str, list[TemplateCluster]] = {}
    for source_family in sorted(records_by_source):
        clusters_by_source[source_family] = cluster_source_records(
            source_family,
            records_by_source[source_family],
            args.threshold,
        )
    clusters = [
        cluster
        for source in sorted(clusters_by_source)
        for cluster in clusters_by_source[source]
    ]
    clusters.sort(
        key=lambda cluster: (
            -cluster.support_occurrences,
            cluster.source_family,
            cluster.cluster_id,
        )
    )
    evaluation = evaluate_frozen_oracle(
        clusters_by_source,
        args.oracle_root,
        args.threshold,
    )
    model = {
        "schema": "ck3chronicle-empirical-template-calibration",
        "schema_version": 3,
        "algorithm": {
            "source_family_hard_partition": True,
            "locator_masking": "deterministic-v2-semantic-evidence-separation",
            "script_location_tail_in_template_identity": False,
            "repeated_clause_expansion": "persistent-reader-v1",
            "structured_key_slots": "multi-key-with-optional-key-v1",
            "script_system_layering": "exact-outer-envelope-plus-reason-contract-v1",
            "alignment": "difflib-sequence-matcher-ordered-tokens",
            "cluster_threshold": args.threshold,
            "stable_token_ratio": 0.80,
            "status": "wip_calibration_not_production",
        },
        "summary": {
            "distinct_error_logs": len(logs),
            "excluded_error_logs": len(excluded_logs),
            "duplicate_copies_skipped": len(duplicates),
            "timestamped_blocks": sum(
                item["timestamped_blocks"] for item in evidence_stats.values()
            ),
            "source_families": len(records_by_source),
            "unique_masked_sequences": sum(len(items) for items in records_by_source.values()),
            "clusters": len(clusters),
        },
        "evidence": evidence_stats,
        "excluded_evidence": [
            {**dataclasses.asdict(item), "path": str(item.path)}
            for item in excluded_logs
        ],
        "duplicates": duplicates,
        "evaluation": evaluation,
        "clusters": [serializable_cluster(cluster) for cluster in clusters],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    model_path = args.output_dir / "empirical_template_model.json"
    report_path = args.output_dir / "EMPIRICAL_TEMPLATE_CALIBRATION.md"
    model_path.write_text(
        json.dumps(model, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_report(model, report_path)
    print(json.dumps(model["summary"], indent=2))
    print(json.dumps(model["evaluation"], indent=2)[:6000])
    print(f"model={model_path}")
    print(f"report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
