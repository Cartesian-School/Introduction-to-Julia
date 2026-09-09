#!/usr/bin/env python3
"""Fixture-based tests for tools/check_course.py.

Each scenario builds an isolated bilingual course tree and runs the real
validator as a subprocess.
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

PL_FILES = {
    0: "Lesson_0_Julia_Cartesian_School_PL.ipynb",
    1: "Lesson_1_Strings_Julia_Cartesian_School_PL.ipynb",
    2: "Lesson_2_Data_Structures_Julia_Cartesian_School_PL.ipynb",
    3: "Lesson_3_Loops_Julia_Cartesian_School_PL.ipynb",
    4: "Lesson_4_Conditionals_Julia_Cartesian_School_PL.ipynb",
    5: "Lesson_5_Functions_Julia_Cartesian_School_PL.ipynb",
    6: "Lesson_6_Packages_Julia_Cartesian_School_PL.ipynb",
    7: "Lesson_7_Plotting_Julia_Cartesian_School_PL.ipynb",
    8: "Lesson_8_Multiple_Dispatch_Julia_Cartesian_School_PL.ipynb",
    9: "Lesson_9_Julia_is_Fast_Cartesian_School_PL.ipynb",
    10: "Lesson_10_Linear_Algebra_Concepts_Julia_Cartesian_School_PL.ipynb",
    11: "Lesson_11_Linear_Algebra_in_Julia_Cartesian_School_PL.ipynb",
    12: "Lesson_12_Factorizations_and_Other_Fun_Julia_Cartesian_School_PL.ipynb",
    13: "Lesson_13_Numerical_Computing_Julia_Cartesian_School_PL.ipynb",
    14: "Lesson_14_Final_Project_Capstone_Julia_Cartesian_PL.ipynb",
}
RU_FILES = {
    lesson: name.replace("_PL.ipynb", "_RU.ipynb").replace("Cartesian_PL", "Cartesian_School_RU")
    for lesson, name in PL_FILES.items()
}
RU_FILES[14] = "Lesson_14_Final_Project_Capstone_Julia_Cartesian_School_RU.ipynb"


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


def notebook(lang: str, lesson: int) -> dict:
    readme = "../README.pl.md" if lang == "PL" else "../README.ru.md"
    heading = "Informacje o lekcji" if lang == "PL" else "Информация об уроке"
    cells = [
        md(f"# Julia {'od zera' if lang == 'PL' else 'с нуля'} -- Lesson {lesson}\n"),
        md(f"## {heading}\n\nLesson {lesson} fixture.\n"),
        code("x = 1 + 1\n"),
    ]
    nav: list[str] = []
    files = PL_FILES if lang == "PL" else RU_FILES
    if lesson > 0:
        nav.append(f"[<- Lesson {lesson - 1}]({files[lesson - 1]})  \n")
    nav.append(f"[{'Spis treści' if lang == 'PL' else 'Оглавление'}]({readme})")
    if lesson < 14:
        nav.append(f"  \n[Lesson {lesson + 1} ->]({files[lesson + 1]})\n")
    cells.append(md("".join(nav)))
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Julia 1.11", "language": "julia", "name": "julia-1.11"},
            "language_info": {"name": "julia"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def path_for(root: Path, lang: str, lesson: int) -> Path:
    files = PL_FILES if lang == "PL" else RU_FILES
    return root / lang / files[lesson]


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def write_course(root: Path) -> None:
    for lang in ("PL", "RU"):
        (root / lang).mkdir(parents=True, exist_ok=True)
        for lesson in range(15):
            write_json(path_for(root, lang, lesson), notebook(lang, lesson))

    (root / "Project.toml").write_text("[deps]\n", encoding="utf-8")
    (root / "Manifest.toml").write_text("manifest_format = \"2.0\"\n", encoding="utf-8")
    (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (root / "LICENSE-CC-BY-NC-SA.md").write_text("CC\n", encoding="utf-8")
    (root / "README.md").write_text("[Polski](README.pl.md) [Русский](README.ru.md)\n", encoding="utf-8")
    (root / "README.pl.md").write_text("[English](README.md) [Русский](README.ru.md)\n", encoding="utf-8")
    (root / "README.ru.md").write_text("[English](README.md) [Polski](README.pl.md)\n", encoding="utf-8")


def run_checker(root: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--strict"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout + proc.stderr


def load_nb(root: Path, lang: str, lesson: int) -> dict:
    return json.loads(path_for(root, lang, lesson).read_text(encoding="utf-8"))


def save_nb(root: Path, lang: str, lesson: int, nb: dict) -> None:
    write_json(path_for(root, lang, lesson), nb)


def expect_pass(name: str, failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_course(root)
        rc, output = run_checker(root)
        if rc == 0:
            print(f"PASS {name}")
        else:
            print(f"FAIL {name}")
            failures.append(f"{name}\n{output}")


def expect_rejected(name: str, check_name: str, mutate, failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_course(root)
        mutate(root)
        rc, output = run_checker(root)
        if rc != 0 and check_name in output:
            print(f"PASS {name}")
        else:
            print(f"FAIL {name}")
            failures.append(f"{name}\n{output}")


def main() -> int:
    failures: list[str] = []

    expect_pass("clean bilingual 15+15 fixture passes", failures)
    expect_rejected("missing PL Lesson 14 fails", "PL-inventory", lambda root: path_for(root, "PL", 14).unlink(), failures)
    expect_rejected("missing RU Lesson 14 fails", "RU-inventory", lambda root: path_for(root, "RU", 14).unlink(), failures)

    def duplicate(root: Path) -> None:
        shutil.copy2(path_for(root, "PL", 1), root / "PL" / "Lesson_1_Duplicate_Cartesian_School_PL.ipynb")

    expect_rejected("duplicate lesson number fails", "PL-legacy-notebooks", duplicate, failures)
    expect_rejected("malformed notebook JSON fails", "valid-json", lambda root: path_for(root, "PL", 3).write_text("{ nope", encoding="utf-8"), failures)

    def wrong_header(root: Path) -> None:
        nb = load_nb(root, "PL", 4)
        nb["cells"][0]["source"] = ["# Julia od zera -- Lesson 99\n"]
        nb["cells"][1]["source"] = ["## Informacje o lekcji\nwrong header fixture.\n"]
        save_nb(root, "PL", 4, nb)

    expect_rejected("filename/header Lesson mismatch fails", "lesson-header", wrong_header, failures)
    expect_rejected("PL/RU missing counterpart fails", "pl-ru-parity", lambda root: path_for(root, "RU", 2).unlink(), failures)

    def cell_count(root: Path) -> None:
        nb = load_nb(root, "RU", 5)
        nb["cells"].append(md("extra\n"))
        save_nb(root, "RU", 5, nb)

    expect_rejected("PL/RU cell-count mismatch fails", "pl-ru-parity", cell_count, failures)

    def cell_type(root: Path) -> None:
        nb = load_nb(root, "RU", 6)
        nb["cells"][1]["cell_type"] = "raw"
        save_nb(root, "RU", 6, nb)

    expect_rejected("PL/RU cell-type-sequence mismatch fails", "pl-ru-parity", cell_type, failures)

    def broken_link(root: Path) -> None:
        nb = load_nb(root, "PL", 7)
        nb["cells"][-1]["source"] = ["[Spis treści](../README.pl.md)\n[broken](missing.ipynb)\n"]
        save_nb(root, "PL", 7, nb)

    expect_rejected("broken local notebook navigation fails", "local-links", broken_link, failures)

    def token(root: Path) -> None:
        nb = load_nb(root, "PL", 8)
        nb["cells"][2]["source"] = ['token = "ghp_abcdefghijklmnopqrstuvwxyz0123456789"\n']
        save_nb(root, "PL", 8, nb)

    expect_rejected("embedded GitHub-like token fails", "repository-hygiene", token, failures)

    def local_path(root: Path) -> None:
        nb = load_nb(root, "RU", 9)
        nb["cells"][1]["source"] = ["## Информация об уроке\n/home/ssb/private/file.csv\n"]
        save_nb(root, "RU", 9, nb)

    expect_rejected("local /home or /media path fails", "repository-hygiene", local_path, failures)

    def polish_marker(root: Path) -> None:
        nb = load_nb(root, "RU", 10)
        nb["cells"][1]["source"] = ["## Cele lekcji\n"]
        save_nb(root, "RU", 10, nb)

    expect_rejected("obvious Polish marker in RU notebook fails", "language-contamination", polish_marker, failures)

    def russian_marker(root: Path) -> None:
        nb = load_nb(root, "PL", 11)
        nb["cells"][1]["source"] = ["## Цели урока\n"]
        save_nb(root, "PL", 11, nb)

    expect_rejected("obvious Russian marker in PL notebook fails", "language-contamination", russian_marker, failures)

    def stale_readme(root: Path) -> None:
        (root / "README.md").write_text("https://github.com/Cartesian-School/Introduction-to-Julia\n", encoding="utf-8")

    expect_rejected("stale Introduction-to-Julia repository link in README fails", "documentation", stale_readme, failures)

    print()
    total = 15
    print(f"{total - len(failures)}/{total} validation scenarios passed")
    if failures:
        print("\nFAILURES:")
        for failure in failures:
            print(failure.splitlines()[0])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
