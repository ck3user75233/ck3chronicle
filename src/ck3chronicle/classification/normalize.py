"""Deterministic CK3 diagnostic normalization used by inference.

Only empirically approved transformations live here. Symbol suffixes such as
``*_effect`` never discover a template; they can be checked only after a
contract has been assigned.
"""

from __future__ import annotations

import re
from typing import Sequence


LOCATOR = "<LOCATOR>"
KEY = "<KEY>"
OPTIONAL_KEY = "<OPTIONAL_KEY>"
TYPE = "<TYPE>"
PARAM = "<PARAM>"
VALUE = "<VALUE>"
TRUNCATED_REASON = "<TRUNCATED_REASON>"

HEADER_RE = re.compile(
    r"^\[\d{2}:\d{2}:\d{2}\](?:\[[^\]]+\])?\[[^\]]+\]:\s*"
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


def block_message(raw_block: str) -> str:
    """Remove the timestamp header and join one stored source block."""
    lines = raw_block.splitlines()
    if not lines:
        return ""
    first_line = lines[0]
    if first_line.startswith("\ufeff"):
        first_line = first_line[1:]
    header = HEADER_RE.sub("", first_line, count=1).strip()
    continuations = [line.strip() for line in lines[1:] if line.strip()]
    return re.sub(r"\s+", " ", " ".join([header, *continuations])).strip()


def split_location_evidence(text: str) -> tuple[str, str | None]:
    match = SCRIPT_LOCATION_TAIL_RE.search(text)
    if match is None:
        return text.strip(), None
    return text[: match.start()].rstrip(), text[match.end() :].strip() or None


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


def normalize_structured_slots(text: str) -> str:
    def replace_travel_character(match: re.Match[str]) -> str:
        return (
            match.group("prefix")
            + f"{KEY} ( {KEY} {OPTIONAL_KEY} )"
            + match.group("suffix")
        )

    def replace_activity(match: re.Match[str]) -> str:
        return (
            match.group("prefix")
            + f"'{KEY}'"
            + match.group("character_prefix")
            + f"{KEY} ( {KEY} {OPTIONAL_KEY} )"
            + match.group("suffix")
        )

    def replace_comparison(match: re.Match[str]) -> str:
        return (
            match.group("prefix")
            + f"'{KEY}'"
            + match.group("middle")
            + f"'{KEY}'"
            + match.group("suffix")
        )

    normalized = TRAVEL_CHARACTER_REFERENCE_RE.sub(replace_travel_character, text)
    normalized = ACTIVITY_EVENT_REFERENCE_RE.sub(replace_activity, normalized)
    match = SCRIPT_SYSTEM_ROLE_RE.match(normalized)
    if match is not None:
        suffix = match.group("suffix")
        stripped = suffix.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            reason = stripped[1:-1].strip()
            if SCRIPT_TRAVEL_RE.match(reason) is not None:
                reason = f"{KEY} ( {KEY} {OPTIONAL_KEY} )'s travel plan have no valid destinations"
            if TRIBUTARY_REASON_RE.match(reason) is not None:
                reason = (
                    f"Tried to make '{KEY} of {KEY} ( {KEY} {OPTIONAL_KEY} )' a "
                    f"Tributary contract with Suzerain '{KEY} of {KEY} ( {KEY} "
                    f"{OPTIONAL_KEY} )', but they are already a vassal of {KEY} of "
                    f"{KEY} ( {KEY} {OPTIONAL_KEY} )"
                )
            suffix = f" [ {reason} ]"
        normalized = (
            match.group("prefix")
            + normalize_key_path(match.group("expression"))
            + " "
            + match.group("role")
            + suffix
        )
    normalized = COMPARISON_TYPE_MISMATCH_RE.sub(replace_comparison, normalized)
    trigger_description = TRIGGER_DESCRIPTION_RE.match(normalized)
    if trigger_description is not None:
        normalized = (
            f"{KEY}: {trigger_description.group('body')} at file: {LOCATOR}"
        )
    flavorization = FLAVORIZATION_TITLE_RE.match(normalized)
    if flavorization is not None:
        normalized = flavorization.group("prefix") + OPTIONAL_KEY
    normalized = normalize_known_key_grammars(normalized)
    return normalized


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
        # Everything after the period is source location evidence.  CK3 emits
        # equivalent ``file``/``Near file`` spellings and sometimes names a
        # runtime descriptor instead of a filesystem path; none changes the
        # missing-localization-key contract.
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


def _normalize_persistent_clause(text: str) -> str:
    clause = PERSISTENT_NEAR_LINE_RE.sub("", text).strip(" ,")
    unknown = UNKNOWN_TRIGGER_KEY_RE.match(clause)
    if unknown is not None:
        return unknown.group("prefix") + KEY
    failed = FAILED_KEY_REFERENCE_RE.match(clause)
    if failed is not None:
        return failed.group("prefix") + f"{KEY} : {KEY}"
    return clause


def semantic_units(source_family: str, message: str) -> tuple[str, ...]:
    """Expand repeated clauses into occurrences without changing template ID."""
    if source_family.casefold() == "pdx_persistent_reader.cpp":
        wrapper = PERSISTENT_WRAPPER_RE.match(message)
        if wrapper is not None:
            inner = wrapper.group("inner")
            starts = list(PERSISTENT_CLAUSE_START_RE.finditer(inner))
            if starts:
                units: list[str] = []
                for index, start in enumerate(starts):
                    end = starts[index + 1].start() if index + 1 < len(starts) else len(inner)
                    unit = _normalize_persistent_clause(inner[start.start() : end])
                    if unit:
                        units.append(unit)
                if units:
                    return tuple(units)
    semantic, _ = split_location_evidence(message)
    return (normalize_structured_slots(semantic),) if semantic else ()


def mask_locators(text: str) -> str:
    text = WINDOWS_PATH_RE.sub(LOCATOR, text)
    text = QUOTED_PATH_RE.sub(LOCATOR, text)
    text = RELATIVE_PATH_RE.sub(LOCATOR, text)
    text = FILENAME_RE.sub(LOCATOR, text)
    return LINE_LOCATOR_RE.sub(LOCATOR, text)


def tokenize(text: str) -> tuple[str, ...]:
    semantic, _ = split_location_evidence(text)
    masked = mask_locators(normalize_structured_slots(semantic))
    result: list[str] = []
    for token in TOKEN_RE.findall(masked)[:384]:
        if token == LOCATOR and result and result[-1] == LOCATOR:
            continue
        result.append(token)
    return tuple(result)


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


def legacy_diagnostic_lead(text: str) -> tuple[str, ...]:
    """Return the v4.6 model's historical lead for compatibility.

    v4.6 generated generic lead words by removing the bare words ``key``,
    ``locator``, and ``type`` after quote masking.  That made the index less
    semantically precise, but it did not remove those literals from template
    tokens or identity.  The frozen model contains those historical leads, so
    inference accepts them alongside the corrected lead until a newly trained
    model revision replaces v4.6.
    """
    semantic, _ = split_location_evidence(text)
    masked = mask_locators(normalize_structured_slots(semantic))
    prefix = SCRIPT_SYSTEM_PREFIX_RE.match(masked)
    prefix_contract: str | None = None
    if prefix is not None:
        context = prefix.group("context") or ""
        context_words = [
            word.casefold()
            for word in re.findall(r"[A-Za-z_][A-Za-z0-9_#@-]*", context)
        ]
        prefix_contract = "prefix:" + (
            "_".join(context_words) if context_words else "plain"
        )
    if SCRIPT_SYSTEM_ROLE_RE.match(masked) is not None:
        return diagnostic_lead(text)
    wrapper = PERSISTENT_WRAPPER_RE.match(masked)
    if wrapper is not None:
        focus = wrapper.group("inner")
    else:
        introductions = list(ERROR_INTRO_RE.finditer(masked))
        focus = masked[introductions[-1].end() :] if introductions else masked
        focus = QUOTED_VALUE_RE.sub(f" {KEY} ", focus)
    words = [
        token.casefold()
        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_#@-]*", focus)
        if token.casefold() not in {"key", "optional_key", "locator", "type"}
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
