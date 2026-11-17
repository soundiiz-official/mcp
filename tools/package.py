#!/usr/bin/env python3
"""Check native client configuration and create a reproducible release ZIP."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
MCP_URL = "https://soundiiz.com/mcp"
RUNTIME_FILES = (
    "README.md",
    "CHANGELOG.md",
    "gemini-extension.json",
    ".antigravity-plugin/plugin.json",
    "mcp_config.json",
    "rules/soundiiz.md",
    "assets/soundiiz-512.png",
)


def checked_path(relative):
    path = ROOT / relative
    resolved = path.resolve(strict=True)
    resolved.relative_to(ROOT)
    if any(part == "keys" or part.startswith("parameters") for part in resolved.parts):
        raise ValueError("Forbidden path: " + relative)
    if path.is_symlink() or not path.is_file():
        raise ValueError("Release files must be regular files: " + relative)
    return path


def load_json(relative):
    return json.loads(checked_path(relative).read_text(encoding="utf-8"))


def check():
    gemini = load_json("gemini-extension.json")
    antigravity = load_json(".antigravity-plugin/plugin.json")
    mcp = load_json("mcp_config.json")
    version = gemini["version"]
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version):
        raise ValueError("Use a MAJOR.MINOR.PATCH package version")
    if antigravity["version"] != version:
        raise ValueError("Client package versions differ")
    if gemini["name"] != "soundiiz" or antigravity["name"] != "soundiiz":
        raise ValueError("Native manifests must use the Soundiiz package identity")
    if gemini["mcpServers"] != {"soundiiz": {"type": "http", "url": MCP_URL}}:
        raise ValueError("Gemini connection differs from the public MCP contract")
    if mcp["mcpServers"] != {"soundiiz": {"serverUrl": MCP_URL}}:
        raise ValueError("Antigravity connection differs from the public MCP contract")
    if gemini.get("contextFileName") != "rules/soundiiz.md":
        raise ValueError("Gemini must reference the shared usage guide")
    checked_path(gemini["contextFileName"])
    if antigravity.get("logo") != "assets/soundiiz-512.png":
        raise ValueError("Antigravity must reference the bundled official logo")
    for field in ("displayName", "description", "author", "homepage", "repository"):
        if not antigravity.get(field):
            raise ValueError("Missing Antigravity presentation field: " + field)
    if not 1 <= len(antigravity.get("suggestedPrompts", [])) <= 3:
        raise ValueError("Provide one to three Antigravity starter prompts")
    if "## " + version + " " not in checked_path("CHANGELOG.md").read_text(encoding="utf-8"):
        raise ValueError("The package version needs a changelog entry")
    logo = checked_path(antigravity["logo"]).read_bytes()
    if not logo.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("The bundled logo must be a PNG")
    width, height = struct.unpack(">II", logo[16:24])
    if width != height or width < 128:
        raise ValueError("The logo must be square and at least 128 pixels")
    for relative in RUNTIME_FILES:
        raw = checked_path(relative).read_bytes()
        if relative.endswith((".md", ".json")):
            if b"\r" in raw or not raw.endswith(b"\n"):
                raise ValueError("Text files must use UTF-8 with LF endings: " + relative)
            raw.decode("utf-8")
            if re.search(rb"github_pat_|gh[pousr]_[A-Za-z0-9]{16,}|GITHUB_TOKEN=", raw):
                raise ValueError("Credential-like value in release file: " + relative)
    return version


def package_bytes():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(RUNTIME_FILES):
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, checked_path(relative).read_bytes())
    data = buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if set(archive.namelist()) != set(RUNTIME_FILES) or archive.testzip():
            raise ValueError("Release archive integrity check failed")
        for relative in RUNTIME_FILES:
            if archive.read(relative) != checked_path(relative).read_bytes():
                raise ValueError("Release archive differs from source: " + relative)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run offline checks (also the default)")
    parser.add_argument("--output", type=Path, help="Write a reproducible release ZIP")
    args = parser.parse_args()
    version = check()
    print("Soundiiz " + version + ": client configuration and release files checked")
    if args.output:
        data = package_bytes()
        target = args.output.expanduser().resolve()
        if target == ROOT or ROOT in target.parents:
            raise ValueError("Keep generated release archives outside the source repository")
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if target.read_bytes() != data:
                raise ValueError("Refusing to replace a different existing archive: " + str(target))
        else:
            with target.open("xb") as output:
                output.write(data)
        print(str(target) + ": " + str(len(data)) + " bytes")
        print("SHA-256 " + hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        print("Package check failed: " + str(error), file=sys.stderr)
        sys.exit(1)
