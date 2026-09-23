# Reproduction index

Run all commands from the repository root with `requirements-replay.txt`.
The index uses study names rather than guessed manuscript table numbers: the
final manuscript was not supplied for this repository release audit.

| Study / result | Released evidence | Replay stage (`--only`) | Capability |
| --- | --- | --- | --- |
| SCEI image evaluation, four checkpoints | `results/scei_images_n300_eval_v1/` | Not replayable from this checkout | Aggregate files present; raw predictions and `release_manifest.json` absent |
| 64-scene neural mitigation diagnostic | `evidence/verification_diagnostic_n64/` | `verification-diagnostic` | 2,560 archived calls and paired statistics |
| 128-scene mitigation confirmation | `evidence/verification_confirmation_n128/` | `verification-confirmation` | 3,584 archived calls, probes, coverage and paired statistics |
| Media and object-association diagnostic | `evidence/channel_binding_n128/` | `channel-study` | 4,608 archived calls, image-free traces and paired tests |
| Retrospective Read + rules analysis | `evidence/read_symbolic_n128/` | `retrospective-checker` | 512 archived reads; no new inference |
| Prospective symbolic-checker confirmation | `evidence/symbolic_confirmation_n128/` | `symbolic-confirmation` | 1,536 archived calls, tokens, coverage and paired tests |
| Qwen3.5-27B replication | `evidence/strong_model_n128/` | `strong-model` | 1,280 archived calls and five budget/strategy arms |
| Rule-explicit fixed-reference confirmation | `evidence/rule_explicit_confirmation_n128/` and `experiments/task_preserving_content_confirm128_20260908/` | See historical scripts | Separate study; not the three-state DC-ASR |
| COCO/VOC three-renderer delivery matrix | `results/contraledger_delivery_matrix_v1/` | No complete public raw replay | Aggregate CSV/JSON only; raw assets and predictions remain external |

`python scripts/reproduce_release.py --list` prints the exact underlying
commands. Each replay checks the existing scored evidence rather than accepting
new outputs or overwriting the historical result. `--tests` additionally runs
the scoped scoring, parsing, coverage and export regressions.

## Repeating inference

Numerical replay is available for the six stages above. Repeating inference
requires licensed original pixels, exact frozen manifests/requests, downloaded
checkpoint bytes, and a compatible GPU runtime. See [data availability](DATA_AVAILABILITY.md)
and [environments](ENVIRONMENTS.md). Rebuilding scenes with a new planner or new
model weights is a new run, not byte-identical reproduction of a frozen study.

Configuration templates use portable local locations. Copy a template to a
`*.local.yaml` file and set its paths before running it. The historical evidence
and recorded configuration hashes remain unchanged by template cleanup.

## Protocol correction

The historical three-state Knowledge call passes `source_path` to the model
and asks it to ignore that image. It must be described as a knowledge probe with
the clean source image, not text-only/image-free reasoning. The separate
channel study includes genuinely image-free calls and verifies the absence of
visual tensors. These protocols are different.

Keep Read + rules separate from the workbench's transcription-assisted neural
decision. Report failure/abstention denominators, actual token counts, and
output-cap sensitivity alongside comparative accuracy.
