"""Verify the exact export file set and hashes without extracting a zip."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


def safe_name(name: str) -> bool:
    parts = PurePosixPath(name).parts
    return bool(parts and not name.startswith('/') and '\\' not in name
                and ':' not in name and all(p not in ('..', '.') for p in parts)
                and PurePosixPath(name).as_posix() == name)


def verify_contents(contents: dict[str, bytes]) -> None:
    if any(not safe_name(name) for name in contents):
        raise ValueError('unsafe or noncanonical archive path')
    manifest = json.loads(contents['EXPORT_MANIFEST.json'])
    if manifest.get('schema') != 'contraledger-review-export-v2':
        raise ValueError('unknown export schema')
    expected = manifest['files']
    if set(contents) != set(expected) | {'EXPORT_MANIFEST.json'}:
        raise ValueError('missing or unexpected export file')
    for name, digest in expected.items():
        if hashlib.sha256(contents[name]).hexdigest() != digest:
            raise ValueError('export hash mismatch: ' + name)


def verify_directory(root: Path) -> None:
    contents = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError('symlink in export')
        if path.is_file():
            contents[path.relative_to(root).as_posix()] = path.read_bytes()
    verify_contents(contents)


def verify_zip(path: Path) -> None:
    with zipfile.ZipFile(path) as bundle:
        names = bundle.namelist()
        if len(names) != len(set(names)):
            raise ValueError('duplicate archive member')
        if any((i.external_attr >> 16) & 0o170000 == 0o120000 for i in bundle.infolist()):
            raise ValueError('symlink in archive')
        verify_contents({name: bundle.read(name) for name in names})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    verify_directory(args.path) if args.path.is_dir() else verify_zip(args.path)
    print('PASS: exact file set and all export SHA-256 hashes.')
