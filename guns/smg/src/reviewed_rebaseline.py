"""Explicit reviewed paint journal update; normal builds never invoke it.

Require the old manifest, actual handoff and new GLB hashes in REVIEW.md.
The existing geometry/layout checks must pass before recording the change.
All wear, albedo and specular bounds remain unchanged.
"""
import argparse
import hashlib
import json
from pathlib import Path

from finish_review import BASE, layout, signature


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--old-manifest-sha256', required=True)
    parser.add_argument('--old-source', type=Path, required=True)
    parser.add_argument('--old-glb-sha256', required=True)
    parser.add_argument('--new-glb-sha256', required=True)
    parser.add_argument('--reason', required=True)
    args = parser.parse_args()
    destination = BASE / 'src/accepted_paint.json'
    source = BASE / 'export/smg.glb'
    assert sha(destination) == args.old_manifest_sha256, 'Wrong previous manifest; stop and review'
    assert sha(args.old_source) == args.old_glb_sha256, 'Wrong handoff GLB'
    assert sha(source) == args.new_glb_sha256, 'Wrong reviewed GLB'
    old = json.loads(destination.read_text())
    text = (BASE / 'REVIEW.md').read_text()
    assert all(value in text for value in (
        args.old_manifest_sha256, args.old_glb_sha256, old['reviewed_glb_sha256'],
        args.new_glb_sha256, args.reason)), 'Record all hashes and reason in REVIEW.md first'
    assert signature(args.old_source) == signature(source), 'Handoff geometry, UVs, rig or clips changed'
    layout()  # Independent accepted gun and detachable geometry baselines.
    updated = dict(old)
    updated['authored_roughness'] = .42
    updated['reviewed_glb_sha256'] = args.new_glb_sha256
    updated['reviewed_changes'] = old.get('reviewed_changes', []) + [dict(
        previous_manifest_sha256=args.old_manifest_sha256,
        previous_journal_glb_sha256=old['reviewed_glb_sha256'],
        actual_handoff_glb_sha256=args.old_glb_sha256,
        reviewed_glb_sha256=args.new_glb_sha256,
        previous_authored_roughness=old['authored_roughness'],
        authored_roughness=.42, reason=args.reason)]
    destination.write_text(json.dumps(updated, indent=2) + '\n')
    print('REVIEWED REBASELINE', args.old_glb_sha256, '->', args.new_glb_sha256)


if __name__ == '__main__':
    main()
