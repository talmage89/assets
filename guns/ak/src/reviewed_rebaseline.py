"""Explicit reviewed paint-bake acceptance; never invoked by make.

Normal bake_identity.py recording still refuses to overwrite a baseline.
This command requires both exact hashes in REVIEW.md and preserves the
historical non-image signature and every existing rounding bound.
"""
import argparse
import json
from pathlib import Path

from bake_identity import BASE, record, sha


def reviewed_record(old, new, old_manifest_sha256, reason):
    assert new['export'] == old['export'], 'Geometry, tangents, rig, clips or JSON semantics changed'
    for key in ('block_samples','prime','maximum_component_difference','maximum_changed_texels_per_map'):
        assert new[key] == old[key], 'Never change a bake tolerance during re-baselining'
    new['historical_handoff_sha256'] = old.get('historical_handoff_sha256',old['accepted_glb_sha256'])
    new['reviewed_changes'] = old.get('reviewed_changes',[]) + [dict(
        previous_glb_sha256=old['accepted_glb_sha256'],
        reviewed_glb_sha256=new['accepted_glb_sha256'],
        previous_manifest_sha256=old_manifest_sha256,
        previous_map_hashes={name:dict(decoded_sha256=row['decoded_sha256'],png_sha256=row['png_sha256'])
                             for name,row in old['maps'].items()},
        reason=reason)]
    return new


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--old-manifest-sha256',required=True)
    p.add_argument('--new-glb-sha256',required=True)
    p.add_argument('--reason',required=True)
    a=p.parse_args()
    destination=BASE/'src/accepted_bake.json'
    contents=destination.read_bytes()
    assert sha(contents)==a.old_manifest_sha256, 'Wrong previous manifest; stop and review'
    old=json.loads(contents)
    text=(BASE/'REVIEW.md').read_text()
    assert all(s in text for s in (old['accepted_glb_sha256'],a.new_glb_sha256,a.reason)), 'Record old/new hashes and reason in REVIEW.md first'
    new=record(a.source,a.new_glb_sha256)
    new=reviewed_record(old,new,a.old_manifest_sha256,a.reason)
    destination.write_text(json.dumps(new,indent=2)+'\n')
    print('REVIEWED REBASELINE',old['accepted_glb_sha256'],'->',new['accepted_glb_sha256'])


if __name__=='__main__':main()
