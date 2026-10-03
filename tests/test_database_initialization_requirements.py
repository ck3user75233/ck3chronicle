"""Owner-approved explicit database naming and initialization boundary."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest

from ck3chronicle.pipeline.repository import create_database, open_database_readonly
from ck3chronicle.pipeline.schema import SCHEMA_VERSION


class DatabaseInitializationTests(unittest.TestCase):
    def test_existing_runtime_directory_uses_schema_and_utc_initialization_time(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old = root / 'ck3chronicle.db'
            old.write_bytes(b'legacy evidence is not replaced')
            stamp = datetime(2026, 9, 29, 10, 23, 45, tzinfo=timezone(timedelta(hours=8)))
            with create_database(root, initialized_at=stamp) as db:
                path = db.path
                self.assertEqual(path.name, f'ck3chronicle-schema{SCHEMA_VERSION}-20260929T022345Z.sqlite3')
                self.assertEqual(db.metadata['created_at'], '2026-09-29T02:23:45.000000+00:00')
                self.assertEqual(db.metadata['database_id'], path.stem)
                self.assertEqual(db.review_root, root / 'review' / path.stem)
                self.assertNotIn('generation_id', db.metadata)
                self.assertEqual(db.list_runs(), [])
            with open_database_readonly(path) as db:
                self.assertEqual(db.metadata['schema_version'], SCHEMA_VERSION)
            self.assertEqual(old.read_bytes(), b'legacy evidence is not replaced')

    def test_same_second_initialization_cannot_overwrite_existing_database(self):
        with tempfile.TemporaryDirectory() as temporary:
            stamp = datetime(2026, 9, 29, tzinfo=timezone.utc)
            with create_database(Path(temporary), initialized_at=stamp) as db:
                path = db.path
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                create_database(Path(temporary), initialized_at=stamp)
            self.assertEqual(path.read_bytes(), before)

    def test_open_does_not_search_or_create_a_database(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(ValueError):
                open_database_readonly(root)
            missing = root / 'missing.sqlite3'
            with self.assertRaises(ValueError):
                open_database_readonly(missing)
            self.assertFalse(missing.exists())


if __name__ == '__main__':
    unittest.main()
