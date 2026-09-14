# ContraLedger — anonymous review artifact

This review export contains the executable three-state verification workbench,
constraint compiler, analysis scripts, paired evidence and bounded supplementary
diagnostics. It has no development Git history, author contacts, host addresses,
private configuration, model weights, or bundled third-party photographs.

## Quick start

```bash
pip install -r requirements-workbench.txt
python scripts/launch_verification_gradio.py --config configs/verification_workbench.yaml
```

Configure a locally downloaded checkpoint first. Qwen2.5-VL and Qwen3-VL adapters
load local files only. Set the available device in the YAML. A GPU is needed for
real model evaluation; CPU-only tests do not substitute for model experiments.
The UI accepts a photograph and an object label supplied by the user, constructs
clearly labeled synthetic valid/invalid records and shows raw and correct answers.

## CPU checks and evidence replay

```bash
python -m pytest tests/test_verification_workbench.py tests/test_verification_display.py tests/test_rule_confirmation_table.py -q
python scripts/make_rule_confirmation_table.py --evidence evidence/rule_explicit_confirmation_n128/analysis.json --output review-table
python scripts/replay_verification_diagnostic.py --evidence evidence/verification_diagnostic_n64
python scripts/replay_verification_confirmation.py --evidence evidence/verification_confirmation_n128
python scripts/analyze_channel_study.py --replay evidence/channel_binding_n128
python -m pytest tests/test_channel_study.py -q
python -m unittest discover -s tests -p test_transcribed_record_checker.py -v
python scripts/evaluate_transcribed_record_checker.py --output evidence/read_symbolic_n128 --replay
python scripts/analyze_symbolic_confirmation.py --replay evidence/symbolic_confirmation_n128
python -m unittest discover -s tests -p test_symbolic_confirmation.py -v
python scripts/analyze_strong_model.py --replay evidence/strong_model_n128
python -m unittest discover -s tests -p test_strong_model.py -v
```

See `docs/verification_workbench.md` for CLI evaluation and the meaning of each
denominator. Attack success means a false record is accepted *after both controls
pass*. Invalid-record accuracy measures correct rejection, so it points in the
opposite direction. A failed control is neither attack success nor demonstrated
defense. One example cannot estimate population performance.

## Evidence scope

`evidence/main_comparison/` retains the main paired-comparison numerical evidence;
the twenty corrected baseline comparisons show no significant method advantage.
`evidence/rule_explicit_confirmation_n128/` contains the separate fixed-reference
128-source confirmation. Both the Qwen-7B positive result and Qwen3-VL null are
retained. The supplementary strategy diagnostic is a new protocol on reused
sources, not a claim of unseen-scene transfer or superior attack performance.
`evidence/verification_confirmation_n128/` adds the prospectively registered
comparison of read-then-verify with self-check on 128 different archived scenes.
All 3,584 calls, paired effects and both model outcomes are retained. The scenes
are disjoint from the earlier 64-scene diagnostic by ID and original image hash;
they are not globally unseen benchmark sources. See its README for the results.
`evidence/channel_binding_n128/` adds 4,608 frozen calls separating record pixels,
exact supplied fields, genuinely image-free reasoning, and controlled object
swaps. Supplied fields and locations are oracle diagnostics, not deployable
defenses. The object-swap records remain pixel-identical when objects move.
All full-set scores, ten prespecified tests and separate-call controls are
retained, including failures and null results. Original record templates are
reused; these are digital composites, not new natural measurements.

`evidence/read_symbolic_n128/` adds a retrospective template-aware symbolic
checker applied to all 512 actual model transcriptions, with zero new inference
calls. Pair scores are 124/128 and 127/128; all parse abstentions count incorrect.
It does not receive gold fields. Known schemas, reused scenes and unequal output
caps limit this result; it is not independent defense confirmation.

`evidence/symbolic_confirmation_n128/` contains the subsequent prospectively
registered comparison on 128 different archived scenes, excluding both previous
diagnostic populations by item ID and exact original-source hash. Direct,
reason-then-answer and transcription each have one call and a 384-token output
cap; actual input/output lengths and cap hits are retained. All 1,536 fresh
calls and four corrected comparisons are released. Equal output caps do not
mean equal actual computation; the checker also uses authored schema rules.

`evidence/strong_model_n128/` adds the subsequent Qwen3.5-27B replication on
the same fixed 128 scenes. It contains all 1,280 newly registered calls: three
384-token non-thinking arms, longer reasoned responses at 2,048 tokens, and
thinking-mode responses at 4,096 tokens including reasoning. All four corrected
contrasts, measured token use, cap hits and optimistic format bounds remain
visible. This is a larger open-checkpoint replication on previously evaluated
scenes, not closed-model or new-schema validation. Greedy controlled settings
differ from the model provider's recommended sampled benchmark settings.

Some archived experiment scripts depend on original registered photos and
historical build products. These dependencies are described in their READMEs;
they are not silently replaced by generated evidence. Obtain COCO/VOC images
from their original providers under the corresponding terms. This code export
does not grant a license to those datasets or to model weights. Existing
third-party notices remain with their source files.

Path redactions change archive bytes but not the numerical evidence. Historical
hashes in evidence refer to the executed private archive; `EXPORT_MANIFEST.json`
records the actual anonymous-export file hashes. This export supports inspection
and scoped numerical replay; it does not certify every historical run as fully
reproducible or remove the limitations stated in the paper.
