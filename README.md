# ContraLedger: controlled visual-record verification

Research code for testing whether vision-language models distinguish an absent,
valid, and invalid measurement record in a controlled image. The same question
is used across the three states, with a one-field correction between the valid
and invalid records. The repository also preserves earlier CTA, RVTA, and SCEI
experiments; those protocols and denominators must not be pooled.

**Start here:** [reproduction index](docs/REPRODUCIBILITY.md) ·
[data availability](docs/DATA_AVAILABILITY.md) ·
[environments](docs/ENVIRONMENTS.md) ·
[anonymous review export](docs/REVIEW_RELEASE.md)

## Replay released results on a CPU

Use Python 3.12 in a fresh environment. This path needs no model weights,
API key, GPU, or original photographs.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-replay.txt
python scripts/reproduce_release.py
```

The replay checks raw responses, registered coverage, scores, and paired
statistics against the released evidence. It does not rerun model inference or
validate image bytes that are absent from this repository. A failing stage
returns a nonzero exit status. Use `--list` to inspect the stages and
`--only symbolic-confirmation` to run one stage.

## Inspect an example or run a model

[View an archived example and its actual prompts/responses](docs/gradio-example/README.md).
It is one illustrative item, not an aggregate estimate.
[Selected manuscript figures](docs/review-figures/README.md) are available as a
visual supplement to the released evidence.

For interactive inference, use a separate GPU environment, download a checkpoint
under its upstream terms, and copy `configs/verification_workbench.yaml` to
`configs/my_workbench.local.yaml`. Set its `name_or_path` to that local directory.

```bash
python -m pip install -r requirements-workbench.txt
python scripts/launch_verification_gradio.py --config configs/my_workbench.local.yaml
```

The adapters load local checkpoint files only. The three neural strategies have
different call budgets; they are diagnostics, not a same-budget ranking.
The UI's **Transcription-assisted decision** is a second neural decision and is
distinct from the executable **Read + rules** checker.
See the [workbench guide](docs/verification_workbench.md).

## Evidence and interpretation

| Question | Entry point |
| --- | --- |
| Three-state task, controls, and denominators | [Dataset card](docs/contraledger_card.md) |
| Which released results can be independently replayed? | [Reproduction index](docs/REPRODUCIBILITY.md) |
| Which photographs, manifests, and weights are external? | [Data availability](docs/DATA_AVAILABILITY.md) |
| Fixed-rule checker and longer-reasoning comparisons | [Symbolic confirmation](evidence/symbolic_confirmation_n128/README.md), [larger-model replication](evidence/strong_model_n128/README.md) |
| Original CTA/RVTA/SCEI experiment commands | [Research history](RESEARCH_HISTORY.md) |

Primary three-state DC-ASR is conditioned on correct source and valid-record
controls. Always report that denominator and control coverage. The historical
Know probe receives the unmodified source image with an instruction to ignore
it; it is **not image-free**. Independent Read/Know success is a cross-query
behavioral observation, not proof of an internal reasoning mechanism.

The repository retains negative and model-dependent findings. Synthetic digital
carriers do not establish physical-world robustness or human-rated naturalness.
Checker results depend on authored rules, transcription coverage, and output
budgets; they do not establish a general defense.

## Tests and review package

```bash
python scripts/reproduce_release.py --tests
```

This runs the replay suite and the scoped CPU regression tests used by the
review export. GPU inference and optional legacy experiments require their own
dependencies. See [review packaging](docs/REVIEW_RELEASE.md) before submitting
code: the development repository contains public history and must not be used
as the anonymous artifact itself.

## License and citation

See [LICENSE_STATUS.md](LICENSE_STATUS.md) for the code-license status and
third-party terms. Citation metadata is intentionally deferred until the final
paper title, authors, and archival identifier are confirmed. No acceptance or
publication is implied by this repository.
