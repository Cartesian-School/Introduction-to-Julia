#!/usr/bin/env python3
"""Negative tests for tools/check_course.py.

A validator that only ever reports PASS is worthless. This builds deliberately
corrupted course fixtures in a temporary directory and asserts that
check_course.py rejects each one, so the guard itself stays honest.

Usage:
    python3 tools/test_check_course.py

Exit code 0 = the validator correctly rejected every corruption.
"""
from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "check_course.py")

NAV = "---\n\n*(начало курса)* | [Оглавление](README.md) | [Следующее занятие →](NEXT.md)"
OBJECTIVES = "## 🎯 После этого занятия вы сможете\n\n- делать что-нибудь полезное;"


def notebook(cells, kernel="Julia 1.11.3"):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": kernel, "language": "julia", "name": "julia-1.11"},
            "language_info": {"name": "julia", "version": "1.11.3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def code(src, ec=None, outs=None):
    return {"cell_type": "code", "execution_count": ec, "metadata": {},
            "outputs": outs or [], "source": [src]}


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": [src]}


def healthy_cells(lesson=1):
    """A minimal notebook that should pass every check."""
    return [
        md("# Занятие"),
        md(OBJECTIVES),
        md(f"#### ✅ Задание {lesson}.1\n\nСделайте что-нибудь."),
        code("# Ваше решение\n", 1),
        md("**Правильное решение:**"),
        code("x = 1 + 1\n", 2),
        code(f'@assert x == 2\nprintln("✔ Задание {lesson}.1 выполнено")\n', 3,
             [{"output_type": "stream", "name": "stdout",
               "text": [f"✔ Задание {lesson}.1 выполнено\n"]}]),
        md(NAV),
    ]


def write_course(root, mutate=None):
    """Write a 13-notebook course; `mutate` may corrupt notebook 01."""
    names = ["01 - a.ipynb", "02 - b.ipynb", "03 - c.ipynb", "04 - d.ipynb",
             "05 - e.ipynb", "06 - f.ipynb", "07 - g.ipynb", "08 - h.ipynb",
             "09 - i.ipynb", "10 - j.ipynb", "11 - k.ipynb", "12 - l.ipynb",
             "13 - m.ipynb"]
    for idx, name in enumerate(names):
        nb = notebook(healthy_cells(idx + 1))
        if idx == 0 and mutate:
            mutate(nb)
        with io.open(os.path.join(root, name), "w", encoding="utf-8") as fh:
            json.dump(nb, fh, ensure_ascii=False)
    # Nav targets must resolve (and must not look like a 14th notebook).
    for stub in ("README.md", "NEXT.md"):
        io.open(os.path.join(root, stub), "w", encoding="utf-8").write("stub\n")


def run_checker(root):
    proc = subprocess.run([sys.executable, CHECKER], cwd=root,
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout


# --------------------------------------------------------------------------- #
# Each corruption, and the check that must catch it.
def corrupt_unexpected_error(nb):
    nb["cells"][5]["outputs"] = [{"output_type": "error", "ename": "UndefVarError",
                                  "evalue": "UndefVarError: `y` not defined"}]


def corrupt_exec_counts(nb):
    nb["cells"][3]["execution_count"] = 9        # out of order


def corrupt_absolute_path(nb):
    nb["cells"][5]["outputs"] = [{"output_type": "stream", "name": "stdout",
                                  "text": ["/home/someuser/secret/project\n"]}]


def corrupt_windows_path(nb):
    nb["cells"][5]["outputs"] = [{"output_type": "stream", "name": "stdout",
                                  "text": ["C:\\Users\\Author\\course\n"]}]


def corrupt_secret(nb):
    nb["cells"][5]["source"] = ['token = "ghp_abcdefghijklmnopqrstuvwxyz0123456789"\n']


def corrupt_missing_solution(nb):
    nb["cells"][4] = md("(решение вырезано)")    # removes "Правильное решение"


def corrupt_kernel(nb):
    nb["metadata"]["kernelspec"]["display_name"] = "Julia 1.6.0"


def corrupt_missing_objectives(nb):
    nb["cells"][1] = md("просто текст без целей занятия")


def corrupt_missing_nav(nb):
    nb["cells"][-1] = md("конец")


def corrupt_stale_output(nb):
    nb["cells"].append(code("", None,
                            [{"output_type": "stream", "name": "stdout", "text": ["stale\n"]}]))


def corrupt_exercise_numbering(nb):
    nb["cells"][2] = md("#### ✅ Задание 7.1\n\nНомер не совпадает с занятием.")


def corrupt_broken_link(nb):
    nb["cells"][-1] = md("---\n\n[Оглавление](README.md) | [нет такого](99%20-%20missing.md)")


def corrupt_invalid_json(path):
    io.open(path, "w", encoding="utf-8").write("{ this is not json ")


CASES = [
    ("unexpected error output",   corrupt_unexpected_error,     "unexpected-errors"),
    ("non-monotonic exec counts", corrupt_exec_counts,          "exec-order"),
    ("absolute Linux path",       corrupt_absolute_path,        "no-local-paths"),
    ("absolute Windows path",     corrupt_windows_path,         "no-local-paths"),
    ("embedded GitHub token",     corrupt_secret,               "no-local-paths"),
    ("missing worked solution",   corrupt_missing_solution,     "exercise-solutions"),
    ("wrong kernel",              corrupt_kernel,               "kernel"),
    ("missing objectives",        corrupt_missing_objectives,   "objectives"),
    ("missing navigation",        corrupt_missing_nav,          "navigation"),
    ("stale output, no exec",     corrupt_stale_output,         "fresh-outputs"),
    ("exercise numbered wrong",   corrupt_exercise_numbering,   "exercise-numbering"),
    ("broken internal link",      corrupt_broken_link,          "internal-links"),
]


def main() -> int:
    failures = []

    # 0. Control: an uncorrupted fixture must PASS, otherwise the negative
    #    results below would be meaningless.
    with tempfile.TemporaryDirectory() as root:
        write_course(root)
        rc, out = run_checker(root)
        if rc != 0:
            failures.append("CONTROL: clean fixture should pass but did not\n" + out)
            print("  ✘ control (clean fixture should pass)")
        else:
            print("  ✔ control (clean fixture passes)")

    # 1. Each corruption must be rejected by the expected check.
    for label, mutate, expected_check in CASES:
        with tempfile.TemporaryDirectory() as root:
            write_course(root, mutate)
            rc, out = run_checker(root)
            caught = rc != 0 and any(
                line.strip().startswith("✘") and expected_check in line
                for line in out.splitlines())
            if caught:
                print(f"  ✔ rejected: {label}  (via {expected_check})")
            else:
                print(f"  ✘ NOT rejected: {label}  (expected {expected_check})")
                failures.append(f"{label}\n{out}")

    # 2. Wrong notebook count.
    with tempfile.TemporaryDirectory() as root:
        write_course(root)
        os.remove(os.path.join(root, "13 - m.ipynb"))
        rc, out = run_checker(root)
        if rc != 0 and "lesson-count" in out:
            print("  ✔ rejected: wrong notebook count  (via lesson-count)")
        else:
            failures.append("wrong notebook count\n" + out)
            print("  ✘ NOT rejected: wrong notebook count")

    # 3. Invalid notebook JSON.
    with tempfile.TemporaryDirectory() as root:
        write_course(root)
        corrupt_invalid_json(os.path.join(root, "01 - a.ipynb"))
        rc, out = run_checker(root)
        if rc != 0 and "valid-json" in out:
            print("  ✔ rejected: invalid notebook JSON  (via valid-json)")
        else:
            failures.append("invalid JSON\n" + out)
            print("  ✘ NOT rejected: invalid notebook JSON")

    print()
    total = len(CASES) + 3
    print(f"  {total - len(failures)}/{total} corruption scenarios correctly rejected")
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print("  -", f.splitlines()[0])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
