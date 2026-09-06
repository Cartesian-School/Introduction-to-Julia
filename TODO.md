# TODO — deferred work

Items carried over from [`AUDIT_REPORT.md`](AUDIT_REPORT.md) that were **not**
fixed. Everything requiring a Julia toolchain has now been completed; what
remains is content authoring and one structural decision.

---

## Done — notebook regeneration pass (Julia 1.11.3)

All 13 notebooks were re-executed top-to-bottom with `nbconvert --execute`
against Julia 1.11.3 on Linux. Recorded here so the next maintainer knows what
state the outputs are in:

- [x] **MAJ-5** — every notebook now reports kernel `Julia 1.11.3`.
- [x] **MAJ-7** — execution counts are monotonic `1..N` in all 13.
- [x] **MAJ-4** — lesson 7's `Pkg.add("Plots")` runs clean; 0 errors.
- [x] **NEW-2** — lesson 10's Python comparison **works**; 0 errors.
- [x] **Manifest hash** — `Pkg.resolve()` refreshed `project_hash` with no
      dependency-version churn, confirming the `[compat]` bounds were correct.

Only **13 error outputs** remain across the whole course, and every one is an
intentional teaching demonstration (lessons 1, 2, 3, 6, 9 — `MethodError`,
`ParseError`, `KeyError`, all with explanatory prose around them).

---

## Content work

- [ ] **Add worked solutions to the blank exercises.**
      Lesson 3 follows a three-cell pattern: `# Ваше решение` → `# Правильное
      решение:` → `@assert`. Ten exercises across lessons **1, 6, 12 and 13**
      have the blank and the assert but **no solution cell**, so their asserts
      fail on a clean run. Their outputs are currently cleared (they ship
      un-run, showing nothing rather than red errors), but the underlying gap
      is unfixed:

      | Lesson | Undefined in the assert |
      |---|---|
      | 1 — Getting started | `days`, `days_float` |
      | 6 — Functions | `add_one`, `A1` |
      | 12 — Linear algebra in Julia | `dot_v`, `outer_v`, `cross_v` |
      | 13 — Factorizations | `A_eigv`, `A_diag`, `A_lowertri` |

- [ ] **MIN-8 — Add exercises to lessons 10–13.**
      Lessons 1–9 average 2.2 numbered `Задание` blocks each. Lessons 12 and 13
      carry an "Упражнения" heading with nothing under it.

- [ ] **MIN-9 — Add executable content to lesson 11.**
      `11 - Linear algebra concepts.ipynb` is 18 Markdown cells with zero code —
      the only lesson a student cannot run. Either add worked Julia examples or
      merge it into lesson 12 as a theory preamble.

- [ ] **MIN-10 — Expand the exposition in lesson 2.**
      945 Cyrillic characters across 9 Markdown cells supporting 19 code cells,
      roughly a fifth of the prose density of comparable lessons.

- [ ] **MIN-12 — Add cross-lesson navigation.** No next/previous links, no index.

- [ ] **MIN-16 — Split overlong paragraphs** in lessons 10, 13, 3, 7.

- [ ] **MIN-17 — Vary repeated phrasing (optional).** Two sentences appear 3×
      each; acceptable as a deliberate refrain.

---

## Environment caveats found during the re-run

- [ ] **PyCall needs `ENV["PYTHON"]=""` on many Linux systems.**
      Lesson 10 installs `PyCall` via `Pkg.add`. That builds against the system
      `python3`, which fails with *"Couldn't find libpython"* on distributions
      whose Python ships without a shared `libpython` (hit here with Python
      3.14). The fix is to build against PyCall's own Conda Python:

      ```julia
      ENV["PYTHON"] = ""
      using Pkg; Pkg.build("PyCall")
      ```

      Worth adding to lesson 10 as a troubleshooting note, or students on Linux
      will hit exactly the failure that made this section broken to begin with.

- [ ] **Lesson 8's UnicodePlots cell renders only interactively.**
      Under `nbconvert` the cell raises
      `ArgumentError: Plots(UnicodePlots): saving to '.png' requires 'import
      FreeType, FileIO'`, because batch execution asks for a PNG while
      UnicodePlots draws terminal text. Its output is cleared; it works fine in
      a live session. Adding `FreeType`/`FileIO` to the project would silence it
      at the cost of two dependencies that nothing else needs.

- [ ] **Notebook `Pkg` calls mutate the project files.**
      Lessons 7, 8, 10 and 13 contain 16 `Pkg.add`/`Pkg.rm` calls. Running them
      rewrites `Project.toml`/`Manifest.toml` — during this pass it added
      `Colors`, `Conda`, `PyCall`, `UnicodePlots` and **silently dropped `Plots`
      and `PlotlyJS` from `[compat]`**. Both files were restored from a snapshot
      afterwards. Anyone re-running the notebooks must do the same, or run them
      against a throwaway environment.

---

## Structure

- [ ] **MAJ-8 — Directory restructure.** Deferred for maintainer decision; the
      proposed layout is in `AUDIT_REPORT.md`. It rewrites every path in the
      repository, so settle it before the course is published widely.

- [ ] **Relocate root-level assets.** `animation.gif` (lesson 8) and
      `Example.jl` (lesson 7) sit in the repository root. Subsumed by MAJ-8.

- [x] **CI workflow location.** ✅ At `.github/workflows/ci.yaml`.

- [ ] **Switch to a live CI badge.** `README.md` uses a static placeholder.
      After the workflow's first successful run on `main`, replace it with
      `https://github.com/Cartesian-School/Introduction-to-Julia/actions/workflows/ci.yaml/badge.svg`.
      Kept static for now so `link-check` does not fail on a URL that 404s until
      the workflow exists on the default branch.

---

## Won't fix

- **MIN-3 / MIN-4 — Plotly CDN pin and vendor tracking URL.** Both lived in
  saved PlotlyJS output blobs and were regenerated during the re-run.

- **MIN-14 — "так же" → "также".** Withdrawn. All six occurrences are the
  comparative "так же, как" ("just as … as"), which is correct Russian. The
  original finding came from a grep that did not check for the following "как".
