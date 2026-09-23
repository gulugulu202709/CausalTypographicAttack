# Environments and compute

## CPU verification

`requirements-replay.txt` pins the direct dependencies for the scoped CPU replay
and regression suite on Python 3.12. It is not a reconstruction of the original
GPU environment. Run with `PYTHONUTF8=1` on Windows when invoking historical
scripts directly; the unified runner sets this for its child processes.

## Recorded inference environments

| Study | Recorded environment | Evidence |
| --- | --- | --- |
| Media/channel study | Python 3.10.12; PyTorch 2.5.1+cu121; Transformers 5.9.0; NumPy 1.26.4; Pillow 12.2.0 | `evidence/channel_binding_n128/runtime_checkpoint_snapshot.json` |
| Verification workbench validation | Python 3.10; PyTorch 2.5.1+cu121; Transformers 5.9.0; Gradio 6.26.0 | `docs/verification_workbench.md` |
| Qwen3.5-27B replication | Python 3.12.13; vLLM 0.19.1; PyTorch 2.10.0+cu129; Transformers 5.14.1; two RTX A6000 GPUs, approximately 48 GB each | `evidence/strong_model_n128/runtime_audit.json` |

These are recorded version snapshots, not newly validated universal install
recipes. `requirements.txt` and the optional GPU/UI requirements express broad
development constraints; installing their latest allowed versions does not
guarantee reproduction. Original complete transitive dependency locks are not
available for every experiment and have not been fabricated.

The larger-model README supplies an immutable upstream checkpoint revision and
a reference launcher. Other releases provide available checkpoint file hashes;
do not silently substitute the latest model revision. Download into a local
directory, record the revision and hashes, and set `name_or_path` in a private
config. Keep distinct model-family environments separate where needed.

Full-study wall time and peak-memory measurements are not uniformly published.
Released token/latency traces describe the measured calls, not a guaranteed
hardware requirement. No GPU inference was performed as part of this packaging
change. The CPU checks only validate the released evidence and code paths.
