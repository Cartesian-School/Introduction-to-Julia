# Course Repository Audit Report

**Repository:** Introduction-to-Julia (Russian-language edition)
**Audit date:** 2026-09-06
**Commit audited:** `d9d1699`
**Scope:** 13 Jupyter notebooks (`.ipynb`), 1 Julia source file (`.jl`), 2 TOML
configuration files, 3 Markdown files, 1 binary asset.

---

## Remediation status (updated 2026-09-06)

A remediation pass has since been applied on branch `fix/audit-remediation`.
**Sections 1–3 below are preserved as the historical record of commit
`d9d1699`** and still use the pre-rename filenames (`010`–`013`); this section
records what changed. Open items are tracked in [`TODO.md`](TODO.md).

| Finding | Status |
|---|---|
| CRIT-1 exercise asserts | ✅ Fixed — see note below |
| CRIT-2 README stub | ✅ Fixed |
| CRIT-3 licensing undeclared | ✅ Fixed |
| MAJ-1 `Manifest.toml` untracked | ✅ Fixed — now tracked |
| MAJ-2 no version bounds | ✅ Fixed — `[compat]` added |
| MAJ-3 lesson numbering | ✅ Fixed — `010`–`013` → `10`–`13` |
| MAJ-4 broken install cell | ⚠️ Partial — outputs cleared, not re-run |
| MAJ-5 kernel 1.6.0 | ⛔ Blocked — needs Julia |
| MAJ-6 duplicate titles | ✅ Fixed — renamed to `11 - Linear algebra concepts` / `12 - Linear algebra in Julia` |
| MAJ-7 execution order | ⛔ Blocked — needs Julia |
| MAJ-8 directory layout | ⏸️ Deferred by decision |
| MIN-1 stale anchor, MIN-2 twitter→x | ✅ Fixed — MIN-1 target corrected, see below |
| MIN-6 stray heading | ✅ Fixed |
| MIN-13 "Одинадцатый", MIN-15 "обьявите" | ✅ Fixed |
| MIN-14 "так же" | ❌ **Withdrawn — false positive** |
| MIN-3/4, MIN-8/9/10/11/12, MIN-16/17 | ⏸️ Deferred to `TODO.md` |

### Correction to MIN-1

The original finding correctly identified the anchor as stale but proposed the
wrong replacement. Fetching the live page shows the current Documenter anchor is
neither the old `#Access-arrays-in-memory-order,-along-columns-1` nor the
de-suffixed form the audit suggested, but a named anchor:

```text
https://docs.julialang.org/en/v1/manual/performance-tips/#man-performance-column-major
```

`04 - Loops.ipynb` now uses that verified target.

### Correction to MIN-14

**MIN-14 is withdrawn.** All six occurrences are the comparative construction
"так же, как" ("just as … as"), which is correct Russian — not the conjunction
"также". The original finding came from a grep that did not check for the
following "как". No text was changed.

### Amendment to CRIT-1

The defect was larger than first reported. Cell 117 was not merely blank: its
source was the incomplete assignment `my_phonebook =` with an empty right-hand side (a `ParseError` if run),
and it carried a **stale output from an earlier version of the exercise**
showing `Dict{String, String}` with different names (Света/Гена) — directly
contradicting the asserts below it, which require Евгений/Константин in a
`Dict{String, Any}`. Exercise 3.2 was also the only exercise in the lesson with
no "Правильное решение" cell. Fixed by repairing the template, clearing the
stale output, adding the missing solution cell, and clearing the two failed
asserts.

### New findings raised during remediation

#### NEW-1 (Critical, resolved) — Author's local filesystem paths leaked throughout saved outputs

**164 occurrences across 9 notebooks** embedded the author's absolute Windows
home directory in saved cell outputs — inside `MethodError` messages,
`ParseError` locations, `Pkg` status lines, and clickable `file://` method
links:

```text
c:\Users\Siergej Sobolewski\Kursy Cartesian School\Julia\Introduction-to-Julia-main\...
C:\Users\Siergej Sobolewski\.julia\packages\PyCall\1gn3u\src\...
C:\Users\Siergej Sobolewski\.vscode\extensions\julialang.language-julia-1.127.2\...
```

This exposes the author's OS account name and directory structure in a
repository configured to push to a public remote.

**Status:** ✅ **Resolved.** All 164 occurrences were rewritten to `~` /
`~\Introduction-to-Julia`, in two passes (a second pass was needed for
double-escaped paths nested inside JSON string outputs). The surrounding
path structure was preserved, since `.julia/packages/…` is pedagogically
meaningful, and no output was deleted — the error demonstrations still teach
what they were written to teach.

#### NEW-2 (Critical, open) — Lesson 10's Python comparison does not run

`10 - Julia is fast.ipynb` fails in a **10-cell cascade**. `PyCall` fails to
precompile at cell 75, and every dependent cell then raises `UndefVarError`:

| Cell | Failure |
|---|---|
| 73 | `PkgError` — `Conda` not in project or manifest |
| 75 | `ErrorException` — failed to precompile `PyCall` |
| 78, 81 | `pybuiltin`, `pysum` not defined |
| 86, 89 | `@benchmark`, `py_list_bench` not defined |
| 92 | `d` not defined — **the benchmark results dictionary** |
| 99 | `Conda.jl` cannot install to its default location |
| 101, 114 | `pyimport`, `@py_str` not defined |

The lesson's conclusion cells (166–167) quote specific timings —
`numpy.sum(a)` at 1.9 ms, pure Python at 875–1011 ms — that **the notebook's own
execution never produced**. The prose asserts results the code did not generate.
The Julia-versus-C benchmarks in the same lesson are unaffected and do run.

These outputs were deliberately **left in place**: clearing them would make a
non-functional section of the flagship "Julia is fast" lesson look healthy
without repairing it. Requires Julia to fix — tracked in `TODO.md`.

---

## 0. Method and coverage

| Check | How it was performed | Coverage |
|---|---|---|
| Broken links | Regex extraction of all `http(s)://` targets and Markdown `[](…)` pairs from every notebook cell source, followed by a heuristic (non-network) review. | 8 authored link targets |
| Internal references | Search for relative Markdown links, `<img src=…>` tags, `include("…")` calls, and file-name literals. | All 13 notebooks |
| Incomplete sections | `TODO` / `FIXME` / `TBD` / `XXX` / `HACK` scan across cell **source** (base64 output blobs excluded). | All 13 notebooks + `.jl` + `.toml` |
| Dependency validation | `Project.toml` / `Manifest.toml` inspection; cross-check against `git ls-files`. | Full |
| Structural consistency | File naming, lexicographic ordering, kernel metadata, execution-count monotonicity, exercise coverage. | Full |
| Style & grammar | Paragraph-length distribution, repeated-sentence frequency, targeted Russian orthography checks. | All Markdown cells |

> **Note on link verification.** Live HTTP verification was not run — the
> network request was declined in this environment, and the task specifies a
> "dry-run regex + heuristic check". Every finding in §1.1 is therefore a
> *structural* or *staleness* judgement about the URL, not a confirmed HTTP
> failure. Findings marked **[unverified]** need one CI run of the
> `link-check` job in `.github/workflows/ci.yaml` to confirm or clear.

**Language note.** The repository is an English-titled fork whose *content* is
entirely in Russian. Several findings below concern the mismatch between the
two.

---

## 1. CRITICAL

Issues that mislead or block a student on first contact.

### CRIT-1 — Exercise verification cells ship in a failed state

**File:** `03 - Data structures.ipynb`, cells 118 and 119

Both saved cells contain a stored `AssertionError` output:

```julia
@assert my_phonebook == Dict("Евгений" => 8675309, "Константин" => "555-2368")
@assert typeof(my_phonebook) == Dict{String, Any}
```

A student opening the notebook sees two red failures before running anything,
and cannot tell whether the exercise is broken or their own work is. These are
*verification* asserts for the phonebook exercise, not the intentional
error-demonstration cells found elsewhere in the course.

**Remediation:** Complete the exercise in a scratch copy so the asserts pass,
re-run, and commit the passing outputs — or clear the outputs of these two
cells so no stale failure is displayed.

### CRIT-2 — `README.md` was a non-functional stub

**File:** `README.md` (as of `d9d1699`)

The entire file was four lines, with the `# Introduction-to-Julia` heading
duplicated and no description, prerequisites, installation instructions, usage
guidance, or licence statement. For a public course repository the README *is*
the landing page.

**Status:** ✅ **Resolved** by Task 2 of this initialization pass.

### CRIT-3 — Dual-licence model was undeclared

**Files:** `LICENSE.md` (removed), `LICENSE-CC-BY-NC-SA.md`

`LICENSE-CC-BY-NC-SA.md` was present and complete (438 lines, Sections 1–8 of
the CC BY-NC-SA 4.0 legal code), but **nothing in the repository stated which
licence governed which material.** A reader saw an MIT file and a CC file side
by side with no scoping rule, and `LICENSE.md` carried only the upstream
`Copyright (c) 2018-2020: Julia Computing, Inc.` notice with no notice for the
present author.

**Status:** ✅ **Resolved.** `LICENSE` now carries both the upstream Julia
Computing notice (retention is required by the MIT terms for this derivative
work) and the 2026 Siergej Sobolewski notice, plus an explicit scope clause.
The split is restated in `README.md` § Licence. `LICENSE.md` was removed as
superseded.

---

## 2. MAJOR

Issues that break reproducibility, ordering, or trust in the material.

### MAJ-1 — `Manifest.toml` is git-ignored, so the environment is not reproducible

`Manifest.toml` exists on disk (68 KB, `julia_version = "1.11.3"`) but is
**untracked**, because the old `.gitignore` ignored it at line 24:

```text
.gitignore:24:Manifest.toml    Manifest.toml
```

That rule is correct for a *library* and wrong for an *application*. This
repository is a pinned teaching environment: without the manifest, every
student resolves a different dependency set, and the benchmark timings in
`010 - Julia is fast.ipynb` are not comparable to the ones baked into the
notebook.

**Status:** ⚠️ **Partially resolved.** The rewritten `.gitignore` no longer
ignores `Manifest.toml` and documents why. **Action still required:** run
`git add Manifest.toml` to actually commit it.

### MAJ-2 — `Project.toml` has no version bounds and no identity

```toml
[deps]
BenchmarkTools = "6e4b80f9-…"
GR = "28b8d3ca-…"
…
```

Missing entirely: a `[compat]` section, a `julia = "1.11"` bound, and
`name`/`uuid`/`version` keys. Eight direct dependencies are declared with **no
version pin on any of them**. `Symbolics`, `SymbolicUtils`, and `Plots` all
make breaking changes across minor releases, so a fresh `Pkg.instantiate()` on
a future date can resolve a set the notebooks were never tested against.

**Remediation:**

```toml
[compat]
BenchmarkTools = "1"
GR = "0.73"
JordanForm = "0.1"
LinearAlgebraX = "0.2"
PlotlyJS = "0.18"
Plots = "1"
SymbolicUtils = "3"
Symbolics = "6"
julia = "1.11"
```

Verify each bound against the resolved versions in `Manifest.toml` before
committing.

### MAJ-3 — Lesson numbering breaks lexicographic ordering

Lessons 10–13 are named `010`, `011`, `012`, `013` while lessons 1–9 use two
digits (`01`…`09`). Under byte-order sorting — which is what GitHub's file
listing, `ls`, and most file managers use — this yields:

```text
01 - Getting started        ← lesson 1
010 - Julia is fast         ← lesson 10  ✗ sorts second
011 - Basic linear algebra  ← lesson 11  ✗
012 - Basic linear algebra  ← lesson 12  ✗
013 - Factorizations…       ← lesson 13  ✗
02 - Strings                ← lesson 2
```

Lessons 10–13 appear immediately after lesson 1, so the course reads in the
wrong order in the very listing a student browses first.

**Remediation:** Rename `010…013` to `10…13` (`git mv "010 - Julia is fast.ipynb" "10 - Julia is fast.ipynb"`, etc.).

### MAJ-4 — The canonical install step in the Packages lesson ships broken

**File:** `07 - Packages.ipynb`, cell 17

```julia
using Pkg
Pkg.add("Plots")
```

Saved output is a `Pkg.Types.PkgError`: `Error building 'PyCall'` during
`Conda` precompilation. This is *the* install cell of the lesson whose subject
is package management. A student reads the lesson on how to add packages and
sees the demonstration fail. Related noise: cells 30 and 43 carry `stderr`
output, and `010 - Julia is fast.ipynb` cell 73 stores
`PkgError: … * Conda (not found in project or manifest)`.

**Remediation:** Re-run lesson 07 in a clean depot where the `PyCall`/`Conda`
build succeeds (or drop the `PyCall` dependency path entirely, since no lesson
requires Python interop) and commit clean outputs.

### MAJ-5 — Kernel version inconsistency

| Notebook | Kernel |
|---|---|
| `05 - Conditionals.ipynb` | **Julia 1.6.0** |
| all 12 others | Julia 1.11.3 |

Lesson 5 was last executed on a five-year-old LTS kernel. Its outputs were
produced by a different compiler than the rest of the course and may not match
what a student on 1.11.3 sees.

**Remediation:** Re-execute lesson 5 under 1.11.3 and commit.

### MAJ-6 — Two notebooks share the title "Basic linear algebra"

`011 - Basic linear algebra.ipynb` and `012 - Basic linear algebra.ipynb` are
**not** duplicates — 011 is mathematical theory
("Основные понятия линейной алгебры") and 012 is the Julia implementation
("Базовая линейная алгебра в Julia") — but the filenames are indistinguishable
without opening them.

**Remediation:** Rename to reflect the actual split, e.g.
`11 - Linear algebra concepts.ipynb` and
`12 - Linear algebra in Julia.ipynb`.

### MAJ-7 — Ten of thirteen notebooks are not runnable top-to-bottom as saved

Execution counts are non-monotonic in `01`, `02`, `03`, `04`, `06`, `08`, `09`,
`010`, `012`, `013` — cells were run out of order and saved that way. Only
`05`, `07`, and `011` are clean (and `011` only because it contains no code at
all). Combined with MAJ-1, a student who runs "Restart & Run All" is not
guaranteed to reproduce the committed outputs.

**Remediation:** Restart-and-run-all each notebook, then commit. Enforce it
afterwards by adding an `nbconvert --execute` job to `.github/workflows/ci.yaml`.

### MAJ-8 — Flat root directory with no course progression structure

All 13 notebooks, the `animation.gif` asset, `Example.jl`, both TOML files, and
all Markdown files sit in the repository root. There is no `Chapter_01/` (or
`lessons/`, `notebooks/`) grouping, and no module boundaries between the
beginner track (01–09) and the linear-algebra track (10–13).

Files that should move out of the root:

| File | Suggested location | Reason |
|---|---|---|
| `animation.gif` | `assets/images/` | Binary asset; only referenced by `08 - Plotting.ipynb`. |
| `Example.jl` | `src/` or `examples/` | Source sample; only referenced by `07 - Packages.ipynb`. |
| `01…013 *.ipynb` | `lessons/01-basics/`, `lessons/02-linear-algebra/` | Reflects the two distinct tracks. |

**Remediation (proposed layout):**

```text
.
├── lessons/
│   ├── 01-basics/          01 … 09
│   └── 02-linear-algebra/  10 … 13
├── assets/images/          animation.gif, logo
├── examples/               Example.jl
├── .github/workflows/ci.yaml
├── Project.toml, Manifest.toml
└── README.md, LICENSE, LICENSE-CC-BY-NC-SA.md, AUDIT_REPORT.md
```

> Deferred deliberately: renaming and moving 13 tracked notebooks rewrites
> every path in the repository and is beyond the scope of an initialization
> pass. Raised here as a single decision for the maintainer.

---

## 3. MINOR

Polish, consistency, and readability.

### 3.1 Links — heuristic findings

No broken **internal** references were found. All images are base64-embedded
directly in the notebooks, so there are no external image paths to break, and
there are no relative Markdown links or `include("…")` calls between lessons.

| # | URL | Assessment |
|---|---|---|
| MIN-1 | `https://docs.julialang.org/en/v1/manual/performance-tips/#Access-arrays-in-memory-order,-along-columns-1` | **Likely stale anchor [unverified].** The trailing `-1` is the legacy Documenter.jl anchor format from Julia 0.x/1.0. Current docs use `#Access-arrays-in-memory-order,-along-columns`. The page loads; the in-page jump silently fails. |
| MIN-2 | `https://twitter.com/anoackjensen?lang=en` | **Redirect [unverified].** `twitter.com` now 301s to `x.com`; the `?lang=en` parameter is no longer honoured. Update to the canonical handle URL. |
| MIN-3 | `https://cdn.plot.ly/plotly-2.6.3.min.js` | Hard-pinned to Plotly **2.6.3** (2021) inside a saved PlotlyJS output blob. Not broken, but the notebook fetches a four-year-old renderer from a CDN on every open — an offline student sees a blank plot. |
| MIN-4 | `https://go.plotly.com/smarter-ai-data-apps` | Vendor marketing/tracking URL injected by the PlotlyJS output bundle, not authored content. Harmless but worth stripping when outputs are regenerated. |
| MIN-5 | `https://jmeubank.github.io/tdm-gcc/download/`, `https://julialang.org/downloads/`, `https://julialang.org/packages/`, `https://docs.julialang.org/…#Dictionaries`, `…#LinearAlgebra.cross`, `https://github.com/JuliaPy/Conda.jl` | Well-formed, stable targets. No structural concern. |

### 3.2 Incomplete sections

**No genuine `TODO` / `FIXME` / `TBD` markers exist in any cell source.** A
naive `grep` over the raw `.ipynb` files reports six hits for `XXX`/`TBD` in
`08 - Plotting.ipynb` (lines 462, 603, 1127, 1639, 2065) — all are false
positives from base64-encoded image data in stored outputs. Cell-source-level
parsing returns zero hits. No action needed; recorded so the next auditor does
not re-investigate.

### 3.3 Structural consistency

| # | Finding | Location |
|---|---|---|
| MIN-6 | Stray empty heading — the first Markdown cell opens with a bare `#` line before the real `# **🚀 Циклы (Loops) в Julia…**` title. Renders as an empty `<h1>`. | `04 - Loops.ipynb`, cell 0 |
| MIN-7 | Title word order breaks the series convention: "Введение в Julia. **Первый урок.**" where all twelve others use "**Урок** Второй/Третий/…". | `01 - Getting started.ipynb` |
| MIN-8 | No exercises. Lessons 01–09 average 2.2 numbered `Задание` blocks each; lessons `010`, `011`, `012`, `013` have **zero** (`012`/`013` carry an "Упражнения" heading with nothing under it). The advanced track offers no practice. | `010`, `011`, `012`, `013` |
| MIN-9 | Zero code cells — 18 Markdown cells, no Julia. Pure theory in a hands-on course; a student cannot execute anything in lesson 11. | `011 - Basic linear algebra.ipynb` |
| MIN-10 | Thin exposition — 945 Cyrillic characters across 9 Markdown cells for 19 code cells, versus 4 200–8 000 characters in comparable lessons. Lesson 2 is largely untranslated original material with code carrying the explanatory load. | `02 - Strings.ipynb` |
| MIN-11 | Stale checkpoint on disk: `.ipynb_checkpoints/01. Getting started-checkpoint.ipynb`, dated 2022-01-15 and matching no current filename (note the `.` separator versus the current `-`). Correctly git-ignored, but confusing in the working tree. | `.ipynb_checkpoints/` |
| MIN-12 | No cross-lesson navigation — no "next / previous lesson" links anywhere, and no index. Combined with MAJ-3, ordering is left entirely to the file listing. | all notebooks |

### 3.4 Dependency validation

- `requirements.txt`, `package.json`, `environment.yml`: **none present** — correct for a Julia project.
- `Project.toml`: present. See **MAJ-2** (no pins, no identity).
- `Manifest.toml`: present on disk, untracked. See **MAJ-1**.
- `JordanForm` and `LinearAlgebraX` are small single-maintainer packages used only by lessons 12–13; note the bus-factor risk if the course is to be maintained long-term.

### 3.5 Style & grammar

Overall the Russian prose is clear, consistently structured (numbered
`1️⃣ 2️⃣ 3️⃣` topic headers, `📌`/`🔍`/`🚀` markers), and free of the
copy-paste repetition typical of translated courses. Only two sentences recur
three or more times across 22 000+ words:

| # | Finding | Location |
|---|---|---|
| MIN-13 | Orthography: **"Одинадцатый"** → **"Одиннадцатый"** (double *н*). Appears in the lesson title heading. | `011 - Basic linear algebra.ipynb`, cell 0 |
| MIN-14 | Orthography: **"так же"** used where the conjunction **"также"** is meant (2× in `010`, 1× in `011`). Different words in Russian. | `010`, `011` |
| MIN-15 | Orthography: **"обьявить"** → **"объявить"** (hard sign, not soft). | `01 - Getting started.ipynb` |
| MIN-16 | Overlong paragraphs — one block exceeding 600 characters without a break in each of `010`, `013`, `03`, `07`. Split at the natural clause boundary or convert to a bulleted list. | `010`, `013`, `03`, `07` |
| MIN-17 | Repeated phrasing (3× each): "Берём минимальное время выполнения … и переводим в миллисекунды" and "Раскладываем по первой строке:". Acceptable as deliberate pedagogical refrain; vary if the repetition reads as filler. | `010`, `013` |

---

## 4. Summary

| Severity | Count | Open | Resolved in this pass |
|---|---|---|---|
| Critical | 3 | 1 (CRIT-1) | 2 (CRIT-2, CRIT-3) |
| Major | 8 | 8 (MAJ-1 partial) | — |
| Minor | 17 | 17 | — |

### Recommended order of work

1. **CRIT-1** — clear or fix the two failing asserts in lesson 3. One edit; highest student-visible impact.
2. **MAJ-1** — `git add Manifest.toml`. One command; unblocks reproducibility.
3. **MAJ-3 + MAJ-6** — rename `010…013` → `10…13` with descriptive linear-algebra titles. One batch of `git mv`.
4. **MAJ-2** — add `[compat]` bounds derived from the now-committed manifest.
5. **MAJ-4 + MAJ-5 + MAJ-7** — one clean restart-and-run-all pass over all 13 notebooks under Julia 1.11.3, which closes three findings at once.
6. **MAJ-8** — decide on the directory restructure before the repository is published, since it rewrites every path.
7. **Minor** — orthography (MIN-13/14/15) and the stray heading (MIN-6) are five-minute fixes; MIN-8/9/10 are content work to schedule.

### Files added or changed by this initialization pass

| Path | Action |
|---|---|
| `AUDIT_REPORT.md` | created — this document |
| `README.md` | rewritten — full landing page (CRIT-2) |
| `LICENSE` | created — MIT, dual copyright, scope clause (CRIT-3) |
| `LICENSE.md` | removed — superseded by `LICENSE` |
| `LICENSE-CC-BY-NC-SA.md` | verified complete, left unmodified |
| `.gitignore` | rewritten — comprehensive; `Manifest.toml` rule reversed (MAJ-1) |
| `.markdownlint.json` | created — config referenced by the `lint` CI job |
| `.github/workflows/ci.yaml` | created — lint / link-check / build jobs |
| `assets/images/logo-placeholder.txt` | created |

No notebook, `Project.toml`, or `Manifest.toml` content was modified — all
content findings above are reported, not silently repaired.
