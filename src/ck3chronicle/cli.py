"""ck3chronicle CLI entry point."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _spool_once(
    args: argparse.Namespace,
    abort_if=None,
    *,
    capture_metadata: dict[str, object] | None = None,
    crash_folder: Path | None = None,
    include_debug: bool = False,
    on_logs_copied=None,
):
    from . import config
    from .harvester import spool_logs

    logs_root = Path(args.logs) if args.logs else config.ROOT_LOGS
    return spool_logs(
        logs_root,
        config.ROOT_CK3CHRONICLE,
        abort_if=abort_if,
        capture_metadata=capture_metadata,
        crash_folder=crash_folder,
        include_debug=include_debug,
        on_logs_copied=on_logs_copied,
    )


def _print_pending_result(result) -> None:
    print(f"protected pending capture: {result.dest_dir}")
    print(
        f"copied {result.files_copied} evidence file(s); "
        "hashing and SQLite deferred"
    )


def _capture_error(exc: Exception) -> int:
    from .harvester import (
        ArchiveIntegrityError,
        InvalidCaptureInput,
        UnstableCapture,
    )

    if isinstance(exc, InvalidCaptureInput):
        print(f"ERROR [invalid_input]: {exc}", file=sys.stderr)
        return 2
    if isinstance(exc, UnstableCapture):
        print(f"ERROR [rejected_unstable]: {exc}", file=sys.stderr)
        return 3
    if isinstance(exc, ArchiveIntegrityError):
        print(f"ERROR [archive_integrity]: {exc}", file=sys.stderr)
        return 3
    print(f"ERROR: {exc}", file=sys.stderr)
    return 1


def cmd_capture(args: argparse.Namespace) -> int:
    """Immediately protect logs without hashing, parsing, or SQLite."""
    from . import config
    from .watcher import is_process_running

    try:
        if is_process_running("ck3.exe"):
            print(
                "ERROR: ck3.exe is running; refusing to copy a live session",
                file=sys.stderr,
            )
            return 3
        result = _spool_once(
            args,
            abort_if=lambda: is_process_running("ck3.exe"),
            capture_metadata={
                "trigger": "manual_capture",
                "termination_kind": "unknown",
            },
        )
    except Exception as exc:
        return _capture_error(exc)
    _print_pending_result(result)
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    """Observe exact CK3 lifecycles and protect logs after process exit."""
    from datetime import datetime, timezone

    from . import config
    from .harvester import write_playset_template
    from .playset import PLAYSET_FILENAME, extract_playset
    from .watcher import (
        EventJournal,
        WatcherLease,
        find_process,
        infer_termination_from_crashes,
        is_process_running,
        scan_crash_inventory,
        watch_sessions,
    )

    logs_root = (Path(args.logs) if args.logs else config.ROOT_LOGS).resolve()
    crashes_root = config.ROOT_CRASHES.resolve()
    runtime_root = config.ROOT_CK3CHRONICLE.resolve()
    crash_baseline = None
    observed_started_at = None
    observed_ended_at = None
    inferred_termination = "unknown"
    inferred_crash = None

    def annotate_failure(
        exc: Exception,
        *,
        stage: str,
        reason_code: str,
        paths: dict[str, str | None],
    ) -> None:
        setattr(exc, "watcher_stage", stage)
        setattr(exc, "watcher_error_code", reason_code)
        existing = getattr(exc, "watcher_context", None)
        context = dict(existing) if isinstance(existing, dict) else {}
        capture_context = getattr(exc, "capture_context", None)
        if isinstance(capture_context, dict):
            context.update(capture_context)
        context.update(paths)
        setattr(exc, "watcher_context", context)
    if args.once:
        try:
            if is_process_running(args.process_name):
                print(
                    f"ERROR: {args.process_name} is running; close CK3 before one-shot capture",
                    file=sys.stderr,
                )
                return 3
            result = _spool_once(
                args,
                abort_if=lambda: is_process_running(args.process_name),
                capture_metadata={
                    "trigger": "manual_capture",
                    "termination_kind": "unknown",
                },
            )
        except Exception as exc:
            return _capture_error(exc)
        _print_pending_result(result)
        return 0

    captured_template = None

    def create_captured_playset(directory: Path, capture_id: str, captured_at: str) -> None:
        nonlocal captured_template
        context = {"capture_id": capture_id, "staging_dir": str(directory)}
        stage = "extract_playset"
        try:
            members = extract_playset(
                directory / "debug.log",
                roots={
                    "ROOT_GAME": config.ROOT_GAME,
                    "ROOT_STEAM": config.ROOT_STEAM,
                    "ROOT_LOCAL_MODS": config.ROOT_LOCAL_MODS,
                },
                on_warning=lambda warning: lifecycle_event(
                    "playset_metadata_warning", {**context, **warning}
                ),
            )
            stage = "write_playset_template"
            captured_template = write_playset_template(
                directory, captured_at=captured_at, members=members
            )
        except Exception as exc:
            lifecycle_event("playset_template_failed", {
                **context, "stage": stage, "error_type": type(exc).__name__,
                "error": str(exc), "status": "raw_pair_retained",
            })

    def perform_capture(trigger: str, process):
        nonlocal captured_template
        captured_template = None
        termination = inferred_termination if trigger == "process_exit" else "unknown"
        crash = inferred_crash if trigger == "process_exit" else None
        crash_folder = (
            Path(str(crash["folder_path"]))
            if termination == "crash"
            and isinstance(crash, dict)
            and crash.get("folder_path")
            else None
        )
        metadata = {
            "trigger": trigger,
            "process": process.as_dict() if process is not None else None,
            "observed_started_at": (
                observed_started_at if trigger == "process_exit" else None
            ),
            "observed_ended_at": (
                observed_ended_at if trigger == "process_exit" else None
            ),
            "termination_kind": termination,
            "crash": crash,
        }
        try:
            result = _spool_once(
                args,
                abort_if=lambda: find_process(args.process_name) is not None,
                capture_metadata=metadata,
                crash_folder=crash_folder,
                include_debug=True,
                on_logs_copied=create_captured_playset,
            )
        except Exception as exc:
            reason_code = {
                "InvalidCaptureInput": "capture_input_invalid",
                "UnstableCapture": "capture_source_unstable",
            }.get(type(exc).__name__, "capture_copy_failed")
            annotate_failure(
                exc,
                stage=getattr(exc, "capture_stage", "copy_live_logs"),
                reason_code=reason_code,
                paths={
                    "logs_root": str(logs_root),
                    "runtime_root": str(runtime_root),
                    "pending_root": str(runtime_root / "pending"),
                },
            )
            raise
        if "debug.log" not in result.file_names:
            lifecycle_event("debug_capture_failed", {
                "capture_id": result.dest_dir.name,
                "pending_dir": str(result.dest_dir),
                "error_log_preserved": True,
                **(result.debug_capture_failure or {}),
            })
        if captured_template is not None:
            lifecycle_event("playset_template_created", {
                "capture_id": result.dest_dir.name,
                "path": str(result.dest_dir / PLAYSET_FILENAME),
                "error_log_sha256": captured_template.error_log_sha256,
                "debug_log_sha256": captured_template.debug_log_sha256,
                "log_pair_id": captured_template.log_pair_id,
                "member_count": len(captured_template.members),
            })
        lifecycle_event(
            "pending_capture_published",
            {
                "status": "published",
                "trigger": trigger,
                "termination_kind": (
                    termination if trigger == "process_exit" else "unknown"
                ),
                "paths": {
                    "logs_root": str(logs_root),
                    "runtime_root": str(runtime_root),
                    "pending_dir": str(result.dest_dir),
                    "capture_metadata": str(
                        result.dest_dir / "capture-metadata.json"
                    ),
                    "crash_folder": str(crash_folder) if crash_folder else None,
                },
                "files": [
                    {
                        "name": item.name,
                        "source": str(
                            (
                                crash_folder / "exception.txt"
                                if item.name == "crash/exception.txt"
                                and crash_folder is not None
                                else logs_root / item.name
                            )
                        ),
                        "pending": str(result.dest_dir / item.name),
                        "bytes": item.bytes,
                        "source_mtime_ns": item.source_mtime_ns,
                    }
                    for item in result.file_stats
                ],
            },
        )
        return result

    path_authority = {
        "config": {
            "path": str(config.CONFIG_FILE_PATH),
            "authority": "project_config_bootstrap",
            "exists": config.CONFIG_FILE_PATH.is_file(),
            "kind": "file",
        },
        "logs_root": {
            "path": str(logs_root),
            "authority": "paths.root_logs" if not args.logs else "cli.--logs",
            "exists": logs_root.exists(),
            "is_directory": logs_root.is_dir(),
        },
        "crashes_root": {
            "path": str(crashes_root),
            "authority": "paths.root_crashes",
            "exists": crashes_root.exists(),
            "is_directory": crashes_root.is_dir(),
        },
        "runtime_root": {
            "path": str(runtime_root),
            "authority": "paths.root_ck3chronicle",
            "exists": runtime_root.exists(),
            "is_directory": runtime_root.is_dir(),
        },
        "pending_root": {
            "path": str(runtime_root / "pending"),
            "authority": "runtime_layout.pending",
            "exists": (runtime_root / "pending").exists(),
            "is_directory": (runtime_root / "pending").is_dir(),
        },
        "watch_root": {
            "path": str(runtime_root / "watch"),
            "authority": "runtime_layout.watch",
            "exists": (runtime_root / "watch").exists(),
            "is_directory": (runtime_root / "watch").is_dir(),
        },
        "heartbeat": {
            "path": str(runtime_root / "watch" / "watcher-heartbeat.json"),
            "authority": "runtime_layout.watcher_heartbeat",
            "exists": (runtime_root / "watch" / "watcher-heartbeat.json").exists(),
            "kind": "replaceable_file",
        },
        "lease": {
            "path": str(runtime_root / "watch" / "watcher.lock"),
            "authority": "runtime_layout.watcher_lease",
            "exists": (runtime_root / "watch" / "watcher.lock").is_file(),
            "kind": "locked_file",
        },
    }

    try:
        with WatcherLease(runtime_root) as lease, EventJournal(runtime_root) as journal:
            path_authority.update(
                {
                    "event_journal": {
                        "path": str(journal.path),
                        "authority": "runtime_layout.watch_event_journal",
                        "exists": journal.path.is_file(),
                        "kind": "file",
                    },
                    "heartbeat": {
                        "path": str(journal.heartbeat_path),
                        "authority": "runtime_layout.watcher_heartbeat",
                        "exists": journal.heartbeat_path.exists(),
                        "kind": "replaceable_file",
                    },
                    "lease": {
                        "path": str(lease.path),
                        "authority": "runtime_layout.watcher_lease",
                        "exists": lease.path.is_file(),
                        "kind": "locked_file",
                    },
                }
            )
            journal.emit(
                "watcher_paths_resolved",
                {
                    "status": "resolved",
                    "process_name": args.process_name,
                    "paths": path_authority,
                },
            )

            def record_crash_inventory(stage: str):
                inventory = scan_crash_inventory(crashes_root)
                journal.emit(
                    (
                        "crash_inventory_completed"
                        if inventory.available
                        else "crash_inventory_failed"
                    ),
                    {
                        "status": "available" if inventory.available else "failed_closed",
                        "stage": stage,
                        "process_name": args.process_name,
                        "operational_roots": {
                            "config": str(config.CONFIG_FILE_PATH),
                            "logs_root": str(logs_root),
                            "crashes_root": str(crashes_root),
                            "runtime_root": str(runtime_root),
                        },
                        **inventory.event_fields(),
                    },
                )
                return inventory

            def lifecycle_event(event: str, fields: dict) -> None:
                nonlocal crash_baseline
                nonlocal observed_started_at, observed_ended_at
                nonlocal inferred_termination, inferred_crash
                fields.setdefault("process_name", args.process_name)
                if event.endswith("_failed") or event in {
                    "capture_failed",
                    "probe_failed",
                }:
                    fields.setdefault(
                        "operational_roots",
                        {
                            "config": str(config.CONFIG_FILE_PATH),
                            "logs_root": str(logs_root),
                            "crashes_root": str(crashes_root),
                            "runtime_root": str(runtime_root),
                        },
                    )
                if event == "game_started" or (
                    event == "watcher_started"
                    and fields.get("state") == "attached_to_existing_process"
                ):
                    observed_started_at = datetime.now(timezone.utc).isoformat()
                    observed_ended_at = None
                    crash_baseline = record_crash_inventory("process_started")
                    inferred_termination = "unknown"
                    inferred_crash = None
                elif event == "game_exited":
                    observed_ended_at = datetime.now(timezone.utc).isoformat()
                    current_inventory = record_crash_inventory("process_exited")
                    inferred_termination, inferred_crash = infer_termination_from_crashes(
                        crash_baseline,
                        current_inventory,
                    )
                    if inferred_termination == "unknown":
                        journal.emit(
                            "termination_inference_failed",
                            {
                                "status": "failed_closed",
                                "reason_code": "crash_inventory_unavailable",
                                "process_name": args.process_name,
                                "paths": {"crashes_root": str(crashes_root)},
                                "operational_roots": {
                                    "config": str(config.CONFIG_FILE_PATH),
                                    "logs_root": str(logs_root),
                                    "crashes_root": str(crashes_root),
                                    "runtime_root": str(runtime_root),
                                },
                                "baseline_available": bool(
                                    crash_baseline and crash_baseline.available
                                ),
                                "current_available": current_inventory.available,
                            },
                        )
                elif event == "process_replaced":
                    observed_started_at = datetime.now(timezone.utc).isoformat()
                    observed_ended_at = None
                    crash_baseline = record_crash_inventory("process_replaced")
                    inferred_termination = "unknown"
                    inferred_crash = None
                journal.emit(event, fields)

            from .watcher_processing import WatcherProcessing

            processing = WatcherProcessing(runtime_root / "pending", config.watcher_settings(), journal.emit)
            try:
                processing.start()
                watch_sessions(
                    logs_root=logs_root,
                    capture=perform_capture,
                    process_probe=lambda: find_process(args.process_name),
                    event_sink=lifecycle_event,
                    on_capture=processing.on_capture,
                    on_tick=processing.tick,
                    poll_seconds=args.poll_seconds,
                    heartbeat_seconds=args.heartbeat_seconds,
                )
            except KeyboardInterrupt:
                journal.emit("watcher_interrupted", {"status": "stopped"})
            except Exception as exc:
                journal.emit("watcher_failed", {
                    "status": "failed_closed",
                    "stage": getattr(exc, "watcher_stage", "watcher_runtime"),
                    "reason_code": getattr(exc, "watcher_error_code", "watcher_runtime_failed"),
                    "error_type": type(exc).__name__, "error": str(exc),
                    "paths": path_authority,
                })
                return 1
            finally:
                processing.close()
    except Exception as exc:
        # Startup/lease failures need a journal too, but this process must not
        # remove the heartbeat belonging to a watcher that already owns the lease.
        try:
            with EventJournal(runtime_root, cleanup_heartbeat=False) as failed_journal:
                failed_journal.emit("watcher_failed", {
                    "stage": "watcher_startup", "status": "failed_closed",
                    "error_type": type(exc).__name__, "error": str(exc),
                    "paths": path_authority,
                })
        except Exception as logging_error:
            print(f"ERROR: watcher startup failed: {exc}; runtime logging unavailable: {logging_error}",
                  file=sys.stderr)
        return 1
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    from .doctor import run_doctor

    run_doctor()
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    from .pipeline.ingestion import ingest
    from .pipeline.request_handler import COMPLETED
    from .pipeline.schema import encode

    try:
        result = ingest(Path(args.database), capture_directory=args.capture_directory,
                        error_log=args.error_log, captures_root=args.captures_root,
                        package_id=args.package_id)
    except Exception as exc:
        # Admission or result retrieval failed; neither supplies a request outcome.
        print(encode(dict(error=str(exc), exception_class=type(exc).__name__)), file=sys.stderr)
        return 1
    print(encode(dict(status=result.status, run_id=result.run_id,
                      log_sha256=result.log_sha256, warnings=list(result.warnings),
                      error=result.error, exception_class=result.exception_class, details=result.details,
                      capture_directory=str(result.capture_directory) if result.capture_directory else None)))
    return 0 if result.status == COMPLETED else 1


def cmd_runs(args: argparse.Namespace) -> int:
    from .reporting.cli import cmd_runs as run
    return run(args)


def cmd_report(args: argparse.Namespace) -> int:
    from .reporting.cli import cmd_report as run
    return run(args)


def _register_reporting(sub):
    runs = sub.add_parser('runs', help='List all package Runs by Run ID, including unavailable source dates.')
    runs.add_argument('--database', type=Path, help='Existing database; defaults to watcher.database in current config.')
    runs.add_argument('--package-id', required=True, help='Explicit stored processing package.')
    runs.add_argument('--format', choices=('text', 'json'), default='text')
    runs.add_argument('--offset', type=int, default=0)
    runs.add_argument('--limit', type=int, default=50)
    runs.add_argument('--output', type=Path, help='UTF-8 destination; default stdout.')
    runs.set_defaults(func=cmd_runs)
    _add_foreground_logging(runs)
    report = sub.add_parser('report', help='Investigate stored diagnostics and current candidate sources.')
    report.add_argument('run', help='Run ID or latest (latest requires --package-id).')
    report.add_argument('--database', type=Path, help='Existing database; defaults to watcher.database in current config.')
    report.add_argument('--package-id', help="Processing package; a named Run's stored lineage may supply it.")
    mode = report.add_mutually_exclusive_group(required=True)
    mode.add_argument('--preset', choices=('hotspots', 'frequent', 'syntax', 'new', 'symbol'))
    mode.add_argument('--custom', action='store_true', help='Explicit non-preset investigation; requires --query.')
    report.add_argument('--query', type=Path, help='Validated structured JSON query/refinement.')
    report.add_argument('--format', choices=('text', 'json', 'html'), default='text')
    report.add_argument('--output', type=Path, help='UTF-8 destination; required for HTML.')
    report.add_argument('--limit', type=int, help='Current and per-Run display limit; default 50.')
    report.add_argument('--historical-limit', type=int, help='Separate previously observed display limit; default 20.')
    report.add_argument('--no-history', action='store_true', help='Omit recent-Run comparisons (conflicts with new/trailing queries).')
    report.add_argument('--verbose', action='store_true', help='Numbered source excerpts; HTML writes a linked appendix.')
    report.add_argument('--source-context', type=Path, help='Optional source-selection JSON, separate from required scope.source.')
    report.add_argument('--source-root', action='append', help='Optional absolute source root; repeat to preserve caller order.')
    report.add_argument('--source-directory', action='append', help='Optional directory relative to each context root.')
    report.add_argument('--no-recursive', action='store_true', help='Optional context: enumerate selected directories only.')
    report.add_argument('--ripgrep', default='rg', help='Source library content-search executable.')
    report.set_defaults(func=cmd_report)
    _add_foreground_logging(report)


def _add_foreground_logging(parser):
    parser.add_argument('--log-dir', type=Path,
                        help='Invocation journal directory; defaults to configured runtime logging.')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ck3chronicle",
        description=(
            "CK3 log memory — preserve and triage "
            "Crusader Kings III runtime logs."
        ),
    )

    sub = parser.add_subparsers(dest="command", required=True)

    _register_reporting(sub)

    p_ingest = sub.add_parser('ingest', help='Store a completed capture or explicit manual error log.')
    inputs = p_ingest.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--capture-directory', type=Path)
    inputs.add_argument('--error-log', type=Path)
    p_ingest.add_argument('--database', required=True, help='Explicit existing SQLite database file.')
    p_ingest.add_argument('--captures-root', type=Path, help='Pending directory for an unprotected manual log.')
    p_ingest.add_argument('--package-id', help='Retained executable package; omission uses catalog default.')
    p_ingest.set_defaults(func=cmd_ingest)
    _add_foreground_logging(p_ingest)

    p_capture = sub.add_parser(
        "capture",
        help="Copy error.log to the pending queue; defer hashing and SQLite.",
    )

    p_capture.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")

    p_capture.set_defaults(func=cmd_capture)
    _add_foreground_logging(p_capture)

    p_watch = sub.add_parser(
        "watch",
        help="Protect error.log/debug.log and their hashed playset after CK3 exits; journal outcomes.",
    )

    p_watch.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")

    p_watch.add_argument(
        "--process-name", default="ck3.exe", help="Exact CK3 process name."
    )

    p_watch.add_argument("--poll-seconds", type=float, default=0.5, metavar="N")

    p_watch.add_argument(
        "--heartbeat-seconds",
        type=float,
        default=30.0,
        metavar="N",
        help="Write an auditable watcher heartbeat every N seconds.",
    )

    p_watch.add_argument(
        "--once",
        action="store_true",
        help="Copy the current completed-session logs once, then exit.",
    )

    p_watch.set_defaults(func=cmd_watch)

    p_doctor = sub.add_parser("doctor", help="Health check.")

    p_doctor.set_defaults(func=cmd_doctor)
    _add_foreground_logging(p_doctor)

    return parser


def _foreground(args: argparse.Namespace):
    """Own one foreground stream; component return codes remain authoritative."""
    from uuid import uuid4
    from . import config, runtime_logging as backend

    invocation_id = uuid4().hex
    directory = (args.log_dir.expanduser().resolve() if args.log_dir is not None
                 else config.ROOT_CK3CHRONICLE / 'logging')
    destination = backend.invocation_log_path(directory, args.command, invocation_id)
    handler = backend.configure_runtime_logging(destination=destination,
                                                settings=backend.logging_settings())
    logger = backend.get_logger('cli')
    try:
        with backend.log_context(invocation_id=invocation_id, foreground_invocation=True):
            backend.event(logger, 'invocation_started', operation=args.command,
                          source_file=__file__, journal_path=str(destination))
            try:
                result = args.func(args)
            except BaseException as error:
                if isinstance(error, SystemExit):
                    fields = dict(outcome='success' if error.code in (None, 0) else 'nonzero_exit',
                                  exit_code=error.code)
                else:
                    fields = dict(outcome='interrupted' if isinstance(error, KeyboardInterrupt) else 'failed',
                                  exception_class=type(error).__name__)
                backend.event(logger, 'invocation_finished', **fields,
                              exc_info=not isinstance(error, (SystemExit, KeyboardInterrupt)))
                raise
            else:
                backend.event(logger, 'invocation_finished',
                              outcome='success' if result in (None, 0) else 'nonzero_exit',
                              exit_code=result)
                return result
    finally:
        try:
            backend.close_runtime_logging(handler)
        except BaseException:
            pass


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command in {'capture', 'ingest', 'runs', 'report', 'doctor'}:
        sys.exit(_foreground(args))
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
