<div align="center">

<img src="https://github.com/Cartesian-School/Julia-from-zero/blob/main/assets/images/kurs_logo.png" alt="Julia language logo" width="220" />

# Julia from Zero

### Programming, Scientific Computing, and Numerical Methods in Julia

**A practical course for programmers — from the first notebook to a complete capstone project.**

[![Course CI](https://github.com/Cartesian-School/Julia-from-zero/actions/workflows/ci.yaml/badge.svg?branch=main&event=push)](https://github.com/Cartesian-School/Julia-from-zero/actions/workflows/ci.yaml)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-yellow.svg)](LICENSE)
[![Course Content: CC BY-NC-SA 4.0](https://img.shields.io/badge/course%20content-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE-CC-BY-NC-SA.md)
[![Julia](https://img.shields.io/badge/Julia-1.11.x-9558B2.svg)](https://julialang.org/)
![Lessons](https://img.shields.io/badge/lessons-15-blue.svg)
![Primary content language](https://img.shields.io/badge/primary%20content%20language-Polish-red.svg)

**English** · [Polski](README.pl.md) · [Русский](README.ru.md)

</div>

---

## About the course

**Julia from Zero** is a practical Julia course created by **Cartesian School** for learners who already understand core programming concepts and want to learn Julia from the ground up — from syntax and data structures to performance-oriented programming, linear algebra, numerical methods, and a complete capstone project.

“From Zero” means **from zero in Julia**, not from zero in programming. The course does not require prior Julia experience, but it does assume familiarity with concepts such as variables, functions, loops, conditionals, and basic data types.

The course contains **15 lessons, numbered from Lesson 0 to Lesson 14**. The material progresses from the first notebook to the capstone project **ThermalLab**, which combines modeling, multiple dispatch, visualization, performance analysis, linear algebra, and numerical computing.

The Polish lesson notebooks are stored in the [`PL/`](PL/) directory.

---

## Public repository and project mission

This repository is public in order to make Julia easier to learn and to contribute to the popularization of the Julia language and its ecosystem — especially among Polish-speaking programmers, students, and engineers.

The author’s goal is to support the Julia community by:

- creating accessible learning materials in Polish;
- showing practical Julia use cases in programming, scientific computing, and numerical methods;
- publishing executable examples, exercises, and projects that can be studied and extended;
- encouraging learners to continue with the official Julia documentation and the broader package ecosystem.

### Important licensing distinction

Code authored by Cartesian School is released as **open-source software under the MIT License**.

Original educational content authored by Cartesian School is distributed under **CC BY-NC-SA 4.0**. That means it can be shared and adapted under the terms of that license, including attribution and non-commercial restrictions.

Third-party materials remain under their own original licenses and attribution requirements.

---

## What you will learn

By the end of the course, you will be able to:

- write clear and idiomatic Julia code;
- work with Unicode strings, tuples, dictionaries, sets, vectors, and matrices;
- use loops, conditionals, comprehensions, broadcasting, and iterators;
- design functions with positional, keyword, default, and varargs parameters;
- understand the difference between a function and a method;
- use **multiple dispatch** as a foundation for extensible API design;
- manage packages and environments through `Pkg`, `Project.toml`, and `Manifest.toml`;
- create plots and analyze data with `Plots.jl`;
- measure performance correctly and interpret benchmarks responsibly;
- understand the impact of JIT compilation, allocations, type stability, and memory locality;
- perform practical linear algebra in Julia;
- solve linear systems with the `\` operator;
- use LU, QR, Cholesky, SVD, EVD, and Schur factorizations;
- understand special matrix structures and why they matter;
- analyze numerical error, conditioning, and stability;
- implement basic root-finding, differentiation, and integration methods;
- solve simple ODEs with Euler and RK4 methods;
- build a complete project that combines data modeling, algorithms, tests, performance analysis, visualization, and reporting.

---

## Who this course is for

This course is especially suitable for:

- programmers coming from Python, C, C++, Rust, Java, MATLAB, R, or similar languages;
- students and graduates of technical disciplines;
- engineers working with modeling and computation;
- learners interested in scientific computing, data analysis, and numerical methods;
- developers who want to understand Julia’s distinctive programming model built around multiple dispatch.

### Prerequisites

| Requirement | Level |
|---|---|
| Basic programming knowledge | **Required** |
| Prior Julia knowledge | **Not required** |
| Jupyter Notebook / JupyterLab | Helpful, but not required |
| Linear algebra | Helpful from Lesson 10 onward; core ideas are explained in the course |
| Numerical methods | Not required; introduced in Lesson 13 |

---

## Course structure

### Block I — Julia language foundations

| Lesson | Topic | Notebook |
|---:|---|---|
| 0 | **Getting Started** | [Open Lesson 0](PL/Lesson_0_Julia_Cartesian_School_PL.ipynb) |
| 1 | **Strings** | [Open Lesson 1](PL/Lesson_1_Strings_Julia_Cartesian_School_PL.ipynb) |
| 2 | **Data Structures** | [Open Lesson 2](PL/Lesson_2_Data_Structures_Julia_Cartesian_School_PL.ipynb) |
| 3 | **Loops** | [Open Lesson 3](PL/Lesson_3_Loops_Julia_Cartesian_School_PL.ipynb) |
| 4 | **Conditionals** | [Open Lesson 4](PL/Lesson_4_Conditionals_Julia_Cartesian_School_PL.ipynb) |
| 5 | **Functions** | [Open Lesson 5](PL/Lesson_5_Functions_Julia_Cartesian_School_PL.ipynb) |

### Block II — Ecosystem, plotting, and Julia’s programming model

| Lesson | Topic | Notebook |
|---:|---|---|
| 6 | **Packages** | [Open Lesson 6](PL/Lesson_6_Packages_Julia_Cartesian_School_PL.ipynb) |
| 7 | **Plotting** | [Open Lesson 7](PL/Lesson_7_Plotting_Julia_Cartesian_School_PL.ipynb) |
| 8 | **Multiple Dispatch** | [Open Lesson 8](PL/Lesson_8_Multiple_Dispatch_Julia_Cartesian_School_PL.ipynb) |

### Block III — Performance and linear algebra

| Lesson | Topic | Notebook |
|---:|---|---|
| 9 | **Julia is Fast** | [Open Lesson 9](PL/Lesson_9_Julia_is_Fast_Cartesian_School_PL.ipynb) |
| 10 | **Linear Algebra Concepts** | [Open Lesson 10](PL/Lesson_10_Linear_Algebra_Concepts_Julia_Cartesian_School_PL.ipynb) |
| 11 | **Linear Algebra in Julia** | [Open Lesson 11](PL/Lesson_11_Linear_Algebra_in_Julia_Cartesian_School_PL.ipynb) |
| 12 | **Factorizations and Other Fun** | [Open Lesson 12](PL/Lesson_12_Factorizations_and_Other_Fun_Julia_Cartesian_School_PL.ipynb) |

### Block IV — Numerical methods and capstone

| Lesson | Topic | Notebook |
|---:|---|---|
| 13 | **Numerical Computing** | [Open Lesson 13](PL/Lesson_13_Numerical_Computing_Julia_Cartesian_School_PL.ipynb) |
| 14 | **Final Project / Capstone — ThermalLab** | [Open Lesson 14](PL/Lesson_14_Final_Project_Capstone_Julia_Cartesian_PL.ipynb) |

> The `PL/` directory also contains an earlier Lesson 0 variant: `Lesson_0_Julia_Cartesian_School_Professional.ipynb`. The table above points to the canonical Polish Lesson 0 file.

---

## Capstone project — ThermalLab

Lesson 14 is not just another isolated notebook. It is the course capstone project that integrates the material from the entire program.

**ThermalLab** models a cooling process according to Newton’s law of cooling and includes:

- custom types `ThermalModel`, `MeasurementSet`, and `SimulationResult`;
- an abstract integrator interface;
- Euler and RK4 implementations through multiple dispatch;
- synthetic measurement generation;
- parameter estimation using least squares;
- residuals, MAE, RMSE, and `R²`;
- accuracy-versus-cost comparison;
- optional visualization with `Plots.jl`;
- CSV export;
- validation and contract-style tests.

The project demonstrates the full workflow:

> **problem → model → code → computation → validation → result**

---

## Repository languages

The canonical lesson content of this edition is currently developed **in Polish** and stored in [`PL/`](PL/).

The repository documentation is maintained in three languages:

- **English:** [README.md](README.md)
- **Polski:** [README.pl.md](README.pl.md)
- **Русский:** [README.ru.md](README.ru.md)

Julia code, function names, APIs, identifiers, and terminology that must remain aligned with technical documentation are kept in English.

---

## Installation

### 1. Install Julia

The course is developed for the **Julia 1.11.x** series.

Official installation instructions:

<https://julialang.org/downloads/>

Check your installation:

```bash
julia --version
```

### 2. Clone the repository

```bash
git clone https://github.com/Cartesian-School/Julia-from-zero.git
cd Julia-from-zero
```

### 3. Recreate the project environment

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

The repository uses:

- `Project.toml` — declared project dependencies;
- `Manifest.toml` — resolved dependency versions.

### 4. Run Jupyter

If you use IJulia:

```bash
julia --project=. -e 'using IJulia; notebook(dir=".")'
```

or simply:

```bash
jupyter lab
```

Then go to the `PL/` directory and start with:

[`PL/Lesson_0_Julia_Cartesian_School_PL.ipynb`](PL/Lesson_0_Julia_Cartesian_School_PL.ipynb)

---

## How to work through the course

Go through the notebooks in order, from **Lesson 0** to **Lesson 14**.

Recommended workflow:

1. read the goal of the section;
2. run the example;
3. study the output;
4. solve the exercise on your own;
5. only then compare your work with the sample solution;
6. check the `@assert` statements and the checkpoint;
7. before moving on, make sure you understand not only the syntax, but also *why* the code works.

The notebooks follow a shared teaching pattern:

| Element | Meaning |
|---|---|
| **Goal** | what you should learn in the section |
| **Theory** | a definition or rule |
| **Example** | executable code |
| **Analysis** | interpretation of what happens |
| **Important** | a key rule to remember |
| **Typical mistake** | a common problem |
| **Try it yourself** | a small experiment |
| **Practice** | an exercise |
| **Summary** | the main takeaways |

---

## Reproducibility and environment safety

The course is designed so that package-related examples do not silently and unexpectedly modify the project environment.

In particular:

- notebooks should not automatically execute `Pkg.add(...)` unless explicitly necessary;
- package experiments may use temporary environments;
- dependencies should be restored through `Pkg.instantiate()`;
- code that depends on optional packages should behave predictably even if the package is not installed.

---

## Repository validation

The repository contains a CI workflow in `.github/workflows/ci.yaml`.

If the repository provides tools such as:

```bash
python3 tools/check_course.py
python3 tools/test_check_course.py
```

they should be run before merging changes into `main`.

After modifying notebooks, you should also:

1. run the notebook from start to finish;
2. verify that there are no unexpected exceptions;
3. check navigation and Markdown links;
4. verify environment consistency;
5. confirm that CI covers the current set of Polish notebooks.

**The README should not claim that all 15 lessons have passed end-to-end execution unless the current repository revision has actually been validated that way.**

---

## Technical quality standards

While developing the course, special attention is paid to:

- semantic correctness of Julia code;
- correctness of API examples;
- proper use of Unicode;
- clear distinction between broadcasting and linear algebra;
- correct use of multiple dispatch;
- responsible benchmarking methodology;
- distinction between algorithmic stability and problem conditioning;
- numerical correctness;
- non-misleading performance comparisons;
- reproducible environments;
- consistent didactic structure across Lessons 0–14.

---

## Origins, attribution, and third-party material

Part of the historical basis of this repository traces back to educational material from JuliaAcademy / JuliaTutorials.

The current **Julia from Zero** edition has been substantially redesigned and extended by Cartesian School: the course structure, teaching layer, language, exercises, topical scope, and organization have been changed, and new material has been added on performance, linear algebra, factorizations, numerical methods, and the capstone project.

Third-party material remains subject to its original copyright, license terms, and attribution requirements.

This Cartesian School repository is **not** an official Julia language course and is **not** an official JuliaHub product.

---

## Licensing

| Material | License |
|---|---|
| Code authored by Cartesian School | [MIT License](LICENSE) |
| Original educational content authored by Cartesian School | [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA.md) |
| Third-party materials | according to their original licenses and attribution requirements |

The Cartesian School licenses do not replace or override the licenses of third-party materials.

---

## Contributing

Issues and pull requests are welcome.

Before submitting changes:

1. run the modified notebook from start to finish;
2. verify that stored outputs are current;
3. run repository validators;
4. check Markdown links;
5. avoid accidental notebook JSON formatting noise;
6. do not commit local paths, secrets, tokens, or credentials.

---

## Contact

**Author:** Siergej Sobolewski  
**Project:** Cartesian School  
**Email:** [s.sobolewski@hotmail.com](mailto:s.sobolewski@hotmail.com)

Repository:

<https://github.com/Cartesian-School/Julia-from-zero>

If you find a conceptual, technical, language, or numerical issue, you can:

- open a GitHub Issue;
- submit a Pull Request;
- contact the author by email.

---

## Acknowledgements

Thanks to:

- the creators of the Julia language;
- the Julia community;
- the authors of the official documentation and packages used in the course;
- the authors of JuliaAcademy / JuliaTutorials materials, which historically formed part of the starting point for this repository.

---

<div align="center">

### Cartesian School

**Learn Programming. Build Real Software. Master AI.**

**English** · [Русский](README.ru.md) · [Polski](README.pl.md)

</div>
