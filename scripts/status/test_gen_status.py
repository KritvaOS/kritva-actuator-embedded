#!/usr/bin/env python3
"""Unit tests for gen_status.py (fail-closed behaviour)."""
import csv, json, subprocess, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_status as g

SCHEMA = Path(__file__).resolve().parents[2] / "status" / "status.schema.json"


class T(unittest.TestCase):
    def mk(self, rows):
        d = Path(tempfile.mkdtemp())
        p = d / "t.csv"
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, ["task_id", "legacy_id", "title", "execution", "readiness", "implementation_commit"])
            w.writeheader(); w.writerows(rows)
        return p

    def row(self, **k):
        r = dict(task_id="X-1", legacy_id="", title="t", execution="NOT_STARTED", readiness="PLANNABLE", implementation_commit="")
        r.update(k); return r

    def test_ok(self):
        self.assertEqual(len(g.read_tasks(self.mk([self.row()]))), 1)

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            g.read_tasks(self.mk([self.row(), self.row()]))

    def test_bad_enum(self):
        with self.assertRaises(ValueError):
            g.read_tasks(self.mk([self.row(execution="DONE")]))

    def test_bad_sha(self):
        with self.assertRaises(ValueError):
            g.read_tasks(self.mk([self.row(implementation_commit="abc")]))

    def test_validator_rejects_extra(self):
        schema = json.loads(SCHEMA.read_text())
        self.assertTrue(g.validate({"schema_version": "2.0", "bogus": 1}, schema))


if __name__ == "__main__":
    unittest.main()
