from __future__ import annotations

import hashlib
import re

from .models import Confidence, Severity

VOLATILE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bline:\s*\d+\b", re.I), "line:<N>"),
    (re.compile(r"\bline\s+\d+\b", re.I), "line <N>"),
    (re.compile(r"\bnear line:\s*\d+\b", re.I), "near line:<N>"),
    (re.compile(r"\bcolumn:\s*\d+\b", re.I), "column:<N>"),
    (re.compile(r"\bInternal ID:?\s*-?\d+\b", re.I), "Internal ID:<ID>"),
    (re.compile(r"\bHistorical ID\s+[A-Za-z0-9_\-]+\b", re.I), "Historical ID:<ID>"),
    (re.compile(r"\bCharacter\s*-\s*-?\d+\b", re.I), "Character-<ID>"),
    (re.compile(r"\bCulture\s*-\s*-?\d+\b", re.I), "Culture-<ID>"),
    (re.compile(r"\bAccolade\s*-\s*-?\d+\b", re.I), "Accolade-<ID>"),
    (re.compile(r"\bTask_contract\s*-\s*-?\d+\b", re.I), "Task_contract-<ID>"),
    (re.compile(r"\bargs#\d+\b", re.I), "args#<ID>"),
    (re.compile(r"\bhash#\d+\b", re.I), "hash#<ID>"),
    (re.compile(r"0x[a-fA-F0-9]+"), "<HEX>"),
]

CLASSIFIERS: list[tuple[str, Severity, Confidence, re.Pattern[str]]] = [
    ("Syntax / Structural", "Fatal", "High", re.compile(r"Unexpected token|Failed to read key reference|Invalid date string|unbalanced brace|Error parsing", re.I)),
    ("Scope Mismatch", "High", "High", re.compile(r"Wrong scope|Inconsistent .* scopes|expected character|expected title|expected province|scope type", re.I)),
    ("Script Execution", "High", "High", re.compile(r"Script system error|PostValidate|Failed context switch|Scoped object.*not valid|returned an unset scope|Failed to fetch", re.I)),
    ("Missing Reference", "High", "High", re.compile(r"Unknown trigger|Unknown effect|Invalid database object|Cannot find|not found|does not exist|Undefined event target|Failed to find", re.I)),
    ("Localization", "Low", "High", re.compile(r"Duplicate localization key|missing localization|Unrecognized loc key|Unknown loc key|hash collision|Unlocalized text|Key is missing localization", re.I)),
    ("Asset / Graphics", "Low", "Medium", re.compile(r"Duplicate texture|pdxmesh|mesh|DDS|mipmap|3d-type|material|shader|texture streaming|type_icon|icon .*doesn.t exist", re.I)),
    ("GUI / Interface", "Medium", "Medium", re.compile(r"gui/|Widget cannot|animation|data property|pdx_gui", re.I)),
    ("Mod Descriptor / Metadata", "Low", "High", re.compile(r"Invalid supported_version|descriptor", re.I)),
    ("Database Conflict", "Medium", "Medium", re.compile(r"database_conflicts|defined multiple times|only one version will be loaded|overridden", re.I)),
    ("Engine / System", "Low", "Medium", re.compile(r"audio|FMOD|travel plan|succession order|AI tried", re.I)),
]


def raw_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def normalize_text(text: str) -> str:
    result = text
    for pattern, replacement in VOLATILE_PATTERNS:
        result = pattern.sub(replacement, result)
    result = re.sub(r"[ \t]+", " ", result)
    return result.strip()


def normalized_signature(text: str) -> str:
    return raw_hash(normalize_text(text))


def classify_issue(text: str) -> tuple[str, Severity, Confidence]:
    for category, severity, confidence, pattern in CLASSIFIERS:
        if pattern.search(text):
            return category, severity, confidence
    return "Unclassified", "Unknown", "Low"
