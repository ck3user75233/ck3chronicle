"""Independent minimal model and human-approved classification examples.

This fixture is not learner output. Its five contracts were written directly
from the takeover product contract and the user's L1/L2/key decisions. Cluster
IDs were independently calculated from source family plus literal template
tokens with Windows cryptography APIs.
"""
from __future__ import annotations

import json
from pathlib import Path


SOURCE = "jomini_script_system.cpp"


def _cluster(
    cluster_id: str,
    source_family: str,
    medoid: str,
    semantic_lead: list[str],
    template_tokens: list[str],
    *,
    layer_contracts: dict | None = None,
) -> dict:
    return {
        "cluster_id": cluster_id,
        "source_family": source_family,
        "medoid": medoid,
        "semantic_lead": semantic_lead,
        "template": " ".join(template_tokens),
        "template_tokens": template_tokens,
        "support_occurrences": 2,
        "support_evidence_count": 2,
        "support_evidence_ids": ["training-a", "training-b"],
        "unique_sequences": 1,
        "examples": [medoid],
        "location_evidence_examples": [],
        "structured_slot_examples": [],
        "layer_contracts": layer_contracts,
    }


PLAIN_FAILED = [
    "Script", "system", "error", "!", "Error", ":", "<KEY>", "trigger",
    "[", "Failed", "context", "switch", "]",
]
SCOPE_FAILED = [
    "Script", "system", "error", "!", "Error", ":", "scope", ":",
    "<KEY>", ".", "<KEY>", "trigger", "[", "Failed", "context", "switch", "]",
]
PLAIN_WRONG_SCOPE = [
    "Script", "system", "error", "!", "Error", ":", "<KEY>", "trigger",
    "[", "Wrong", "scope", "for", "trigger", ":", "character", ",",
    "expected", "culture", "]",
]
TRAVEL = [
    "Script", "system", "error", "!", "Error", ":", "<KEY>", "effect", "[",
    "<KEY>", "(", "<KEY>", "<OPTIONAL_KEY>", ")", "'", "s", "travel",
    "plan", "have", "no", "valid", "destinations", "]",
]
LOCALIZATION = [
    "Localization", "key", "'", "<KEY>", "'", "is", "defined", "in", "both",
    "<LOCATOR>", "and", "<LOCATOR>",
]


MODEL = {
    "schema": "ck3chronicle-empirical-template-calibration",
    "schema_version": 3,
    "revision": {
        "revision_id": "reboot-test-model",
        "normalizer_version": "ck3-empirical-template-normalizer-v4.6",
        "clusterer_version": "ordered-token-clusterer-v4-bounded-script-layers",
        "threshold": 0.72,
        "training_sha256": ["training-a", "training-b"],
    },
    "algorithm": {
        "cluster_threshold": 0.72,
        "normalizer_version": "ck3-empirical-template-normalizer-v4.6",
        "clusterer_version": "ordered-token-clusterer-v4-bounded-script-layers",
    },
    "summary": {"distinct_error_logs": 2, "clusters": 5},
    "clusters": [
        _cluster(
            "fc12b3d364faee03",
            "pdx_localize.cpp",
            "Localization key 'Rome' is defined in both 'localization/english/a.yml' and 'localization/english/b.yml'",
            ["localization", "key"],
            LOCALIZATION,
        ),
        _cluster(
            "33824ae4410d9837",
            SOURCE,
            "Script system error! Error: check_scope trigger [ Failed context switch ]",
            ["prefix:plain", "trigger", "plain:key", "failed", "context"],
            PLAIN_FAILED,
            layer_contracts={
                "l1_outer_template": "Script system error ! Error : <KEY> trigger",
                "l1_outer_tokens": PLAIN_FAILED[:8],
                "l2_reason_template": "Failed context switch",
                "l2_reason_tokens": ["Failed", "context", "switch"],
            },
        ),
        _cluster(
            "1ca3d0b7aefad729",
            SOURCE,
            "Script system error! Error: scope:actor.target trigger [ Failed context switch ]",
            ["prefix:plain", "trigger", "scope:key.key", "failed", "context"],
            SCOPE_FAILED,
            layer_contracts={
                "l1_outer_template": "Script system error ! Error : scope : <KEY> . <KEY> trigger",
                "l1_outer_tokens": SCOPE_FAILED[:12],
                "l2_reason_template": "Failed context switch",
                "l2_reason_tokens": ["Failed", "context", "switch"],
            },
        ),
        _cluster(
            "7040da88e42f3501",
            SOURCE,
            "Script system error! Error: has_flag trigger [ Wrong scope for trigger: character, expected culture ]",
            ["prefix:plain", "trigger", "plain:key", "wrong", "scope"],
            PLAIN_WRONG_SCOPE,
            layer_contracts={
                "l1_outer_template": "Script system error ! Error : <KEY> trigger",
                "l1_outer_tokens": PLAIN_WRONG_SCOPE[:8],
                "l2_reason_template": "Wrong scope for trigger : character , expected culture",
                "l2_reason_tokens": [
                    "Wrong", "scope", "for", "trigger", ":", "character", ",",
                    "expected", "culture",
                ],
            },
        ),
        _cluster(
            "63c6f785dd9cbc48",
            SOURCE,
            "Script system error! Error: cancel_travel effect [ Aethelred of k_england (Internal ID: 77 - Historical ID old_77)'s travel plan have no valid destinations ]",
            ["prefix:plain", "effect", "plain:key", "s", "travel"],
            TRAVEL,
            layer_contracts={
                "l1_outer_template": "Script system error ! Error : <KEY> effect",
                "l1_outer_tokens": TRAVEL[:8],
                "l2_reason_template": "<KEY> ( <KEY> <OPTIONAL_KEY> ) ' s travel plan have no valid destinations",
                "l2_reason_tokens": TRAVEL[9:-1],
            },
        ),
    ],
}


def write_model(path: Path) -> None:
    path.write_text(
        json.dumps(MODEL, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
