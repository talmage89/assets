"""Build four independent block manifests and placeable checkpoint buildings."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import bpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(ROOT),str(HERE)]
from kit import tiling
from plan import PROOF,load
from graphics import generate
from geometry import palette
from building import Building
from delivery import externalize,bundle_hash


def count(obs):
    return sum(len(o.data.loop_triangles) for o in obs)


def build_block(seed,region,count_lots=7,path=None,context=False):
    p=load(seed,region,count_lots,path);out=Path('build/context/blocks')/(region+'-'+str(seed)) if context else Path('build/blocks')/region;out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sheet,layout=generate(Path('build/signs'));mats=palette(sheet);rows=[]
    for lot in p['lots']:
        b=Building(lot,mats,layout);root,obs,doors=b.build()
        bpy.context.view_layer.update()
        # Static render batches are consolidated inside the one placeable root.
        fixed=[o for o in obs if o.parent==root];moving=[o for o in obs if o.parent!=root]
        bpy.ops.object.select_all(action='DESELECT')
        for o in fixed:o.select_set(True)
        bpy.context.view_layer.objects.active=fixed[0];bpy.ops.object.join();fixed[0].name=lot['id']+'__Static'
        obs=[fixed[0]]+moving
        for o in obs:o.data.calc_loop_triangles()
        objects=[root]+list(root.children_recursive)
        # External image URIs are canonical across the entire family.
        export=(out if context else Path('export'))/(lot['id']+'.gltf');export.parent.mkdir(exist_ok=True)
        bpy.ops.object.select_all(action='DESELECT')
        for o in objects:o.select_set(True)
        embedded=Path('build/delivery')/(lot['id']+'.glb');embedded.parent.mkdir(parents=True,exist_ok=True)
        tiling.export(embedded,objects)
        externalize(embedded,export)
        doc=json.loads(export.read_text());budget=30000 if lot['stories']==3 or lot['corner'] else 20000
        tris=count(obs)
        if tris>budget:raise ValueError(f"{lot['id']}: {tris} > {budget}")
        row=dict(id=lot['id'],triangles=tris,budget=budget,materials=len(doc.get('materials',[])),
                 gltf_bytes=export.stat().st_size,bin_bytes=export.with_suffix('.bin').stat().st_size,
                 bundle_sha256=bundle_hash(export),position=[lot['x'],lot['y'],0],doors=[o.name for o in doors],source=str(export))
        rows.append(row);root.location=(lot['x'],lot['y'],0)
    bpy.context.view_layer.update();sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc['stage']=p['stage']
    blend=out/'block.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend.resolve()))
    tiling.export(out/'block.glb')
    if not context:
        from street import build_street
        street_root,street_meta=build_street(p,mats)
        street_glb=Path('build/street')/(region+'.glb');street_glb.parent.mkdir(exist_ok=True)
        tiling.export(street_glb,[street_root]+list(street_root.children_recursive))
        externalize(street_glb,Path('export')/('DowntownStreet_'+region+'.gltf'))
        street_meta['source']='export/DowntownStreet_'+region+'.gltf'
        (out/'street.json').write_text(json.dumps(street_meta,indent=2)+'\n')
    meta=dict(**p,buildings=rows,triangles=sum(r['triangles'] for r in rows))
    (out/'block.json').write_text(json.dumps(meta,indent=2)+'\n')
    return dict(region=region,seed=seed,triangles=meta['triangles'],buildings=rows,source=str(out/'block.glb'))


def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=Path('build/downtown.blend'))
    a.add_argument('--wear',type=float,default=1.0);a.add_argument('--seed',type=int);a.add_argument('--region',default='midwest');a.add_argument('--count',type=int,default=7);a.add_argument('--plan',type=Path)
    args=a.parse_args(sys.argv[sys.argv.index('--')+1:]);__import__('age').AMOUNT=args.wear;args.out.parent.mkdir(parents=True,exist_ok=True)
    cases=[(args.seed,args.region)] if args.seed is not None else PROOF
    rows=[build_block(seed,region,args.count,args.plan) for seed,region in cases]
    # The main sentinel is a deterministic manifest; all four group outputs are declared in Make.
    bpy.ops.wm.save_as_mainfile(filepath=str(args.out.resolve()))
    (args.out.with_suffix('.json')).write_text(json.dumps(dict(stage='baked shared external delivery',blocks=rows),indent=2)+'\n')
    print('DOWNTOWN',[(r['region'],r['triangles']) for r in rows],flush=True)
if __name__=='__main__':main()
