#!/usr/bin/env python3
"""Negative tests for tools/check_course.py.

The test suite creates a minimal canonical PL/Lesson_0..14 course in a
temporary directory and verifies that deliberate structural corruptions are
rejected by the validator.

Usage:
    python3 tools/test_check_course.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_course.py"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": [text]}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [text],
    }


def notebook(lesson: int) -> dict:
    return {
        "cells": [
            md(f"# Julia od zera — **Lesson {lesson}**\n"),
            md("## Cele lekcji\n\nPo tej lekcji potrafisz pracować z przykładowym materiałem.\n"),
            code("x = 1 + 1\n"),
            md("## Podsumowanie\n"),
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Julia",
                "language": "julia",
                "name": "julia",
            },
            "language_info": {"name": "julia"},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }


def canonical_name(lesson: int) -> str:
    return f"Lesson_{lesson}_Fixture_Cartesian_School_PL.ipynb"


def write_course(root: Path) -> None:
    (root / "PL").mkdir(parents=True, exist_ok=True)

    for lesson in range(15):
        path = root / "PL" / canonical_name(lesson)
        path.write_text(json.dumps(notebook(lesson), ensure_ascii=False), encoding="utf-8")

    for readme in ("README.md", "README.pl.md", "README.ru.md"):
        (root / readme).write_text("stub\n", encoding="utf-8")


def run_checker(root: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(CHECKER)],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout


def expect_rejected(root: Path, check_name: str) -> bool:
    rc, output = run_checker(root)
    return rc != 0 and any(
        line.strip().startswith("✘") and check_name in line
        for line in output.splitlines()
    )


def main() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_course(root)
        rc, output = run_checker(root)
        if rc == 0:
            print("  ✔ control: canonical 15-lesson PL fixture passes")
        else:
            print("  ✘ control: canonical fixture failed")
            failures.append("control\n" + output)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_course(root)
        (root / "PL" / canonical_name(14)).unlink()
        if expect_rejected(root, "lesson-count"):
            print("  ✔ rejected: missing Lesson 14")
        else:
            print("  ✘ NOT rejected: missing Lesson 14")
            failures.append("missing lesson")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_course(root)
        src = root / "PL" / canonical_name(1)
        dst = root / "PL" / "Lesson_1_Duplicate_Cartesian_School_PL.ipynb"
        shutil.copy2(src, dst)
        rc, output = run_checker(root)
        caught = rc != 0 and (
            "lesson-count" in output or "lesson-numbering" in output
        )
        if caught:
            print("  ✔ rejected: duplicate lesson number")
        else:
            print("  ✘ NOT rejected: duplicate lesson number")
            failures.append("duplicate lesson number")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_course(root)
        path = root / "PL" / canonical_name(3)
        path.write_text("{ not valid json", encoding="utf-8")
        if expect_rejected(root, "valid-json"):
            print("  ✔ rejected: invalid notebook JSON")
        else:
            print("  ✘ NOT rejected: invalid notebook JSON")
            failures.append("invalid json")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_course(root)
        path = root / "PL" / canonical_name(4)
        nb = json.loads(path.read_text(encoding="utf-8"))
        nb["cells"][0]["source"] = ["# Julia od zera — **Lesson 99**\n"]
        path.write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")
        if expect_rejected(root, "lesson-title"):
            print("  ✔ rejected: title/filename lesson mismatch")
        else:
            print("  ✘ NOT rejected: title/filename lesson mismatch")
            failures.append("wrong title")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_course(root)
        path = root / "PL" / canonical_name(5)
        nb = json.loads(path.read_text(encoding="utf-8"))
        nb["cells"][2]["source"] = ['token = "ghp_abcdefghijklmnopqrstuvwxyz0123456789"\n']
        path.write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")
        if expect_rejected(root, "no-leaks"):
            print("  ✔ rejected: embedded token")
        else:
            print("  ✘ NOT rejected: embedded token")
            failures.append("secret")

    print()
    total = 6
    print(f"  {total - len(failures)}/{total} validation scenarios passed")

    if failures:
        print("\nFAILURES:")
        for failure in failures:
            print("  -", failure.splitlines()[0])
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
