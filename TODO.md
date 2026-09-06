# TODO — deferred work

Items carried over from [`AUDIT_REPORT.md`](AUDIT_REPORT.md) that were **not**
fixed during the remediation pass. None are bugs; they are content and
structure work that needs an author decision or a working Julia toolchain.

---

## Blocked — requires Julia 1.11.3

The remediation environment had no Julia installed and no permission to
download one, so nothing that needs notebook execution could be completed or
verified.

### Runbook

Run this on a machine with network access, then commit the resulting notebooks.
Keep the depot off any FAT/exFAT volume — Julia needs symlinks and permission
bits that vfat cannot store.

```bash
# 1. Install Julia 1.11.3
curl -fsSL https://install.julialang.org | sh
juliaup add 1.11.3 && juliaup default 1.11.3
julia --version          # expect: julia version 1.11.3

# 2. Restore the environment and refresh Manifest.toml's project_hash,
#    which adding [compat] invalidated.
cd /path/to/Introduction-to-Julia
julia --project=. -e 'using Pkg; Pkg.instantiate(); Pkg.resolve()'
git diff --stat Manifest.toml    # expect: project_hash only, no version churn

# 3. Install the Jupyter kernel
julia --project=. -e 'using Pkg; Pkg.add("IJulia")'

# 4. Restart & Run All, in place, for every lesson.
#    Drop --allow-errors for lessons with no intentional error demos
#    (04, 05, 07, 08, 11, 12, 13) so a genuine failure stops the run.
for nb in *.ipynb; do
  echo "== $nb"
  jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=julia-1.11 \
    --ExecutePreprocessor.timeout=1800 \
    --allow-errors "$nb" || echo "FAILED: $nb"
done
```

Lessons 2, 3, 6, and 9 contain **intentional** `MethodError` / `ParseError`
demonstrations. Those must survive the re-run; only unintended failures should
disappear. Diff the error counts before and after rather than assuming a clean
run is correct.

After re-running, re-check that no local paths crept back in (see NEW-1):

```bash
grep -l "$(whoami)\|/home/\|C:.Users" *.ipynb
```

- [ ] **MAJ-5 — Re-run lesson 5 under Julia 1.11.3.**
      `05 - Conditionals.ipynb` still declares a `Julia 1.6.0` kernel. The
      metadata was deliberately **not** edited by hand: rewriting the kernelspec
      without re-executing would claim a provenance the outputs do not have.
      Restart & Run All under 1.11.3 fixes metadata and outputs together.

- [ ] **MAJ-7 — Restart & Run All across all 13 notebooks.**
      Execution counts are still non-monotonic. As above, renumbering the
      `execution_count` fields by hand was rejected: it would make the notebooks
      *look* reproducible while destroying the only signal that they are not.

- [ ] **NEW-2 — Repair the Python comparison in lesson 10.**
      `10 - Julia is fast.ipynb` cells 73–114 fail in a cascade: `PyCall` fails
      to precompile, and every downstream cell then raises `UndefVarError`
      (`pybuiltin`, `pysum`, `@benchmark`, `py_list_bench`, `d`, `pyimport`,
      `@py_str`). The lesson's conclusion cells (166–167) quote NumPy and pure
      Python timings that the notebook never produced.
      Needs a working `PyCall` + `Conda` + `numpy`, then a full re-run. If
      Python interop cannot be made to work reliably for students, consider
      dropping the Python comparison and rewriting the conclusion around the
      Julia-versus-C results, which do run.

- [ ] **Refresh `Manifest.toml`'s `project_hash`.**
      Adding `[compat]` to `Project.toml` invalidates the hash recorded in the
      manifest. Run `julia --project=. -e 'using Pkg; Pkg.resolve()'`. The
      bounds were chosen to match the already-resolved versions exactly, so
      this should refresh the hash without changing any dependency version.

- [ ] **MAJ-4 (partial) — Regenerate lesson 7's install cells.**
      The failed `PyCall` build output on cell 17 and the noisy `stderr` on
      cells 30 and 43 were *cleared*, not re-run. A clean execution would
      restore the legitimate `Pkg` output a student should expect to see.

---

## Content improvements

- [ ] **MIN-8 — Add exercises to lessons 10–13.**
      Lessons 1–9 average 2.2 numbered `Задание` blocks each; lessons 10–13 have
      none. Lessons 12 and 13 carry an "Упражнения" heading with nothing under
      it.

- [ ] **MIN-9 — Add executable content to lesson 11.**
      `11 - Linear algebra concepts.ipynb` is 18 Markdown cells with zero code.
      It is the only lesson a student cannot run. Either add worked Julia
      examples, or merge it into lesson 12 as a theory preamble.

- [ ] **MIN-10 — Expand the exposition in lesson 2.**
      `02 - Strings.ipynb` has 945 Cyrillic characters across 9 Markdown cells
      supporting 19 code cells — roughly a fifth of the prose density of
      comparable lessons. Largely untranslated original material.

- [ ] **MIN-12 — Add cross-lesson navigation.**
      No "next / previous lesson" links and no index notebook. Ordering is left
      entirely to the file listing.

- [ ] **MIN-16 — Split overlong paragraphs.**
      One block over 600 characters without a break in each of lessons 10, 13,
      3, and 7.

- [ ] **MIN-17 — Vary repeated phrasing (optional).**
      "Берём минимальное время выполнения … и переводим в миллисекунды" and
      "Раскладываем по первой строке:" each appear 3×. Acceptable as a
      deliberate refrain; revisit only if it reads as filler.

---

## Structure

- [ ] **MAJ-8 — Directory restructure.** Deferred for maintainer decision.
      The proposed layout is in `AUDIT_REPORT.md`. It rewrites every path in the
      repository, so it should be settled before the course is published widely.

- [ ] **Relocate root-level assets.** `animation.gif` (used only by lesson 8)
      and `Example.jl` (used only by lesson 7) sit in the repository root.
      Subsumed by MAJ-8 if that is adopted.

- [x] **CI workflow location.** ✅ Moved to `.github/workflows/ci.yaml`, where
      GitHub Actions auto-discovers it.

- [ ] **Switch to a live CI badge.** `README.md` currently uses a static
      placeholder badge. After the workflow's first successful run on `main`,
      replace it with:
      `https://github.com/Cartesian-School/Introduction-to-Julia/actions/workflows/ci.yaml/badge.svg`
      It is left static for now so the `link-check` job does not fail on a
      badge URL that 404s until the workflow exists on the default branch.

---

## Won't fix

- **MIN-3 / MIN-4 — Plotly CDN pin and vendor tracking URL.** Both are embedded
  in saved PlotlyJS output blobs, not in authored content. They will disappear
  when lesson 8's outputs are regenerated (MAJ-7).

- **MIN-14 — "так же" → "также".** Withdrawn. All six occurrences are the
  comparative construction "так же, как" ("just as … as"), which is correct
  Russian. The original audit finding was a false positive from a grep that did
  not check for the following "как".
