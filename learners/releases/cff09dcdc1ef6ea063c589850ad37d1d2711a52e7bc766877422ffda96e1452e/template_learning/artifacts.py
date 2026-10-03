"""One candidate model builder/serializer for the CLI and incremental registry."""
from __future__ import annotations
import json
import hashlib
from copy import deepcopy
import os
import tempfile
from pathlib import Path
from template_learning.clustering import CLUSTERER_VERSION, cluster_source_records
from template_learning.inventory import sha256_file
from template_learning import constructions
from template_learning.patterns import SLOT_DEFINITIONS
from template_learning.matching_defaults import parameter_piece_ranges
from template_learning.matching_primitives import display_pattern
from template_learning.literal_guidance import LITERAL_GUIDANCE
from template_learning.owner_rules import OWNER_RULES, CONSTRUCTIONS, INFERENCE_POLICY
from template_learning.records import FEATURE_VERSION, SequenceRecord, identity
from template_learning.research_matching import evaluate_records
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.selection_evidence import independent_support, selection_evidence
from template_learning.template_retirement import retire_fixed_observations

MODEL_SCHEMA = "ck3chronicle.native-message-model"
MODEL_VERSION = 5

LEARNER_IMPLEMENTATION_FILES = (
    "records.py", "clustering.py", "patterns.py", "regions.py", "literal_guidance.py", "diagnostic_wording.py",
    "owner_rules.py", "owner_rules.json", "constructions.py", "parameter_structures.py", "full_ids.py",
    "artifacts.py", "inventory.py", "evidence.py", "research_matching.py",
    "incremental_template_registry.py", "learn_error_templates.py",
    "assignment.py", "selection_evidence.py", "template_retirement.py",
    "continuations.py", "matching_primitives.py", "matching_defaults.py",
    "native_matching.py", "matching_validation.py", "matcher_loader.py",
    "additive_learning.py", "evidence_serialization.py",
)


def learner_identity():
    """Pin evidence state to the actual learner, not just its display version."""
    hashes = {name: sha256_file(Path(__file__).with_name(name))
              for name in LEARNER_IMPLEMENTATION_FILES}
    return dict(version=CLUSTERER_VERSION, implementation_hashes=hashes,
                sha256=identity((CLUSTERER_VERSION, hashes)))


def canonical_bytes(value):
    return (json.dumps(value,ensure_ascii=True,sort_keys=True,indent=2)+"\n").encode()


def _context_patterns(cluster, threshold):
    contexts = {key:context for r in cluster.records for key,context in r.contexts.items()}
    result = {}
    for name in ("prefix","suffix") if contexts else ():
        pool = {c[name]["text"]:SequenceRecord(cluster.source_family,c[name]["text"],
            tuple(tuple(p) for p in c[name]["pieces"]),"context:"+name) for c in contexts.values()}
        result[name] = [_pattern(c) for c in cluster_source_records(cluster.source_family,list(pool.values()),threshold)]
    return result


def _learning_support(cluster):
    minimum=INFERENCE_POLICY['template_support']['minimum_distinct_examples']
    return independent_support(cluster,minimum)


def _pattern(cluster):
    support=_learning_support(cluster)
    return dict(template_id=cluster.template_id, source_family=cluster.source_family,
        context_kind=cluster.context_kind, context_patterns={},
        construction_id=constructions.identity(cluster.source_family,cluster.medoid.text),
        parameter_structures=[v[1] for _,v in sorted(parameter_piece_ranges(cluster.medoid.pieces,cluster.source_family).items())],
        parts=cluster.parts, display=display_pattern(cluster.parts),
        status="unresolved" if cluster.failures else "supported" if support['eligible'] else "provisional",
        learning_support=support, selection_evidence=selection_evidence(cluster,support),
        unsupported_members=cluster.failures,inference_refinements=cluster.refinements,
        region_hypotheses=cluster.hypotheses)


def _continuation_contract(cluster):
    from template_learning.continuations import native_layout, match_components
    from template_learning.matching_defaults import match_pattern
    if not cluster.medoid.continuations:
        return None
    rule = next((r for r in OWNER_RULES['continuation_structures']
                 if r['source'] == cluster.source_family and
                 'continuation:' + r['recovery_structure'] == cluster.context_kind), None)
    if rule is None:
        raise ValueError('recovered component structure has no model declaration')
    contracts = []
    for part in cluster.parts:
        if part.get('type') != rule['reference_type']:
            continue
        layouts = {identity(native_layout(e)[0]):native_layout(e)[0]
                   for r in cluster.records for e in r.continuations}
        if any(v['label'] != rule['label'] for v in layouts.values()):
            continue
        contract = dict(rule_id=rule['id'], opening_slot=part['name'],
            reference_type=rule['reference_type'], value_type=rule['value_type'],
            minimum_entries=rule['minimum_entries'], layouts=[layouts[k] for k in sorted(layouts)])
        if all(match_components(contract,r.continuations,
               match_pattern(cluster.parts,r.text,pieces=r.pieces) or []) is not None
               for r in cluster.records):
            contracts.append(contract)
    if len(contracts) != 1:
        return None
    return contracts[0]


def _learn_pool(source, records, threshold, review):
    """Rediscover every template from this build's native evidence."""
    retained = []
    for cluster in cluster_source_records(source,records,threshold,review=review):
        item = _pattern(cluster)
        contract = _continuation_contract(cluster)
        item['continuation'] = contract
        if cluster.medoid.continuations:
            if contract is None:
                item['status'] = 'unresolved'
                item['unsupported_members'] = ['continuation reference lacks a unique supported opening field']
            else:
                item['template_id'] = identity([item['template_id'],contract])[:24]
        item.update(context_patterns=_context_patterns(cluster,threshold),
            unique_messages=len(cluster.records), support_occurrences=sum(r.occurrences for r in cluster.records),
            evidence_record_ids=[identity(r.key) for r in cluster.records])
        retained.append(item)
    return retained


def build_model(records_by_source, evidence_stats, *, parser, threshold=.72,
                duplicates=(), excluded_evidence=(), previous_model=None):
    from template_learning import additive_learning
    prior_matcher = None
    update_sources = []
    if previous_model is not None:
        if previous_model['algorithm'].get('learner_identity') != learner_identity():
            raise ValueError('additive learning requires the same learner implementation')
        if previous_model['algorithm']['cluster_threshold'] != threshold:
            raise ValueError('additive learning requires the same inference threshold')
        if (previous_model['owner_rules'] != OWNER_RULES or
                any(previous_model['parser'][key] != parser.reference.to_dict()[key]
                    for key in ('version', 'sha256'))):
            raise ValueError('additive learning requires the same rules and pinned parser')
        if not set(previous_model['evidence']) <= set(evidence_stats):
            raise ValueError('additive learning requires cumulative evidence; use a fresh build to remove inputs')
        from template_learning.native_matching import Matcher
        prior_matcher = Matcher(previous_model)
    templates, source_summary, discovery_review, retirement_review = [], {}, [], []
    if previous_model is not None:
        retirement_review = deepcopy(previous_model['template_retirement'])
    sources = set(records_by_source)
    for source in sorted(sources):
        records = records_by_source.get(source,[])
        protected = ()
        if previous_model is None:
            complete = _learn_pool(source,records,threshold,discovery_review)
        else:
            previous = [t for t in previous_model['templates'] if t['source_family'] == source]
            complete, protected, detail = additive_learning.learn_source(
                source, records, previous, prior_matcher, threshold, _learn_pool, discovery_review)
            update_sources.append(detail)
        complete,retired=retire_fixed_observations(complete,records,protected_template_ids=protected)
        retirement_review.extend(retired)
        templates.extend(complete)
        source_summary[source] = dict(unique_messages=len(records),templates=len(complete),
            occurrences=sum(r.occurrences for r in records))
        print(f"Learned {source}: {len(records)} distinct messages -> {len(complete)} outer message candidates",flush=True)
    all_patterns = templates
    unresolved = [dict(evidence_sha256=sha,**row) for sha,stats in evidence_stats.items() for row in stats["unresolved_emissions"]]
    model = dict(schema=MODEL_SCHEMA,schema_version=MODEL_VERSION,record_scope="message",
        parser={**parser.reference.to_dict(),"artifact":"parser.py"},
        algorithm=dict(feature_version=FEATURE_VERSION,clusterer_version=CLUSTERER_VERSION,
            implementation_hashes=learner_identity()['implementation_hashes'],
            learner_identity=learner_identity(),
            source_family_hard_partition=True,cluster_threshold=threshold,
            literal_support="all distinct native member messages of this complete candidate",
            medoid_selection="deterministic spread: up to 40 candidates against up to 100 distinct variants; all variants enter template alignment",
            occurrence_weighting=False,additional_preprocessing=[],case_sensitive_retrieval=True,
            literal_refinement="case-only substitutions and empirically supported wording retained; presumed-literal guidance enabled="+str(LITERAL_GUIDANCE['enabled']),
            template_imports=False,
            build_strategy=additive_learning.STRATEGY_VERSION if previous_model is not None else 'fresh-native-batch',
            discovery_scope="cumulative unsettled native evidence; retain same-version settled definitions"
                if previous_model is not None else "all selected native evidence"),
        slot_definitions=SLOT_DEFINITIONS,owner_overrides=[],literal_guidance=LITERAL_GUIDANCE,owner_rules=OWNER_RULES,
        assignment_policy=OWNER_RULES['assignment_policy'], template_retirement=retirement_review,
        region_discovery=dict(decisions=discovery_review,
            stopping_condition="one original-group sweep; accepted unions are not reopened"),
        summary=dict(distinct_error_logs=len(evidence_stats),source_families=len(sources),
            emissions=sum(s["timestamped_blocks"] for s in evidence_stats.values()),
            messages=sum(s["recovered_messages"] for s in evidence_stats.values()),
            unique_messages=sum(len(r) for r in records_by_source.values()),templates=len(templates),
            confirmed_templates=0,
            supported_templates=sum(t['status'] in {'supported','confirmed'} for t in templates),
            provisional_templates=sum(t['status']=='provisional' for t in templates),
            unresolved_emissions=len(unresolved),unresolved_candidates=sum(bool(t["unsupported_members"]) for t in all_patterns)),
        by_source=source_summary, templates=templates, constructions=CONSTRUCTIONS,
        evidence={sha:{k:v for k,v in s.items() if k!="unresolved_emissions"} for sha,s in evidence_stats.items()},
        excluded_evidence=list(excluded_evidence), duplicates=list(duplicates),
        status="research_candidate_not_promoted",
        diagnostic_policy=dict(learning_unit="complete outer message",reason_fields="intact owner-declared content",
            template_support="At least two distinct native messages, including variation in every slot type; exact repetitions do not increase support. Redundant fixed KEY observations retire without re-inference. One complete assignment is selected; evidence ties remain provisional.",
            slot_evidence="candidate member messages only",detached_component_learning=False))
    if previous_model is not None:
        model['learning_update'] = dict(strategy=additive_learning.STRATEGY_VERSION,
            parent_revision=previous_model['revision_id'], sources=update_sources,
            transitions=additive_learning.lifecycle(previous_model['templates'], templates, retirement_review))
    evaluation_summary,evaluated,_ = evaluate_records(model,records_by_source,evidence_stats)
    model["summary"]["training_outcomes"] = evaluation_summary["counts"]
    model["revision_id"] = identity(model)[:24]
    review_rows = []
    for row in evaluated:
        # Every match is a complete diagnostic; competing candidates stay visible.
        kind = row['context_kind']
        key = (row['source_family'],kind,row['native'])
        if row['continuations']:
            key = (*key,identity(row['continuations']))
        row.update(record_id=identity(key),
            example_id=identity((*key,sorted(row["contexts"]))),
            template_id=row['selected_assignment']['template_id'] if row['selected_assignment'] else None,
            captures=row['selected_assignment']['captures'] if row['selected_assignment'] else None)
        review_rows.append(row)
    return model,dict(schema="ck3chronicle.native-model-evidence",parser=model["parser"],
        records=review_rows,unresolved=unresolved)


def write_report(model, path):
    lines = ["# Native learner candidate", "", "Research output; no runtime promotion or SQL processing.","",
        "Source-specific learning; literal/slot inference uses distinct messages, not occurrence weighting.","",
        "```json",json.dumps(model["summary"],indent=2),"```","",
        "| Source | Distinct messages | Outer candidates | Occurrences |","|---|---:|---:|---:|"]
    for source,row in model["by_source"].items():
        lines.append(f"| {source} | {row['unique_messages']} | {row['templates']} | {row['occurrences']} |")
    lines += ["",
        "Full native examples, capture byte offsets, declared construction boundaries and every occurrence are in native_evidence.json. Exact model patterns are in empirical_template_model.json. All candidates require semantic review."]
    path.write_text("\n".join(lines)+"\n",encoding="utf-8")


def write_bundle(root, model, evidence, *, parser, build_command):
    from template_learning.evidence_serialization import write_native_evidence
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    folder = root/model["revision_id"]
    payloads = {"empirical_template_model.json":canonical_bytes(model),
        "parser.py":Path(parser.implementation.__file__).read_bytes(),
        "parser-manifest.json":canonical_bytes(model["parser"]),
        "assignment.py":Path(__file__).with_name('assignment.py').read_bytes(),
        "continuations.py":Path(__file__).with_name('continuations.py').read_bytes()}
    descriptor, temporary_name = tempfile.mkstemp(prefix='.native-evidence-', dir=root)
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        evidence_hash = write_native_evidence(temporary, evidence)
        manifest = dict(schema="ck3chronicle.native-candidate-bundle",schema_version=1,
            revision_id=model["revision_id"], parser=model["parser"], build_command=build_command,
            hashes={**{name:hashlib.sha256(data).hexdigest() for name,data in payloads.items()},
                    'native_evidence.json':evidence_hash})
        # Immutable revision contents. Reproduction commands are metadata, not a
        # reason to overwrite a previous bundle with the same learned model.
        if folder.exists():
            current = json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
            if current["hashes"] != manifest["hashes"]:
                raise ValueError(f"immutable candidate revision disagrees: {folder}")
            load_bundle(folder)
            return folder
        folder.mkdir()
        for name,data in payloads.items():
            (folder/name).write_bytes(data)
        os.replace(temporary, folder/'native_evidence.json')
        (folder/"manifest.json").write_bytes(canonical_bytes(manifest))
        write_report(model,folder/"REVIEW.md")
        load_bundle(folder)
        return folder
    finally:
        temporary.unlink(missing_ok=True)


def load_bundle(folder):
    folder = Path(folder).resolve()
    manifest = json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema")!="ck3chronicle.native-candidate-bundle" or manifest.get("schema_version")!=1:
        raise ValueError("unsupported native bundle schema")
    if set(manifest["hashes"])!={"empirical_template_model.json","native_evidence.json","parser.py","parser-manifest.json","assignment.py","continuations.py"}:
        raise ValueError("incomplete native bundle hash manifest")
    for name,digest in manifest["hashes"].items():
        path = (folder/name).resolve()
        if path.parent != folder or sha256_file(path) != digest:
            raise ValueError(f"candidate artifact hash mismatch: {name}")
    model = json.loads((folder/"empirical_template_model.json").read_text(encoding="utf-8"))
    if model.get("schema")!=MODEL_SCHEMA or model.get("schema_version")!=MODEL_VERSION or model.get("record_scope")!="message":
        raise ValueError("unsupported native model schema")
    if model["constructions"] != CONSTRUCTIONS:
        raise ValueError("candidate construction declarations differ from the selected learner rules")
    if model['algorithm']['clusterer_version']!=CLUSTERER_VERSION or model['owner_rules']!=OWNER_RULES:
        raise ValueError('candidate inference revision differs from the selected learner; rebuild explicitly')
    if model["parser"] != manifest["parser"] or model["parser"] != json.loads((folder/"parser-manifest.json").read_text(encoding="utf-8")):
        raise ValueError("model/parser manifest disagreement")
    if model["revision_id"]!=manifest["revision_id"] or model["revision_id"]!=identity({k:v for k,v in model.items() if k!="revision_id"})[:24]:
        raise ValueError("model revision identity disagreement")
    parser = load_parser(reference_from_manifest(folder/"parser-manifest.json"))
    return model,parser
