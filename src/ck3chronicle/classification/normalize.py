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
KEY_PATH_NAMESPACE_RE = re.compile(
    r"^(?P<namespace>scope|var|cp|title)\s*:\s*(?P<path>.+)$", re.IGNORECASE
)
KEY_PATH_SEGMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_#@-]*$")
PUNCTUATION = frozenset("'\"`()[]{}:;,.!?/\\")


def split_location_evidence(text: str) -> tuple[str, str | None]:
    match = SCRIPT_LOCATION_TAIL_RE.search(text)
    if match is None:
        return text.strip(), None
    return text[: match.start()].rstrip(), text[match.end() :].strip() or None


def extract_structured_slots(text: str) -> tuple[dict[str, object], ...]:
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
    return (
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
    match = SCRIPT_SYSTEM_ROLE_RE.match(text)
    if match is None:
        return text
    suffix = match.group("suffix")
    stripped = suffix.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        reason = stripped[1:-1].strip()
        if SCRIPT_TRAVEL_RE.match(reason) is not None:
            reason = f"{KEY} ( {KEY} {OPTIONAL_KEY} )'s travel plan have no valid destinations"
        suffix = f" [ {reason} ]"
    return (
        match.group("prefix")
        + normalize_key_path(match.group("expression"))
        + " "
        + match.group("role")
        + suffix
    )


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
        close_index = len(tokens) - 1 - tuple(reversed(tokens)).index("]")
    except ValueError:
        return None
    if close_index <= open_index + 1 or open_index == 0:
        return None
    outer = tuple(tokens[:open_index])
    if outer[-1].casefold() not in {"trigger", "effect"}:
        return None
    return outer, tuple(tokens[open_index + 1 : close_index])


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
    focus = re.sub(r"(['\"])(?:\\.|(?!\1).)*\1", f" {KEY} ", masked)
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
    return tuple(words[:2])


def reason_lead(tokens: Sequence[str]) -> tuple[str, ...]:
    slots = {KEY, OPTIONAL_KEY, LOCATOR, TYPE, "<VALUE>", "<PARAM>"}
    return tuple(
        token.casefold()
        for token in tokens
        if token not in PUNCTUATION and token not in slots
    )[:2]
