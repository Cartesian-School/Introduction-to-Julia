# TODO

Status of the course. Items are in exactly one of three states:

- **✅ Completed** — done and verified by execution or by `tools/check_course.py`.
- **⏸️ Deferred, non-blocking** — a deliberate decision, not an outstanding defect.
  Does **not** block publication.
- **🔴 Open** — a real defect that still needs work.

> **There are currently no 🔴 Open items.**

---

## ✅ Completed

### Technical remediation

- [x] All 13 notebooks execute top-to-bottom under Julia 1.11.3.
- [x] Kernel metadata consistent; execution counts monotonic `1..N`.
- [x] `Manifest.toml` tracked; `[compat]` bounds match resolved versions.
- [x] Lesson numbering `010`–`013` → `10`–`13`; linear-algebra titles disambiguated.
- [x] No absolute local paths or secrets in committed outputs.

### Course structure

- [x] Learning objectives in all 13 lessons.
- [x] Navigation footer in all 13 lessons.
- [x] Every exercise has a worked solution and executable verification
      (**26 verified exercises**).

### Lesson content

- [x] **Lesson 2 — UTF-8 string indexing.** Was the largest remaining gap.
      Now teaches `String`/`Char`, `length` vs `ncodeunits`, why indices are byte
      offsets rather than character ordinals, `firstindex`/`lastindex`/
      `nextind`/`prevind`, `eachindex`, `for c in s`, and `collect` with its
      allocation caveat. Includes a **live Cyrillic `StringIndexError`
      demonstration** on `"Привет"[2]` and an exercise (2.3) checking real
      understanding of characters versus bytes.
- [x] **Lesson 3 — heterogeneity as a trade-off.** No longer says `Vector{Any}`
      is simply bad. Explains boxing, dynamic dispatch and lost specialisation,
      measures the cost (40 µs / 0 allocations versus 3.1 ms / ~100 000
      allocations at n = 100 000), and introduces small `Union`s —
      `Union{Missing, Float64}`, `skipmissing`, `coalesce`, and why
      `missing == missing` is `missing`.
- [x] **Lesson 8 — `plot` versus `plot!`.** Explicit section on the `!`
      convention, working with the plot object explicitly rather than relying on
      implicit "current plot" state, the backend concept, and exercise 8.3 with
      object-level structural verification.
- [x] **Lesson 9 — multiple dispatch to flagship standard.** Method specificity
      with the type hierarchy, the `isa`-chain anti-pattern rewritten with
      dispatch, genuine two-argument dispatch, ambiguity and how it is resolved,
      and a warning against over-annotation. Two new exercises (9.2, 9.3).
      Also corrected a factual error: the lesson claimed dispatch happens at
      compile time rather than at runtime.
- [x] **Lessons 10–13** professionalized in the previous pass (performance
      methodology, executable linear-algebra bridge, corrected `LinearAlgebra`
      claims, factorization preconditions and reuse).
- [x] **MIN-16 — long paragraphs.** Resolved. The one genuinely dense block
      (lesson 7's advantages list) was reformatted. Lessons 3, 10 and 13 were
      resolved by the content rewrites. No prose paragraph over 600 characters
      remains; the two blocks a length heuristic still flags are bulleted lists,
      already one item per line, and splitting them further would fragment them.

### Environment and tooling

- [x] **Package-environment safety.** Lessons 7, 8, 10, 13 no longer mutate the
      course environment. Lesson 7 teaches `Pkg.activate(; temp=true)` as its
      own subject matter. Verified by SHA-256 across a full 13-notebook run.
- [x] **`tools/check_course.py`** — 13 invariants, wired into CI.
- [x] **`tools/test_check_course.py`** — 15 corruption scenarios, all rejected;
      a clean control fixture passes. Runs in CI **before** the validator.

---

## ⏸️ Deferred, non-blocking

These are architectural or cosmetic decisions, not defects.

- [ ] **MAJ-8 — directory restructure.**
      **DEFERRED — NON-BLOCKING ARCHITECTURAL MAINTENANCE.**
      Explicitly excluded from this pass. Stable repository links are worth more
      than tidier paths. If it is ever revisited, write `STRUCTURE_PROPOSAL.md`
      first. This does **not** affect publication readiness.

- [ ] **Live CI badge.** `README.md` uses a static badge by design. A GitHub
      Actions badge URL returns 404 until the workflow has run on the default
      branch, which would fail the `link-check` job on the very pull request
      that introduces it. The README makes no claim about live CI status, so
      this is not misleading. Swap it after the workflow's first successful run
      on `main`.

- [ ] **Russian table of contents.** Navigation footers link to `README.md`,
      which is in English because it is also the GitHub landing page. A separate
      Russian course map would be a nicety, not a fix.

---

## Environment caveats (documented in the lessons themselves)

- **`PyCall` and `libpython`.** Lesson 10's Python comparison needs a Python
  with a shared `libpython`; many Linux distributions and Python 3.14 ship
  without one. The lesson documents `ENV["PYTHON"]=""` + `Pkg.build("PyCall")`
  as a **conditional** remedy — to be applied only if the error appears.
  `PyCall` is deliberately not a course dependency: adding it to `Project.toml`
  would break `Pkg.instantiate()` for every student lacking `libpython`.

- **UnicodePlots renders only interactively.** Under `nbconvert` the backend is
  asked for a PNG and raises `ArgumentError`. The demonstration is optional and
  temp-scoped. Adding `FreeType`/`FileIO` to silence it would add two
  dependencies nothing else needs.

---

## Withdrawn findings

- **MIN-14 — "так же" → "также".** All occurrences are the comparative
  "так же, как", which is correct Russian.
- **MIN-3 / MIN-4 — Plotly CDN pin and vendor tracking URL.** Lived in saved
  output blobs; regenerated during re-execution.
