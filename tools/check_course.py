#!/usr/bin/env python3
"""Repository integrity checks for Cartesian School "Julia from Zero".

The checker validates stable repository invariants for the bilingual course.
It deliberately does not execute notebooks end-to-end.

Usage:
    python3 tools/check_course.py
    python3 tools/check_course.py --strict
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    import nbformat
except ImportError:  # pragma: no cover
    nbformat = None

EXPECTED_LESSONS = range(15)
LANGUAGES = ("PL", "RU")
REQUIRED_ROOT_FILES = (
    "PL",
    "RU",
    "Project.toml",
    "Manifest.toml",
    "README.md",
    "README.pl.md",
    "README.ru.md",
    "LICENSE",
    "LICENSE-CC-BY-NC-SA.md",
)
DOC_FILES = ("README.md", "README.pl.md", "README.ru.md", "Project.toml")

LESSON_SLUGS = {
    0: "Julia",
    1: "Strings",
    2: "Data_Structures",
    3: "Loops",
    4: "Conditionals",
    5: "Functions",
    6: "Packages",
    7: "Plotting",
    8: "Multiple_Dispatch",
    9: "Julia_is_Fast",
    10: "Linear_Algebra_Concepts",
    11: "Linear_Algebra_in_Julia",
    12: "Factorizations_and_Other_Fun",
    13: "Numerical_Computing",
    14: "Final_Project_Capstone",
}

CANONICAL_NOTEBOOKS = {
    "PL": {
        0: "PL/Lesson_0_Julia_Cartesian_School_PL.ipynb",
        1: "PL/Lesson_1_Strings_Julia_Cartesian_School_PL.ipynb",
        2: "PL/Lesson_2_Data_Structures_Julia_Cartesian_School_PL.ipynb",
        3: "PL/Lesson_3_Loops_Julia_Cartesian_School_PL.ipynb",
        4: "PL/Lesson_4_Conditionals_Julia_Cartesian_School_PL.ipynb",
        5: "PL/Lesson_5_Functions_Julia_Cartesian_School_PL.ipynb",
        6: "PL/Lesson_6_Packages_Julia_Cartesian_School_PL.ipynb",
        7: "PL/Lesson_7_Plotting_Julia_Cartesian_School_PL.ipynb",
        8: "PL/Lesson_8_Multiple_Dispatch_Julia_Cartesian_School_PL.ipynb",
        9: "PL/Lesson_9_Julia_is_Fast_Cartesian_School_PL.ipynb",
        10: "PL/Lesson_10_Linear_Algebra_Concepts_Julia_Cartesian_School_PL.ipynb",
        11: "PL/Lesson_11_Linear_Algebra_in_Julia_Cartesian_School_PL.ipynb",
        12: "PL/Lesson_12_Factorizations_and_Other_Fun_Julia_Cartesian_School_PL.ipynb",
        13: "PL/Lesson_13_Numerical_Computing_Julia_Cartesian_School_PL.ipynb",
        14: "PL/Lesson_14_Final_Project_Capstone_Julia_Cartesian_PL.ipynb",
    },
    "RU": {
        0: "RU/Lesson_0_Julia_Cartesian_School_RU.ipynb",
        1: "RU/Lesson_1_Strings_Julia_Cartesian_School_RU.ipynb",
        2: "RU/Lesson_2_Data_Structures_Julia_Cartesian_School_RU.ipynb",
        3: "RU/Lesson_3_Loops_Julia_Cartesian_School_RU.ipynb",
        4: "RU/Lesson_4_Conditionals_Julia_Cartesian_School_RU.ipynb",
        5: "RU/Lesson_5_Functions_Julia_Cartesian_School_RU.ipynb",
        6: "RU/Lesson_6_Packages_Julia_Cartesian_School_RU.ipynb",
        7: "RU/Lesson_7_Plotting_Julia_Cartesian_School_RU.ipynb",
        8: "RU/Lesson_8_Multiple_Dispatch_Julia_Cartesian_School_RU.ipynb",
        9: "RU/Lesson_9_Julia_is_Fast_Cartesian_School_RU.ipynb",
        10: "RU/Lesson_10_Linear_Algebra_Concepts_Julia_Cartesian_School_RU.ipynb",
        11: "RU/Lesson_11_Linear_Algebra_in_Julia_Cartesian_School_RU.ipynb",
        12: "RU/Lesson_12_Factorizations_and_Other_Fun_Julia_Cartesian_School_RU.ipynb",
        13: "RU/Lesson_13_Numerical_Computing_Julia_Cartesian_School_RU.ipynb",
        14: "RU/Lesson_14_Final_Project_Capstone_Julia_Cartesian_School_RU.ipynb",
    },
}

PL_MARKERS = (
    "Informacje o lekcji",
    "Cele lekcji",
    "Przykładowe rozwiązanie",
    "Twoje rozwiązanie",
    "Podsumowanie lekcji",
    "Źródła do dalszego",
    "[Spis treści]",
)
RU_MARKERS = (
    "Информация об уроке",
    "Цели урока",
    "Пример решения",
    "Ваше решение",
    "Итоги урока",
    "Источники для дальнейшего",
    "[Оглавление]",
)

LEAK_PATTERNS = (
    (re.compile(r"[A-Za-z]:\\+Users\\+[A-Za-z0-9_. -]+\\+", re.I), "Windows user path"),
    (re.compile(r"/home/(?!<)[A-Za-z0-9_.-]+/"), "Linux home path"),
    (re.compile(r"/Users/[A-Za-z0-9_.-]+/"), "macOS home path"),
    (re.compile(r"/media/[A-Za-z0-9_.-]+/"), "removable-media path"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), "GitHub token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"), "GitHub token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b(?:api[_-]?key|token|password|secret)\s*=\s*['\"][^'\"]{12,}['\"]"), "credential assignment"),
)

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_SRC_RE = re.compile(r"<img\s+[^>]*src=[\"']([^\"']+)[\"']", re.I)
RESULTS: list[tuple[str, str, str]] = []


@dataclass(frozen=True)
class NotebookInfo:
    path: Path
    language: str
    lesson: int
    data: dict
    cell_types: tuple[str, ...]


def report(level: str, check: str, message: str) -> None:
    RESULTS.append((level, check, message))


def text_from_source(source: object) -> str:
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return source if isinstance(source, str) else ""


def notebook_text(nb: dict) -> str:
    return "\n".join(text_from_source(cell.get("source", "")) for cell in nb.get("cells", []))


def redact(value: str) -> str:
    return "<redacted>" if len(value) <= 12 else f"{value[:6]}...{value[-4:]}"


def parse_lesson_number(path: Path) -> int | None:
    match = re.match(r"Lesson_(\d+)_", path.name)
    return int(match.group(1)) if match else None


def canonical_path(language: str, lesson: int) -> Path:
    return Path(CANONICAL_NOTEBOOKS[language][lesson])


def check_repository_structure(root: Path) -> None:
    missing = [name for name in REQUIRED_ROOT_FILES if not (root / name).exists()]
    if missing:
        report("FAIL", "repository-structure", f"missing required paths: {', '.join(missing)}")
    else:
        report("PASS", "repository-structure", "required course files and language directories exist")


def check_inventory(root: Path) -> list[Path]:
    expected_paths: list[Path] = []
    for language in LANGUAGES:
        lang_dir = root / language
        if not lang_dir.is_dir():
            report("FAIL", f"{language}-inventory", f"missing {language}/ directory")
            continue
        canonical = {root / rel for rel in CANONICAL_NOTEBOOKS[language].values()}
        present_lesson_files = sorted(lang_dir.glob("Lesson_*.ipynb"))
        extra_lesson_files = [path for path in present_lesson_files if path not in canonical]
        if extra_lesson_files:
            details = ", ".join(str(path.relative_to(root)) for path in extra_lesson_files)
            report("FAIL", f"{language}-legacy-notebooks", f"unexpected Lesson_*.ipynb files: {details}")
        else:
            report("PASS", f"{language}-legacy-notebooks", "no duplicate or legacy Lesson_*.ipynb files found")

        missing_lessons = []
        for lesson in EXPECTED_LESSONS:
            path = canonical_path(language, lesson)
            expected_paths.append(path)
            if not (root / path).exists():
                missing_lessons.append(lesson)
        if missing_lessons:
            report("FAIL", f"{language}-inventory", f"missing canonical lessons: {missing_lessons}")
        else:
            report("PASS", f"{language}-inventory", "exactly 15 canonical notebooks for Lesson 0..14")
    return expected_paths


def load_notebooks(root: Path, paths: list[Path]) -> dict[tuple[str, int], NotebookInfo]:
    notebooks: dict[tuple[str, int], NotebookInfo] = {}
    failures = 0
    for language in LANGUAGES:
        for lesson in EXPECTED_LESSONS:
            path = canonical_path(language, lesson)
            full_path = root / path
            if not full_path.exists():
                continue
            try:
                with io.open(full_path, encoding="utf-8") as handle:
                    data = json.load(handle)
            except UnicodeDecodeError as exc:
                report("FAIL", "valid-json", f"{path}: not valid UTF-8: {exc}")
                failures += 1
                continue
            except json.JSONDecodeError as exc:
                report("FAIL", "valid-json", f"{path}: malformed JSON: {exc}")
                failures += 1
                continue
            except OSError as exc:
                report("FAIL", "valid-json", f"{path}: cannot read file: {exc}")
                failures += 1
                continue
            cells = data.get("cells") if isinstance(data, dict) else None
            cell_types = tuple(cell.get("cell_type", "") for cell in cells) if isinstance(cells, list) else ()
            notebooks[(language, lesson)] = NotebookInfo(path, language, lesson, data, cell_types)

    if failures:
        report("FAIL", "valid-json", f"{failures} notebook(s) failed JSON/UTF-8 parsing")
    elif len(notebooks) == len(paths):
        report("PASS", "valid-json", f"all {len(notebooks)} canonical notebooks parse as UTF-8 JSON")
    return notebooks


def check_notebook_schema(notebooks: dict[tuple[str, int], NotebookInfo]) -> None:
    bad: list[str] = []
    for info in notebooks.values():
        nb = info.data
        if not isinstance(nb, dict):
            bad.append(f"{info.path}: notebook root must be a JSON object")
            continue
        if nb.get("nbformat") != 4:
            bad.append(f"{info.path}: expected nbformat 4, got {nb.get('nbformat')!r}")
        cells = nb.get("cells")
        if not isinstance(cells, list) or not cells:
            bad.append(f"{info.path}: cells must be a non-empty list")
            continue
        for index, cell in enumerate(cells):
            if not isinstance(cell, dict):
                bad.append(f"{info.path} cell {index}: cell must be an object")
                continue
            if cell.get("cell_type") not in {"markdown", "code", "raw"}:
                bad.append(f"{info.path} cell {index}: invalid cell_type={cell.get('cell_type')!r}")
            if not isinstance(cell.get("source", []), (list, str)):
                bad.append(f"{info.path} cell {index}: source must be a string or list")
            if cell.get("cell_type") == "code":
                if "execution_count" not in cell:
                    bad.append(f"{info.path} cell {index}: code cell missing execution_count")
                if not isinstance(cell.get("outputs"), list):
                    bad.append(f"{info.path} cell {index}: code cell outputs must be a list")
        if nbformat is not None:
            try:
                nbformat.validate(nb)
            except Exception as exc:  # noqa: BLE001
                bad.append(f"{info.path}: nbformat validation failed: {exc}")

    if bad:
        for item in bad[:40]:
            report("FAIL", "notebook-schema", item)
    else:
        report("PASS", "notebook-schema", "all canonical notebooks have valid nbformat-4 structure")


def check_kernel_metadata(notebooks: dict[tuple[str, int], NotebookInfo]) -> None:
    bad: list[str] = []
    for info in notebooks.values():
        metadata = info.data.get("metadata", {})
        kernelspec = metadata.get("kernelspec", {}) if isinstance(metadata, dict) else {}
        language_info = metadata.get("language_info", {}) if isinstance(metadata, dict) else {}
        values = [
            str(kernelspec.get("language", "")),
            str(kernelspec.get("name", "")),
            str(kernelspec.get("display_name", "")),
            str(language_info.get("name", "")) if isinstance(language_info, dict) else "",
        ]
        populated = [value.lower() for value in values if value]
        if populated and not any("julia" in value for value in populated):
            bad.append(f"{info.path}: kernel/language metadata does not identify Julia")
    if bad:
        for item in bad:
            report("FAIL", "julia-kernel", item)
    else:
        report("PASS", "julia-kernel", "kernel metadata is absent or compatible with Julia")


def check_lesson_headers(notebooks: dict[tuple[str, int], NotebookInfo]) -> None:
    bad: list[str] = []
    for info in notebooks.values():
        header_text = "\n".join(
            text_from_source(cell.get("source", ""))
            for cell in info.data.get("cells", [])[:10]
            if cell.get("cell_type") == "markdown"
        )
        if not re.search(rf"\bLesson\s+{info.lesson}\b", header_text, re.I):
            bad.append(f"{info.path}: header does not identify Lesson {info.lesson}")
    if bad:
        for item in bad:
            report("FAIL", "lesson-header", item)
    else:
        report("PASS", "lesson-header", "every notebook header identifies the filename lesson number")


def check_language_contamination(notebooks: dict[tuple[str, int], NotebookInfo]) -> None:
    bad: list[str] = []
    for info in notebooks.values():
        text = notebook_text(info.data)
        forbidden = PL_MARKERS if info.language == "RU" else RU_MARKERS
        for marker in forbidden:
            if marker in text:
                bad.append(f"{info.path}: unexpected marker {marker!r}")
    if bad:
        for item in bad[:40]:
            report("FAIL", "language-contamination", item)
    else:
        report("PASS", "language-contamination", "no obvious cross-language pedagogical markers detected")


def check_parity(notebooks: dict[tuple[str, int], NotebookInfo]) -> None:
    bad: list[str] = []
    for lesson in EXPECTED_LESSONS:
        pl = notebooks.get(("PL", lesson))
        ru = notebooks.get(("RU", lesson))
        if not pl or not ru:
            missing = "PL" if not pl else "RU"
            bad.append(f"Lesson {lesson}: missing {missing} counterpart")
            continue
        expected_slug = LESSON_SLUGS[lesson]
        if expected_slug not in pl.path.name or expected_slug not in ru.path.name:
            bad.append(f"Lesson {lesson}: filename slug does not match expected topic {expected_slug!r}")
        if pl.data.get("nbformat") != ru.data.get("nbformat"):
            bad.append(f"Lesson {lesson}: nbformat mismatch")
        if len(pl.cell_types) != len(ru.cell_types):
            bad.append(f"Lesson {lesson}: cell-count mismatch PL={len(pl.cell_types)} RU={len(ru.cell_types)}")
        elif pl.cell_types != ru.cell_types:
            bad.append(f"Lesson {lesson}: cell-type sequence mismatch")
    if bad:
        for item in bad:
            report("FAIL", "pl-ru-parity", item)
    else:
        report("PASS", "pl-ru-parity", "PL and RU notebooks match by lesson, topic slug, nbformat, cell count, and cell types")


def iter_links(text: str) -> list[str]:
    links = [match.group(2).strip() for match in MARKDOWN_LINK_RE.finditer(text)]
    links.extend(match.group(1).strip() for match in HTML_SRC_RE.finditer(text))
    return links


def is_external_or_special(target: str) -> bool:
    parsed = urlparse(target)
    return bool(parsed.scheme in {"http", "https", "mailto", "tel"} or target.startswith("#"))


def link_exists(root: Path, source_path: Path, target: str) -> bool:
    local = unquote(target.split("#", 1)[0])
    if not local:
        return True
    candidate = (source_path.parent / local).resolve()
    root_resolved = root.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        return False
    return candidate.exists()


def check_local_links(root: Path, notebooks: dict[tuple[str, int], NotebookInfo]) -> None:
    broken: list[str] = []
    nav_errors: list[str] = []
    for info in notebooks.values():
        targets: list[str] = []
        for cell in info.data.get("cells", []):
            if cell.get("cell_type") != "markdown":
                continue
            text = text_from_source(cell.get("source", ""))
            targets.extend(target for target in iter_links(text) if not is_external_or_special(target))

        target_names = [Path(unquote(target.split("#", 1)[0])).name for target in targets]
        expected_readme = "../README.pl.md" if info.language == "PL" else "../README.ru.md"
        if expected_readme not in targets:
            nav_errors.append(f"{info.path}: missing language README link {expected_readme}")
        if info.lesson > 0 and canonical_path(info.language, info.lesson - 1).name not in target_names:
            nav_errors.append(f"{info.path}: missing previous lesson link")
        if info.lesson < 14 and canonical_path(info.language, info.lesson + 1).name not in target_names:
            nav_errors.append(f"{info.path}: missing next lesson link")
        for target in targets:
            if not link_exists(root, root / info.path, target):
                broken.append(f"{info.path} -> {target}")

    for doc_name in ("README.md", "README.pl.md", "README.ru.md"):
        doc_path = root / doc_name
        if not doc_path.exists():
            continue
        text = doc_path.read_text(encoding="utf-8")
        for target in iter_links(text):
            if not is_external_or_special(target) and not link_exists(root, doc_path, target):
                broken.append(f"{doc_name} -> {target}")

    if broken or nav_errors:
        for item in sorted(set(nav_errors + broken))[:60]:
            report("FAIL", "local-links", item)
    else:
        report("PASS", "local-links", "notebook navigation and local Markdown/HTML links resolve")


def check_hygiene(root: Path, paths: list[Path]) -> None:
    hits: list[str] = []
    for relative in paths:
        path = root / relative
        if not path.exists() or path.is_dir():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern, label in LEAK_PATTERNS:
            for match in pattern.finditer(text):
                hits.append(f"{relative}: {label}: {redact(match.group(0))}")
    if hits:
        for hit in hits[:40]:
            report("FAIL", "repository-hygiene", hit)
    else:
        report("PASS", "repository-hygiene", "no user paths or credential patterns detected in notebooks/docs")


def check_docs(root: Path) -> None:
    bad: list[str] = []
    for doc_name in DOC_FILES:
        path = root / doc_name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "Cartesian-School/Introduction-to-Julia" in text:
            bad.append(f"{doc_name}: stale Introduction-to-Julia repository URL/reference")
        if re.search(r"\b13\s+(lessons|lekcji|урок)", text, re.I):
            bad.append(f"{doc_name}: stale 13-lesson count")
        stale_paths = re.findall(r"Lesson_[^)\s\"]*Professional[^)\s\"]*|(?:\d{2}|12|13)%20-%20[^)\s\"]*\.ipynb", text)
        if stale_paths:
            bad.append(f"{doc_name}: stale notebook path(s): {', '.join(sorted(set(stale_paths))[:5])}")
    if bad:
        for item in bad:
            report("FAIL", "documentation", item)
    else:
        report("PASS", "documentation", "documentation/config has no stale repository names, lesson counts, or legacy notebook paths")


def check_unicode(paths: list[Path]) -> None:
    bad: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            report("FAIL", "unicode-utf8", f"{path}: not valid UTF-8")
            continue
        if unicodedata.normalize("NFC", text) != text:
            bad.append(str(path))
    if bad:
        report("WARN", "unicode-nfc", f"non-NFC text in: {', '.join(bad[:20])}")
    else:
        report("PASS", "unicode-nfc", "checked text files are NFC-normalized")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args()

    root = Path.cwd()
    RESULTS.clear()
    check_repository_structure(root)
    expected_notebooks = check_inventory(root)
    notebooks = load_notebooks(root, expected_notebooks)
    if notebooks:
        check_notebook_schema(notebooks)
        check_kernel_metadata(notebooks)
        check_lesson_headers(notebooks)
        check_parity(notebooks)
        check_local_links(root, notebooks)
        check_language_contamination(notebooks)
    hygiene_paths = expected_notebooks + [Path(name) for name in DOC_FILES]
    check_hygiene(root, hygiene_paths)
    check_docs(root)
    check_unicode(hygiene_paths)

    width = max((len(check) for _, check, _ in RESULTS), default=12)
    fails = warns = 0
    for level, check, message in RESULTS:
        fails += level == "FAIL"
        warns += level == "WARN"
        print(f"{level:4} {check.ljust(width)}  {message}")
    print()
    print(f"{len(RESULTS) - fails - warns} passed, {warns} warning(s), {fails} failure(s)")
    return 1 if fails or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
