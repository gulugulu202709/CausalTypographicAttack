#!/usr/bin/env bash
set -euo pipefail

cd /disk2/anonymous/causal_typographic_attack

run_one() {
  local gpu="$1"
  local config="$2"
  local extra_pythonpath="${3:-}"
  if [[ -n "$extra_pythonpath" ]]; then
    CUDA_VISIBLE_DEVICES="$gpu" PYTHONPATH="$extra_pythonpath" \
      /disk2/anonymous/.venv/bin/python scripts/run_contraledger_threeway.py --config "$config"
  else
    CUDA_VISIBLE_DEVICES="$gpu" \
      /disk2/anonymous/.venv/bin/python scripts/run_contraledger_threeway.py --config "$config"
  fi
}

run_one "${1:-0}" configs/contraledger_threeway_qwen3_n200.yaml
run_one "${1:-0}" configs/contraledger_threeway_qwen7_n200.yaml
run_one "${1:-0}" configs/contraledger_threeway_llava_n200.yaml \
  /disk2/anonymous/cta_crossvl_env/lib/python3.10/site-packages
run_one "${1:-0}" configs/contraledger_threeway_internvl_n200.yaml \
  /disk2/anonymous/cta_internvl_env/lib/python3.10/site-packages
