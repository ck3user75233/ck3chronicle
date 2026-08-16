"""Independent contracts for empirical-template to canonical projection.

All diagnostics in this module are invented.  They encode grammar invariants,
not rows, IDs, hashes, or concrete values from an evaluation corpus.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from ck3chronicle.classification.inference import ClassificationResult, Classifier
from ck3chronicle.classification.model import (
    CLUSTERER_VERSION,
    MODEL_SCHEMA,
    MODEL_SCHEMA_VERSION,
    NORMALIZER_VERSION,
    load_model,
)
from ck3chronicle.classification.normalize import KEY, diagnostic_lead, tokenize
from ck3chronicle.classification.projection_catalog import (
    PROJECTION_SCHEMA,
    PROJECTION_SCHEMA_VERSION,
    ProjectionCatalog,
    ProjectionCatalogIntegrityError,
    composed_contract_id_for,
    contract_id_for,
    load_projection_catalog,
)
from ck3chronicle.parser.log_blocks import TimestampedLogBlock
from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.normalize import normalize as normalize_issue
from ck3chronicle.semantic_projection import (
    SemanticProjectionError,
    analyze_complete_message,
    project_issue,
    project_normalized_issue,
)


SOURCE_FAMILY = "invented_semantics.cpp"
MEDOID = "Widget symbol 'amber_widget' cannot be resolved"
TEMPLATE_TOKENS = (
    "Widget",
    "symbol",
    "'",
    KEY,
    "'",
    "cannot",
    "be",
    "resolved",
)
CONTRACT_ID = contract_id_for(SOURCE_FAMILY, TEMPLATE_TOKENS)
MODEL_REVISION = "invented-projection-model-v1"


def _write_model(path: Path) -> str:
    model = {
        "schema": MODEL_SCHEMA,
        "schema_version": MODEL_SCHEMA_VERSION,
        "revision": {
            "revision_id": MODEL_REVISION,
            "normalizer_version": NORMALIZER_VERSION,
            "clusterer_version": CLUSTERER_VERSION,
            "threshold": 0.72,
        },
        "algorithm": {
            "normalizer_version": NORMALIZER_VERSION,
            "clusterer_version": CLUSTERER_VERSION,
            "cluster_threshold": 0.72,
        },
        "clusters": [
            {
                "cluster_id": CONTRACT_ID,
                "source_family": SOURCE_FAMILY,
                "medoid": MEDOID,
                "semantic_lead": list(diagnostic_lead(MEDOID)),
                "template_tokens": list(TEMPLATE_TOKENS),
                "support_occurrences": 3,
                "support_evidence_count": 2,
            }
        ],
    }
    path.write_text(
        json.dumps(model, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_catalog(path: Path, model_sha256: str) -> str:
    catalog = {
        "schema": PROJECTION_SCHEMA,
        "schema_version": PROJECTION_SCHEMA_VERSION,
        "revision_id": "invented-projection-catalog-v1",
        "model_revision_id": MODEL_REVISION,
        "model_sha256": model_sha256,
        "projections": [
            {
                "contract_id": CONTRACT_ID,
                "contract_kind": "model_full",
                "source_family": SOURCE_FAMILY,
                "accounting": "classified",
                "category": "symbol_resolution",
                "error_type": "undefined_symbol",
                "tags": ["invented"],
                "confidence_by_assignment": {"full": "high"},
                "primary_locator_ordinal": 1,
                "slot_projections": [
                    {
                        "role": "key",
                        "ordinal": 1,
                        "target": "referenced_symbol",
                    }
                ],
            }
        ],
    }
    path.write_text(
        json.dumps(catalog, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _custom_projection_runtime(
    tmp_path: Path,
    *,
    source_family: str,
    message: str,
    template_tokens: tuple[str, ...],
    reference_projections: list[dict[str, object]],
    primary_locator_ordinal: int | None = None,
) -> tuple[Classifier, ProjectionCatalog, str]:
    """Build one invented, hash-bound model/catalog pair for a grammar test."""
    contract_id = contract_id_for(source_family, template_tokens)
    model_path = tmp_path / "custom-model.json"
    model = {
        "schema": MODEL_SCHEMA,
        "schema_version": MODEL_SCHEMA_VERSION,
        "revision": {
            "revision_id": MODEL_REVISION,
            "normalizer_version": NORMALIZER_VERSION,
            "clusterer_version": CLUSTERER_VERSION,
            "threshold": 0.72,
        },
        "algorithm": {
            "normalizer_version": NORMALIZER_VERSION,
            "clusterer_version": CLUSTERER_VERSION,
            "cluster_threshold": 0.72,
        },
        "clusters": [
            {
                "cluster_id": contract_id,
                "source_family": source_family,
                "medoid": message,
                "semantic_lead": list(diagnostic_lead(message)),
                "template_tokens": list(template_tokens),
                "support_occurrences": 2,
                "support_evidence_count": 2,
            }
        ],
    }
    model_path.write_text(
        json.dumps(model, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    model_sha256 = hashlib.sha256(model_path.read_bytes()).hexdigest()
    loaded_model = load_model(model_path, expected_sha256=model_sha256)

    catalog_path = tmp_path / "custom-catalog.json"
    catalog = {
        "schema": PROJECTION_SCHEMA,
        "schema_version": PROJECTION_SCHEMA_VERSION,
        "revision_id": "invented-custom-catalog-v1",
        "model_revision_id": MODEL_REVISION,
        "model_sha256": model_sha256,
        "projections": [
            {
                "contract_id": contract_id,
                "contract_kind": "model_full",
                "source_family": source_family,
                "accounting": "classified",
                "category": "script_system",
                "error_type": "invented_failure",
                "tags": ["invented"],
                "confidence_by_assignment": {"full": "high"},
                "primary_locator_ordinal": primary_locator_ordinal,
                "slot_projections": [],
                "reference_projections": reference_projections,
            }
        ],
    }
    catalog_path.write_text(
        json.dumps(catalog, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    catalog_sha256 = hashlib.sha256(catalog_path.read_bytes()).hexdigest()
    loaded_catalog = load_projection_catalog(
        catalog_path,
        expected_sha256=catalog_sha256,
        model=loaded_model,
    )
    return Classifier(loaded_model), loaded_catalog, contract_id


def _custom_block(
    source_family: str,
    message: str,
    *,
    continuation_lines: list[str] | None = None,
) -> TimestampedLogBlock:
    header = f"[10:11:12][E][{source_family}:19]: {message}"
    continuations = continuation_lines or []
    return TimestampedLogBlock(
        timestamp="10:11:12",
        level="E",
        source_tag=f"{source_family}:19",
        source_family=source_family,
        header_line=header,
        continuation_lines=continuations,
        raw_block="\n".join((header, *continuations, "")),
        log_relpath="logs/error.log",
        line_number=1,
        end_line=1 + len(continuations),
    )


@pytest.fixture
def projection_runtime(tmp_path: Path):
    model_path = tmp_path / "invented-model.json"
    model_sha256 = _write_model(model_path)
    model = load_model(model_path, expected_sha256=model_sha256)
    catalog_path = tmp_path / "invented-projections.json"
    catalog_sha256 = _write_catalog(catalog_path, model_sha256)
    catalog = load_projection_catalog(
        catalog_path,
        expected_sha256=catalog_sha256,
        model=model,
    )
    return Classifier(model), catalog


def _block(symbol: str, path: str, line: int, *, level: str = "E") -> TimestampedLogBlock:
    header = (
        f"[12:34:56][{level}][{SOURCE_FAMILY}:73]: "
        f"Widget symbol '{symbol}' cannot be resolved"
    )
    continuation = f"Script location: file: {path} line: {line} (invented:setup)"
    raw = header + "\n" + continuation + "\n"
    return TimestampedLogBlock(
        timestamp="12:34:56",
        level=level,
        source_tag=f"{SOURCE_FAMILY}:73",
        source_family=SOURCE_FAMILY,
        header_line=header,
        continuation_lines=[continuation],
        raw_block=raw,
        log_relpath="logs/error.log",
        line_number=41,
        end_line=42,
    )


def test_projection_keeps_key_and_locator_typed_and_identity_stable(
    projection_runtime,
) -> None:
    classifier, catalog = projection_runtime
    first_block = _block(
        "azure_widget", "common/invented/azure_widget.txt", 81
    )
    second_block = _block(
        "vermilion_widget", "events/invented/vermilion_widget.txt", 907
    )
    first_result = classifier.classify_block(
        SOURCE_FAMILY, first_block.raw_block
    )[0]
    second_result = classifier.classify_block(
        SOURCE_FAMILY, second_block.raw_block
    )[0]

    first = project_normalized_issue(first_result, first_block, catalog)
    second = project_normalized_issue(second_result, second_block, catalog)

    assert first_result.contract_id == second_result.contract_id == CONTRACT_ID
    assert first.signature == second.signature
    assert first.primary_file == "common/invented/azure_widget.txt"
    assert first.primary_line == 81
    assert first.referenced_symbols == ["azure_widget"]
    assert "common/invented/azure_widget.txt" not in first.referenced_symbols
    assert second.primary_file == "events/invented/vermilion_widget.txt"
    assert second.primary_line == 907
    assert second.referenced_symbols == ["vermilion_widget"]


def test_signature_includes_source_family_but_not_engine_source_line() -> None:
    draft = IssueDraft(
        category="script_system",
        error_type="invented_failure",
        tags=[],
        engine_source="invented_alpha.cpp:17",
        sample_message="Invented semantic contract <KEY>",
        primary_file=None,
        primary_line=None,
        referenced_symbols=["first_key"],
        referenced_objects=[],
        extra_json={},
        severity="error",
        confidence="high",
        raw_block="invented",
        log_relpath="error.log",
        line_number=1,
    )

    first = normalize_issue(draft)
    same_family = normalize_issue(replace(draft, engine_source="invented_alpha.cpp:999"))
    different_family = normalize_issue(replace(draft, engine_source="invented_beta.cpp:17"))

    assert first.signature == same_family.signature
    assert first.signature != different_family.signature


def test_script_location_on_continuation_is_read_but_not_stored_as_object(
    projection_runtime,
) -> None:
    classifier, catalog = projection_runtime
    block = _block("lapis_widget", "common/invented/lapis_widget.txt", 29)
    result = classifier.classify_block(SOURCE_FAMILY, block.raw_block)[0]

    draft = project_issue(result, block, catalog)

    assert draft.primary_file == "common/invented/lapis_widget.txt"
    assert draft.primary_line == 29
    assert draft.referenced_objects == []
    assert "Script location" in analyze_complete_message(result, block).complete_message


def test_complete_message_analysis_has_no_classifier_token_limit(
    projection_runtime,
) -> None:
    classifier, _catalog = projection_runtime
    block = _block("long_widget", "common/invented/long_widget.txt", 733)
    result = classifier.classify(SOURCE_FAMILY, MEDOID)
    filler = " ".join(f"context_{index}" for index in range(450))
    tail = "Script location: file: common/invented/tail_widget.txt line: 733"
    long_block = replace(
        block,
        continuation_lines=[filler, tail],
        raw_block=block.header_line + "\n" + filler + "\n" + tail + "\n",
    )

    evidence = analyze_complete_message(result, long_block)

    assert evidence.raw_block == long_block.raw_block
    assert len(evidence.complete_message.split()) > 450
    assert evidence.locators[-1].path == "common/invented/tail_widget.txt"
    assert evidence.locators[-1].line == 733


def test_one_literal_near_miss_falls_back_and_retains_lexical_severity(
    projection_runtime,
) -> None:
    classifier, catalog = projection_runtime
    block = _block("ochre_widget", "common/invented/ochre_widget.txt", 12)
    near_miss_raw = block.raw_block.replace("cannot be resolved", "cannot be resolve")
    near_miss_block = replace(
        block,
        header_line=block.header_line.replace("cannot be resolved", "cannot be resolve"),
        raw_block=near_miss_raw,
    )
    result = classifier.classify_block(SOURCE_FAMILY, near_miss_raw)[0]

    draft = project_issue(result, near_miss_block, catalog)

    assert result.assignment_level == "unknown"
    assert result.contract_id is None
    assert draft.category == "unclassified"
    assert draft.error_type == "unknown"
    assert draft.confidence == "low"
    assert draft.severity == "error"
    assert draft.referenced_symbols == []
    assert draft.referenced_objects == []


def test_severity_comes_from_lexical_level_for_exact_contract(
    projection_runtime,
) -> None:
    classifier, catalog = projection_runtime
    block = _block(
        "silver_widget", "common/invented/silver_widget.txt", 6, level="W"
    )
    result = classifier.classify_block(SOURCE_FAMILY, block.raw_block)[0]

    draft = project_issue(result, block, catalog)

    assert draft.category == "symbol_resolution"
    assert draft.confidence == "high"
    assert draft.severity == "warning"


def test_catalog_and_runtime_validate_catalog_contract_and_model_hashes(
    tmp_path: Path,
    projection_runtime,
) -> None:
    classifier, catalog = projection_runtime
    model_path = tmp_path / "second-model.json"
    model_sha256 = _write_model(model_path)
    catalog_path = tmp_path / "catalog.json"
    catalog_sha256 = _write_catalog(catalog_path, model_sha256)

    catalog_path.write_bytes(catalog_path.read_bytes() + b" ")
    with pytest.raises(ProjectionCatalogIntegrityError, match="catalog SHA-256"):
        load_projection_catalog(
            catalog_path,
            expected_sha256=catalog_sha256,
            model=classifier.model,
        )

    block = _block("violet_widget", "common/invented/violet_widget.txt", 43)
    result = classifier.classify_block(SOURCE_FAMILY, block.raw_block)[0]
    with pytest.raises(SemanticProjectionError, match="model SHA-256"):
        project_issue(
            replace(result, model_sha256="0" * 64),
            block,
            catalog,
        )


def test_catalog_rejects_contract_id_not_bound_to_template(tmp_path: Path) -> None:
    model_path = tmp_path / "model.json"
    model_sha256 = _write_model(model_path)
    catalog_path = tmp_path / "catalog.json"
    _write_catalog(catalog_path, model_sha256)
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    raw["projections"][0]["contract_id"] = "0" * 16
    catalog_path.write_text(
        json.dumps(raw, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    catalog_sha256 = hashlib.sha256(catalog_path.read_bytes()).hexdigest()

    with pytest.raises(ProjectionCatalogIntegrityError, match="approved model contract"):
        load_projection_catalog(
            catalog_path,
            expected_sha256=catalog_sha256,
            model=load_model(model_path, expected_sha256=model_sha256),
        )


def test_catalog_validates_composed_l1_l2_identity_against_both_layers(
    tmp_path: Path,
) -> None:
    model_path = tmp_path / "model.json"
    model_sha256 = _write_model(model_path)
    model = load_model(model_path, expected_sha256=model_sha256)
    catalog_path = tmp_path / "catalog.json"
    _write_catalog(catalog_path, model_sha256)
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    outer = ("Script", "system", "error", "!", "Error", ":", KEY, "effect")
    reason = ("Invented", "reviewed", "reason")
    composed_id = composed_contract_id_for(SOURCE_FAMILY, outer, reason)
    raw["projections"].append(
        {
            "contract_id": composed_id,
            "contract_kind": "composed_l1_l2",
            "source_family": SOURCE_FAMILY,
            "l1_outer_tokens": list(outer),
            "l2_reason_tokens": list(reason),
            "accounting": "preserved_unclassified",
            "category": "unclassified",
            "error_type": "unknown",
            "tags": [],
            "confidence_by_assignment": {"l1_l2": "low"},
            "primary_locator_ordinal": None,
            "slot_projections": [],
        }
    )
    catalog_path.write_text(
        json.dumps(raw, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    digest = hashlib.sha256(catalog_path.read_bytes()).hexdigest()

    catalog = load_projection_catalog(
        catalog_path, expected_sha256=digest, model=model
    )

    projection = catalog.projection_for(composed_id)
    assert projection is not None
    assert projection.contract_kind == "composed_l1_l2"
    assert projection.message_template == " ".join((*outer, "[", *reason, "]"))


def test_catalog_rejects_inconsistent_preserved_unclassified_projection(
    tmp_path: Path,
) -> None:
    model_path = tmp_path / "model.json"
    model_sha256 = _write_model(model_path)
    model = load_model(model_path, expected_sha256=model_sha256)
    catalog_path = tmp_path / "catalog.json"
    _write_catalog(catalog_path, model_sha256)
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    raw["projections"][0]["accounting"] = "preserved_unclassified"
    catalog_path.write_text(
        json.dumps(raw, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )
    digest = hashlib.sha256(catalog_path.read_bytes()).hexdigest()

    with pytest.raises(
        ProjectionCatalogIntegrityError, match="preserved-unclassified"
    ):
        load_projection_catalog(catalog_path, expected_sha256=digest, model=model)


def test_template_span_preserves_punctuation_adjacency(tmp_path: Path) -> None:
    source = "invented_event_queue.cpp"
    message = "Event reference alpha_event.0042 cannot be scheduled"
    template = tokenize(message)
    classifier, catalog, contract_id = _custom_projection_runtime(
        tmp_path,
        source_family=source,
        message=message,
        template_tokens=template,
        reference_projections=[
            {
                "capture": "template_span",
                "target": "referenced_symbol",
                "start_ordinal": 3,
                "end_ordinal_exclusive": 6,
            }
        ],
    )
    block = _custom_block(source, message)
    result = classifier.classify_block(source, block.raw_block)[0]

    issue = project_normalized_issue(result, block, catalog)

    assert result.contract_id == contract_id
    assert issue.referenced_symbols == ["alpha_event.0042"]


def test_primary_locator_and_locator_reference_are_independent_roles(
    tmp_path: Path,
) -> None:
    source = "invented_locator.cpp"
    message = (
        "Widget binding failed at line 13 and column 7 in "
        "common/invented/widget.txt Near file: CEventOptionDesc line: 163"
    )
    classifier, catalog, _contract_id = _custom_projection_runtime(
        tmp_path,
        source_family=source,
        message=message,
        template_tokens=tokenize(message),
        primary_locator_ordinal=1,
        reference_projections=[
            {
                "capture": "locator",
                "target": "referenced_object",
                "ordinal": 2,
            }
        ],
    )
    block = _custom_block(source, message)
    result = classifier.classify_block(source, block.raw_block)[0]

    issue = project_normalized_issue(result, block, catalog)

    assert issue.primary_file == "common/invented/widget.txt"
    assert issue.primary_line == 13
    assert issue.referenced_symbols == []
    assert issue.referenced_objects == ["CEventOptionDesc"]


def test_script_outer_expression_preserves_key_relationship_not_spacing(
    tmp_path: Path,
) -> None:
    source = "invented_script_system.cpp"
    first_message = (
        "Script system error! Error: scope:alpha.beta effect "
        "[ Failed context switch ]"
    )
    second_message = first_message.replace("scope:alpha.beta", "scope:gamma.delta")
    classifier, catalog, contract_id = _custom_projection_runtime(
        tmp_path,
        source_family=source,
        message=first_message,
        template_tokens=tokenize(first_message),
        reference_projections=[
            {
                "capture": "script_outer_expression",
                "target": "referenced_symbol",
            }
        ],
    )
    first_block = _custom_block(source, first_message)
    second_block = _custom_block(source, second_message)
    first_result = classifier.classify_block(source, first_block.raw_block)[0]
    second_result = classifier.classify_block(source, second_block.raw_block)[0]

    first = project_normalized_issue(first_result, first_block, catalog)
    second = project_normalized_issue(second_result, second_block, catalog)

    assert first_result.contract_id == second_result.contract_id == contract_id
    assert first.signature == second.signature
    assert first.referenced_symbols == ["scope:alpha.beta"]
    assert second.referenced_symbols == ["scope:gamma.delta"]


def test_slot_composition_retains_exact_ck3_expression(tmp_path: Path) -> None:
    source = "invented_data_factory.cpp"
    message = "Could not find promote for 'war_goal_title' in 'war_goal_title.GetName'."
    template = (
        "Could",
        "not",
        "find",
        "promote",
        "for",
        "'",
        KEY,
        "'",
        "in",
        "'",
        KEY,
        ".",
        KEY,
        "'",
        ".",
    )
    classifier, catalog, _contract_id = _custom_projection_runtime(
        tmp_path,
        source_family=source,
        message=message,
        template_tokens=template,
        reference_projections=[
            {
                "capture": "slot_composition",
                "target": "referenced_symbol",
                "parts": [
                    {"role": "key", "ordinal": 2},
                    {"literal": "."},
                    {"role": "key", "ordinal": 3},
                ],
            }
        ],
    )
    block = _custom_block(source, message)
    result = classifier.classify_block(source, block.raw_block)[0]

    issue = project_normalized_issue(result, block, catalog)

    assert result.assignment_level == "full"
    assert issue.referenced_symbols == ["war_goal_title.GetName"]


def test_equivalent_slot_contract_rejects_disagreement(tmp_path: Path) -> None:
    source = "invented_equivalency.cpp"
    message = 'Missing loc Azure: "Azure"'
    template = ("Missing", "loc", KEY, ":", '"', KEY, '"')
    classifier, catalog, contract_id = _custom_projection_runtime(
        tmp_path,
        source_family=source,
        message=message,
        template_tokens=template,
        reference_projections=[
            {
                "capture": "equivalent_slots",
                "target": "referenced_symbol",
                "role": "key",
                "ordinals": [1, 2],
            }
        ],
    )
    matching_block = _custom_block(source, message)
    matching_result = classifier.classify_block(source, matching_block.raw_block)[0]
    mismatch_block = _custom_block(source, 'Missing loc Azure: "Crimson"')
    mismatch_result = classifier.classify_block(source, mismatch_block.raw_block)[0]

    assert matching_result.contract_id == mismatch_result.contract_id == contract_id
    assert project_normalized_issue(
        matching_result, matching_block, catalog
    ).referenced_symbols == ["Azure"]
    with pytest.raises(SemanticProjectionError, match="equivalent semantic slots"):
        project_issue(mismatch_result, mismatch_block, catalog)


def test_event_uri_is_an_object_not_a_filesystem_locator(tmp_path: Path) -> None:
    source = "invented_audio.cpp"
    message = "Audio failure [event:/Invented/Widget/Chime]"
    classifier, catalog, _contract_id = _custom_projection_runtime(
        tmp_path,
        source_family=source,
        message=message,
        template_tokens=tokenize(message),
        reference_projections=[
            {"capture": "event_uri", "target": "referenced_object"}
        ],
    )
    block = _custom_block(source, message)
    result = classifier.classify_block(source, block.raw_block)[0]

    issue = project_normalized_issue(result, block, catalog)

    assert issue.primary_file is None
    assert issue.referenced_symbols == []
    assert issue.referenced_objects == ["/Invented/Widget/Chime"]
    assert analyze_complete_message(result, block).locators == ()


def test_unknown_argument_list_is_split_without_a_fixed_cardinality(
    tmp_path: Path,
) -> None:
    source = "invented_argument.cpp"
    message = (
        "Compiling source for invented_effect failed for unknown arguments: "
        "FIRST_ARG, SECOND_ARG, THIRD_ARG. At file: "
        "common/invented/effects.txt line: 22"
    )
    classifier, catalog, _contract_id = _custom_projection_runtime(
        tmp_path,
        source_family=source,
        message=message,
        template_tokens=tokenize(message),
        primary_locator_ordinal=1,
        reference_projections=[
            {
                "capture": "unknown_arguments",
                "target": "referenced_symbol",
            }
        ],
    )
    block = _custom_block(source, message)
    result = classifier.classify_block(source, block.raw_block)[0]

    issue = project_normalized_issue(result, block, catalog)

    assert issue.primary_file == "common/invented/effects.txt"
    assert issue.primary_line == 22
    assert issue.referenced_symbols == ["FIRST_ARG", "SECOND_ARG", "THIRD_ARG"]
