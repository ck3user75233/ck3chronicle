"""Checks of the production watcher playset producer and its output contract."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from ck3chronicle import cli, config, harvester, playset, watcher


def mount_line(path: Path) -> str:
    return f"[06:53:35][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: {path}\n"


class PlaysetFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.roots = {
            "ROOT_GAME": self.root / "game",
            "ROOT_STEAM": self.root / "workshop",
            "ROOT_LOCAL_MODS": self.root / "mod",
        }
        for path in self.roots.values():
            path.mkdir()
        self.logs = self.root / "logs"
        self.logs.mkdir()
        self.runtime = self.root / "runtime"
        self.error_bytes = b"[00:00:01][pdx.cpp:1]: one\r\n"
        (self.logs / "error.log").write_bytes(self.error_bytes)
        self.debug = self.logs / "debug.log"
        self.debug.write_text("unrelated debug output\n", encoding="utf-8")
        self.warnings = []

    def extract(self):
        return playset.extract_playset(self.debug, roots=self.roots, on_warning=self.warnings.append)

    def add_mod(self, root_id, folder, name=None):
        path = self.roots[root_id] / folder
        path.mkdir(parents=True)
        if name:
            (path / "descriptor.mod").write_text(f'name="{name}"\n', encoding="utf-8")
        return path


class PlaysetExtractionTests(PlaysetFixture):
    def test_mixed_mounts_keep_emission_order_and_descriptor_names(self):
        dlc = self.roots["ROOT_GAME"] / "dlc" / "dlc016_cp2"
        dlc.mkdir(parents=True)
        (dlc / "dlc016.dlc").write_text(
            '\ufeffname = "West Slavic Attire"\npath="dlc/dlc016_cp2"\npops_id="ck3_dlc016_cp2"',
            encoding="utf-8",
        )
        steam = self.add_mod("ROOT_STEAM", "3765169933", "地图颜色重整工具 - Map Color Reshaper")
        dev = self.add_mod("ROOT_LOCAL_MODS", "compat", "EB+EC724 Compatibility Patch")
        self.debug.write_text("prefix\n" + mount_line(dlc) + mount_line(steam) + mount_line(dev), encoding="utf-8")
        members = self.extract()
        self.assertEqual([m.load_order for m in members], [0, 1, 2, 3])
        self.assertEqual([m.name for m in members], ["CK3 Game Files", "West Slavic Attire", "地图颜色重整工具 - Map Color Reshaper", "EB+EC724 Compatibility Patch"])
        self.assertEqual([m.stable_id for m in members], ["ck3:1158310", "pops:ck3_dlc016_cp2", "steam_workshop:3765169933", None])
        self.assertEqual([m.path for m in members[1:]], [str(dlc), str(steam), str(dev)])
        self.assertEqual([m.root_ID for m in members], ["ROOT_GAME", "ROOT_GAME", "ROOT_STEAM", "ROOT_LOCAL_MODS"])
        self.assertEqual(self.warnings, [])

    def test_associated_workshop_descriptor_supplies_canonical_name(self):
        mod = self.add_mod("ROOT_STEAM", "2692957667")
        descriptor = self.roots["ROOT_LOCAL_MODS"] / "ugc_2692957667.mod"
        descriptor.write_text(f'name="Pervasive Crown Authority"\npath="{mod.as_posix()}"\nremote_file_id="2692957667"', encoding="utf-8")
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        member = self.extract()[1]
        self.assertEqual(member.name, "Pervasive Crown Authority")
        self.assertEqual(member.descriptor_path, str(descriptor))
        self.assertFalse(self.warnings)

    def test_associated_development_descriptor_with_relative_path(self):
        mod = self.add_mod("ROOT_LOCAL_MODS", "dev")
        descriptor = self.roots["ROOT_LOCAL_MODS"] / "dev.mod"
        descriptor.write_text('name="Development mod"\npath="mod/dev"', encoding="utf-8")
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        self.assertEqual(self.extract()[1].name, "Development mod")

    def test_descriptor_comments_escapes_bom_and_nested_fields(self):
        mod = self.add_mod("ROOT_LOCAL_MODS", "dev")
        (mod / "descriptor.mod").write_text(
            '\ufefftags={name="not the name" nested={foo="bar"}}\n# name="wrong"\nname = "A \\"quoted\\" # name"\n', encoding="utf-8"
        )
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        self.assertEqual(self.extract()[1].name, 'A "quoted" # name')

    def test_missing_external_path_retains_unknown_member_and_warns(self):
        missing = self.root / "elsewhere" / "missing"
        self.debug.write_text(mount_line(missing), encoding="utf-8")
        member = self.extract()[1]
        self.assertEqual(member.path, str(missing))
        self.assertEqual(member.name, "UNKNOWN")
        self.assertIsNone(member.root_ID)
        self.assertIn("mounted_path_unavailable", [w["reason_code"] for w in self.warnings])
        self.assertIn("descriptor_missing", [w["reason_code"] for w in self.warnings])

    def test_unfamiliar_mount_can_still_have_a_descriptor(self):
        external = self.root / "external"
        external.mkdir()
        (external / "descriptor.mod").write_text('name="External content"', encoding="utf-8")
        self.debug.write_text(mount_line(external), encoding="utf-8")
        member = self.extract()[1]
        self.assertEqual(member.name, "External content")
        self.assertIsNone(member.root_ID)

    def test_malformed_descriptor_does_not_discard_member(self):
        mod = self.add_mod("ROOT_LOCAL_MODS", "broken")
        (mod / "descriptor.mod").write_text('name="unterminated', encoding="utf-8")
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        self.assertEqual(self.extract()[1].name, "UNKNOWN")
        self.assertIn("descriptor_unreadable", [w["reason_code"] for w in self.warnings])

    def test_conflicting_workshop_id_is_logged_without_changing_membership(self):
        mod = self.add_mod("ROOT_STEAM", "123")
        (mod / "descriptor.mod").write_text('name="A mod"\nremote_file_id="456"', encoding="utf-8")
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        member = self.extract()[1]
        self.assertEqual(member.stable_id, "steam_workshop:123")
        self.assertEqual(member.name, "A mod")
        self.assertEqual(self.warnings[0]["reason_code"], "descriptor_id_mismatch")

    def test_missing_top_level_name_is_visible(self):
        mod = self.add_mod("ROOT_LOCAL_MODS", "nameless")
        (mod / "descriptor.mod").write_text('tags={name="nested"}', encoding="utf-8")
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        member = self.extract()[1]
        self.assertEqual(member.name, "UNKNOWN")
        self.assertIsNotNone(member.descriptor_path)
        self.assertEqual(self.warnings[0]["reason_code"], "descriptor_name_missing")

    def test_no_emissions_returns_base_and_visible_warning(self):
        self.assertEqual(len(self.extract()), 1)
        self.assertEqual(self.warnings[0]["reason_code"], "no_mount_emissions")

    def test_unreadable_mount_metadata_keeps_the_mounted_member(self):
        mod = self.add_mod("ROOT_LOCAL_MODS", "denied")
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        original = Path.is_dir

        def check(path):
            if path == mod:
                raise PermissionError("mounted directory is not readable")
            return original(path)

        with patch.object(Path, "is_dir", check):
            member = self.extract()[1]
        self.assertEqual(member.path, str(mod))
        self.assertEqual(member.name, "UNKNOWN")
        self.assertEqual(self.warnings[0]["reason_code"], "mounted_path_unavailable")


class PlaysetWriterTests(PlaysetFixture):
    def test_template_hashes_exact_bytes_once_and_derives_join(self):
        debug_bytes = b"unrelated\r\n" + "Unicode 字".encode("utf-8")
        self.debug.write_bytes(debug_bytes)
        members = self.extract()
        with patch.object(harvester, "hash_file", wraps=harvester.hash_file) as hashing:
            template = harvester.write_playset_template(self.logs, captured_at="2026-09-28T01:02:03+00:00", members=members)
        self.assertEqual(hashing.call_count, 2)
        data = json.loads((self.logs / "playset.json").read_text(encoding="utf-8"))
        self.assertEqual(data["error_log_sha256"], hashlib.sha256(self.error_bytes).hexdigest())
        self.assertEqual(data["debug_log_sha256"], hashlib.sha256(debug_bytes).hexdigest())
        self.assertEqual(data["log_pair_id"], f"sha256:{data['error_log_sha256']}:{data['debug_log_sha256']}")
        self.assertEqual(data, template.to_dict())
        self.assertEqual(set(data), {"schema_version", "captured_at", "error_log_sha256", "debug_log_sha256", "log_pair_id", "members"})
        self.assertEqual(set(data["members"][0]), {"load_order", "name", "path", "root_ID", "stable_id", "descriptor_path"})
        self.assertFalse((self.logs / ".playset.json.tmp").exists())

    def test_failed_atomic_template_publish_preserves_both_logs(self):
        debug_bytes = self.debug.read_bytes()
        with patch.object(Path, "replace", side_effect=PermissionError("cannot publish template")):
            with self.assertRaises(PermissionError):
                harvester.write_playset_template(self.logs, captured_at="now", members=self.extract())
        self.assertEqual((self.logs / "error.log").read_bytes(), self.error_bytes)
        self.assertEqual(self.debug.read_bytes(), debug_bytes)
        self.assertFalse((self.logs / "playset.json").exists())


class WatcherPlaysetIntegrationTests(PlaysetFixture):
    def run_watcher(self, failure_patch=None):
        args = argparse.Namespace(logs=str(self.logs), once=False, process_name="ck3.exe", poll_seconds=0.001, heartbeat_seconds=30)
        process = watcher.ProcessIdentity(42, "ck3.exe", 123)
        observations = iter([None, process, None, None, None])
        polls = 0
        real_watch = watcher.watch_sessions

        def bounded_watch(**kwargs):
            def sleep(_seconds):
                nonlocal polls
                polls += 1
            return real_watch(**kwargs, sleep=sleep, stop_requested=lambda: polls >= 3)

        stdout, stderr = io.StringIO(), io.StringIO()
        with ExitStack() as stack:
            for key, value in {**self.roots, "ROOT_CK3CHRONICLE": self.runtime, "ROOT_CRASHES": self.root / "crashes"}.items():
                stack.enter_context(patch.object(config, key, value))
            stack.enter_context(patch.object(config, "watcher_settings", return_value=config.WatcherSettings(
                self.runtime, ingest_enabled=False, retention_enabled=False)))
            (self.root / "crashes").mkdir(exist_ok=True)
            stack.enter_context(patch.object(watcher, "find_process", side_effect=lambda _name: next(observations)))
            stack.enter_context(patch.object(watcher, "watch_sessions", side_effect=bounded_watch))
            stack.enter_context(redirect_stdout(stdout))
            stack.enter_context(redirect_stderr(stderr))
            if failure_patch:
                stack.enter_context(failure_patch)
            code = cli.cmd_watch(args)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        events = [json.loads(line) for path in (self.runtime / "watch").glob("events-*.jsonl") for line in path.read_text(encoding="utf-8").splitlines()]
        pending = list((self.runtime / "pending").glob("*")) if (self.runtime / "pending").exists() else []
        return code, events, pending

    def test_actual_cli_lifecycle_produces_pair_template_and_journal(self):
        mod = self.add_mod("ROOT_STEAM", "123", "Active mod")
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        original_debug = self.debug.read_bytes()
        code, events, pending = self.run_watcher()
        self.assertEqual(code, 0)
        self.assertEqual(len(pending), 1)
        directory = pending[0]
        self.assertFalse(directory.name.startswith(".copying-"))
        self.assertEqual((directory / "error.log").read_bytes(), self.error_bytes)
        self.assertEqual((directory / "debug.log").read_bytes(), original_debug)
        data = json.loads((directory / "playset.json").read_text(encoding="utf-8"))
        metadata = json.loads((directory / "capture-metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(data["captured_at"], metadata["captured_at"])
        self.assertEqual(data["members"][1]["name"], "Active mod")
        created = next(e for e in events if e["event"] == "playset_template_created")
        self.assertEqual(created["path"], str(directory / "playset.json"))
        self.assertEqual(created["log_pair_id"], data["log_pair_id"])
        completed = next(e for e in events if e["event"] == "capture_completed")
        self.assertEqual(completed["files_copied"], 2)
        self.assertFalse(list(self.runtime.rglob("*.db")))

    def test_missing_debug_prevents_extraction_and_logs_copy_failure(self):
        self.debug.unlink()
        with patch.object(playset, "extract_playset") as extract:
            code, events, pending = self.run_watcher()
        extract.assert_not_called()
        self.assertEqual(code, 0)
        self.assertEqual(len(pending), 1)
        self.assertFalse(pending[0].name.startswith(".copying-"))
        self.assertTrue((pending[0] / "error.log").is_file())
        self.assertIn("debug_capture_failed", [e["event"] for e in events])
        self.assertIn("capture_completed", [e["event"] for e in events])
        self.assertNotIn("playset_template_created", [e["event"] for e in events])

    def test_missing_error_prevents_extraction(self):
        (self.logs / "error.log").unlink()
        with patch.object(playset, "extract_playset") as extract:
            code, events, pending = self.run_watcher()
        extract.assert_not_called()
        self.assertEqual(code, 0)
        self.assertFalse(pending)
        self.assertIn("capture_failed", [e["event"] for e in events])

    def test_descriptor_warning_reaches_journal_without_stopping_template(self):
        mod = self.add_mod("ROOT_LOCAL_MODS", "nameless")
        self.debug.write_text(mount_line(mod), encoding="utf-8")
        code, events, pending = self.run_watcher()
        self.assertEqual(code, 0)
        warning = next(e for e in events if e["event"] == "playset_metadata_warning")
        self.assertEqual(warning["load_order"], 1)
        self.assertEqual(warning["capture_id"], pending[0].name)
        data = json.loads((pending[0] / "playset.json").read_text(encoding="utf-8"))
        self.assertEqual(data["members"][1]["name"], "UNKNOWN")

    def test_write_failure_is_journaled_and_publishes_protected_raw_pair(self):
        code, events, pending = self.run_watcher(patch.object(harvester, "write_playset_template", side_effect=PermissionError("disk denied")))
        self.assertEqual(code, 0)
        self.assertTrue((pending[0] / "error.log").is_file())
        self.assertTrue((pending[0] / "debug.log").is_file())
        self.assertFalse((pending[0] / "playset.json").exists())
        failure = next(e for e in events if e["event"] == "playset_template_failed")
        self.assertEqual(failure["stage"], "write_playset_template")
        self.assertNotIn("playset_template_created", [e["event"] for e in events])

    def test_extractor_failure_does_not_withhold_protected_error_log(self):
        code, events, pending = self.run_watcher(patch.object(playset, "extract_playset", side_effect=RuntimeError("bug")))
        self.assertEqual(code, 0)
        self.assertFalse(pending[0].name.startswith(".copying-"))
        self.assertTrue((pending[0] / "debug.log").is_file())
        self.assertIn("playset_template_failed", [e["event"] for e in events])
        self.assertIn("capture_completed", [e["event"] for e in events])
        self.assertNotIn("playset_template_created", [e["event"] for e in events])

    def test_protected_debug_read_failure_preserves_pair_and_journals_failure(self):
        code, events, pending = self.run_watcher(patch.object(playset, "extract_playset", side_effect=PermissionError("cannot read debug")))
        self.assertEqual(code, 0)
        self.assertTrue((pending[0] / "debug.log").is_file())
        self.assertFalse((pending[0] / "playset.json").exists())
        failure = next(e for e in events if e["event"] == "playset_template_failed")
        self.assertEqual(failure["stage"], "extract_playset")

    def test_protected_hash_failure_preserves_pair_and_journals_failure(self):
        code, events, pending = self.run_watcher(patch.object(harvester, "hash_file", side_effect=PermissionError("cannot hash protected log")))
        self.assertEqual(code, 0)
        self.assertTrue((pending[0] / "error.log").is_file())
        self.assertTrue((pending[0] / "debug.log").is_file())
        self.assertFalse((pending[0] / "playset.json").exists())
        self.assertIn("playset_template_failed", [e["event"] for e in events])

    def test_background_interrupt_is_journaled_without_terminal_output(self):
        code, events, pending = self.run_watcher(patch.object(watcher, "watch_sessions", side_effect=KeyboardInterrupt))
        self.assertEqual(code, 0)
        self.assertFalse(pending)
        self.assertIn("watcher_interrupted", [e["event"] for e in events])

    def test_lease_failure_is_journaled_without_removing_owners_heartbeat(self):
        watch = self.runtime / "watch"
        watch.mkdir(parents=True)
        heartbeat = watch / "watcher-heartbeat.json"
        heartbeat.write_text('owner heartbeat', encoding="utf-8")
        code, events, _pending = self.run_watcher(patch.object(watcher.WatcherLease, "__enter__", side_effect=watcher.WatcherAlreadyRunning("busy")))
        self.assertEqual(code, 1)
        self.assertEqual(heartbeat.read_text(encoding="utf-8"), "owner heartbeat")
        self.assertEqual(events[0]["event"], "watcher_failed")


if __name__ == "__main__":
    unittest.main()
