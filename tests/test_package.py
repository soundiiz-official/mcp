import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    "README.md", "CHANGELOG.md", "gemini-extension.json",
    ".antigravity-plugin/plugin.json", "mcp_config.json",
    "rules/soundiiz.md", "assets/soundiiz-512.png", "tools/package.py",
)


class PackageCliTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="soundiiz-package-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.source = self.directory / "source"
        for relative in FILES:
            target = self.source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(self.source / "tools/package.py"), *args],
            capture_output=True, text=True, check=False,
        )

    def set_version(self, version):
        for relative in ("gemini-extension.json", ".antigravity-plugin/plugin.json"):
            path = self.source / relative
            manifest = json.loads(path.read_text())
            manifest["version"] = version
            path.write_text(json.dumps(manifest) + "\n")
        changelog = self.source / "CHANGELOG.md"
        changelog.write_text(changelog.read_text().replace("## 1.2.0 ", "## " + version + " ", 1))

    def test_leading_zero_version_is_rejected_before_release(self):
        self.set_version("01.2.0")
        result = self.run_cli("--check")
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("MAJOR.MINOR.PATCH", result.stderr)

    def test_client_version_mismatch_is_rejected(self):
        path = self.source / ".antigravity-plugin/plugin.json"
        manifest = json.loads(path.read_text())
        manifest["version"] = "9.0.0"
        path.write_text(json.dumps(manifest) + "\n")
        result = self.run_cli("--check")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("versions differ", result.stderr)

    def test_release_is_reproducible_and_excludes_contributor_files(self):
        (self.source / "contributor.txt").write_text("Not a runtime asset.\n")
        first = self.directory / "first.zip"
        second = self.directory / "second.zip"
        for output in (first, second):
            result = self.run_cli("--output", str(output))
            self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertIn("gemini-extension.json", archive.namelist())
            self.assertIn(".antigravity-plugin/plugin.json", archive.namelist())
            self.assertIn("rules/soundiiz.md", archive.namelist())
            self.assertNotIn("contributor.txt", archive.namelist())
            self.assertNotIn("tools/package.py", archive.namelist())
            for name in archive.namelist():
                self.assertEqual((self.source / name).read_bytes(), archive.read(name))

    def test_external_symlink_is_rejected(self):
        outside = self.directory / "outside.txt"
        outside.write_text("Not part of the package.\n")
        readme = self.source / "README.md"
        readme.unlink()
        try:
            readme.symlink_to(outside)
        except OSError as error:
            self.skipTest("Symlinks unavailable: " + str(error))
        result = self.run_cli("--check")
        self.assertNotEqual(0, result.returncode)

    def test_generated_archive_cannot_be_written_into_source_repository(self):
        result = self.run_cli("--output", str(self.source / "release.zip"))
        self.assertNotEqual(0, result.returncode)
        self.assertFalse((self.source / "release.zip").exists())
