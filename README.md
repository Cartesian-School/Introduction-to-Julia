<div align="center">

<!-- Logo goes here:
<img src="assets/images/logo.png" alt="Introduction to Julia" width="220">
-->

# Introduction to Julia

**A hands-on, 13-lesson course in Julia for scientific and numerical computing.**

[![Course CI](https://github.com/Cartesian-School/Introduction-to-Julia/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/Cartesian-School/Introduction-to-Julia/actions/workflows/ci.yaml)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-yellow.svg)](LICENSE)
[![Content License: CC BY-NC-SA 4.0](https://img.shields.io/badge/content%20license-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE-CC-BY-NC-SA.md)
[![Julia](https://img.shields.io/badge/julia-1.11.3-9558B2.svg)](https://julialang.org/downloads/)
[![Lessons](https://img.shields.io/badge/lessons-13-blue.svg)](#course-contents)
[![Language](https://img.shields.io/badge/course%20language-Russian-red.svg)](#course-language)

**English** · [Русский](README.ru.md) · [Polski](README.pl.md)

</div>

---

## Overview

**Introduction to Julia** is a practical course for programmers who want to learn Julia through executable examples rather than passive reading.

The course starts with the fundamentals of the language and progresses toward topics that make Julia particularly valuable in scientific, numerical, and performance-oriented computing:

- strings and Unicode;
- data structures and control flow;
- functions and broadcasting;
- package management and reproducible environments;
- plotting and visualization;
- multiple dispatch;
- benchmarking and performance engineering;
- numerical linear algebra;
- matrix factorizations.

All lessons are delivered as Jupyter notebooks. Each notebook combines explanation, runnable examples, exercises, worked solutions, and executable verification.

The material is based on the JuliaAcademy *Introduction to Julia* course and has been substantially adapted, extended, reviewed, and modernized for Julia **1.11.3**. The current edition also includes additional material on performance, numerical linear algebra, and matrix factorizations.

---

## Course language

The **lesson content is written in Russian**. File names, Julia code, API names, and most technical identifiers remain in English.

Repository documentation is available in:

- **English:** [README.md](README.md)
- **Russian:** [README.ru.md](README.ru.md)
- **Polish:** [README.pl.md](README.pl.md)

If you do not read Russian, you can still inspect and execute the Julia code, but the full explanatory layer of the course will not be available to you.

---

## Learning outcomes

By the end of the course, you should be able to:

- **Write idiomatic Julia** using variables, strings, control flow, functions, anonymous functions, broadcasting, and mutation conventions.
- **Work effectively with Julia data structures** including tuples, named tuples, dictionaries, vectors, matrices, and arrays.
- **Understand Unicode-aware string handling** and the difference between character iteration and UTF-8 string indexing.
- **Use multiple dispatch as a design technique**, not merely as syntax for method overloading.
- **Manage packages and reproducible environments** with `Pkg`, `Project.toml`, and `Manifest.toml`.
- **Create plots and visualizations** with `Plots.jl` and multiple plotting backends.
- **Benchmark Julia code correctly** using `BenchmarkTools.jl` and reason about compilation, allocations, type stability, and memory access patterns.
- **Apply numerical linear algebra** using vectors, matrices, norms, determinants, linear systems, and structured matrix types.
- **Use matrix factorizations appropriately**, including LU, QR, Cholesky, SVD, and eigenvalue decomposition.

---

## Target audience

This course is intended for people who already know how to program and want to add Julia to their technical toolkit.

### Prerequisites

| Requirement | Level |
|---|---|
| Prior programming experience | **Required.** Python, MATLAB, R, C, C++, Java, or another language is sufficient. |
| Russian reading ability | **Required for the lesson explanations.** |
| Jupyter familiarity | **Helpful.** Lesson 1 covers the essentials. |
| Linear algebra | **Helpful for lessons 11–13.** Lesson 11 introduces the required concepts. |
| Prior Julia experience | **Not required.** |

This course is **not designed as a first programming course**. It assumes that concepts such as variables, loops, conditions, and functions are already familiar.

---

## Course contents

The course is organized into two tracks:

1. **Julia language fundamentals** — lessons 1–9
2. **Performance and numerical linear algebra** — lessons 10–13

### Track 1 — Julia language fundamentals

| # | Lesson | Main topics |
|---|---|---|
| 1 | [Getting started](01%20-%20Getting%20started.ipynb) | Running Julia, variables, output, comments, arithmetic |
| 2 | [Strings](02%20-%20Strings.ipynb) | Strings, `Char`, interpolation, concatenation, UTF-8, Unicode-safe indexing |
| 3 | [Data structures](03%20-%20Data%20structures.ipynb) | Tuples, named tuples, dictionaries, vectors, matrices, arrays, mutability, element types |
| 4 | [Loops](04%20-%20Loops.ipynb) | `while`, `for`, ranges, collection iteration |
| 5 | [Conditionals](05%20-%20Conditionals.ipynb) | `if` / `elseif` / `else`, ternary expressions, short-circuit evaluation |
| 6 | [Functions](06%20-%20Functions.ipynb) | Function forms, anonymous functions, generic programming, mutating `!` convention, broadcasting |
| 7 | [Packages](07%20-%20Packages.ipynb) | `Pkg`, environments, package installation, reproducibility |
| 8 | [Plotting](08%20-%20Plotting.ipynb) | `Plots.jl`, `plot`, `plot!`, backends, labels, multiple series, animation |
| 9 | [Multiple dispatch](09%20-%20Multiple%20dispatch.ipynb) | Generic functions, methods, type hierarchy, specificity, true multiple dispatch |

### Track 2 — Performance and numerical linear algebra

| # | Lesson | Main topics |
|---|---|---|
| 10 | [Julia is fast](10%20-%20Julia%20is%20fast.ipynb) | Benchmarking, compilation, type stability, allocations, memory order, C/Python comparison |
| 11 | [Linear algebra concepts](11%20-%20Linear%20algebra%20concepts.ipynb) | Vectors, matrices, norms, rank, determinants, transpose vs adjoint, systems of equations |
| 12 | [Linear algebra in Julia](12%20-%20Linear%20algebra%20in%20Julia.ipynb) | `LinearAlgebra`, `dot`, `cross`, `norm`, `det`, `rank`, `\`, structured matrices, BLAS concepts |
| 13 | [Factorizations and other fun](13%20-%20Factorizations%20and%20other%20fun.ipynb) | LU, QR, Cholesky, SVD, eigenvalue decomposition, factorization reuse |

> Lessons 11 and 12 are designed as a pair: lesson 11 develops the mathematical concepts, while lesson 12 applies them directly in Julia.

---

## Installation

### 1. Install Julia

The notebooks are validated against **Julia 1.11.3**.

Using `juliaup` on Linux or macOS:

```bash
curl -fsSL https://install.julialang.org | sh
juliaup add 1.11.3
juliaup default 1.11.3
```

Verify the installation:

```bash
julia --version
```

Expected output:

```text
julia version 1.11.3
```

On Windows, install Julia using `juliaup` from the Microsoft Store or use the official installer available from the [Julia downloads page](https://julialang.org/downloads/).

---

### 2. Clone the repository

```bash
git clone https://github.com/Cartesian-School/Introduction-to-Julia.git
cd Introduction-to-Julia
```

---

### 3. Instantiate the course environment

From the repository root:

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

This restores the dependency set described by `Project.toml` and `Manifest.toml`.

> The first installation may take several minutes because some packages require precompilation.

---

### 4. Install the Jupyter kernel

```bash
julia --project=. -e 'using Pkg; Pkg.add("IJulia"); using IJulia'
```

If Jupyter is not installed, `IJulia` can offer to install a private Miniconda environment.

---

### 5. Launch the notebooks

Using IJulia:

```bash
julia --project=. -e 'using IJulia; notebook(dir=".")'
```

Or, if Jupyter is already installed:

```bash
jupyter lab
```

---

## How to use the course

Work through the notebooks in numerical order.

Inside each notebook:

- Run cells with **`Shift+Enter`**.
- Execute cells from top to bottom.
- Exercises are marked with `✅ Задание N.M`.
- Student work areas are marked with `# Ваше решение`.
- Worked solutions are marked with `# Правильное решение`.
- Verification is usually performed with `@assert` or another executable check.

A successful `@assert` normally produces no output.

Some exceptions are **intentional teaching examples**. The surrounding explanation identifies those cases explicitly.

---

## Reproducibility

The course is designed so that running the notebooks does not silently rewrite the repository environment.

Package-management demonstrations use isolated or temporary environments where required, and the course validator checks repository-level invariants.

The canonical environment is defined by:

- [`Project.toml`](Project.toml)
- [`Manifest.toml`](Manifest.toml)

All 13 notebooks have been executed top-to-bottom under Julia 1.11.3.

---

## Validation

The repository includes a course-level validation harness:

```bash
python3 tools/check_course.py
```

It checks, among other things:

- notebook JSON validity;
- Julia kernel consistency;
- execution-order consistency;
- unexpected error outputs;
- lesson objectives and navigation;
- exercise / worked-solution structure;
- notebook numbering;
- broken internal links;
- leaked absolute paths;
- accidental credential-like content.

The validator itself is tested against intentionally corrupted fixtures:

```bash
python3 tools/test_check_course.py
```

These checks are also integrated into CI.

---

## Known execution notes

### Intentional exceptions

Some notebooks deliberately produce exceptions as part of the teaching material, including examples of:

- `MethodError`
- `ParseError`
- `StringIndexError`
- `KeyError`
- `DimensionMismatch`
- `PosDefException`

These are intentional only where the adjacent lesson text explains them.

### `PyCall` in Lesson 10

On some Linux systems, `PyCall` may fail to build if the selected Python installation does not expose a compatible shared `libpython`.

If that happens, rebuild `PyCall` using its managed Python environment:

```julia
ENV["PYTHON"] = ""
using Pkg
Pkg.build("PyCall")
```

Then restart the Julia kernel.

Only apply this workaround if you encounter the corresponding build error.

---

## Repository quality

The current edition has been reviewed for:

- Julia 1.11.3 compatibility;
- mathematical correctness;
- numerical linear algebra accuracy;
- multiple-dispatch semantics;
- UTF-8 string indexing;
- package-environment reproducibility;
- notebook execution order;
- exercise completeness;
- intentional vs accidental error outputs;
- local-path and credential leakage;
- pedagogical consistency across all 13 lessons.

For the detailed review history, see:


---

## Contributing

Issues and pull requests are welcome.

Before contributing:

2. restart the modified notebook kernel;
3. run the notebook from top to bottom;
4. make sure saved outputs match the current code;
5. run:

```bash
python3 tools/check_course.py
python3 tools/test_check_course.py
```

Please avoid unrelated formatting changes in notebook JSON because they make review significantly harder.

---

## Licensing

This repository uses a dual-license model.

| Material | License | Scope |
|---|---|---|
| Source code | [MIT License](LICENSE) | Julia code cells, helper scripts, CI configuration, environment files |
| Course materials | [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA.md) | Lesson text, educational explanations, exercises, diagrams, images, README content |

Under **CC BY-NC-SA 4.0**, attribution is required, commercial use is not permitted without authorization, and derivative educational material must be distributed under the same license.

Commercial use of the course material — including paid training, corporate workshops, or inclusion in a paid educational product — requires explicit written permission from the copyright holder.

### Copyright

- Copyright © 2018–2020 Julia Computing, Inc. — original JuliaAcademy *Introduction to Julia* material.
- Copyright © 2026 Siergej Sobolewski — Russian translation, adaptation, modernization, and additional course material.

---

## Acknowledgments

This course builds on work by the Julia community and the original JuliaAcademy team.

Special thanks to:

- **[Julia Computing](https://juliacomputing.com/)** and the JuliaAcademy team for the original *Introduction to Julia* course.
- **[Andreas Noack Jensen](https://x.com/anoackjensen)** for original linear-algebra and factorization material that informed later lessons.
- **The Julia community** for the language, documentation, packages, and ecosystem used throughout the course.

---

## Maintainer

Cartesian School

Repository: [github.com/Cartesian-School/Introduction-to-Julia](https://github.com/Cartesian-School/Introduction-to-Julia)

For defects, corrections, or course-improvement proposals, please open a GitHub issue or pull request.

---

<div align="center">

**English** · [Русский](README.ru.md) · [Polski](README.pl.md)

</div>
