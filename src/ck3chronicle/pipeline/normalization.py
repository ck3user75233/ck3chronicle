"""Matching grammar with native value correspondence; no diagnostic semantics.

NORMALIZER_REVISION replaces the selected model's v4.11 identity. Grammar
ports retain case, key/path masks, locator collapsing and layer/lead mechanics.
Differences: strict native headers, recovery before masking, no 384-token cap,
and explicit original values (including absent optionals and removed locators).
No artifact compatibility is asserted. Learner/model features must be evaluated
against this identity; the learner and selected artifact are not modified here.
"""
from __future__ import annotations

import re
from typing import Sequence

from .domain import (ByteSpan, EvidenceSpan, MatchingToken, NormalizedValue,
                     NormalizedView, OccurrenceValue, RecoveredDiagnostic, TokenSpan)
from .emissions import _Text, _collapse, _decode_text, _coalesce
from .diagnostics import _diagnostic_text

NORMALIZER_REVISION = "ck3-native-structural-normalizer-v1"

LOCATOR = "<LOCATOR>"
KEY = "<KEY>"
OPTIONAL_KEY = "<OPTIONAL_KEY>"
TYPE = "<TYPE>"
PARAM = "<PARAM>"
VALUE = "<VALUE>"
TRUNCATED_REASON = "<TRUNCATED_REASON>"

HEADER_RE = re.compile(
    r"^\[\d{2}:\d{2}:\d{2}\]\[[^\]\r\n]+\]\[[^\]\r\n]+\]:\s*"
)

WINDOWS_PATH_RE = re.compile(r"[A-Za-z]:\\[^\r\n\"']+")
QUOTED_PATH_RE = re.compile(r"(?P<quote>[\"'])(?:[^\"'\r\n]*[/\\])[^\"'\r\n]+(?P=quote)")
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
TOKEN_RE = re.compile(
    r"<OPTIONAL_KEY>|<LOCATOR>|<TYPE>|<KEY>|<PARAM>|<VALUE>|"
    r"[A-Za-z_][A-Za-z0-9_#@-]*|"
    r"\d+(?:\.\d+)*|[^\s]"
)
SCRIPT_LOCATION_TAIL_RE = re.compile(r"\s+Script\s+location\s*:\s*", re.IGNORECASE)
SCRIPT_SYSTEM_ROLE_RE = re.compile(
    r"^(?P<prefix>Script\s+system\s+error!\s*(?:\([^\)]*\)\s*)?Error\s*:\s*)"
    r"(?P<expression>.+?)\s+(?P<role>trigger|effect)"
    r"(?P<suffix>\s*\[.*(?:\]\s*)?)$",
    re.IGNORECASE,
)
SCRIPT_SYSTEM_PREFIX_RE = re.compile(
    r"^Script\s+system\s+error!\s*(?P<context>\([^\)]*\))?\s*Error\s*:\s*",
    re.IGNORECASE,
)
SCRIPT_TRAVEL_RE = re.compile(
    r"^(?P<display>.+?)\s+\(\s*Internal\s+ID\s*:?\s*(?P<internal>[^\s\)]+)"
    r"(?:\s*-\s*Historical\s+ID\s*:?\s*(?P<historical>[^\)]+?))?\s*\)"
    r"(?P<possessive>['\u2019]s)\s+travel\s+plan\s+have\s+no\s+valid\s+destinations$",
    re.IGNORECASE,
)
TRAVEL_CHARACTER_REFERENCE_RE = re.compile(
    r"(?P<prefix>Removing\s+travel\s+plan\s+from\s+the\s+character\s+)"
    r"(?P<display>.+?)\s+\(\s*Internal\s+ID\s*:?\s*"
    r"(?P<internal>[^\s\)]+)"
    r"(?:\s*-\s*Historical\s+ID\s+(?P<historical>[^\)]+?))?\s*\)"
    r"(?P<suffix>\s+owner\s+when\s+the\s+travel\s+plan\s+is\s+not\s+ending\s+normally\.?)",
    re.IGNORECASE,
)
ACTIVITY_EVENT_REFERENCE_RE = re.compile(
    r"^(?P<prefix>Trying\s+to\s+trigger\s+activity\s+event\s+)"
    r"(['\"])(?P<event>[^'\"]+)\2"
    r"(?P<character_prefix>\s+for\s+character\s+)"
    r"(?P<display>.+?)\s+\(\s*Internal\s+ID\s*:?\s*"
    r"(?P<internal>[^\s\)]+)"
    r"(?:\s*-\s*Historical\s+ID\s*:?\s*(?P<historical>[^\)]+?))?\s*\)"
    r"(?P<suffix>\s*,\s*but\s+the\s+activity\s+is\s+invalid\s*-\s*skipping\.?)$",
    re.IGNORECASE,
)
PDXMESH_SYNC_RE = re.compile(
    r"^(?P<prefix>pdxmesh\s*\[)\s*(?P<mesh>[^\]\r\n]+)"
    r"(?P<middle>\]\s+is\s+out\s+of\s+sync\s+with\s+its\s+meshsettings\.\s*\[)"
    r"\s*(?P<part>[^\]\r\n]+)(?P<suffix>\]\s+is\s+not\s+in\s+use\s+in\s+file\s*:.*)$",
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
SCRIPTED_EFFECT_DETAILS_RE = re.compile(
    r"^file\s*:\s+.*?\s+line\s*:\s*\d+(?:\s*(?:-|to)\s*\d+)?\s*"
    r"\((?P<effect>[A-Za-z_][A-Za-z0-9_#@-]*)\[args#\d+\]\)\s*:\s*"
    r"(?P=effect)\s*:",
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
RENDERED_CHARACTER_ID_RE = re.compile(
    r"\x15ONCLICK:CHARACTER,(?P<identity>\d+)\s+"
    r"\x15TOOLTIP:CHARACTER,(?P=identity)",
    re.IGNORECASE,
)
FAITH_SCOPE_RE = re.compile(
    r"^(?P<prefix>Failed\s+to\s+scope\s+to\s+(?P<kind>faith|religion)\s+)"
    r"(?P<quote>['\"])(?P<key>[^'\"]+)(?P=quote)"
    r"(?P<suffix>\s+at\s+file\s*:.*)$",
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
    r"(?P<suffix>\s+have\s+the\s+same\s+hash\s*:\s*)(?P<hash>-?\d+)"
    r"(?P<period>\s*\.?)$",
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
COMPARISON_TYPE_MISMATCH_RE = re.compile(
    r"(?P<prefix>Left\s+side\s+and\s+right\s+side\s+during\s+comparison\s+"
    r"were\s+of\s+different\s+types\s*\(\s*left\s+was\s*)"
    r"(['\"])[^'\"]+\2(?P<middle>\s*,\s*right\s+was\s*)"
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
KEY_PATH_NAMESPACE_RE = re.compile(
    r"^(?P<namespace>scope|var|cp|title)\s*:\s*(?P<path>.+)$", re.IGNORECASE
)
KEY_PATH_SEGMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_#@-]*$")
PERSISTENT_WRAPPER_RE = re.compile(
    r'^\s*Error\s*:\s*"(?P<inner>.*)"\s+in\s+file\s*:', re.IGNORECASE
)
ERROR_INTRO_RE = re.compile(r"\bError\s*:\s*", re.IGNORECASE)
QUOTED_VALUE_RE = re.compile(r"(['\"])(?:\\.|(?!\1).)*\1")
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
PUNCTUATION = frozenset("'\"`()[]{}:;,.!?/\\")


def extract_structured_slots(text: str) -> tuple[dict[str, object], ...]:
    def key_slot(name: str, value: str) -> dict[str, object]:
        return {"role": "key", "name": name, "value": value.strip(), "present": True}

    def optional_key_slot(name: str, value: str | None) -> dict[str, object]:
        normalized = value.strip() if value is not None else ""
        return {
            "role": "optional_key",
            "name": name,
            "value": normalized or None,
            "present": bool(normalized),
        }

    def param_slot(name: str, value: str) -> dict[str, object]:
        return {"role": "param", "name": name, "value": value.strip(), "present": True}

    mesh = PDXMESH_SYNC_RE.match(text)
    if mesh is not None:
        return (
            key_slot("mesh", mesh.group("mesh")),
            key_slot("mesh_part", mesh.group("part")),
        )
    decision = DECISION_INTERVAL_RE.match(text)
    if decision is not None:
        return (key_slot("decision", decision.group("key")),)
    loc_key = UNRECOGNIZED_LOC_KEY_RE.match(text)
    if loc_key is not None:
        return (key_slot("localization_key", loc_key.group("key")),)
    theme = EVENT_THEME_KEY_RE.match(text)
    if theme is not None:
        return (
            key_slot("event_theme", theme.group("theme")),
            key_slot("event", theme.group("event")),
        )
    for pattern in (ORPHAN_EVENT_RE, QUEUED_EVENT_RE):
        event = pattern.match(text)
        if event is not None:
            return (key_slot("event", event.group("event")),)
    artifact = ARTIFACT_FEATURE_RE.match(text)
    if artifact is not None:
        display = artifact.group("display").strip()
        return (
            {
                "role": "optional_key",
                "name": "artifact_display",
                "value": display or None,
                "present": bool(display),
            },
            key_slot("artifact_id", artifact.group("identity")),
            key_slot("feature_group", artifact.group("group")),
        )
    faith_scope = FAITH_SCOPE_RE.match(text)
    if faith_scope is not None:
        return (key_slot(faith_scope.group("kind").casefold(), faith_scope.group("key")),)
    postvalidate = POSTVALIDATE_EFFECT_RE.match(text)
    if postvalidate is not None:
        return (key_slot("effect", postvalidate.group("effect")),)
    material = MATERIAL_SHADER_RE.match(text)
    if material is not None:
        return (
            optional_key_slot("shader", material.group("shader")),
            key_slot("mesh", material.group("mesh")),
        )
    collision = LOCALIZATION_HASH_COLLISION_RE.match(text)
    if collision is not None:
        return (
            key_slot("localization_key", collision.group("left")),
            key_slot("localization_key", collision.group("right")),
            param_slot("localization_hash", collision.group("hash")),
        )
    audio = AUDIO_EVENT_INFO_RE.match(text)
    if audio is not None:
        return (key_slot("audio_event", audio.group("event")),)
    unexpected = PERSISTENT_UNEXPECTED_TOKEN_RE.match(text)
    if unexpected is not None:
        return (key_slot("unexpected_token", unexpected.group("token")),)
    flavorization = FLAVORIZATION_TITLE_RE.match(text)
    if flavorization is not None:
        return (optional_key_slot("title", flavorization.group("key")),)
    effect = SCRIPTED_EFFECT_DETAILS_RE.match(text)
    if effect is not None:
        identities: list[dict[str, object]] = [
            key_slot("scripted_effect", effect.group("effect"))
        ]
        seen: set[str] = set()
        for character in RENDERED_CHARACTER_ID_RE.finditer(text):
            value = character.group("identity")
            if value in seen:
                continue
            seen.add(value)
            identities.append(key_slot("character_id", value))
        return tuple(identities)

    activity = ACTIVITY_EVENT_REFERENCE_RE.match(text)
    match = activity or TRAVEL_CHARACTER_REFERENCE_RE.search(text)
    if match is None:
        role = SCRIPT_SYSTEM_ROLE_RE.match(text)
        if role is None:
            return ()
        suffix = role.group("suffix").strip()
        if not (suffix.startswith("[") and suffix.endswith("]")):
            return ()
        reason = suffix[1:-1].strip()
        tributary = TRIBUTARY_REASON_RE.match(reason)
        if tributary is not None:
            slots: list[dict[str, object]] = []
            for prefix in ("first", "second", "third"):
                slots.extend(
                    (
                        key_slot(f"{prefix}_character_display", tributary.group(f"{prefix}_display")),
                        key_slot(f"{prefix}_title", tributary.group(f"{prefix}_title")),
                        key_slot(f"{prefix}_internal_id", tributary.group(f"{prefix}_id")),
                        optional_key_slot(
                            f"{prefix}_historical_id",
                            tributary.group(f"{prefix}_history"),
                        ),
                    )
                )
            return tuple(slots)
        match = SCRIPT_TRAVEL_RE.match(reason)
        if match is None:
            return ()
    display = re.sub(r"\s+of\s*$", "", match.group("display").strip())
    historical = match.group("historical")
    identity_slots: tuple[dict[str, object], ...] = (
        {"role": "key", "name": "character_display", "value": display, "present": True},
        {
            "role": "key",
            "name": "internal_id",
            "value": match.group("internal").strip(),
            "present": True,
        },
        {
            "role": "optional_key",
            "name": "historical_id",
            "value": historical.strip() if historical is not None else None,
            "present": historical is not None,
        },
    )
    if activity is None:
        return identity_slots
    return (
        {
            "role": "key",
            "name": "activity_event",
            "value": activity.group("event").strip(),
            "present": True,
        },
        *identity_slots,
    )


def normalize_key_path(expression: str) -> str:
    expression = expression.strip()
    if KEY in expression:
        return expression
    namespace = ""
    namespace_match = KEY_PATH_NAMESPACE_RE.match(expression)
    if namespace_match is not None:
        namespace = namespace_match.group("namespace") + ":"
        expression = namespace_match.group("path").strip()
    segments = [segment.strip() for segment in expression.split(".")]
    if not segments or not all(KEY_PATH_SEGMENT_RE.fullmatch(item) for item in segments):
        return expression
    return namespace + ".".join(KEY for _ in segments)


def script_system_layers(tokens: Sequence[str]) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    if len(tokens) < 8 or tuple(item.casefold() for item in tokens[:3]) != (
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
        close_index = len(tokens)
        complete = False
    if close_index <= open_index + 1 or open_index == 0:
        return None
    outer = tuple(tokens[:open_index])
    if outer[-1].casefold() not in {"trigger", "effect"}:
        return None
    reason = tuple(tokens[open_index + 1 : close_index])
    if not complete:
        reason = (*reason, TRUNCATED_REASON)
    return outer, reason


def diagnostic_lead(text: str) -> tuple[str, ...]:
    semantic, _ = split_location_evidence(text)
    masked = mask_locators(normalize_structured_slots(semantic))
    faith_scope = FAITH_SCOPE_RE.match(masked)
    if faith_scope is not None:
        return ("failed", "to", "scope", "to", faith_scope.group("kind").casefold())
    prefix = SCRIPT_SYSTEM_PREFIX_RE.match(masked)
    prefix_contract: str | None = None
    if prefix is not None:
        context = prefix.group("context") or ""
        words = [
            word.casefold()
            for word in re.findall(r"[A-Za-z_][A-Za-z0-9_#@-]*", context)
        ]
        prefix_contract = "prefix:" + ("_".join(words) if words else "plain")
    role = SCRIPT_SYSTEM_ROLE_RE.match(masked)
    if role is not None:
        expression = role.group("expression").strip()
        namespace = KEY_PATH_NAMESPACE_RE.match(expression)
        shape_namespace = namespace.group("namespace").casefold() if namespace else "plain"
        shape = shape_namespace + ":" + ".".join("key" for _ in range(expression.count(KEY)))
        reason_words = [
            word.casefold()
            for word in re.findall(r"[A-Za-z_][A-Za-z0-9_#@-]*", role.group("suffix"))
            if word.casefold() not in {"key", "optional_key", "locator", "type"}
        ]
        return prefix_contract or "prefix:plain", role.group("role").casefold(), shape, *reason_words[:2]
    wrapper = PERSISTENT_WRAPPER_RE.match(masked)
    if wrapper is not None:
        focus = wrapper.group("inner")
    else:
        introductions = list(ERROR_INTRO_RE.finditer(masked))
        focus = masked[introductions[-1].end() :] if introductions else masked
        focus = QUOTED_VALUE_RE.sub(f" {KEY} ", focus)
    # Tokenize placeholders as whole units.  Filtering the bare word ``key``
    # would erase semantic phrases such as "Localization key" along with the
    # synthetic <KEY> slot marker.
    words = [
        token.casefold()
        for token in TOKEN_RE.findall(focus)
        if token not in {KEY, OPTIONAL_KEY, LOCATOR, TYPE}
        and token not in PUNCTUATION
        and re.search(r"[A-Za-z0-9]", token)
    ]
    lead = tuple(words[:2])
    return (prefix_contract, *lead) if prefix_contract is not None else lead


def reason_lead(tokens: Sequence[str]) -> tuple[str, ...]:
    slots = {KEY, OPTIONAL_KEY, LOCATOR, TYPE, "<VALUE>", "<PARAM>"}
    return tuple(
        token.casefold()
        for token in tokens
        if token not in PUNCTUATION and token not in slots
    )[:2]


class _Composer:
    """Apply the ported grammar while capturing values at the edit site."""

    def __init__(self, original=None):
        self.original = original
        self.values: list[OccurrenceValue] = []

    def capture(self, text: _Text) -> int:
        origins = text.native_origins()
        if self.original is None:
            value = text.text
        else:
            chunks = []
            for origin in origins:
                raw = self.original.read_bytes(origin.span)
                if len(raw) != origin.span.end - origin.span.start:
                    raise ValueError("incomplete original value read")
                chunks.append(raw)
            value = b"".join(chunks).decode("utf-8", "replace")
        self.values.append(OccurrenceValue(value, origins))
        return len(self.values) - 1

    def mask(self, text: _Text, token: str) -> _Text:
        if text.text == token and any(text.marks):
            return text
        index = self.capture(text)
        return _Text(token, (text.native_origins(),) * len(token),
                     (frozenset((index,)),) * len(token), text.anchor)

    def retain_structured(self, text: _Text) -> None:
        """Span-bearing counterpart of the R2 concrete slot extraction.

        These pre-edit values include identities otherwise swallowed by a
        rendered display or source mask. Field names remain grammar selectors.
        """
        rules = (
            (PDXMESH_SYNC_RE, ("mesh", "part")), (DECISION_INTERVAL_RE, ("key",)),
            (UNRECOGNIZED_LOC_KEY_RE, ("key",)), (EVENT_THEME_KEY_RE, ("theme", "event")),
            (ORPHAN_EVENT_RE, ("event",)), (QUEUED_EVENT_RE, ("event",)),
            (ARTIFACT_FEATURE_RE, ("display", "identity", "group")),
            (FAITH_SCOPE_RE, ("key",)), (POSTVALIDATE_EFFECT_RE, ("effect",)),
            (MATERIAL_SHADER_RE, ("shader", "mesh")),
            (LOCALIZATION_HASH_COLLISION_RE, ("left", "right", "hash")),
            (AUDIO_EVENT_INFO_RE, ("event",)), (PERSISTENT_UNEXPECTED_TOKEN_RE, ("token",)),
            (FLAVORIZATION_TITLE_RE, ("key",)), (SCRIPTED_EFFECT_DETAILS_RE, ("effect",)),
        )
        for pattern, groups in rules:
            match = pattern.match(text.text)
            if match is not None:
                for group in groups:
                    self.capture(text.cut(*match.span(group)).strip())
                if pattern is SCRIPTED_EFFECT_DETAILS_RE:
                    for character in RENDERED_CHARACTER_ID_RE.finditer(text.text):
                        self.capture(text.cut(*character.span("identity")))
                return
        match = ACTIVITY_EVENT_REFERENCE_RE.match(text.text) or TRAVEL_CHARACTER_REFERENCE_RE.search(text.text)
        if match is None:
            role = SCRIPT_SYSTEM_ROLE_RE.match(text.text)
            if role is None:
                return
            suffix = text.cut(*role.span("suffix")).strip()
            if not (suffix.text.startswith("[") and suffix.text.endswith("]")):
                return
            text = suffix.cut(1, len(suffix.text) - 1).strip()
            tributary = TRIBUTARY_REASON_RE.match(text.text)
            if tributary is not None:
                for prefix in ("first", "second", "third"):
                    for field in ("display", "title", "id", "history"):
                        span = tributary.span(f"{prefix}_{field}")
                        if span[0] >= 0:
                            self.capture(text.cut(*span).strip())
                return
            match = SCRIPT_TRAVEL_RE.match(text.text)
        if match is not None:
            if "event" in match.groupdict():
                self.capture(text.cut(*match.span("event")))
            display = text.cut(*match.span("display")).strip()
            ending = re.search(r"\s+of\s*$", display.text)
            self.capture(display.cut(0, ending.start()) if ending else display)
            self.capture(text.cut(*match.span("internal")).strip())
            if match.start("historical") >= 0:
                self.capture(text.cut(*match.span("historical")).strip())

    def recipe(self, text: _Text, match: re.Match[str], parts) -> _Text:
        anchor = text.cut(match.start())
        output = []
        for part in parts:
            if isinstance(part, str):
                output.append(anchor.literal(part))
            else:
                name = part[0]
                start, end = match.span(name)
                if start < 0:
                    # Absent historical IDs are inserted just before the
                    # closing identity envelope, never at another child's ID.
                    start = end = match.end("internal") if "internal" in match.groupdict() else match.start()
                piece = text.cut(start, end)
                output.append(self.mask(piece.strip(), part[1]) if len(part) == 2 else piece)
        return anchor.join(output)

    def known(self, text: _Text) -> _Text:
        rules = (
            (PDXMESH_SYNC_RE, (("prefix",), ("mesh", KEY), ("middle",), ("part", KEY), ("suffix",))),
            (DECISION_INTERVAL_RE, (("key", KEY), ("suffix",))),
            (UNRECOGNIZED_LOC_KEY_RE, (("prefix",), ("key", KEY), ". file: ", ("suffix", LOCATOR))),
            (EVENT_THEME_KEY_RE, (("prefix",), ("theme", KEY), ("middle",), ("event", KEY), ("suffix",))),
            (ORPHAN_EVENT_RE, (("prefix",), ("event", KEY), ("suffix",))),
            (QUEUED_EVENT_RE, (("prefix",), ("event", KEY), ("suffix",))),
            (ARTIFACT_FEATURE_RE, (("prefix",), "'", ("display", OPTIONAL_KEY), "' (", ("identity", KEY), ")", ("middle",), ("group", KEY))),
            (FAITH_SCOPE_RE, (("prefix",), "'", ("key", KEY), "'", ("suffix",))),
            (POSTVALIDATE_EFFECT_RE, (("prefix",), "'", ("effect", KEY), "'", ("suffix",))),
            (MATERIAL_SHADER_RE, (("prefix",), ("shader", OPTIONAL_KEY), ("middle",), ("mesh", KEY), ("suffix",))),
            (LOCALIZATION_HASH_COLLISION_RE, (("prefix",), "'", ("left", KEY), "'", ("middle",), "'", ("right", KEY), "'", ("suffix",), ("hash", PARAM), ("period",))),
            (AUDIO_EVENT_INFO_RE, (("prefix",), "'", ("event", KEY), "'", ("suffix",))),
        )
        for pattern, recipe in rules:
            match = pattern.match(text.text)
            if match is not None:
                return self.recipe(text, match, recipe)
        unexpected = PERSISTENT_UNEXPECTED_TOKEN_RE.match(text.text)
        if unexpected is not None:
            m = unexpected
            return text.join((
                text.cut(*m.span("prefix")), self.mask(text.cut(*m.span("token")).strip(), KEY),
                text.literal(", "), self.mask(text.cut(m.end("token"), m.start("file")), LOCATOR),
                text.cut(*m.span("file")), self.mask(text.cut(m.end("file"), m.start("tail")), LOCATOR),
                text.cut(*m.span("tail")), self.mask(text.cut(m.end("tail"), m.end()), LOCATOR),
            ))
        text = text.sub(SCRIPTED_EFFECT_SOURCE_RE,
                        lambda t, m: t.join((self.mask(t.cut(*m.span()), LOCATOR), t.literal(" "))), count=1)

        def rendered(t, m):
            remainder = t.cut(m.end("prefix"), m.end())
            # Retain the concrete character ID independently of its rendered
            # display (the latter is what this grammar masks).
            for identity in RENDERED_CHARACTER_ID_RE.finditer(remainder.text):
                self.capture(remainder.cut(*identity.span("identity")))
            return t.join((t.cut(*m.span("prefix")), self.mask(remainder, KEY), t.literal(" ")))

        text = text.sub(RENDERED_CHARACTER_RE, rendered).strip()
        prefix_length = len(LOCATOR) + 1 if text.text.startswith(LOCATOR + " ") else 0
        body = text.cut(prefix_length)
        match = SCRIPTED_EFFECT_KEY_RE.match(body.text)
        if match is not None:
            return text.join((text.cut(0, prefix_length), self.recipe(body, match,
                (("effect", KEY), ("separator",), ("scope", TYPE), ("suffix",)))))
        return text

    def key_path(self, text: _Text) -> _Text:
        text = text.strip()
        if KEY in text.text:
            return text
        namespace = KEY_PATH_NAMESPACE_RE.match(text.text)
        prefix = text.cut(0, 0)
        if namespace is not None:
            prefix = text.join((text.cut(*namespace.span("namespace")), text.literal(":")))
            text = text.cut(*namespace.span("path")).strip()
        segments = list(re.finditer(r"[^.]+|(?<=\.)(?=\.)", text.text))
        if not text.text or not all(KEY_PATH_SEGMENT_RE.fullmatch(s.strip()) for s in text.text.split(".")):
            return text  # Same invalid-namespace behavior as the authorized port.
        output = [prefix]
        for index, segment in enumerate(segments):
            if index:
                output.append(text.literal("."))
            output.append(self.mask(text.cut(*segment.span()).strip(), KEY))
        return text.join(output)

    def structured(self, text: _Text) -> _Text:
        travel_recipe = (("prefix",), ("display", KEY), " ( ", ("internal", KEY), " ",
                         ("historical", OPTIONAL_KEY), " )", ("suffix",))
        activity_recipe = (("prefix",), "'", ("event", KEY), "'", ("character_prefix",),
                           ("display", KEY), " ( ", ("internal", KEY), " ",
                           ("historical", OPTIONAL_KEY), " )", ("suffix",))
        text = text.sub(TRAVEL_CHARACTER_REFERENCE_RE, lambda t, m: self.recipe(t, m, travel_recipe))
        text = text.sub(ACTIVITY_EVENT_REFERENCE_RE, lambda t, m: self.recipe(t, m, activity_recipe))
        role = SCRIPT_SYSTEM_ROLE_RE.match(text.text)
        if role is not None:
            suffix = text.cut(*role.span("suffix"))
            stripped = suffix.strip()
            if stripped.text.startswith("[") and stripped.text.endswith("]"):
                reason = stripped.cut(1, len(stripped.text) - 1).strip()
                travel = SCRIPT_TRAVEL_RE.match(reason.text)
                tributary = TRIBUTARY_REASON_RE.match(reason.text)
                if travel is not None:
                    reason = self.recipe(reason, travel, (("display", KEY), " ( ", ("internal", KEY),
                        " ", ("historical", OPTIONAL_KEY), " )'s travel plan have no valid destinations"))
                elif tributary is not None:
                    parts = [reason.literal("Tried to make '")]
                    for index, prefix in enumerate(("first", "second", "third")):
                        for field, token, trailing in (("display", KEY, " of "), ("title", KEY, " ( "),
                                                       ("id", KEY, " "), ("history", OPTIONAL_KEY, " )")):
                            start, end = tributary.span(f"{prefix}_{field}")
                            if start < 0:
                                start = end = tributary.end(f"{prefix}_id")
                            parts.extend((self.mask(reason.cut(start, end).strip(), token), reason.literal(trailing)))
                        if index < 2:
                            parts.append(reason.literal("' a Tributary contract with Suzerain '" if index == 0
                                                        else "', but they are already a vassal of "))
                    reason = reason.join(parts)
                suffix = suffix.join((suffix.literal(" [ "), reason, suffix.literal(" ]")))
            text = text.join((text.cut(*role.span("prefix")), self.key_path(text.cut(*role.span("expression"))),
                              text.literal(" "), text.cut(*role.span("role")), suffix))

        def comparison(t, m):
            return t.join((t.cut(*m.span("prefix")), t.literal("'"),
                self.mask(t.cut(m.end("prefix") + 1, m.start("middle") - 1), KEY), t.literal("'"),
                t.cut(*m.span("middle")), t.literal("'"),
                self.mask(t.cut(m.end("middle") + 1, m.start("suffix") - 1), KEY), t.literal("'"),
                t.cut(*m.span("suffix"))))

        text = text.sub(COMPARISON_TYPE_MISMATCH_RE, comparison)
        description = TRIGGER_DESCRIPTION_RE.match(text.text)
        if description is not None:
            m = description
            text = text.join((self.mask(text.cut(*m.span("key")), KEY), text.literal(": "),
                              text.cut(*m.span("body")), text.literal(" at file: "),
                              self.mask(text.cut(m.end("body"), m.end()), LOCATOR)))
        flavor = FLAVORIZATION_TITLE_RE.match(text.text)
        if flavor is not None:
            text = self.recipe(text, flavor, (("prefix",), ("key", OPTIONAL_KEY)))
        return self.known(text)

    def locators(self, text: _Text) -> _Text:
        for pattern in (WINDOWS_PATH_RE, QUOTED_PATH_RE, RELATIVE_PATH_RE, FILENAME_RE, LINE_LOCATOR_RE):
            text = text.sub(pattern, lambda t, m: self.mask(t.cut(*m.span()), LOCATOR))
        return text

    def persistent(self, text: _Text) -> _Text:
        def remove(t, m):
            self.capture(t.cut(*m.span()))
            return t.cut(m.start(), m.start())
        text = text.sub(PERSISTENT_NEAR_LINE_RE, remove).strip(" ,")
        unknown = UNKNOWN_TRIGGER_KEY_RE.match(text.text)
        if unknown is not None:
            return self.recipe(text, unknown, (("prefix",), ("key", KEY)))
        failed = FAILED_KEY_REFERENCE_RE.match(text.text)
        if failed is not None:
            return self.recipe(text, failed, (("prefix",), ("left", KEY), " : ", ("right", KEY)))
        return text


def _plain(text: str) -> _Text:
    return _decode_text(text.encode("utf-8"), 0)


def block_message(raw_block: str) -> str:
    """Flatten native header/continuation text for grammar-only consumers."""
    first = raw_block.removeprefix("\ufeff")
    return re.sub(r"\s+", " ", HEADER_RE.sub("", first, count=1)).strip()


def split_location_evidence(text: str) -> tuple[str, str | None]:
    match = SCRIPT_LOCATION_TAIL_RE.search(text)
    if match is None:
        return text.strip(), None
    return text[:match.start()].rstrip(), text[match.end():].strip() or None


def normalize_structured_slots(text: str) -> str:
    return _Composer().structured(_plain(text)).text


def normalize_known_key_grammars(text: str) -> str:
    return _Composer().known(_plain(text)).text


def mask_locators(text: str) -> str:
    return _Composer().locators(_plain(text)).text


def tokenize(text: str) -> tuple[str, ...]:
    """The full ported token stream; adjacent locators still coalesce."""
    semantic, _ = split_location_evidence(text)
    masked = mask_locators(normalize_structured_slots(semantic))
    result = []
    for token in TOKEN_RE.findall(masked):
        if token != LOCATOR or not result or result[-1] != LOCATOR:
            result.append(token)
    return tuple(result)


def normalize_for_match(diagnostic: RecoveredDiagnostic) -> NormalizedView:
    """Normalize a recovered child, retaining every edit's concrete value.

    Values removed from matching have token_span=None. All matching tokens also
    have exact original values, permitting learned literal/alternative slots.
    Values/locator facts in the shared envelope never include sibling clauses.
    """
    from .bindings import extract_locators

    composer = _Composer(diagnostic.parent.original)
    composer.values.extend(diagnostic.values)
    text = _diagnostic_text(diagnostic)
    composer.retain_structured(text)
    # Extract locators from original local/shared evidence before any masks.
    for locator in extract_locators(diagnostic):
        composer.values.append(locator.value)
        if locator.line_value is not None:
            composer.values.append(locator.line_value)
    tail = SCRIPT_LOCATION_TAIL_RE.search(text.text)
    if tail is not None:
        composer.capture(text.cut(tail.start()))
        text = text.cut(0, tail.start()).strip()
    if (diagnostic.parent.source_family.casefold() == "pdx_persistent_reader.cpp"
            and _is_recovered_clause(diagnostic, text.text)):
        text = composer.persistent(text)
    text = composer.locators(composer.structured(text))
    tokens: list[MatchingToken] = []
    positions: dict[int, list[int]] = {}
    for match in TOKEN_RE.finditer(text.text):
        piece = text.cut(*match.span())
        token = MatchingToken(piece.text, piece.native_origins())
        if token.text == LOCATOR and tokens and tokens[-1].text == LOCATOR:
            index = len(tokens) - 1
            tokens[-1] = MatchingToken(LOCATOR, _coalesce((*tokens[-1].origins, *token.origins)))
        else:
            index = len(tokens)
            tokens.append(token)
        marks = frozenset(mark for marks in piece.marks for mark in marks)
        if not marks:
            marks = frozenset((composer.capture(piece),))
        for mark in marks:
            positions.setdefault(mark, []).append(index)
    # Pre-edit extracted subvalues (e.g. an unquoted path inside a masked
    # locator, or a character ID inside a rendered display) inherit the
    # containing token positions through origins, without searching text.
    for i, value in enumerate(composer.values):
        if i in positions or not any(o.span.start < o.span.end for o in value.origins):
            continue
        candidates = []
        covered = []
        for index, token in enumerate(tokens):
            hits = [origin for origin in value.origins if any(
                token_origin.scope == origin.scope and token_origin.span.contains(origin.span)
                for token_origin in token.origins)]
            if hits:
                candidates.append(index)
                covered.extend(hits)
        if all(origin in covered for origin in value.origins):
            positions[i] = candidates
    values = tuple(NormalizedValue(value, TokenSpan(min(positions[i]), max(positions[i]) + 1)
                                   if i in positions else None)
                   for i, value in enumerate(composer.values))
    return NormalizedView(diagnostic, NORMALIZER_REVISION, tuple(tokens), values)


def _is_recovered_clause(diagnostic: RecoveredDiagnostic, text: str) -> bool:
    # The native wrapper lives in shared evidence only for recovered clauses.
    # An unwrapped Unknown-trigger emission must retain ordinary R2 behavior.
    if not (UNKNOWN_TRIGGER_KEY_RE.match(text) or FAILED_KEY_REFERENCE_RE.match(text)):
        return False
    for span in diagnostic.shared_spans:
        raw = diagnostic.parent.original.read_bytes(span)
        if re.search(rb'Error\s*:\s*"', raw, re.IGNORECASE):
            return True
    return False
