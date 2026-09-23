# Code-release readiness — 2026-09-23

Target: ICLR 2027 code supplement. Scope: repository and anonymous code
candidate only; no manuscript was supplied or compiled.

## Implemented

- Concise primary README and separate historical research notes.
- Study-to-command index with explicit replay/inference distinctions.
- Data availability and recorded environment documentation.
- Corrected the historical Knowledge-probe description: it includes the clean
  source image; an instruction to ignore it does not make the call image-free.
- Portable local paths in 191 configuration templates; original downloaded
  checkpoint revisions are retained as comments where present.
- Pinned Python 3.12 CPU verification dependencies, unified replay and CI.
- History-free text-only export with identity checks, protected evidence,
  deterministic zip metadata, exact file-set checks and SHA-256 verification.

## Validation

- Six numerical replay stages passed in the development checkout and in the
  actual exported directory: diagnostic, confirmation, channel study,
  retrospective checker, symbolic confirmation and larger-model replication.
- Exported scoped CPU tests: 90 passed, 1 skipped. The skipped test requires a
  Linux integration font and remains enabled for Linux CI.
- 203 configuration files parse as YAML; 162 Python scripts compiled in memory.
  Release tools were also exercised by the build, verification and regressions.
- Archive exact file set and SHA-256 checks passed. Archived responses, primary
  scores, historical parsers and protected code hashes were not rewritten.
- No new GPU inference or original-pixel audit was performed.

## Remaining blockers for a complete submission

1. The rights holder has not selected a project-wide code license. No new
   license grant has been fabricated.
2. SCEI raw predictions/release manifest and primary three-state/delivery-matrix
   registered pixels, manifests and raw journals are not all publicly supplied.
   Aggregate files cannot substitute for those inputs.
3. Final manuscript title, authors, table/figure numbering and archival citation
   metadata have not been supplied. Citation metadata is deferred rather than
   populated with guessed information.
4. Full GPU reconstruction from an empty data directory and all original
   environment locks remain unverified.
5. Anonymous code checks do not certify manuscript/PDF/image metadata or prevent
   research-content-based identity inference. Inspect the final submission.

Status: **verified code-review candidate, with explicit external blockers**.
This is not a certification that the whole ICLR submission is ready.
