#!/usr/bin/env python3
"""Course integrity checks for Introduction-to-Julia.

Validates invariants that a reviewer would otherwise have to check by hand:
notebook validity, kernel consistency, execution order, absence of leaked local
paths, exercise/solution pairing, and navigation.

Usage:
    python3 tools/check_course.py            # report
    python3 tools/check_course.py --strict   # also fail on warnings

Exit code 0 = all checks passed.
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import sys
import unicodedata

EXPECTED_LESSONS = 13
EXPECTED_KERNEL = "Julia 1.11.3"

# Cells that raise on purpose, keyed by notebook prefix. Each entry is the
# exception name a reviewer has accepted as pedagogical. Anything else is a
# genuine failure and gets reported.
# NOTE: LoadError is deliberately absent. In Julia it wraps the real exception,
# so allowing it here would let any failure through. When ename is LoadError we
# look at the wrapped name inside evalue instead.
ALLOWED_ERRORS = {
    "01": {"MethodError"},
    "02": {"ParseError", "Base.Meta.ParseError"},
    "03": {"MethodError", "KeyError"},
    "06": {"MethodError"},
    "09": {"MethodError"},
    "11": {"DimensionMismatch"},
    "13": {"PosDefException"},
}

# Absolute paths and personal identifiers that must never reach a commit.
LEAK_PATTERNS = [
    (re.compile(r"[A-Za-z]:\\+Users\\+", re.I), "Windows user path"),
    (re.compile(r"/home/(?!<)[a-z0-9_-]+/", re.I), "Linux home path"),
    (re.compile(r"/Users/[a-z0-9_-]+/", re.I), "macOS home path"),
    (re.compile(r"/media/[a-z0-9_-]+/", re.I), "removable-media path"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
]

RESULTS: list[tuple[str, str, str]] = []   # (level, check, message)


def report(level: str, check: str, message: str) -> None:
    RESULTS.append((level, check, message))


def notebooks() -> list[str]:
    return sorted(glob.glob("*.ipynb"))


def load(path: str) -> dict:
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- #
def check_count(paths: list[str]) -> None:
    if len(paths) != EXPECTED_LESSONS:
        report("FAIL", "lesson-count",
               f"expected {EXPECTED_LESSONS} notebooks, found {len(paths)}")
    else:
        report("PASS", "lesson-count", f"{EXPECTED_LESSONS} notebooks present")


def check_json(paths: list[str]) -> dict[str, dict]:
    loaded = {}
    for p in paths:
        try:
            loaded[p] = load(p)
        except Exception as exc:                      # noqa: BLE001
            report("FAIL", "valid-json", f"{p}: {exc}")
    if len(loaded) == len(paths):
        report("PASS", "valid-json", f"all {len(paths)} notebooks parse")
    return loaded


def check_kernel(nbs: dict[str, dict]) -> None:
    bad = [p for p, nb in nbs.items()
           if nb.get("metadata", {}).get("kernelspec", {}).get("display_name") != EXPECTED_KERNEL]
    if bad:
        for p in bad:
            got = nbs[p].get("metadata", {}).get("kernelspec", {}).get("display_name")
            report("FAIL", "kernel", f"{p}: kernel is {got!r}, expected {EXPECTED_KERNEL!r}")
    else:
        report("PASS", "kernel", f"all notebooks declare {EXPECTED_KERNEL}")


def check_exec_order(nbs: dict[str, dict]) -> None:
    bad = []
    for p, nb in nbs.items():
        counts = [c.get("execution_count") for c in nb["cells"]
                  if c["cell_type"] == "code" and c.get("execution_count") is not None]
        if counts != sorted(counts) or (counts and counts != list(range(1, len(counts) + 1))):
            bad.append(f"{p}: {counts[:8]}...")
    if bad:
        for b in bad:
            report("FAIL", "exec-order", b)
    else:
        report("PASS", "exec-order", "execution counts are monotonic 1..N everywhere")


def check_errors(nbs: dict[str, dict]) -> None:
    unexpected = []
    total = 0
    for p, nb in nbs.items():
        allowed = ALLOWED_ERRORS.get(p[:2], set())
        for i, cell in enumerate(nb["cells"]):
            for out in cell.get("outputs", []):
                if out.get("output_type") != "error":
                    continue
                total += 1
                ename = out.get("ename", "?")
                evalue = str(out.get("evalue", ""))
                if ename in ("LoadError", "TaskFailedException"):
                    # Unwrap: the informative name is inside the message. Julia
                    # renders it as "ExceptionName: detail", and not every
                    # exception name ends in Error/Exception (DimensionMismatch).
                    inner = set(re.findall(r"[A-Z][A-Za-z.]*(?:Error|Exception|Mismatch)", evalue))
                    lead = re.match(r"\s*([A-Z][A-Za-z0-9_.]*)\s*[:(]", evalue)
                    if lead:
                        inner.add(lead.group(1))
                    inner.discard("LoadError")
                else:
                    inner = {ename}
                if not (inner & allowed):
                    unexpected.append(f"{p} cell {i}: {ename}: {evalue[:70]}")
    if unexpected:
        for u in unexpected:
            report("FAIL", "unexpected-errors", u)
    else:
        report("PASS", "unexpected-errors",
               f"{total} error outputs, all in the reviewed intentional set")


def check_leaks(paths: list[str]) -> None:
    """Notebooks are scanned for everything; prose docs only for secrets.

    AUDIT_REPORT.md deliberately quotes the leaked paths it documents, so
    scanning it for path patterns would flag the evidence rather than a leak.
    Secrets are still checked everywhere -- there is no legitimate reason to
    quote a live token.
    """
    secret_only = {"GitHub token", "AWS access key", "private key"}
    hits = []

    for p in paths:                                   # notebooks: full scan
        text = io.open(p, encoding="utf-8").read()
        for pattern, label in LEAK_PATTERNS:
            for m in pattern.finditer(text):
                hits.append(f"{p}: {label}: {m.group(0)[:50]}")

    for p in ("README.md", "TODO.md", "AUDIT_REPORT.md"):   # docs: secrets only
        if not os.path.exists(p):
            continue
        text = io.open(p, encoding="utf-8").read()
        for pattern, label in LEAK_PATTERNS:
            if label not in secret_only:
                continue
            for m in pattern.finditer(text):
                hits.append(f"{p}: {label}")

    if hits:
        for h in hits[:20]:
            report("FAIL", "no-local-paths", h)
    else:
        report("PASS", "no-local-paths",
               "no local paths in notebooks, no secrets anywhere")


def check_structure(nbs: dict[str, dict]) -> None:
    """Objectives, navigation, and the exercise/solution contract."""
    no_obj, no_nav = [], []
    for p, nb in nbs.items():
        head = "\n".join("".join(c["source"]) for c in nb["cells"][:4])
        if "После этого занятия вы сможете" not in head:
            no_obj.append(p)
        navs = sum(1 for c in nb["cells"] if "Оглавление](README.md)" in "".join(c["source"]))
        if navs != 1:
            no_nav.append(f"{p} ({navs} nav cells)")

    report("FAIL" if no_obj else "PASS", "objectives",
           ", ".join(no_obj) if no_obj else "every lesson states learning objectives")
    report("FAIL" if no_nav else "PASS", "navigation",
           ", ".join(no_nav) if no_nav else "every lesson has exactly one navigation footer")

    # Every "Задание N.M" should be followed somewhere by a worked solution.
    missing = []
    for p, nb in nbs.items():
        text = "\n".join("".join(c["source"]) for c in nb["cells"])
        tasks = set(re.findall(r"Задание\s+(\d+\.\d+)", text))
        if tasks and "равильное решение" not in text:
            missing.append(f"{p}: {len(tasks)} exercise(s), no worked solution")
    report("FAIL" if missing else "PASS", "exercise-solutions",
           "; ".join(missing) if missing else "every lesson with exercises has worked solutions")

    # Lesson numbering inside exercise titles must match the file number.
    mismatched = []
    for p, nb in nbs.items():
        try:
            lesson_no = int(p[:2])
        except ValueError:
            continue
        text = "\n".join("".join(c["source"]) for c in nb["cells"])
        for num in set(re.findall(r"Задание\s+(\d+)\.\d+", text)):
            if int(num) != lesson_no:
                mismatched.append(f"{p}: contains 'Задание {num}.x'")
    report("FAIL" if mismatched else "PASS", "exercise-numbering",
           "; ".join(sorted(set(mismatched))) if mismatched
           else "exercise numbers match their lesson")


def check_outputs_fresh(nbs: dict[str, dict]) -> None:
    """A code cell with output but no execution_count means stale saved output."""
    stale = []
    for p, nb in nbs.items():
        for i, c in enumerate(nb["cells"]):
            if c["cell_type"] == "code" and c.get("outputs") and c.get("execution_count") is None:
                stale.append(f"{p} cell {i}")
    report("FAIL" if stale else "PASS", "fresh-outputs",
           ", ".join(stale[:8]) if stale else "no outputs left over from an unrun cell")


def check_nav_targets(nbs: dict[str, dict]) -> None:
    from urllib.parse import unquote
    broken = []
    for p, nb in nbs.items():
        for c in nb["cells"]:
            for _label, target in re.findall(r"\[([^\]]*)\]\(([^)]+)\)", "".join(c["source"])):
                if target.startswith(("http", "#", "mailto")):
                    continue
                path = unquote(target.split("#")[0])
                if path and not os.path.exists(path):
                    broken.append(f"{p} -> {path}")
    report("FAIL" if broken else "PASS", "internal-links",
           ", ".join(sorted(set(broken))[:8]) if broken
           else "all internal notebook links resolve")


def check_encoding(paths: list[str]) -> None:
    bad = []
    for p in paths:
        text = io.open(p, encoding="utf-8").read()
        if unicodedata.normalize("NFC", text) != text:
            bad.append(p)
    report("WARN" if bad else "PASS", "unicode-nfc",
           ", ".join(bad) if bad else "text is NFC-normalised")


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args()

    paths = notebooks()
    check_count(paths)
    nbs = check_json(paths)
    if nbs:
        check_kernel(nbs)
        check_exec_order(nbs)
        check_errors(nbs)
        check_structure(nbs)
        check_outputs_fresh(nbs)
        check_nav_targets(nbs)
    check_leaks(paths)
    check_encoding(paths)

    width = max(len(c) for _, c, _ in RESULTS)
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
