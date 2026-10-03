"""Owner-directed lossless parsing and continuous-token requirements.

Set CK3_RAW_PARSER_LOG to the genuine protected log annotated in
docs/LEARNER_PARSER_SPEC.md. Captured content is never copied into Git fixtures.
"""
from __future__ import annotations

import dataclasses
import json
import os
from pathlib import Path
import tempfile
import unittest

from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.evidence import read_evidence
from template_learning import records, inventory

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools/template_learning/parsers/v1/manifest.json"


class LexicalRequirements(unittest.TestCase):
    def test_exact_selected_implementation_required(self):
        reference = reference_from_manifest(MANIFEST)
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            load_parser(dataclasses.replace(reference, sha256="0" * 64))


@unittest.skipUnless(os.environ.get("CK3_RAW_PARSER_LOG"), "requires supplied genuine annotated CK3 log")
class NativeParserRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = Path(os.environ["CK3_RAW_PARSER_LOG"])
        cls.parser = load_parser(reference_from_manifest(MANIFEST))
        cls.raw = read_evidence(cls.log, parser=cls.parser)

    def emission(self, line):
        return next(e for e in self.raw.emissions if e.start_line == line)

    def test_complete_original_and_lexical_partition(self):
        """COMPLETE/POSITIONS: every byte, whitespace and punctuation survives."""
        original = self.log.read_bytes()
        self.assertEqual(b"".join(e.native_bytes() for e in self.raw.emissions), original)
        cursor = 0
        for emission in self.raw.emissions:
            self.assertEqual(emission.span.start, cursor)
            self.assertEqual(emission.header_span.end, emission.body_span.start)
            self.assertTrue(self.raw.read_bytes(emission.header_span).endswith(b"]:"))
            pieces = emission.pieces
            self.assertEqual(b"".join(self.raw.read_bytes(p.span) for p in pieces),
                             self.raw.read_bytes(emission.body_span))
            position = emission.body_span.start
            for piece in pieces:
                self.assertEqual(piece.span.start, position)
                self.assertEqual(piece.text.encode("utf-8", "surrogateescape"), self.raw.read_bytes(piece.span))
                position = piece.span.end
            self.assertEqual(position, emission.span.end)
            cursor = emission.span.end
        self.assertEqual(cursor, len(original))

    def test_native_annotated_ranges_and_source(self):
        """SOURCE/RETRIEVAL: physical, engine and message locations stay distinct."""
        span = self.parser.implementation.Span
        for start, end, expected in [
            (60621, 60635, "near line: 261"),
            (60703, 60717, "near line: 273"),
            (516829, 516851, "capital_county.kingdom"),
            (516862, 516883, "Failed context switch"),
            (516888, 516904, "Script location:"),
            (435966, 435990, "Script location: Unknown"),
        ]:
            self.assertEqual(self.raw.read_text(span(start, end)), expected)
        self.assertEqual(self.emission(301).source_tag, "pdx_persistent_reader.cpp:216")
        self.assertIn("capital_county.kingdom", [p.text for p in self.emission(4747).tokens])
        path = "common/activities/guest_invite_rules/activity_invite_rules.txt"
        message = self.emission(4747)
        start = message.body_text.index(path)
        start = message.body_span.start + len(message.body_text[:start].encode("utf-8"))
        pieces = [p for p in message.pieces if start <= p.span.start < start + len(path)]
        self.assertEqual([p.text for p in pieces], [
            "common", "/", "activities", "/", "guest_invite_rules", "/", "activity_invite_rules.txt"])
        self.assertEqual("".join(p.text for p in pieces), path)
        self.assertIn("Script location:", self.emission(3958).body_text)
        self.assertIn("\x15", self.emission(3723).body_text)

    def test_recovered_messages_preserve_parent_shared_content_and_reason(self):
        """MULTI: native siblings recover automatically; failure/reason stays whole."""
        impl = self.parser.implementation
        parent = self.emission(593)
        ranges = tuple(impl.Span(a, b) for a, b in [
            (106325, 106369), (106370, 106414), (106415, 106459)])
        recovery = parent.recovery
        self.assertEqual(recovery.status, "recovered")
        children = recovery.messages
        self.assertEqual(tuple(child.span for child in children), ranges)
        for child, number in zip(children, (420, 421, 422)):
            self.assertEqual(child.text, f"Unknown trigger: kinslayer_3, near line: {number}")
            self.assertIs(child.parent, parent)
            self.assertIs(child.shared_spans, recovery.shared_spans)
        union = sorted([*ranges, *children[0].shared_spans], key=lambda s: s.start)
        self.assertEqual(b"".join(self.raw.read_bytes(s) for s in union), parent.native_bytes())
        script = self.emission(3958)
        self.assertEqual(len(script.recovery.messages), 1)
        self.assertEqual(script.recovery.messages[0].native_bytes(),
                         self.raw.read_bytes(script.body_span))

    def test_native_always_separators_are_individual_tokens(self):
        """Directed separators stay visible even inside a whitespace-free run."""
        separators = set(':/\\{}[]()"=;|')
        for emission in self.raw.emissions:
            for piece in emission.pieces:
                if piece.text == "Div/0":
                    continue
                if any(char in separators for char in piece.text):
                    self.assertEqual(len(piece.text), 1)
                    self.assertEqual(piece.kind, "token")

    def test_optional_debug_reload_and_top_level_metadata(self):
        """METADATA: parser identity once, optional output reproduces native ranges."""
        with tempfile.TemporaryDirectory(dir=ROOT / ".codex-tmp") as folder:
            path = Path(folder) / "raw.json"
            self.raw.save_debug(path)
            replay = self.parser.load_debug(path)
            self.assertEqual(replay.debug_document(), self.raw.debug_document())
        self.assertIn("parser_reference", {f.name for f in dataclasses.fields(self.raw)})
        self.assertNotIn("parser_revision", {f.name for f in dataclasses.fields(self.raw.emissions[0])})


    def test_learner_collector_uses_native_input_without_masks(self):
        """Each recovered message and repetition reaches learner-owned records."""
        stat = self.log.stat()
        digest = inventory.sha256_file(self.log)
        evidence = inventory.ProtectedLog("annotated-log", "protected", self.log, digest, stat.st_size, stat.st_mtime_ns)
        groups, stats = records.collect_records([evidence], parser=self.parser)
        occurrences = [o for rows in groups.values() for r in rows for o in r.native_occurrences]
        expected = [(e.ordinal,m.ordinal) for e in self.raw.emissions for m in e.recovery.messages]
        self.assertEqual(sorted((o["emission_ordinal"],o["message_ordinal"]) for o in occurrences),expected)
        known = {(r.source_family,r.text):r for rows in groups.values() for r in rows}
        for emission in self.raw.emissions:
            for message in emission.recovery.messages:
                record = known[(emission.source_family,message.text)]
                self.assertEqual(tuple(p.text for p in message.tokens), record.tokens)
                self.assertEqual("".join(text for _,text in record.pieces),message.text)
        self.assertEqual(stats[digest]["recovered_messages"],len(expected))

    def test_registry_native_feature_roundtrip(self):
        """Feature caches retain raw references and require the selected parser."""
        from template_learning import incremental_template_registry as registry
        stat = self.log.stat()
        evidence = inventory.ProtectedLog("annotated-log", "protected", self.log, inventory.sha256_file(self.log),
                                       stat.st_size, stat.st_mtime_ns)
        feature = registry.feature_from_log(evidence, parser=self.parser)
        registry.validate_feature(feature, evidence.sha256, parser=self.parser)
        with tempfile.TemporaryDirectory(dir=ROOT / ".codex-tmp") as folder:
            root = Path(folder)
            path = registry.feature_cache_path(root, evidence.sha256, parser=self.parser)
            registry.write_json(path, feature)
            entry = {"sha256": evidence.sha256, "feature_caches": {
                registry.feature_key(self.parser): {
                    "path": str(path.relative_to(root)), "sha256": inventory.sha256_file(path)}},
                "observed_paths": [{"kind": "protected", "path": str(self.log)}]}
            groups, _ = registry.combine_training_records(root, [entry], parser=self.parser)
        self.assertEqual(sum(r.occurrences for rows in groups.values() for r in rows), sum(len(e.recovery.messages) for e in self.raw.emissions))
        self.assertEqual(sum(len(r.native_occurrences) for rows in groups.values() for r in rows), sum(len(e.recovery.messages) for e in self.raw.emissions))
        feature["parser"] = dict(feature["parser"], version="not-the-selected-parser")
        with self.assertRaisesRegex(ValueError, "invalid or stale"):
            registry.validate_feature(feature, evidence.sha256, parser=self.parser)


if __name__ == "__main__":
    unittest.main()
