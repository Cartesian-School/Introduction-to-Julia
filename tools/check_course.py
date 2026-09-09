#!/usr/bin/env python3
"""Integrity checks for the Cartesian School "Julia from Zero" course.

Canonical course layout:
    PL/Lesson_0_*.ipynb
    ...
    PL/Lesson_14_*.ipynb

The checker intentionally validates repository invariants that should remain
stable across notebook revisions. It does not require saved execution outputs
or one exact kernel display-name, because the course notebooks are designed to
be portable across compatible Julia/Jupyter installations.

Usage:
    python3 tools/check_course.py
    python3 tools/check_course.py --strict

Exit code 0 = all required checks passed.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

COURSE_DIR = Path("PL")
EXPECTED_LESSONS = 15
EXPECTED_NUMBERS = set(range(EXPECTED_LESSONS))

LEAK_PATTERNS = [
    (re.compile(r"[A-Za-z]:\\\\+Users\\\\+", re.I), "Windows user path"),
    (re.compile(r"/home/(?!<)[a-z0-9_-]+/", re.I), "Linux home path"),
    (re.compile(r"/Users/[a-z0-9_-]+/", re.I), "macOS home path"),
    (re.compile(r"/media/[a-z0-9_-]+/", re.I), "removable-media path"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
]

RESULTS: list[tuple[str, str, str]] = []


def report(level: str, check: str, message: str) -> None:
    RESULTS.append((level, check, message))


def notebook_paths() -> list[Path]:
    if not COURSE_DIR.is_dir():
        return []
    return sorted(COURSE_DIR.glob("Lesson_*.ipynb"))


def lesson_number(path: Path) -> int | None:
    match = re.match(r"Lesson_(\d+)_", path.name)
    return int(match.group(1)) if match else None


def load(path: Path) -> dict:
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def check_inventory(paths: list[Path]) -> None:
    if not COURSE_DIR.is_dir():
        report("FAIL", "course-dir", "missing canonical PL/ directory")
        return
    report("PASS", "course-dir", "canonical PL/ directory present")

    numbers = [lesson_number(p) for p in paths]
    invalid_names = [str(p) for p, number in zip(paths, numbers) if number is None]
    if invalid_names:
        report("FAIL", "lesson-names", ", ".join(invalid_names))
    else:
        report("PASS", "lesson-names", "all canonical notebooks use Lesson_<N>_*.ipynb")

    valid_numbers = [n for n in numbers if n is not None]

    if len(paths) != EXPECTED_LESSONS:
        report(
            "FAIL",
            "lesson-count",
            f"expected {EXPECTED_LESSONS} canonical notebooks in PL/, found {len(paths)}",
        )
    else:
        report("PASS", "lesson-count", f"{EXPECTED_LESSONS} canonical notebooks present")

    duplicates = sorted({n for n in valid_numbers if valid_numbers.count(n) > 1})
    if duplicates:
        report("FAIL", "lesson-numbering", f"duplicate lesson numbers: {duplicates}")
    elif set(valid_numbers) != EXPECTED_NUMBERS:
        missing = sorted(EXPECTED_NUMBERS - set(valid_numbers))
        extra = sorted(set(valid_numbers) - EXPECTED_NUMBERS)
        report(
            "FAIL",
            "lesson-numbering",
            f"expected Lesson 0..14; missing={missing}, extra={extra}",
        )
    else:
        report("PASS", "lesson-numbering", "exactly one notebook for every Lesson 0..14")


def check_json(paths: list[Path]) -> dict[Path, dict]:
    loaded: dict[Path, dict] = {}
    for path in paths:
        try:
            loaded[path] = load(path)
        except Exception as exc:  # noqa: BLE001
            report("FAIL", "valid-json", f"{path}: {exc}")

    if len(loaded) == len(paths):
        report("PASS", "valid-json", f"all {len(paths)} notebooks parse as JSON")
    return loaded


def check_notebook_schema(nbs: dict[Path, dict]) -> None:
    bad: list[str] = []
    for path, nb in nbs.items():
        if nb.get("nbformat") != 4:
            bad.append(f"{path}: nbformat={nb.get('nbformat')!r}")
            continue
        cells = nb.get("cells")
        if not isinstance(cells, list) or not cells:
            bad.append(f"{path}: missing/non-list/empty cells")
            continue
        for index, cell in enumerate(cells):
            if cell.get("cell_type") not in {"markdown", "code", "raw"}:
                bad.append(f"{path} cell {index}: invalid cell_type={cell.get('cell_type')!r}")
                break
            if not isinstance(cell.get("source", []), (list, str)):
                bad.append(f"{path} cell {index}: invalid source")
                break

    if bad:
        for item in bad:
            report("FAIL", "notebook-schema", item)
    else:
        report("PASS", "notebook-schema", "all notebooks have valid nbformat-4 structure")


def check_titles(nbs: dict[Path, dict]) -> None:
    bad: list[str] = []
    for path, nb in nbs.items():
        number = lesson_number(path)
        text = "\n".join(
            "".join(cell.get("source", []))
            if isinstance(cell.get("source", []), list)
            else str(cell.get("source", ""))
            for cell in nb.get("cells", [])[:8]
            if cell.get("cell_type") == "markdown"
        )
        if number is not None and not re.search(rf"\bLesson\s+{number}\b", text, re.I):
            bad.append(f"{path}: title/header does not identify Lesson {number}")

    if bad:
        for item in bad:
            report("FAIL", "lesson-title", item)
    else:
        report("PASS", "lesson-title", "every notebook header matches its lesson number")


def check_code_cell_shape(nbs: dict[Path, dict]) -> None:
    bad: list[str] = []
    for path, nb in nbs.items():
        for index, cell in enumerate(nb.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue
            if "outputs" not in cell or not isinstance(cell.get("outputs"), list):
                bad.append(f"{path} cell {index}: code cell outputs must be a list")
            if "execution_count" not in cell:
                bad.append(f"{path} cell {index}: code cell missing execution_count")
    if bad:
        for item in bad[:20]:
            report("FAIL", "code-cells", item)
    else:
        report("PASS", "code-cells", "all code cells have Jupyter execution/output fields")


def check_leaks(paths: list[Path]) -> None:
    hits: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for pattern, label in LEAK_PATTERNS:
            for match in pattern.finditer(text):
                hits.append(f"{path}: {label}: {match.group(0)[:50]}")

    secret_labels = {"GitHub token", "AWS access key", "private key"}
    for name in ("README.md", "README.pl.md", "README.ru.md"):
        path = Path(name)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern, label in LEAK_PATTERNS:
            if label not in secret_labels:
                continue
            if pattern.search(text):
                hits.append(f"{path}: {label}")

    if hits:
        for hit in hits[:20]:
            report("FAIL", "no-leaks", hit)
    else:
        report("PASS", "no-leaks", "no local user paths or credential patterns detected")


def check_internal_links(nbs: dict[Path, dict]) -> None:
    """Check local Markdown links conservatively."""
    broken: list[str] = []
    for source_path, nb in nbs.items():
        for cell in nb.get("cells", []):
            source = cell.get("source", [])
            text = "".join(source) if isinstance(source, list) else str(source)
            for _label, target in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", text):
                target = target.strip()
                if not target or target.startswith(("http://", "https://", "#", "mailto:")):
                    continue

                local = unquote(target.split("#", 1)[0])
                if not local:
                    continue

                candidate_relative = source_path.parent / local
                candidate_root = Path(local)
                if candidate_relative.exists() or candidate_root.exists():
                    continue

                broken.append(f"{source_path} -> {local}")

    if broken:
        for item in sorted(set(broken))[:20]:
            report("WARN", "internal-links", item)
    else:
        report("PASS", "internal-links", "all checked local Markdown links resolve")


def check_encoding(paths: list[Path]) -> None:
    bad: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if unicodedata.normalize("NFC", text) != text:
            bad.append(str(path))
    report(
        "WARN" if bad else "PASS",
        "unicode-nfc",
        ", ".join(bad) if bad else "notebook text is NFC-normalised",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args()

    paths = notebook_paths()
    check_inventory(paths)

    nbs = check_json(paths) if paths else {}
    if nbs:
        check_notebook_schema(nbs)
        check_titles(nbs)
        check_code_cell_shape(nbs)
        check_internal_links(nbs)

    check_leaks(paths)
    check_encoding(paths)

    width = max((len(check) for _, check, _ in RESULTS), default=12)
    fails = warns = 0

    for level, check, message in RESULTS:
        if level == "FAIL":
            fails += 1
        elif level == "WARN":
            warns += 1
        mark = {"PASS": "✔", "WARN": "!", "FAIL": "✘"}[level]
        print(f"  {mark} {check.ljust(width)}  {message}")

    print()
    print(f"  {len(RESULTS) - fails - warns} passed, {warns} warning(s), {fails} failure(s)")
    return 1 if fails or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
