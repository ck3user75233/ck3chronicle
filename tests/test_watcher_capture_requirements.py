"""Requirement-derived checks for the narrow watcher/capture boundary."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from ck3chronicle import harvester
from ck3chronicle.harvester import (
    CAPTURE_METADATA_NAME,
    UnstableCapture,
    spool_logs,
)
from ck3chronicle.watcher import (
    CrashInventory,
    ProcessIdentity,
    scan_crash_inventory,
    watch_sessions,
)


class CaptureBoundaryTests(unittest.TestCase):
    def test_default_manual_capture_contains_error_log_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            runtime = root / "runtime"
            logs.mkdir()
            (logs / "error.log").write_text(
                "[00:00:01][pdx.cpp:1]: one\n", encoding="utf-8"
            )
            (logs / "debug.log").write_text("debug\n", encoding="utf-8")
            (logs / "game.log").write_text("game\n", encoding="utf-8")

            result = spool_logs(
                logs,
                runtime,
                capture_metadata={
                    "trigger": "process_exit",
                    "termination_kind": "normal",
                },
            )

            self.assertEqual(result.file_names, ("error.log",))
            self.assertTrue((result.dest_dir / "error.log").is_file())
            self.assertFalse((result.dest_dir / "debug.log").exists())
            self.assertFalse((result.dest_dir / "game.log").exists())
            metadata = json.loads(
                (result.dest_dir / CAPTURE_METADATA_NAME).read_text(encoding="utf-8")
            )
            self.assertEqual(metadata["trigger"], "process_exit")
            self.assertEqual(metadata["termination_kind"], "normal")

    @unittest.skipUnless(os.name == "nt", "NTFS ACL requirement is Windows-only")
    def test_published_capture_inherits_pending_directory_acl(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            runtime = root / "runtime"
            logs.mkdir()
            (logs / "error.log").write_text(
                "[00:00:01][pdx.cpp:1]: one\n", encoding="utf-8"
            )

            result = spool_logs(logs, runtime)
            environment = os.environ.copy()
            environment["CK3CHRONICLE_ACL_PATH"] = str(result.dest_dir)
            powershell = shutil.which("pwsh") or shutil.which("powershell.exe")
            self.assertIsNotNone(powershell)
            acl = subprocess.run(
                [
                    powershell,
                    "-NoProfile",
                    "-Command",
                    "(Get-Acl -LiteralPath $env:CK3CHRONICLE_ACL_PATH)."
                    "AreAccessRulesProtected",
                ],
                capture_output=True,
                text=True,
                env=environment,
            )

            self.assertEqual(acl.returncode, 0, msg=acl.stderr)
            self.assertEqual(acl.stdout.strip(), "False")

    def test_pair_callback_sees_full_copies_and_metadata_before_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            logs.mkdir()
            contents = {"error.log": b"error\r\n", "debug.log": b"debug\r\n\x00all original bytes"}
            for name, raw in contents.items():
                (logs / name).write_bytes(raw)
            callbacks = []

            def after_copies(directory, capture_id, captured_at):
                self.assertTrue(directory.name.startswith(".copying-"))
                self.assertFalse((root / "runtime" / "pending" / capture_id).exists())
                for name, raw in contents.items():
                    self.assertEqual((directory / name).read_bytes(), raw)
                metadata = json.loads((directory / CAPTURE_METADATA_NAME).read_text(encoding="utf-8"))
                self.assertEqual(metadata["captured_at"], captured_at)
                self.assertEqual(metadata["capture_id"], capture_id)
                callbacks.append(capture_id)

            result = spool_logs(logs, root / "runtime", include_debug=True, on_logs_copied=after_copies)
            self.assertEqual(callbacks, [result.dest_dir.name])
            self.assertEqual(result.file_names, ("error.log", "debug.log"))
            self.assertEqual(result.files_copied, 2)

    def test_debug_copy_failure_preserves_error_and_does_not_call_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            logs.mkdir()
            (logs / "error.log").write_bytes(b"error")
            (logs / "debug.log").write_bytes(b"debug")
            copy = harvester._copy_exact

            def fail_debug(source, target):
                if source.name == "debug.log":
                    raise PermissionError("cannot copy debug")
                return copy(source, target)

            callback = Mock()
            with patch.object(harvester, "_copy_exact", side_effect=fail_debug):
                result = spool_logs(logs, root / "runtime", include_debug=True, on_logs_copied=callback)
                callback.assert_not_called()
            self.assertEqual(result.debug_capture_failure['error_type'], 'PermissionError')
            self.assertEqual((result.dest_dir / "error.log").read_bytes(), b"error")
            self.assertFalse(result.dest_dir.name.startswith(".copying-"))
            self.assertFalse((result.dest_dir / "debug.log").exists())

    def test_unavailable_exception_does_not_discard_error_log(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            runtime = root / "runtime"
            crash = root / "ck3_20260908_010203"
            logs.mkdir()
            crash.mkdir()
            (logs / "error.log").write_text(
                "[00:00:01][pdx.cpp:1]: one\n", encoding="utf-8"
            )
            (crash / "exception.txt").write_text("exception\n", encoding="utf-8")

            exact_copy = harvester._copy_exact

            def deny_exception(source: Path, target: Path) -> None:
                if source.name == "exception.txt":
                    raise PermissionError("simulated attachment denial")
                exact_copy(source, target)

            with patch(
                "ck3chronicle.harvester._copy_exact",
                side_effect=deny_exception,
            ):
                result = spool_logs(logs, runtime, crash_folder=crash)

            self.assertTrue((result.dest_dir / "error.log").is_file())
            self.assertFalse((result.dest_dir / "crash" / "exception.txt").exists())
            metadata = json.loads(
                (result.dest_dir / CAPTURE_METADATA_NAME).read_text(encoding="utf-8")
            )
            self.assertEqual(metadata["crash_exception"]["status"], "unavailable")

    def test_error_log_change_during_copy_is_not_published(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            runtime = root / "runtime"
            logs.mkdir()
            source = logs / "error.log"
            source.write_text(
                "[00:00:01][pdx.cpp:1]: one\n",
                encoding="utf-8",
            )
            exact_copy = harvester._copy_exact

            def mutate_source(copied_from: Path, copied_to: Path) -> None:
                exact_copy(copied_from, copied_to)
                copied_from.write_text(
                    "[00:00:01][pdx.cpp:1]: changed\n",
                    encoding="utf-8",
                )

            with patch(
                "ck3chronicle.harvester._copy_exact",
                side_effect=mutate_source,
            ):
                with self.assertRaises(UnstableCapture):
                    spool_logs(logs, runtime)

            published = [
                child
                for child in (runtime / "pending").iterdir()
                if child.is_dir() and not child.name.startswith(".copying-")
            ]
            self.assertEqual(published, [])


class WatcherLifecycleTests(unittest.TestCase):
    def test_only_an_observed_exit_triggers_capture(self) -> None:
        process = ProcessIdentity(123, "ck3.exe", 456)
        observations = iter((None, process, process, None))
        events: list[str] = []
        captures: list[tuple[str, ProcessIdentity | None]] = []
        exhausted = False

        def probe() -> ProcessIdentity | None:
            nonlocal exhausted
            try:
                return next(observations)
            except StopIteration:
                exhausted = True
                return None

        count = watch_sessions(
            logs_root=Path("logs"),
            capture=lambda trigger, identity: captures.append((trigger, identity)),
            process_probe=probe,
            event_sink=lambda event, _fields: events.append(event),
            stop_requested=lambda: exhausted,
            sleep=lambda _seconds: None,
            heartbeat_seconds=60.0,
        )

        self.assertEqual(count, 1)
        self.assertEqual(captures, [("process_exit", process)])
        self.assertIn("game_started", events)
        self.assertIn("game_exited", events)

    def test_crash_inventory_ignores_unrelated_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "ck3_20260908_010203").mkdir()
            (root / "unrelated-tool-output").mkdir()

            inventory: CrashInventory = scan_crash_inventory(root)

            self.assertTrue(inventory.available)
            self.assertEqual(
                tuple(name for name, _mtime_ns in inventory.folders),
                ("ck3_20260908_010203",),
            )


if __name__ == "__main__":
    unittest.main()
