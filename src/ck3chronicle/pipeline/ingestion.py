"""Application ingest composition over the existing classifier/storage boundary."""
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import time

from ck3chronicle import harvester
from ck3chronicle.runtime_logging import event, get_logger
from . import catalog, contracts
from .aggregation import RecordAccumulator
from .capture_access import CaptureBusyError, capture_access, completed_directory, regular_file
from .domain import RunAccounting, ReviewMetadata, RunResult
from .model import read_json
from .playsets import PlaysetError, stored_playset
from .repository import DuplicateRunError
from .request_handler import COMPLETED, NOT_COMPLETED, HandlerClient
from .review import ReviewWriter
from .schema import encode

logger = get_logger('preparation')


class IngestInputError(ValueError):
    """Invalid or changing input; protected evidence remains in place."""


@dataclass(frozen=True)
class IngestResult:
    status: str
    run_id: str | None = None
    log_sha256: str | None = None
    capture_directory: Path | None = None
    stored: RunResult | None = None
    warnings: tuple[str, ...] = ()
    error: str | None = None
    exception_class: str | None = None
    details: dict | None = None


def application_revision() -> str:
    """Fingerprint actual application source, including dirty/installed code."""
    root = Path(__file__).resolve().parents[1]
    sources = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(root.rglob('*.py'))}
    return 'application-source-sha256:' + hashlib.sha256(encode(sources).encode('ascii')).hexdigest()


def _protect_manual(path: Path, captures_root: Path) -> Path:
    """Reuse capture's stable copy and inherited-ACL staging for an explicit file."""
    regular_file(path)
    if path.stat().st_size == 0:
        raise IngestInputError('manual error log is empty')
    root = Path(captures_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    stage = harvester._make_inheriting_staging_directory(root, '.copying-')
    now = datetime.now(timezone.utc)
    name = now.strftime('%Y%m%dT%H%M%S.%fZ') + '-' + stage.name.removeprefix('.copying-')
    try:
        harvester._copy_stable_without_hash(path, stage / 'error.log')
        metadata = dict(schema_version=1, capture_id=name, captured_at=now.isoformat(),
                        trigger='manual_ingest', manual_input=str(path))
        (stage / 'capture-metadata.json').write_text(encode(metadata) + '\n', encoding='utf-8')
        stage.rename(root / name)
    except Exception as exc:
        setattr(exc, 'capture_directory', stage)
        raise
    return root / name


def _read_playset(directory, metadata, digest):
    path = directory / 'playset.json'
    if not path.exists() and not path.is_symlink():
        return None
    try:
        value = read_json(regular_file(path).read_bytes())
        if value is None:
            raise PlaysetError('completed playset must be an object')
        stored_playset(value, error_log_sha256=digest)
        if value['captured_at'] != metadata.get('captured_at'):
            raise PlaysetError('playset capture time mismatch')
        if harvester.hash_file(regular_file(directory / 'debug.log')) != value['debug_log_sha256']:
            raise PlaysetError('playset debug-log hash mismatch')
        return value
    except (OSError, ValueError, UnicodeError) as exc:
        raise PlaysetError(f'{path}: {exc}') from exc


def ingest(database: Path, *, capture_directory: Path | None = None,
           error_log: Path | None = None, captures_root: Path | None = None,
           package_id: str | None = None) -> IngestResult:
    """Submit to the shared handler and wait for a three-state terminal result.

    database is the exact existing SQLite file. Admission failures raise directly;
    accepted request failures return NOT_COMPLETED with ordinary error information.
    For nonblocking application use, HandlerClient.submit('ingest', arguments).
    """
    client = HandlerClient(database)
    ref = client.submit('ingest', dict(capture_directory=capture_directory,
        error_log=error_log, captures_root=captures_root, package_id=package_id))
    return ingest_result(client.result(ref))


def ingest_result(outcome) -> IngestResult:
    """Decode the ingestion value returned by a request reference."""
    if outcome.value is None:
        directory = (outcome.details or {}).get('capture_directory')
        return IngestResult(outcome.status, capture_directory=Path(directory) if directory else None,
                            warnings=tuple((outcome.details or {}).get('warnings', ())),
                            error=outcome.error, exception_class=outcome.exception_class, details=outcome.details)
    value = dict(outcome.value)
    if value['capture_directory']:
        value['capture_directory'] = Path(value['capture_directory'])
    value['warnings'] = tuple(value['warnings'])
    if value['stored']:
        stored = value['stored']
        value['stored'] = RunResult(**dict(stored, accounting=RunAccounting(**stored['accounting']),
                                          review=ReviewMetadata(**stored['review'])))
    return IngestResult(**value)


def _duplicate(run_id, digest, directory, warnings=()):
    return IngestResult(NOT_COMPLETED, run_id, digest, directory,
                        warnings=(*warnings, f'complete log already stored as {run_id}; duplicate ingestion not completed'))


@contextmanager
def _wait_for_capture(directory, stopping):
    waiting = None
    while True:
        access = capture_access(directory)
        try:
            access.__enter__()
            break
        except CaptureBusyError:
            if waiting is None:
                waiting = time.monotonic()
                event(logger, 'capture_wait_started', capture_directory=str(directory))
            if stopping.wait(.05):
                raise RuntimeError('handler shut down while waiting for capture')
    try:
        if waiting is not None:
            event(logger, 'capture_wait_resumed', capture_directory=str(directory),
                  elapsed_seconds=time.monotonic() - waiting)
        yield
    finally:
        access.__exit__(None, None, None)


def _ingest(database_call, stopping, *, capture_directory=None, error_log=None,
            captures_root=None, package_id=None) -> IngestResult:
    """Handler preparation only; all repository work uses its database queue."""
    started = time.monotonic()

    def prepared(directory):
        event(logger, 'preparation_completed',
              **({'capture_directory': str(directory)} if directory else {}),
              elapsed_seconds=time.monotonic() - started)

    if (capture_directory is None) == (error_log is None):
        raise IngestInputError('supply exactly one of capture_directory or error_log')
    if capture_directory is not None and captures_root is not None:
        raise IngestInputError('captures_root is only used to protect a manual input')
    if error_log is not None:
        path = Path(error_log).absolute()
        if path.name == 'error.log' and (path.parent / 'capture-metadata.json').exists():
            capture_directory = path.parent
        else:
            digest = harvester.hash_file(regular_file(path))
            existing = database_call('find_run_by_log_hash', dict(log_sha256=digest))
            if existing:
                prepared(None)
                return _duplicate(existing['run_id'], digest, None)
            if captures_root is None:
                raise IngestInputError('unprotected manual input requires captures_root')
            capture_directory = _protect_manual(path, captures_root)
    directory = completed_directory(capture_directory)
    warnings = ()
    try:
        with _wait_for_capture(directory, stopping):
            path = regular_file(directory / 'error.log')
            if path.stat().st_size == 0:
                raise IngestInputError('captured error log is empty')
            digest = harvester.hash_file(path)
            existing = database_call('find_run_by_log_hash', dict(log_sha256=digest))
            if existing:
                prepared(directory)
                return _duplicate(existing['run_id'], digest, directory)
            try:
                metadata = read_json(regular_file(directory / 'capture-metadata.json').read_bytes())
                if not isinstance(metadata, dict):
                    raise ValueError('capture metadata must be an object')
            except (OSError, ValueError) as exc:
                raise IngestInputError(str(exc)) from exc
            warnings = ()
            try:
                playset = _read_playset(directory, metadata, digest)
            except PlaysetError as exc:
                # Owner policy: the error log remains independently useful.
                # Preserve supplied JSON, expose the problem and store unknown
                # playset availability through the existing canonical model.
                warnings = (str(exc),)
                event(logger, 'ingestion_warning', level='WARNING',
                      capture_directory=str(directory), message=str(exc))
                playset = None
            classifier = catalog.load_selected_classifier(package_id=package_id)
            lineage = contracts.run_lineage(classifier.package,
                                            application_revision=application_revision())
            lineage.update(model_schema_version=classifier.package.manifest['model_schema_version'],
                           package_schema_version=classifier.package.manifest['schema_version'])
            raw = classifier.read_log(path)
            if hashlib.sha256(raw.source.data).hexdigest() != digest:
                raise IngestInputError('error log changed between hashing and parsing')
            definitions = contracts.materialize_definitions(classifier.package)
            accumulator = RecordAccumulator()
            writer = ReviewWriter(raw)
            for result in classifier.classify_raw(raw):
                if stopping.is_set():
                    raise RuntimeError('handler shut down during preparation')
                writer.observe(result)
                if result.disposition == 'record':
                    definition = definitions[result.selected.template_id]
                    accumulator.add(definition, contracts.prepare_record(definition, result))
            records = accumulator.records()
            prepared(directory)
            try:
                stored = database_call('write_run', dict(log_sha256=digest, facts=metadata, lineage=lineage,
                    records=records, review_writer=writer, playset=playset))
            except DuplicateRunError as exc:
                return _duplicate(exc.existing_run_id, digest, directory, warnings)
            return IngestResult(COMPLETED, stored.run_id, digest, directory, stored, warnings)
    except Exception as exc:
        setattr(exc, 'capture_directory', directory)
        setattr(exc, 'warnings', warnings)
        raise
