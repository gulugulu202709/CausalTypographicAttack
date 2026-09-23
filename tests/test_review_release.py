"""Export checks must reject tampering and protect recorded evidence."""
import hashlib
import json
from pathlib import Path
import pytest
from scripts.review_export import check_text, protected, redact
from scripts.verify_review_release import safe_name, verify_contents


def artifact():
    data = b'archived response\n'
    manifest = {'schema': 'contraledger-review-export-v2',
                'files': {'evidence/raw.jsonl': hashlib.sha256(data).hexdigest()}}
    return {'evidence/raw.jsonl': data, 'EXPORT_MANIFEST.json': json.dumps(manifest).encode()}


def test_manifest_rejects_changed_missing_and_extra_bytes():
    original = artifact()
    verify_contents(original)
    changed = dict(original, **{'evidence/raw.jsonl': b'altered'})
    missing = {k: v for k, v in original.items() if k != 'evidence/raw.jsonl'}
    extra = dict(original, **{'private.txt': b'extra'})
    for contents in (changed, missing, extra):
        with pytest.raises(ValueError):
            verify_contents(contents)


@pytest.mark.parametrize('name', ['../secret', '/absolute', 'C:/secret', 'x\\y', 'x/../y', 'x//y'])
def test_unsafe_names_rejected(name):
    assert not safe_name(name)


def test_raw_evidence_and_executed_checker_are_protected():
    assert protected(Path('evidence/symbolic_confirmation_n128/raw/qwen7.jsonl'))
    assert protected(Path('evidence/read_symbolic_n128/protocol.json'))
    assert protected(Path('scripts/evaluate_transcribed_record_checker.py'))
    assert not protected(Path('docs/ENVIRONMENTS.md'))


def test_identity_cleanup_preserves_numeric_content():
    source = '/home/researcher/models/model accuracy=0.75 Researcher'
    actual = redact(source, {'Researcher': 'Anonymous'})
    assert actual == '/path/to/local/models/model accuracy=0.75 Anonymous'
    check_text(actual, {'Researcher': 'Anonymous'})


def test_unredacted_identity_rejected():
    with pytest.raises(ValueError):
        check_text('contact Researcher', {'Researcher': 'Anonymous'})


def test_credential_boundary_does_not_match_task_protocol_name():
    check_text('task-preserving-content-confirmation-128', {})
    with pytest.raises(ValueError):
        check_text('token=' + 'sk-' + 'x' * 30, {})
