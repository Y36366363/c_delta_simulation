"""Verify original experiment sources without changing frozen manifest hashes.

Only the explicitly archived pre-September-15 cdelta source has a version map.
All other files remain strict checks against the current path. The archived
file is a source artifact, not imported by the current public implementation.
"""
from pathlib import Path
from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256

ROOT = Path(__file__).resolve().parents[1]
LEGACY_CDELTA_HASH = '32f0dd80097bb1a7c207b18edcb8b54069ea473291627e649a717705a23d5be7'
LEGACY_CDELTA_PATH = 'archive/source_snapshots/cdelta_20260914.py'


def frozen_source_check(path, expected_hash, *, root=ROOT):
    current = root / path
    if current.is_file() and normalized_text_sha256(current) == expected_hash:
        return {'passed': True, 'verified_path': path, 'version': 'current'}
    if path == 'src/cdelta.py' and expected_hash == LEGACY_CDELTA_HASH:
        snapshot = root / LEGACY_CDELTA_PATH
        return {'passed': snapshot.is_file() and normalized_text_sha256(snapshot) == expected_hash,
                'verified_path': LEGACY_CDELTA_PATH, 'version': 'archived 176248b'}
    return {'passed': False, 'verified_path': path, 'version': 'unmatched'}
