# Data Model

SQLite is the recommended MVP database.

## sessions

```text
session_id
started_at
ended_at
ingested_at
ck3_version
playset_name
mod_list_hash
mod_load_order_hash
git_branch
git_commit
git_dirty
crash_detected
crash_folder_id
parser_version
schema_version
```

## log_snapshots

```text
snapshot_id
session_id
log_name
source_path
retained_path
size_bytes
sha256
captured_at
```

## crash_folders

```text
crash_folder_id
session_id
source_path
folder_name
crash_timestamp
folder_hash
dump_present
readable_metadata_present
linked_by
confidence
```

## crash_artifacts

```text
artifact_id
crash_folder_id
source_path
retained_path
file_name
artifact_type
size_bytes
sha256
captured_at
```

Artifact types:

```text
copied_log
dump
metadata
exception
unknown
```

## issues

```text
issue_id
normalized_signature
normalization_version
first_seen_session_id
first_seen_at
category
severity
confidence
canonical_message
ignored
ignore_reason
ignore_created_at
```

## issue_occurrences

```text
occurrence_id
issue_id
session_id
log_name
raw_block_hash
raw_sample
occurrence_count
first_line_number
last_line_number
primary_file
primary_line
primary_symbol
call_stack_json
extracted_file_paths_json
created_at
```

## source_resolutions

```text
source_resolution_id
session_id
issue_id
file_path
winning_source_name
winning_source_type
winning_source_path
load_order_index
our_submod_override
override_chain_json
recently_modified
diff_vs_original_summary
diff_vs_predecessor_summary
confidence
reason
created_at
```

## fixability_assessments

```text
fixability_id
session_id
issue_id
score
severity_weight
regression_weight
crash_weight
our_submod_weight
recent_modification_weight
small_diff_weight
upstream_penalty
known_noise_penalty
recommendation
confidence
reason
created_at
```

## baselines

```text
baseline_id
name
session_id
created_at
description
```

## ignored_issues

```text
ignored_issue_id
issue_id
reason
created_at
expires_at
```

## schema_migrations

```text
version
applied_at
description
```

## Future tables

Later phases may add:

```text
workspaces
workspace_files
session_file_state
git_state
issue_file_links
external_validator_runs
issue_enrichments
repair_plans
repair_verifications
```
