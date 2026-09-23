# Data and artifact availability

This document distinguishes files included here from artifacts that still need
an external release. It does not imply that every historical experiment is
fully reproducible from a fresh checkout.

| Asset | Available here | Remaining requirement |
| --- | --- | --- |
| Six CPU replay studies | Released predictions/journals, scoring inputs and analysis | `requirements-replay.txt`; original photographs are unnecessary for numerical replay |
| SCEI-Images-300 victim results | Summary CSVs, table and `public_analysis.json` | Raw predictions and `release_manifest.json` referenced by the validator are absent; full replay is unavailable |
| SCEI-Images-300 metadata | All 300 scene selections and symbolic records | Read per-image license metadata |
| SCEI-Images-300 pixels | 206 scenes with clean/false/corrected images | 94 scenes withheld under the recorded ND-license policy; do not equate 206-image evaluation with n=300 |
| Three-state 200-item confirmation | Construction code and configuration templates | Frozen `runs/contraledger_threeway_n200_v1frozen/` is not included |
| COCO/VOC delivery matrix | Summary CSVs and audit/analysis JSON | Raw prediction journals and frozen images remain in the research artifact store; no public download is supplied here |
| Symbolic and stronger-model inference | Frozen textual requests, responses and audit metadata | Original registered scene packets and licensed image bytes; some original registrations/source snapshots remain external |
| Model checkpoints | Model identities and available checkpoint audits | Download separately under each provider's terms; adapters use local files only |

The SCEI pixel release can be checked with `sha256sum -c SHA256SUMS` from
`datasets/scei_images_coco_n300/`. Its dataset card and `source_licenses.jsonl`
record sources and attribution. The anonymous review export includes two
manuscript plots and four screenshots of one archived Gradio example. The
screenshots include a source photograph already shown in the public example;
upstream image rights remain with the original licensor. The export does not
provide the original study image corpus or model weights.

## Required before claiming complete end-to-end reproduction

1. Provide a stable, review-accessible archive for each missing registered
   manifest and prediction journal, with SHA-256 checksums.
2. For photographs that cannot be redistributed, supply permitted source IDs,
   acquisition instructions, frozen construction inputs and expected hashes.
   A generic instruction to download COCO/VOC is not a complete reconstruction
   recipe for a particular registered scene packet.
3. Test those instructions from an empty data directory in the documented GPU
   environment. Record runtime and memory use for each primary experiment.
4. Match the final manuscript's tables and figures to this index. No table
   numbering or unprovided manuscript content has been invented.

These are outstanding release requirements, not completed experiments. Keep
the missing assets explicit in the paper's reproducibility statement until
they have actually been supplied and verified.
