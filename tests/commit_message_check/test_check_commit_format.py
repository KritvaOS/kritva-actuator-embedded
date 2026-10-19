#!/usr/bin/env python3
# Unit tests for the commit format checker (kritva-program decision D-070).

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "security"))
import check_commit_format as ccf  # noqa: E402

FOOT = "\n\nTask: ACT-X-001"


class FormatTests(unittest.TestCase):
    def test_conventional_header_with_task_footer_passes(self):
        self.assertEqual(ccf.problems("feat(core): add thing" + FOOT), [])

    def test_several_ids_pass(self):
        self.assertEqual(ccf.problems("fix(api): repair thing\n\nTasks: ACT-X-001, ACT-X-002"), [])

    def test_missing_footer_is_rejected(self):
        self.assertTrue(ccf.problems("feat(core): add thing"))

    def test_plain_sentence_header_is_rejected(self):
        self.assertTrue(ccf.problems("Add Core lifecycle state API" + FOOT))

    def test_unknown_type_is_rejected(self):
        self.assertTrue(ccf.problems("update(core): add thing" + FOOT))

    def test_two_footers_are_rejected(self):
        self.assertTrue(ccf.problems("feat(core): add thing\n\nTask: ACT-X-001\nTask: ACT-X-002"))

    def test_none_is_allowed_only_on_docs_or_chore(self):
        self.assertEqual(ccf.problems("docs(readme): fix wording\n\nTasks: None (record correction)"), [])
        self.assertTrue(ccf.problems("feat(core): add thing\n\nTasks: None (no task)"))

    def test_subject_id_must_be_in_the_footer(self):
        self.assertTrue(ccf.problems("feat(core): add thing [ACT-X-009]" + FOOT))

    def test_session_trailer_is_rejected(self):
        self.assertTrue(ccf.problems("feat(core): add thing" + FOOT + "\n\nClaude-Session: https://example.test/s"))

    def test_merge_commit_passes(self):
        self.assertEqual(ccf.problems("Merge pull request #1 from x/y"), [])

    def test_co_authored_by_is_allowed(self):
        self.assertEqual(ccf.problems("feat(core): add thing" + FOOT + "\n\nCo-Authored-By: A <a@b.c>"), [])


if __name__ == "__main__":
    unittest.main()
