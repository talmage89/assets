"""Six actual construction builds with source/GLB verification, no rendering."""
import argparse
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from build import build,save
from plan import generate,PROOF_SEEDS
from check_mesh import source_check,delivery_check

SEEDS=PROOF_SEEDS


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('build/seeds'));p.add_argument('--seeds',default=','.join(map(str,SEEDS)))
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
    rows=[];seeds=list(map(int,a.seeds.split(',')))
    for seed in seeds:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        dest=a.out/f'house-{seed}.blend';report=save(build(generate(seed)),dest)
        row=dict(seed=seed,source=source_check(dest));row['glb']=delivery_check(dest);rows.append(row)
    # A second actual build must reproduce the same geometry digest and count.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    first=json.loads((a.out/f'house-{seeds[0]}.json').read_text())
    repeated=save(build(generate(seeds[0])),a.out/'repeat.blend')
    assert first['geometry_sha256']==repeated['geometry_sha256']
    import hashlib
    repeat_hash=hashlib.sha256((a.out/'repeat.glb').read_bytes()).hexdigest()
    assert repeat_hash==rows[0]['glb']['sha256'], 'Checkpoint GLB byte repeatability'
    # Exercise a caller-authored plan, not just the default seed dictionary.
    overrides=dict(main=dict(width=12.192,depth=8.5344,roof='gable',pitch=.5),
        garage=dict(side='left',width=7.0104,depth=7.0104),bays=5,porch='gable',
        cladding=dict(Main=dict(front='veneer'),Garage=dict(front='siding')),
        colors=dict(siding=[.35,.39,.31],door=[.22,.036,.027]))
    from check_plan import check
    authored_plan=generate(6,overrides);check(authored_plan)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    dest=a.out/'authored.blend';save(build(authored_plan),dest)
    authored=dict(source=source_check(dest));authored['glb']=delivery_check(dest)
    (a.out/'checks.json').write_text(json.dumps(dict(passed=True,rows=rows,authored_plan=authored,
        repeat_geometry_sha256=repeated['geometry_sha256'],repeat_glb_sha256=repeat_hash),indent=2))
    print('MESH_SWEEP',len(rows),'built and checked; deterministic repeat passed')
