"""One explicit current database. No adoption, migration, or repair on opening."""
import json
import sqlite3

SCHEMA_VERSION = 3
APPLICATION_ID = 0x434B3652
LINEAGE_FIELDS = frozenset(('contract_version', 'model_revision', 'package_id',
    'package_manifest_sha256', 'parser', 'matcher_api_version', 'selector_version',
    'classifier_revision', 'application_revision', 'model_schema_version',
    'package_schema_version'))


def encode(value) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False)


def check_lineage(lineage):
    if set(lineage) != LINEAGE_FIELDS or any(not lineage[k] for k in LINEAGE_FIELDS):
        raise ValueError('complete Task 05 processing lineage required')
    return json.loads(encode(lineage))


DDL = '''
CREATE TABLE database_info (
 singleton INTEGER PRIMARY KEY CHECK(singleton=1),
 database_id TEXT NOT NULL UNIQUE, schema_version INTEGER NOT NULL,
 created_at TEXT NOT NULL
);
CREATE TABLE runs (
 sequence INTEGER PRIMARY KEY,
 run_id TEXT NOT NULL UNIQUE, log_sha256 TEXT NOT NULL UNIQUE,
 processed_at TEXT NOT NULL, processed_utc TEXT NOT NULL,
 identity_timestamp TEXT NOT NULL, identity_timezone TEXT NOT NULL,
 identity_basis TEXT NOT NULL CHECK(identity_basis IN ('original_log_creation','processing')),
 facts_json TEXT NOT NULL, counters_json TEXT NOT NULL, lineage_json TEXT NOT NULL
);
CREATE TABLE definitions (
 definition_id INTEGER PRIMARY KEY,
 model_revision TEXT NOT NULL, contract_version TEXT NOT NULL, template_id TEXT NOT NULL,
 source_family_json TEXT NOT NULL, definition_json TEXT NOT NULL,
 UNIQUE(model_revision,contract_version,template_id)
);
CREATE TABLE playsets (
 run_id TEXT PRIMARY KEY REFERENCES runs(run_id),
 playset_captured INTEGER NOT NULL CHECK(playset_captured IN (0,1)),
 schema_version INTEGER, error_log_sha256 TEXT, debug_log_sha256 TEXT,
 log_pair_id TEXT, captured_at TEXT
);
CREATE TABLE playset_members (
 run_id TEXT NOT NULL REFERENCES playsets(run_id), load_order INTEGER NOT NULL,
 name TEXT NOT NULL, path TEXT NOT NULL, root_ID TEXT, stable_id TEXT, descriptor_path TEXT,
 PRIMARY KEY(run_id,load_order)
);
CREATE TABLE diagnostics (
 run_id TEXT NOT NULL REFERENCES runs(run_id), ordinal INTEGER NOT NULL,
 definition_id INTEGER NOT NULL REFERENCES definitions(definition_id),
 identity_digest TEXT NOT NULL, values_json TEXT NOT NULL,
 match_status TEXT NOT NULL CHECK(match_status IN ('template','provisional')),
 occurrence_count INTEGER NOT NULL CHECK(occurrence_count>0),
 error_type TEXT NOT NULL CHECK(error_type='unknown'), provenance_json TEXT NOT NULL,
 PRIMARY KEY(run_id,ordinal)
);
CREATE INDEX diagnostic_identity ON diagnostics(run_id,identity_digest);
CREATE INDEX diagnostic_status ON diagnostics(run_id,match_status);
CREATE INDEX diagnostic_definition ON diagnostics(definition_id);
CREATE INDEX definition_source ON definitions(source_family_json);
CREATE TABLE review (
 run_id TEXT PRIMARY KEY REFERENCES runs(run_id),
 log_reference TEXT NOT NULL UNIQUE, manifest_reference TEXT NOT NULL UNIQUE,
 log_sha256 TEXT NOT NULL, log_bytes INTEGER NOT NULL CHECK(log_bytes>=0),
 emission_count INTEGER NOT NULL CHECK(emission_count>=0),
 unit_count INTEGER NOT NULL CHECK(unit_count>=0),
 availability TEXT NOT NULL CHECK(availability='available'),
 routing_counts_json TEXT NOT NULL, source_counts_json TEXT NOT NULL
);
'''


def initialize(connection, *, database_id, created_at):
    connection.executescript(DDL)
    connection.execute('INSERT INTO database_info VALUES (1,?,?,?)',
                       (database_id, SCHEMA_VERSION, created_at))
    connection.execute(f'PRAGMA application_id={APPLICATION_ID}')
    connection.execute(f'PRAGMA user_version={SCHEMA_VERSION}')
    connection.commit()


def validate(connection) -> dict:
    if (connection.execute('PRAGMA application_id').fetchone()[0] != APPLICATION_ID
            or connection.execute('PRAGMA user_version').fetchone()[0] != SCHEMA_VERSION):
        raise ValueError(f'incompatible database: explicit reset required; initialize schema {SCHEMA_VERSION}')
    # Check the physical tables/columns without updating or loading model resources.
    expected = sqlite3.connect(':memory:')
    try:
        expected.executescript(DDL)
        for table in ('database_info', 'runs', 'definitions', 'diagnostics', 'review',
                      'playsets', 'playset_members'):
            actual = [tuple(row) for row in connection.execute(f'PRAGMA table_info({table})')]
            if actual != expected.execute(f'PRAGMA table_info({table})').fetchall():
                raise ValueError('incompatible physical schema; explicit reset required: ' + table)
    finally:
        expected.close()
    rows = connection.execute('SELECT * FROM database_info').fetchall()
    if len(rows) != 1 or rows[0]['schema_version'] != SCHEMA_VERSION:
        raise ValueError('missing or unsupported database metadata')
    row = dict(rows[0])
    row.pop('singleton')
    return row
