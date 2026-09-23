# Anonymous review candidate

The public development repository and its history are not the anonymous
artifact. Build a separate scoped export with an explicit identity map:

```bash
python scripts/build_anonymous_release.py --source . --output work/review-candidate --terms /path/to/private-redactions.json
python scripts/verify_review_release.py work/review-candidate
python work/review-candidate/scripts/reproduce_release.py --tests
```

Use a new output directory for every build. The map is a JSON object of exact
identity strings to neutral replacements. Keep it outside version control and
outside the exported directory. Include author names, account names, email
addresses, institutional identifiers, private hosts, and public project links
where relevant; preserve third-party attribution. Do not put credentials in
this mapping: remove/revoke actual exposed credentials through a separate
review if any are found. The builder rejects credential-like tokens without
printing their values.

The export includes code, configuration templates, scoped tests, textual
evidence, aggregate results and the reviewer-facing guides. It excludes Git
history, development plans, research-history notes, local configuration files,
most image binaries and weights. The two selected paper plots and four
Gradio screenshots are explicitly allowlisted in `scripts/review_export.py`.
The Gradio image comparison includes a source photograph used in the existing
public example; its upstream rights are not granted by this artifact.
Source-paper files are not included.

The builder refuses to redact any file used by the six CPU replay chains.
Changing an archived journal and then recomputing its hash would invalidate
the original evidence identity. If protected evidence contains identifying
material, prepare an explicitly documented derived evidence release rather
than bypassing this check. Only unprotected documentation and path metadata
may be redacted; `EXPORT_MANIFEST.json` lists changes and file hashes. Original
registration hashes still refer to the original experiments.

The build runs all six CPU replay stages **before** publishing the zip. The
verification tool checks every file, unexpected files and unsafe archive paths.
The zip uses fixed timestamps and permissions. A successful build establishes
scoped numerical replay and automated identity checks, not guaranteed anonymity
against inference from distinctive research content.

Before submission, inspect the final archive itself, check the final manuscript
and image/PDF metadata separately, provide the missing primary-study artifacts
listed in `DATA_AVAILABILITY.md`, and confirm the project license and citation
metadata. Do not call the whole submission ready while those items are pending.
