# ck3chronicle 0.0.3 — release notes

The archive receipt and `release-manifest.json` identify the application,
runtime, tools, model, Learner, notices and exact manual files in your bundle.

## Application changes

- The handler retains **1,024 completed public-request results**. Outstanding
  requests are excluded from completed-result eviction. Stored Runs and
  content-hash deduplication remain independent of this temporary cache.
- `ingest --package-id` help clarifies that omission uses the saved configured
  model pin. Model selection behavior is unchanged.

## Manual edition: 12 October 2026

The [user manual](docs/user/README.md) begins with Product Version, Introduction
and Orientation, followed by installation, everyday workflows and detailed
references. It covers application **0.0.3**. Examples use portable paths;
replace them with your selected settings and data locations. The manifest's
`manual_revision` and document hashes identify the included edition.

## Data and component information

Raw-log retention defaults to 30 days from capture and operates independently of
successful ingestion. Disabled ingestion with enabled retention remains valid.
Stored diagnostic history and native review shards are preserved. An unavailable
request result alone does not establish whether ingestion succeeded; inspect
stored history and the [request-result guidance](docs/user/CLI_REFERENCE.md#request-results-and-stored-ingestion).

See [third-party notices](THIRD_PARTY_NOTICES.md) for component notices and
provenance status. Preserve the archive as supplied; use a new folder for another
build and keep user data separately.

[Manual contents](docs/user/README.md)
