#!/usr/bin/env python3
"""Prepare the static Eduforn site for GitHub Pages without editing source files."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist" / "github-pages"
WEB_EXTENSIONS = {".html", ".css", ".js", ".webmanifest", ".xml"}
ROOT_PATH_LITERAL = re.compile(r"(?P<quote>[\"'`])/(?!/)")


def deployment_base(explicit: str | None) -> str:
    value = explicit
    if value is None:
        value = os.environ.get("PAGES_BASE_PATH") or None
    if value is None:
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        if "/" in repository:
            owner, name = repository.split("/", 1)
            value = "" if name.casefold() == f"{owner}.github.io".casefold() else name
        else:
            value = ""

    value = value.strip()
    if value in {"", "/"}:
        return ""
    if ".." in value or "?" in value or "#" in value:
        raise ValueError("Base path must be a simple repository path, for example /Eduforn-website-design/")
    return "/" + value.strip("/") + "/"


def ignore_source(directory: str, names: list[str]) -> set[str]:
    ignored = {".git", ".github", ".codex", ".agents", "sources", "scripts", "dist", "__pycache__"}
    ignored_files = {"AGENTS.md", "README.md", ".gitignore"}
    return {name for name in names if name in ignored or name in ignored_files or name.startswith(".")}


def build(base_path: str) -> Path:
    # This is a fixed, generated subdirectory. Refuse to remove anything else.
    if OUTPUT.exists():
        resolved_output = OUTPUT.resolve()
        expected_output = (ROOT / "dist" / "github-pages").resolve()
        if resolved_output != expected_output or resolved_output.parent != (ROOT / "dist").resolve():
            raise RuntimeError(f"Refusing to clean unexpected output directory: {resolved_output}")
        shutil.rmtree(resolved_output)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT, OUTPUT, ignore=ignore_source)

    if base_path:
        for file_path in OUTPUT.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in WEB_EXTENSIONS:
                source = file_path.read_text(encoding="utf-8")
                file_path.write_text(ROOT_PATH_LITERAL.sub(lambda match: match.group("quote") + base_path, source), encoding="utf-8")

    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    return OUTPUT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-path", help="Override the GitHub Pages path, e.g. /Eduforn-website-design/; use / for a root domain")
    args = parser.parse_args()
    base_path = deployment_base(args.base_path)
    output = build(base_path)
    print(f"Prepared {output.relative_to(ROOT)} (base path: {base_path or '/'})")


if __name__ == "__main__":
    main()
