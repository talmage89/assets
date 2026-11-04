"""Independent comparison of accepted SUV assemblies and pivot contracts.

The optical patch, grille, arch toes and hood sampling intentionally change.
The accepted cabin, drivetrain, wheels, hardware and painted door positions
must remain exact. This compares actual vertices and node matrices, not inputs.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
import numpy as np


def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));bpy.context.view_layer.update()
    parts={};pivots={}
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH' and (ob.get('part_category') in ['interior','underbody','tires','wheels','brakes','mechanisms','doors']):
            parts[ob.name]=dict(points=np.asarray([tuple(ob.matrix_world@v.co) for v in ob.data.vertices]),faces=[tuple(f.vertices) for f in ob.data.polygons])
        if 'pivot_axis' in ob:
            pivots[ob.name]=dict(matrix=[list(row) for row in ob.matrix_world],axis=ob['pivot_axis'],range=list(ob['range_degrees']))
    return parts,pivots


def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);before,source=Path(a.before),Path(a.source)
    old,pivots=snapshot(before);new,current=snapshot(source);rows={};errors=[]
    for name,r in old.items():
        q=new.get(name);same=q is not None and r['points'].shape==q['points'].shape
        error=float(np.max(np.abs(q['points']-r['points']))) if same else None
        topology=same and q['faces']==r['faces']
        rows[name]=dict(maximum_coordinate_delta_m=error,topology_identical=topology)
        if error is None or error>1e-7 or not topology:errors.append(name)
    if current!=pivots:errors.append('Pivot transforms, axes or ranges changed')
    report=dict(passed=not errors,errors=errors,accepted_parts=len(rows),accepted_pivots=len(pivots),pivots_identical=current==pivots,parts=rows,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),before_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),scope='Actual world vertices, polygon connectivity and pivot contracts; appearance and articulation are separate checks')
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2));print('SUV_PRESERVATION',report['passed'],len(rows),'parts',errors)
    if errors:raise AssertionError(errors)


if __name__=='__main__':main()
