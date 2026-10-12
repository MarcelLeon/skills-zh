"""Public/private boundary regression checks."""

import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "repository_validator",
    Path(__file__).resolve().parents[1] / "scripts" / "validate_repository.py",
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PublicContentTests(unittest.TestCase):
    def test_private_paths_are_rejected_and_product_files_are_allowed(self):
        for path in (
            "articles/weekly/day/cnblogs.md", "private/archive.zip",
            "publishing/notes.md", "content-ops/accounts.json",
            "ARTICLE_PLAYBOOK.md", "output/xiaohongshu_payload/body.txt",
            "output/preview-evidence.md", ".env", ".env.dev.local",
        ):
            with self.subTest(path=path):
                self.assertTrue(VALIDATOR.is_private_file(path))
        for path in (
            "skills/docx/SKILL.md", "sync/day-report.md",
            "THIRD_PARTY_NOTICES.md", ".env.example", "PUBLIC_CONTENT.md",
        ):
            with self.subTest(path=path):
                self.assertFalse(VALIDATOR.is_private_file(path))

    def test_index_gate_rejects_forced_private_file_and_personal_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes.md").write_text(
                "/" + "Users/" + "private-user/project", encoding="utf-8",
            )
            result = subprocess.CompletedProcess(
                args=[], returncode=0,
                stdout=b"articles/draft.md\0notes.md\0", stderr=b"",
            )
            errors = []
            with patch.object(VALIDATOR, "ROOT", root), patch.object(
                VALIDATOR.subprocess, "run", return_value=result,
            ):
                VALIDATOR.validate_public_content(errors)
            self.assertEqual(len(errors), 2)
            self.assertIn("private content", errors[0])
            self.assertIn("personal home path", errors[1])

    def test_unreadable_index_fails_closed(self):
        result = subprocess.CompletedProcess(
            args=[], returncode=1, stdout=b"", stderr=b"failure",
        )
        errors = []
        with patch.object(VALIDATOR.subprocess, "run", return_value=result):
            VALIDATOR.validate_public_content(errors)
        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
