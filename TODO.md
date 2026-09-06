# TODO — remaining work

Status after the professionalization pass on `feat/professionalize-julia-course`.
Nothing below is marked done unless it was verified by execution or by
`tools/check_course.py`.

---

## Done

### Technical remediation (earlier pass)

- [x] All 13 notebooks execute top-to-bottom under Julia 1.11.3.
- [x] Kernel metadata consistent; execution counts monotonic `1..N`.
- [x] `Manifest.toml` tracked; `[compat]` bounds match resolved versions.
- [x] Lesson numbering `010`–`013` → `10`–`13`; linear-algebra titles disambiguated.
- [x] No absolute local paths or secrets in committed outputs.

### Course professionalization (this pass)

- [x] **Learning objectives** in all 13 lessons.
- [x] **Navigation footer** in all 13 lessons (previous / contents / next).
- [x] **Worked solutions for every exercise.** Closes the `days`, `days_float`,
      `add_one`, `A1`, `dot_v`, `outer_v`, `cross_v`, `A_eigv`, `A_diag`,
      `A_lowertri` items, plus gaps found in lessons 2, 7 and 9 that were not
      previously recorded.
- [x] **Lesson 11 is executable** — was 18 Markdown cells with no code, now 38
      code cells. Added `norm`, `rank`, transpose vs adjoint, eigenvalue
      intuition, and why `A \ b` beats `inv(A) * b`.
- [x] **Lesson 12 corrected** — the false claim that `A'A` is shorthand for
      `transpose(A) * A`, the wrong mechanism for underdetermined and
      rank-deficient solves, and a misleading `Symmetric` example on a
      non-symmetric matrix.
- [x] **Lesson 13** — Cholesky preconditions (`isposdef`, `PosDefException`,
      `check=false`), factorization reuse across right-hand sides, and a
      rebuilt exercise block. Two of the three old exercises were unpassable:
      one compared floats with `==`, the other against rounded display values.
- [x] **Lesson 10** — performance methodology: global-scope benchmarking, type
      stability with `@code_warntype`, column-major traversal, broadcast fusion.
      Three new exercises.
- [x] **Package-environment safety** — lessons 7, 8, 10, 13 no longer mutate
      the course environment. Lesson 7 teaches `Pkg.activate(; temp=true)`
      explicitly. Verified by checksum across a full 13-notebook run.
- [x] **Validation harness** — `tools/check_course.py`, 13 invariants, wired
      into CI, negative-tested against a broken fixture.
- [x] **Mathematical corrections** — lesson 11 stated `X = A^{-1}` for the
      inverse method; the correct formula is `X = A^{-1}B`.

---

## Open — content

- [ ] **MIN-10 — Lesson 2 (Strings) needs depth.**
      This is the largest remaining content gap. The lesson has 19 code cells
      supported by only ~9 Markdown cells and does not cover:
      - the `String` / `Char` distinction in enough depth;
      - **UTF-8 byte indexing** — the single most important Julia-specific
        pitfall for anyone arriving from Python, where `s[i]` is a character.
        In Julia indices are byte offsets and not every offset is valid;
      - `firstindex` / `lastindex` / `nextind` / `eachindex` for safe traversal;
      - multiline strings, comparison, and the common `String` functions.
      Teaching `s[2]` without explaining that it can throw
      `StringIndexError` on non-ASCII text would leave a real trap in place.

- [ ] **Lesson 9 (Multiple dispatch) deserves flagship treatment.**
      It correctly shows methods and type annotations, but does not yet:
      - contrast dispatch with C++/Java overloading (dispatch is on the runtime
        types of *all* arguments, and resolved dynamically);
      - show a design where dispatch replaces an `if x isa ...` chain;
      - discuss method specificity and ambiguity;
      - warn against over-annotating argument types.

- [ ] **Lesson 3 (Data structures) — the heterogeneity trade-off.**
      Currently implies `Vector{Any}` is simply bad. The honest framing is a
      trade-off: `Any` costs a pointer indirection and blocks specialisation,
      but is the right choice for genuinely heterogeneous data. `NamedTuple`
      and `struct` should be presented as the usual alternatives.

- [ ] **MIN-16 — long paragraphs** in lessons 3 and 7 (10 and 13 were addressed).

- [ ] **Lesson 8 (Plotting)** — the backend concept is mentioned but not
      explained; `plot` / `plot!` mutation semantics deserve a short note.

---

## Open — structure

- [ ] **MAJ-8 — directory restructure.** Deliberately not done: stable
      repository links are worth more than tidier paths right now. If it is
      ever done, `STRUCTURE_PROPOSAL.md` should be written first.

- [ ] **Live CI badge.** `README.md` uses a static placeholder. Swap it for
      `https://github.com/Cartesian-School/Introduction-to-Julia/actions/workflows/ci.yaml/badge.svg`
      after the workflow's first successful run on `main` — before then the URL
      404s and would fail the `link-check` job.

- [ ] **Russian table of contents.** Navigation footers link to `README.md`,
      which is in English. A short Russian course map would serve the actual
      reader better.

---

## Environment caveats

- [ ] **`PyCall` and `libpython`.** Lesson 10's Python comparison needs a Python
      with a shared `libpython`; many Linux distributions and Python 3.14 do not
      ship one. The lesson documents `ENV["PYTHON"]=""` + `Pkg.build("PyCall")`
      as a conditional remedy. `PyCall` is deliberately **not** a course
      dependency: putting it in `Project.toml` would break `Pkg.instantiate()`
      for every student whose system lacks `libpython`.

- [ ] **UnicodePlots renders only interactively.** Under `nbconvert` the backend
      is asked for a PNG and raises `ArgumentError`. The demonstration is
      optional and temp-scoped; adding `FreeType`/`FileIO` to silence it would
      add two dependencies nothing else needs.

---

## Won't fix

- **MIN-14 — "так же" → "также".** Withdrawn: all occurrences are the
  comparative "так же, как", which is correct Russian.

- **MIN-3 / MIN-4 — Plotly CDN pin and vendor tracking URL.** Lived in saved
  output blobs; regenerated during re-execution.
