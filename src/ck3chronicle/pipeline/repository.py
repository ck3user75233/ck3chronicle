"""Current-schema SQLite and native-shard completion boundary.

write_run owns staging, finalization, publication and commit. Task 07 supplies
truthful input facts and finished Task 05 results; it must not publish shards.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path, PurePosixPath
import re
import secrets
import sqlite3
import string
import uuid

from .contracts import identity_data, identity_digest, render_regions
from .domain import DiagnosticRecord, ResultIntegrityError, ReviewMetadata, RunResult
from . import review, schema


class DuplicateRunError(ValueError):
    def __init__(self, run_id):
        self.existing_run_id = run_id
        super().__init__('complete log already stored as ' + run_id)


class RunWriteError(RuntimeError):
    """No success returned. Reopen/check hash before retry or orphan cleanup."""
    def __init__(self, message, *, published_run_id=None, staging_reference=None):
        self.published_run_id = published_run_id
        self.staging_reference = staging_reference
        super().__init__(message)


def _name(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', value):
        raise ValueError('database identity must be a safe explicit name')
    return value


def _timestamp(value):
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('timestamp must include an explicit timezone')
    return value.isoformat(timespec='microseconds')


def _connect(path, readonly):
    uri = path.as_uri() + ('?mode=ro' if readonly else '?mode=rw')
    connection = sqlite3.connect(uri, uri=True, isolation_level=None)
    try:
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys=ON')
        if not readonly:
            connection.execute('PRAGMA synchronous=FULL')
    except BaseException:
        connection.close()
        raise
    return connection


def create_database(root: Path, *, initialized_at: datetime | None = None):
    """Create a schema/timestamp-named SQLite file without replacing any file.

    root may be an existing directory, including the configured runtime root.
    The returned Database.path is the exact path callers must persist in config.
    No discovery, migration, reset or adoption occurs when opening a database.
    """
    root = Path(root).resolve()
    now = initialized_at or datetime.now(timezone.utc)
    _timestamp(now)  # require an aware timestamp before reserving a file
    now = now.astimezone(timezone.utc)
    database_id = f"ck3chronicle-schema{schema.SCHEMA_VERSION}-{now.strftime('%Y%m%dT%H%M%SZ')}"
    root.mkdir(exist_ok=True)
    path = root / f'{database_id}.sqlite3'
    with path.open('xb'):
        pass  # exclusive reservation: a same-second collision never overwrites
    connection = None
    try:
        (root / 'review' / database_id / '.staging').mkdir(parents=True)
        connection = sqlite3.connect(path)
        schema.initialize(connection, database_id=database_id,
                          created_at=_timestamp(now))
    finally:
        if connection is not None:
            connection.close()
    return open_database(path)


def open_database(path: Path):
    """Open existing supported storage, without migration/adoption/creation."""
    return Database(path, readonly=False)


def open_database_readonly(path: Path):
    """SQLite mode=ro; does not create paths or inspect review/model/log files."""
    return Database(path, readonly=True)


class Database:
    def __init__(self, path: Path, *, readonly: bool):
        self.path = Path(path).resolve()
        if not self.path.is_file():
            raise ValueError(f'existing SQLite database file required: {self.path}')
        self.root = self.path.parent
        self.connection = _connect(self.path, readonly)
        try:
            self._metadata = schema.validate(self.connection)
            _name(self._metadata['database_id'])
        except BaseException:
            self.connection.close()
            raise

    @property
    def metadata(self):
        """Independent storage identity/schema/creation facts."""
        return deepcopy(self._metadata)

    @property
    def review_root(self):
        return self.root / 'review' / self._metadata['database_id']

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @staticmethod
    def _run(row):
        if row is None:
            return None
        result = dict(row)
        for field in ('facts', 'counters', 'lineage'):
            result[field] = json.loads(result.pop(field + '_json'))
        return result

    def find_run_by_log_hash(self, log_sha256: str):
        return self._run(self.connection.execute(
            'SELECT * FROM runs WHERE log_sha256=?', (log_sha256,)).fetchone())

    def get_run(self, run_id: str):
        return self._run(self.connection.execute('SELECT * FROM runs WHERE run_id=?', (run_id,)).fetchone())

    def list_runs(self, *, limit: int | None = None, offset: int = 0):
        """Newest processing UTC first, then descending successful insertion sequence.

        Original/lifecycle chronology is available only when supplied in facts;
        this query never substitutes copied-file creation times for those facts.
        """
        if (limit is not None and (type(limit) is not int or limit < 0)
                or type(offset) is not int or offset < 0):
            raise ValueError('nonnegative integer pagination required')
        rows = self.connection.execute(
            'SELECT * FROM runs ORDER BY processed_utc DESC, sequence DESC LIMIT ? OFFSET ?',
            (-1 if limit is None else limit, offset))
        return [self._run(row) for row in rows]

    def latest_run(self):
        rows = self.list_runs(limit=1)
        return rows[0] if rows else None

    def read_diagnostics(self, run_id: str, *, match_status: str | None = None,
                         source_family: str | None = None):
        """Stored records + definitions; first representative occurrence order.

        Includes both statuses by default. Unknown Run or no matches returns [].
        Ordinal is Run-local record order, not a diagnostic identity or timestamp.
        """
        if match_status not in (None, 'template', 'provisional'):
            raise ValueError('unsupported match_status filter')
        query = '''SELECT d.*, f.definition_json, f.source_family_json
                   FROM diagnostics d JOIN definitions f USING(definition_id) WHERE d.run_id=?'''
        args = [run_id]
        if match_status is not None:
            query += ' AND d.match_status=?'
            args.append(match_status)
        if source_family is not None:
            query += ' AND f.source_family_json=?'
            args.append(schema.encode(source_family))
        result = []
        for row in self.connection.execute(query + ' ORDER BY d.ordinal', args):
            item = dict(row)
            for field in ('definition', 'values', 'provenance', 'source_family'):
                item[field] = json.loads(item.pop(field + '_json'))
            result.append(item)
        return result

    def read_playset(self, run_id: str):
        """SQL-only accepted producer values, with members in original order."""
        row = self.connection.execute('SELECT * FROM playsets WHERE run_id=?', (run_id,)).fetchone()
        if row is None:
            return None
        result = dict(row)
        result.pop('run_id')
        result['playset_captured'] = bool(result['playset_captured'])
        result['members'] = [dict(r) for r in self.connection.execute(
            'SELECT load_order,name,path,root_ID,stable_id,descriptor_path '
            'FROM playset_members WHERE run_id=? ORDER BY load_order', (run_id,))]
        return result

    def read_review_metadata(self, run_id: str):
        """Stored availability only. Missing Run returns None; no filesystem IO."""
        row = self.connection.execute('SELECT * FROM review WHERE run_id=?', (run_id,)).fetchone()
        if row is None:
            return None
        result = dict(row)
        for field in ('routing_counts', 'source_counts'):
            result[field] = json.loads(result.pop(field + '_json'))
        return result

    def resolve_review_reference(self, reference: str) -> Path:
        """Lexical resolution from this explicit database root; no availability check."""
        path = PurePosixPath(reference)
        if (path.parts[:2] != ('review', self._metadata['database_id'])
                or path.is_absolute() or '..' in path.parts or '\\' in reference or ':' in reference):
            raise ValueError('review reference outside database namespace')
        return self.root.joinpath(*path.parts)

    def _check_records(self, records, lineage):
        identities = {}
        definitions = {}
        for record in records:
            if (not isinstance(record, DiagnosticRecord) or type(record.occurrence_count) is not int
                    or record.occurrence_count < 1 or record.error_type != 'unknown'
                    or record.match_status not in ('template', 'provisional')):
                raise ResultIntegrityError('invalid compact diagnostic record')
            definition = record.definition
            if (definition['model_revision'] != lineage['model_revision']
                    or definition['contract_version'] != lineage['contract_version']):
                raise ResultIntegrityError('definition differs from Run lineage')
            # Structural serialized correspondence only; no semantic interpretation.
            render_regions(definition, record.values)
            key = definition['template_id']
            if key in definitions and definitions[key] != definition:
                raise ResultIntegrityError('conflicting definitions within Run')
            definitions[key] = definition
            equality = identity_data(record.values)
            bucket = identities.setdefault(identity_digest(record.values), [])
            if equality in bucket:
                raise ResultIntegrityError('input records are not aggregated by full identity')
            bucket.append(equality)

    def write_run(self, *, log_sha256: str, facts: dict, lineage: dict,
                  records: tuple[DiagnosticRecord, ...], review_writer: review.ReviewWriter,
                  playset: dict | None = None, processed_at: datetime | None = None,
                  reliable_original_log_created_at: datetime | None = None) -> RunResult:
        """Complete one Run; exceptions are never RunResult values.

        facts is lossless JSON capture/lifecycle/crash provenance; unavailable
        observations should be explicit nulls. The reliable_original... argument
        is a caller assertion about the original file, NEVER the copy's ctime.
        All publication/transaction work is owned here, including failure cleanup.
        """
        if self.connection.in_transaction:
            raise ValueError('write_run requires an idle connection')
        if not isinstance(log_sha256, str) or not re.fullmatch('[0-9a-f]{64}', log_sha256):
            raise ValueError('full lowercase SHA-256 required')
        existing = self.find_run_by_log_hash(log_sha256)
        if existing:
            raise DuplicateRunError(existing['run_id'])
        lineage = schema.check_lineage(lineage)
        from .playsets import stored_playset
        playset = stored_playset(playset, error_log_sha256=log_sha256)
        records = deepcopy(tuple(records))
        self._check_records(records, lineage)
        accounting = review_writer.accounting(records)
        if not isinstance(facts, dict):
            raise ValueError('explicit Run facts object required')
        facts_json = schema.encode(facts)
        processed_at = processed_at or datetime.now(timezone.utc)
        processed = _timestamp(processed_at)
        identity_time = reliable_original_log_created_at or processed_at
        identity_timestamp = _timestamp(identity_time)
        identity_timezone = getattr(identity_time.tzinfo, 'key', str(identity_time.tzinfo))
        basis = 'original_log_creation' if reliable_original_log_created_at is not None else 'processing'
        stored_lineage = dict(lineage, database_schema_version=schema.SCHEMA_VERSION,
                              database_id=self._metadata['database_id'])
        stage = self.review_root / '.staging' / uuid.uuid4().hex
        stage_created = False
        published = None
        run_id = None
        try:
            stage.mkdir()
            stage_created = True
            staged = review_writer.stage(stage)
            self.connection.execute('BEGIN IMMEDIATE')
            existing = self.find_run_by_log_hash(log_sha256)
            if existing:
                raise DuplicateRunError(existing['run_id'])
            # Serialize writers using SQLite. Collision checks precede publication.
            for _ in range(100):
                run_id = identity_time.strftime('%Y%m%d-') + ''.join(
                    secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                destination = self.review_root / run_id
                if self.get_run(run_id) is not None or destination.exists():
                    continue
                try:
                    self.connection.execute('''INSERT INTO runs
                        (run_id,log_sha256,processed_at,processed_utc,identity_timestamp,
                         identity_timezone,identity_basis,facts_json,counters_json,lineage_json)
                        VALUES (?,?,?,?,?,?,?,?,?,?)''',
                        (run_id, log_sha256, processed,
                         _timestamp(processed_at.astimezone(timezone.utc)), identity_timestamp,
                         identity_timezone, basis, facts_json, schema.encode(accounting.counts),
                         schema.encode(stored_lineage)))
                except sqlite3.IntegrityError:
                    if self.get_run(run_id) is not None:
                        continue
                    raise
                break
            else:
                raise RuntimeError('Run-ID collision retry exhausted')
            self._insert_records(run_id, records)
            self.connection.execute('INSERT INTO playsets VALUES (?,?,?,?,?,?,?)',
                (run_id, playset['playset_captured'], playset['schema_version'],
                 playset['error_log_sha256'], playset['debug_log_sha256'],
                 playset['log_pair_id'], playset['captured_at']))
            self.connection.executemany('INSERT INTO playset_members VALUES (?,?,?,?,?,?,?)',
                [(run_id, *(member[k] for k in ('load_order', 'name', 'path', 'root_ID',
                    'stable_id', 'descriptor_path'))) for member in playset['members']])
            manifest = review.finalize(stage, staged, run_id=run_id, lineage=stored_lineage,
                                       log_sha256=log_sha256, accounting=accounting, playset=playset)
            # mkdir is exclusive on Windows and POSIX. Only this attempt owns the
            # new destination; each file moves from staging into this empty path.
            destination.mkdir()
            published = run_id
            for name in (review.LOG_NAME, review.MANIFEST_NAME):
                (stage / name).rename(destination / name)
            review.sync_directory(destination)
            review.sync_directory(self.review_root)
            stage.rmdir()
            review.verify_published(destination, manifest)
            prefix = destination.relative_to(self.root).as_posix()
            metadata = ReviewMetadata(prefix + '/' + review.LOG_NAME,
                prefix + '/' + review.MANIFEST_NAME, staged['log_sha256'], staged['log_bytes'],
                accounting.counts['review_emissions'], accounting.counts['review_units'],
                'available', staged['routing_counts'], staged['source_counts'])
            self.connection.execute('INSERT INTO review VALUES (?,?,?,?,?,?,?,?,?,?)',
                (run_id, metadata.log_reference, metadata.manifest_reference, metadata.log_sha256,
                 metadata.log_bytes, metadata.emission_count, metadata.unit_count, metadata.availability,
                 schema.encode(metadata.routing_counts), schema.encode(metadata.source_counts)))
            # Construct before commit so no fallible file work follows a commit.
            result = RunResult(run_id, self._metadata['database_id'], log_sha256, accounting, metadata)
            self.connection.commit()
            return result
        except BaseException as exc:
            # Never delete published files here: commit errors can have uncertain
            # outcomes. Explicit cleanup checks the recovered DB under its lock.
            try:
                self.connection.rollback()
            except sqlite3.Error:
                pass
            if stage_created:
                try:
                    self._remove_owned_directory(stage)
                except OSError:
                    pass
            if isinstance(exc, (DuplicateRunError, KeyboardInterrupt, SystemExit)):
                raise
            raise RunWriteError(str(exc), published_run_id=published,
                staging_reference=stage.relative_to(self.root).as_posix()) from exc

    def _insert_records(self, run_id, records):
        definition_ids = {}
        for ordinal, record in enumerate(records):
            definition = record.definition
            key = tuple(definition[k] for k in ('model_revision', 'contract_version', 'template_id'))
            if key not in definition_ids:
                row = self.connection.execute('''SELECT definition_id,definition_json FROM definitions
                    WHERE model_revision=? AND contract_version=? AND template_id=?''', key).fetchone()
                encoded = schema.encode(definition)
                if row is not None:
                    if row['definition_json'] != encoded:
                        raise ResultIntegrityError('definition conflicts with stored identity')
                    definition_ids[key] = row['definition_id']
                else:
                    cursor = self.connection.execute('''INSERT INTO definitions
                        (model_revision,contract_version,template_id,source_family_json,definition_json)
                        VALUES (?,?,?,?,?)''', (*key, schema.encode(definition['source_family']), encoded))
                    definition_ids[key] = cursor.lastrowid
            self.connection.execute('INSERT INTO diagnostics VALUES (?,?,?,?,?,?,?,?,?)',
                (run_id, ordinal, definition_ids[key], identity_digest(record.values),
                 schema.encode(record.values), record.match_status, record.occurrence_count,
                 record.error_type, schema.encode(record.provenance)))

    def _remove_owned_directory(self, directory):
        """Bounded two-file cleanup; never recursive and never follows links."""
        if not directory.exists():
            return
        root = self.review_root.resolve()
        if directory.is_symlink() or not directory.resolve().is_relative_to(root):
            raise ValueError('cleanup path escapes review ownership')
        children = list(directory.iterdir())
        if any(p.name not in (review.LOG_NAME, review.MANIFEST_NAME)
               or not p.is_file() or p.is_symlink() for p in children):
            raise ValueError('unexpected contents; cleanup refused')
        for child in children:
            child.unlink()
        directory.rmdir()

    def cleanup_unaccepted(self, run_id: str) -> bool:
        """Explicit post-failure cleanup; accepted Run shards are always refused.

        Reopen after uncertain commit/recovery. Takes the same SQLite writer lock,
        checks identity if a manifest exists, deletes only the two known files.
        """
        if not re.fullmatch(r'\d{8}-[A-Z0-9]{6}', run_id) or self.connection.in_transaction:
            raise ValueError('valid Run ID and idle connection required')
        self.connection.execute('BEGIN IMMEDIATE')
        try:
            if self.get_run(run_id) is not None:
                raise ValueError('accepted Run shard cannot be cleaned as an orphan')
            directory = self.review_root / run_id
            manifest_path = directory / review.MANIFEST_NAME
            if manifest_path.exists():
                manifest = json.loads(manifest_path.read_bytes())
                if (manifest['run_id'] != run_id or
                        manifest['lineage']['database_id'] != self._metadata['database_id']):
                    raise ValueError('orphan manifest identity differs')
            existed = directory.exists()
            self._remove_owned_directory(directory)
            return existed
        finally:
            self.connection.rollback()

    def cleanup_staging(self, stage_name: str) -> None:
        """Remove one identified interrupted stage ONLY with all writers stopped.

        Staging precedes the SQL transaction, so a SQL lock cannot prove a stage
        is abandoned. Caller owns the quiescence requirement; never sweep by age.
        """
        if not re.fullmatch('[0-9a-f]{32}', stage_name):
            raise ValueError('explicit staging directory name required')
        self._remove_owned_directory(self.review_root / '.staging' / stage_name)
