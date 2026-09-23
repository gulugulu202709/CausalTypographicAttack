"""Build and replay a history-free review candidate without editing evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.reproduce_release import run_stage
from scripts.verify_review_release import verify_directory

ALLOWED = {'.py', '.yaml', '.yml', '.json', '.jsonl', '.md', '.tex', '.txt', '.csv'}
FOLDERS = ('cta', 'scripts', 'configs', 'tests', 'evidence', 'experiments', 'results', 'schemas')
GUIDES = ('REPRODUCIBILITY.md', 'DATA_AVAILABILITY.md', 'ENVIRONMENTS.md',
          'REVIEW_RELEASE.md', 'contraledger_card.md', 'contraledger_dataset.md',
          'verification_workbench.md')
REVIEW_BINARIES = (
    'docs/review-figures/contraledger_threeway_results.png',
    'docs/review-figures/contraledger_results_main_20260908.png',
    'docs/gradio-example/question.png',
    'docs/gradio-example/images.png',
    'docs/gradio-example/interface.png',
    'docs/gradio-example/checks.png',
)
REPLAY_EVIDENCE = {
    'verification_diagnostic_n64', 'verification_confirmation_n128',
    'channel_binding_n128', 'read_symbolic_n128',
    'symbolic_confirmation_n128', 'strong_model_n128',
}
# Supplemental audit: not an input to numerical replay.
UNPROTECTED_AUDIT = 'evidence/strong_model_n128/executed_source_audit.json'
CREDENTIAL = re.compile(r'(?<![a-zA-Z0-9_])(?:olp_[a-zA-Z0-9]{15,}|gh[pousr]_[a-zA-Z0-9]{20,}|hf_[a-zA-Z0-9]{20,}|sk-[a-zA-Z0-9_-]{24,})')
PRIVATE_ROOT = re.compile(r'/(?:home|Users)/[^/\s\"\'\\]+/|/disk\d+/[^/\s\"\'\\]+/')
WINDOWS_ROOT = re.compile(r'[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s\"\']+[\\/]+', re.I)
PRIVATE_HOST = re.compile(r'https?://(?:(?:10|192\.168)\.(?:\d{1,3}\.){1,2}\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?::\d+)?')

README = '''# ContraLedger — anonymous review candidate

This review artifact contains code, configuration templates, six independently
replayable evidence chains, scoped tests, two manuscript plots, and four Gradio
interface screenshots. Git history, personal configuration, weights and
historical planning notes are excluded.
Primary-study asset gaps remain: see `docs/DATA_AVAILABILITY.md`.

[Inspect the manuscript plots](docs/review-figures/README.md) and
[all four Gradio interface views](docs/gradio-example/README.md).

## CPU verification

Use Python 3.12 in a fresh environment:

```bash
python -m pip install -r requirements-replay.txt
python scripts/verify_review_release.py .
python scripts/reproduce_release.py --tests
```

The builder ran all six numerical replay stages before creating this archive.
These validate archived responses, coverage, scoring and paired statistics;
they do not rerun inference or independently audit absent image pixels. SCEI
victim-result aggregates and the COCO/VOC delivery matrix are included for
inspection, but missing raw journals prevent their full replay.

See `docs/REPRODUCIBILITY.md` for the study-to-command map and
`docs/ENVIRONMENTS.md` for the pinned CPU environment and recorded GPU versions.
The historical three-state Knowledge probe retains the clean source image;
only the separate channel study includes genuinely image-free calls.

For optional inference, obtain a licensed local checkpoint, copy
`configs/verification_workbench.yaml` to a `*.local.yaml` file, configure its
paths/device and follow `docs/verification_workbench.md`. The transcription-
assisted neural decision differs from the executable Read + rules checker.

## Integrity, rights and limits

Protected replay inputs and hash-bound code retain their original bytes after
LF normalization. Identity substitutions in those files are refused. Other
redactions are listed in `EXPORT_MANIFEST.json` with hashes of actual exported
files. Historical registration hashes refer to the original experiments,
not a new preregistration of this export.

Original source and third-party attribution remain subject to their stated
terms. See `LICENSE_STATUS.md`; this artifact does not grant rights to upstream
photographs, weights or baseline components. No acceptance, complete end-to-end
reproducibility, or guaranteed anonymity is claimed. Inspect this archive and
the final manuscript before submission.
'''


def protected(relative: Path) -> bool:
    name = relative.as_posix()
    if name in {'cta/transcribed_record_checker.py', 'scripts/evaluate_transcribed_record_checker.py'}:
        return True
    return (len(relative.parts) > 2 and relative.parts[0] == 'evidence'
            and relative.parts[1] in REPLAY_EVIDENCE and relative.suffix != '.md'
            and name != UNPROTECTED_AUDIT)


def redact(text: str, replacements: dict[str, str]) -> str:
    for old in sorted(replacements, key=len, reverse=True):
        text = re.sub(re.escape(old), lambda _: replacements[old], text, flags=re.I)
    text = PRIVATE_ROOT.sub('/path/to/local/', text)
    text = WINDOWS_ROOT.sub('/path/to/local/', text)
    return PRIVATE_HOST.sub('http://127.0.0.1', text)


def check_text(text: str, replacements: dict[str, str]) -> None:
    if CREDENTIAL.search(text):
        raise ValueError('credential-like token in candidate; value suppressed')
    if any(re.search(re.escape(term), text, re.I) for term in replacements):
        raise ValueError('identity substitution incomplete; value suppressed')
    if PRIVATE_ROOT.search(text) or WINDOWS_ROOT.search(text) or PRIVATE_HOST.search(text):
        raise ValueError('private path or host remains; value suppressed')


def collect(source: Path) -> list[Path]:
    files = []
    for folder in FOLDERS:
        files.extend(p for p in (source / folder).rglob('*')
                     if p.is_file() and p.suffix in ALLOWED
                     and not p.name.endswith('.local.yaml')
                     and '__pycache__' not in p.parts)
    files.extend(source / 'docs' / name for name in GUIDES)
    files.extend(source / 'docs' / 'review-figures' / name for name in ('README.md',))
    files.extend(source / 'docs' / 'gradio-example' / name for name in ('README.md', 'result.json'))
    files.extend(source / name for name in ('requirements.txt', 'requirements-workbench.txt',
                 'requirements-replay.txt', 'pytest.ini', 'LICENSE_STATUS.md'))
    files.extend(source.glob('LICENSE'))
    files.extend(source.glob('NOTICE*'))
    return sorted(set(files))


def build(source: Path, destination: Path, terms: Path) -> Path:
    source, destination, terms = source.resolve(), destination.resolve(), terms.resolve()
    archive = destination.with_suffix('.zip')
    if source == destination or destination in source.parents:
        raise ValueError('output must not contain the source tree')
    if destination.exists() or archive.exists():
        raise FileExistsError('use a new output directory and archive name')
    if destination == terms or destination in terms.parents:
        raise ValueError('private identity map must be outside the export')
    replacements = json.loads(terms.read_text(encoding='utf-8-sig'))
    if not isinstance(replacements, dict) or any(not isinstance(k, str) or not k
            or not isinstance(v, str) for k, v in replacements.items()):
        raise ValueError('identity map must contain nonempty string keys and string values')
    entries, changes = {}, []
    for path in collect(source):
        relative = path.relative_to(source)
        if path.is_symlink():
            raise ValueError('symlinks are not allowed in the export')
        original = path.read_text(encoding='utf-8-sig')
        text = redact(original, replacements)
        try:
            check_text(text, replacements)
        except ValueError as error:
            raise ValueError(f'{relative.as_posix()}: {error}') from None
        if text != original:
            if protected(relative):
                raise ValueError(f'identity redaction would change protected replay input: {relative.as_posix()}')
            changes.append(relative.as_posix())
        entries[relative.as_posix()] = text.replace('\r\n', '\n').encode('utf-8')
    for name in REVIEW_BINARIES:
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'missing or unsafe review figure: {name}')
        entries[name] = path.read_bytes()
    entries['README.md'] = README.encode('utf-8')
    entries['.gitignore'] = b'__pycache__/\n*.pyc\n.pytest_cache/\nruns/\nwork/\n.venv/\nconfigs/*.local.yaml\n'
    entries['.gitattributes'] = b'* text=auto eol=lf\n'
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in entries.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    manifest = {
        'schema': 'contraledger-review-export-v2',
        'files': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(entries.items())},
        'redacted_files': sorted(changes),
        'scope': 'review code plus two manuscript plots and four Gradio screenshots; historical hashes unchanged; missing assets documented',
    }
    (destination / 'EXPORT_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    verify_directory(destination)
    run_stage(['scripts/reproduce_release.py'], destination)
    verify_directory(destination)
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(destination.rglob('*')):
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(destination).as_posix(), (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, path.read_bytes())
    print(json.dumps({'files': len(entries) + 1, 'redacted_files': len(changes),
                      'archive': str(archive), 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest()}))
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--terms', type=Path, required=True)
    args = parser.parse_args()
    build(args.source, args.output, args.terms)


if __name__ == '__main__':
    main()
