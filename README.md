<div align="center">

<!-- Logo goes here: <img src="assets/images/logo.png" alt="Introduction to Julia" width="220"> -->

# Introduction to Julia

**Введение в Julia — a hands-on, 13-lesson course in scientific computing with Julia.**

[![CI](https://img.shields.io/badge/build-not%20yet%20configured-lightgrey.svg)](.github/workflows/ci.yaml)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-yellow.svg)](LICENSE)
[![Content License: CC BY-NC-SA 4.0](https://img.shields.io/badge/content%20license-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE-CC-BY-NC-SA.md)
[![Julia](https://img.shields.io/badge/julia-1.11.3-9558B2.svg)](https://julialang.org/downloads/)
[![Notebooks](https://img.shields.io/badge/lessons-13-blue.svg)](#course-contents)
[![Language](https://img.shields.io/badge/language-Русский-red.svg)](#a-note-on-language)

</div>

---

## About this course

Julia was built to end the "two-language problem" — the habit of prototyping in
a comfortable high-level language and then rewriting the hot paths in C for
speed. Julia gives you the readability of Python with performance in the same
class as C, from a single codebase.

This course teaches that from the ground up. It starts with variables and
strings and ends with matrix factorizations, working entirely inside Jupyter
notebooks so that every concept is something you *run*, not something you read
about. Each lesson mixes explanation, worked examples you execute cell by cell,
and numbered exercises with verification asserts.

The material is a Russian-language adaptation and extension of the JuliaAcademy
*Introduction to Julia* course, with four additional lessons on linear algebra
and factorizations that go well beyond the original.

### A note on language

**The lesson content is written in Russian.** File names and code are in
English. If you do not read Russian, the executable Julia code and the exercise
structure still stand on their own, but the explanatory prose will not be
usable to you.

---

## Learning objectives

By the end of the course you will be able to:

- **Write idiomatic Julia** — variables, string interpolation, control flow, and functions, including the terse one-line and anonymous forms Julia code relies on.
- **Choose the right data structure** — tuples, dictionaries, arrays, and named tuples, and explain the mutability and performance trade-offs between them.
- **Use multiple dispatch as a design tool** — Julia's central abstraction, and understand why it, rather than class-based OO, is how Julia code is organized.
- **Reason about Julia's performance model** — benchmark with `BenchmarkTools.jl`, read `@time` output, and understand why type stability and memory access order dominate runtime.
- **Manage packages and environments** — `Pkg`, `Project.toml`, and `Manifest.toml`, and produce a reproducible environment for your own work.
- **Visualize data** — build plots with `Plots.jl` and `PlotlyJS.jl`, switch backends, and animate results.
- **Apply linear algebra numerically** — matrix and vector operations, determinants, solving linear systems, and the LU / QR / eigen factorizations behind them.

---

## Target audience

This course is for someone who can already program and wants to add Julia.

### Prerequisites

| Requirement | Level |
|---|---|
| Prior programming experience | **Required.** Any language — Python, MATLAB, R, C. You should be comfortable with variables, loops, and functions as concepts. |
| Reading Russian | **Required.** All explanatory material is in Russian. See [A note on language](#a-note-on-language). |
| Jupyter notebooks | **Helpful.** Basic familiarity with running cells. Lesson 1 covers the essentials. |
| Linear algebra | **Helpful, lessons 11–13 only.** Lesson 11 reviews the theory from scratch, so the first ten lessons need none. |
| Prior Julia experience | **Not required.** The course starts at `println("Hello, World!")`. |

**Not a good fit if** you have never programmed before — the course moves
quickly and assumes you already know what a loop is.

---

## Course contents

The course runs in two tracks: language fundamentals (1–9) and numerical linear
algebra (10–13).

### Track 1 — Language fundamentals

| # | Lesson | Topics |
|---|---|---|
| 1 | [Getting started](01%20-%20Getting%20started.ipynb) | Running Julia, `println`, variables, comments, basic arithmetic |
| 2 | [Strings](02%20-%20Strings.ipynb) | String literals, interpolation with `$`, concatenation |
| 3 | [Data structures](03%20-%20Data%20structures.ipynb) | Tuples, named tuples, dictionaries, arrays, mutability |
| 4 | [Loops](04%20-%20Loops.ipynb) | `while` and `for`, iteration over ranges and collections |
| 5 | [Conditionals](05%20-%20Conditionals.ipynb) | `if`/`elseif`/`else`, ternary operator, short-circuit evaluation |
| 6 | [Functions](06%20-%20Functions.ipynb) | Declaration forms, anonymous functions, duck typing, mutating (`!`) conventions, broadcasting |
| 7 | [Packages](07%20-%20Packages.ipynb) | `Pkg`, adding and using packages, the package ecosystem |
| 8 | [Plotting](08%20-%20Plotting.ipynb) | `Plots.jl`, backends, layering plots, animation |
| 9 | [Multiple dispatch](09%20-%20Multiple%20dispatch.ipynb) | Methods, type annotations, dispatch as Julia's core abstraction |

### Track 2 — Performance and linear algebra

| # | Lesson | Topics |
|---|---|---|
| 10 | [Julia is fast](10%20-%20Julia%20is%20fast.ipynb) | Benchmarking with `BenchmarkTools.jl`, comparison against C and Python, why Julia is fast |
| 11 | [Linear algebra concepts](11%20-%20Linear%20algebra%20concepts.ipynb) | Vectors, matrices, matrix arithmetic, determinants — mathematical theory |
| 12 | [Linear algebra in Julia](12%20-%20Linear%20algebra%20in%20Julia.ipynb) | The same operations in code: array construction, `*`, `\`, transpose, `LinearAlgebra` |
| 13 | [Factorizations and other fun](13%20-%20Factorizations%20and%20other%20fun.ipynb) | LU, QR, eigendecompositions, special matrix types, generic linear algebra |

> Lessons 11 and 12 are a matched pair: 11 develops the mathematics, 12
> implements the same operations in Julia.

---

## Installation and setup

### 1. Install Julia

Download Julia **1.11.3** (the version every notebook in this course was
executed against) from the official site:

```bash
# Linux / macOS — via juliaup, the official version manager
curl -fsSL https://install.julialang.org | sh
juliaup add 1.11.3
juliaup default 1.11.3
```

On Windows, install [juliaup from the Microsoft Store](https://julialang.org/downloads/),
or download the installer directly. Verify:

```bash
julia --version
# julia version 1.11.3
```

### 2. Clone the repository

```bash
git clone https://github.com/Cartesian-School/Introduction-to-Julia.git
cd Introduction-to-Julia
```

### 3. Install the course dependencies

From the repository root, instantiate the project environment. This reads
`Project.toml` and installs `Plots`, `PlotlyJS`, `BenchmarkTools`, `Symbolics`,
and the rest:

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

> **First run takes a while.** `Plots.jl` and `Symbolics.jl` are large and
> precompile on first install — expect 5–15 minutes. This happens once.

### 4. Install the Jupyter kernel

```bash
julia --project=. -e 'using Pkg; Pkg.add("IJulia"); using IJulia'
```

`IJulia` will offer to install a private Miniconda with Jupyter if you do not
already have one. Accept it unless you want to use an existing Jupyter
installation.

### 5. Launch

```bash
julia --project=. -e 'using IJulia; notebook(dir=".")'
```

Or, if you already run Jupyter:

```bash
jupyter lab
```

---

## Usage

**Work through the lessons in the numbered order given in
[Course contents](#course-contents)** — each builds on the last.

Inside a notebook:

- Run a cell with **`Shift+Enter`**. Run every cell in order; several lessons depend on state set up in earlier cells.
- **Exercises** are marked `✅ Задание N.M` and are followed by an `@assert` cell that verifies your answer. A green (no output) result means you got it right; a red `AssertionError` means try again.
- **Some errors are intentional.** Lessons 2, 3, 6, and 9 deliberately trigger `MethodError` and `ParseError` to demonstrate Julia's type system. The surrounding text says so when this is the case.

To run the standalone example module used in lesson 7:

```bash
julia --project=. -e 'include("Example.jl"); println(hello("Julia"))'
# Hello, Julia
```

### Known issues

All 13 notebooks were last executed top-to-bottom under Julia 1.11.3, so the
saved outputs match what a clean **Restart & Run All** produces.

**Some errors in the output are intentional.** Lessons 1, 2, 3, 6, and 9
deliberately trigger `MethodError`, `ParseError`, and `KeyError` to demonstrate
the type system; the surrounding text says so each time. Those 13 cells are the
only error outputs in the course.

Two things to be aware of:

- **Exercises ship un-run.** The `@assert` verification cells below each
  `# Ваше решение` block have no saved output — that is expected. Run them after
  writing your solution: no output means it passed. Ten exercises in lessons 1,
  6, 12, and 13 do not yet include a worked solution cell
  (see [`TODO.md`](TODO.md)).
- **`PyCall` in lesson 10 may fail to build on Linux** with *"Couldn't find
  libpython"* if your system Python has no shared library. Fix it with:

  ```julia
  ENV["PYTHON"] = ""
  using Pkg; Pkg.build("PyCall")
  ```

If a saved output looks wrong, **restart the kernel and run all cells** — your
own run is the source of truth.

---

## Contributing

Issues and pull requests are welcome. Before opening one, please check
[`AUDIT_REPORT.md`](AUDIT_REPORT.md) — the known problems are already catalogued
there with severity and suggested fixes.

If you submit a notebook change, restart the kernel and run all cells before
committing, so that saved outputs match the code.

---

## Licence

This repository is **dual-licensed.**

> The source code contained in this repository is licensed under the MIT
> License. All course materials, including slides, text, diagrams, and
> educational resources, are licensed under the CC BY-NC-SA 4.0 License. You
> may use the code freely, but you may not use the course content for
> commercial purposes without explicit permission.

In practice:

| Material | Licence | Covers |
|---|---|---|
| **Source code** | [MIT](LICENSE) | Julia code cells in the notebooks, `Example.jl`, `.github/workflows/ci.yaml`, `Project.toml` / `Manifest.toml` |
| **Course materials** | [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA.md) | Lesson prose, explanations, diagrams, images, exercises, and this README |

Under **CC BY-NC-SA 4.0** you must give appropriate credit (**BY**), may not use
the material commercially (**NC**), and must distribute any derivative under the
same licence (**SA**). Commercial use — including paid training, corporate
workshops, or bundling into a paid product — requires explicit written
permission from the copyright holder.

### Copyright

- Copyright © 2018–2020 Julia Computing, Inc. — original JuliaAcademy *Introduction to Julia* material, used under the MIT License.
- Copyright © 2026 Siergej Sobolewski — Russian translation, adaptation, and lessons 10–13.

---

## Acknowledgments

- **[Julia Computing](https://juliacomputing.com/) and the JuliaAcademy team** — for the original *Introduction to Julia* course this adaptation is built on.
- **[Andreas Noack Jensen](https://x.com/anoackjensen)** (MIT & JuliaComputing) — author of the original linear algebra and factorization material behind lessons 12 and 13.
- **The Julia community** — for `Plots.jl`, `BenchmarkTools.jl`, `Symbolics.jl`, `IJulia.jl`, and the ecosystem this course depends on.

*Contributors to this edition will be listed here. If you have contributed and
are not credited, please open an issue.*
