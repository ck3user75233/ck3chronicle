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
    r"(?:\s*(?:-|to)\s*\d+)?\b",
    re.IGNORECASE,
)
TOKEN_RE = re.compile(
    r"<OPTIONAL_KEY>|<LOCATOR>|<TYPE>|<KEY>|[A-Za-z_][A-Za-z0-9_#@-]*|"
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
    r"title\s+)(?P<key>[^\s]+)\s*$",
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
    activity = ACTIVITY_EVENT_REFERENCE_RE.match(text)
    match = activity or TRAVEL_CHARACTER_REFERENCE_RE.search(text)
    if match is None:
        role = SCRIPT_SYSTEM_ROLE_RE.match(text)
        if role is None:
            return ()
        suffix = role.group("suffix").strip()
        if not (suffix.startswith("[") and suffix.endswith("]")):
            return ()
        match = SCRIPT_TRAVEL_RE.match(suffix[1:-1].strip())
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
        normalized = flavorization.group("prefix") + KEY
    return normalized


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
