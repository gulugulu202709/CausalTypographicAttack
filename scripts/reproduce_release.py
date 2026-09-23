"""Run the published CPU evidence replays without changing recorded results."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STAGES = {
    "verification-diagnostic": ["scripts/replay_verification_diagnostic.py", "--evidence", "evidence/verification_diagnostic_n64"],
    "verification-confirmation": ["scripts/replay_verification_confirmation.py", "--evidence", "evidence/verification_confirmation_n128"],
    "channel-study": ["scripts/analyze_channel_study.py", "--replay", "evidence/channel_binding_n128"],
    "retrospective-checker": ["scripts/evaluate_transcribed_record_checker.py", "--output", "evidence/read_symbolic_n128", "--replay"],
    "symbolic-confirmation": ["scripts/analyze_symbolic_confirmation.py", "--replay", "evidence/symbolic_confirmation_n128"],
    "strong-model": ["scripts/analyze_strong_model.py", "--replay", "evidence/strong_model_n128"],
}
CPU_TESTS = [
    "tests/test_contraledger.py", "tests/test_contraledger_threeway.py",
    "tests/test_verification_workbench.py", "tests/test_verification_display.py",
    "tests/test_rule_confirmation_table.py", "tests/test_channel_study.py",
    "tests/test_channel_analysis.py", "tests/test_verification_confirmation.py",
    "tests/test_transcribed_record_checker.py", "tests/test_symbolic_confirmation.py",
    "tests/test_strong_model.py", "tests/test_review_release.py",
]


def run_stage(args: list[str], root: Path = ROOT) -> None:
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    # Historical replay code uses assertions for integrity checks.
    env.pop("PYTHONOPTIMIZE", None)
    subprocess.run([sys.executable, *args], cwd=root, env=env, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--only", choices=STAGES, action="append")
    parser.add_argument("--tests", action="store_true", help="also run scoped CPU regressions")
    args = parser.parse_args()
    if args.list:
        for name, command in STAGES.items():
            print(f"{name}: python {' '.join(command)}")
        return
    for name in args.only or STAGES:
        print(f"\nChecking {name}", flush=True)
        run_stage(STAGES[name])
    if args.tests:
        run_stage(["-m", "pytest", "-p", "no:cacheprovider", "-q", *CPU_TESTS])
    print("PASS: selected released evidence checks. No new model inference or original-pixel audit.")


if __name__ == "__main__":
    main()
