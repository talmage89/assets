"""Independent comparison of accepted SUV assemblies and pivot contracts.

The optical patch, grille, arch toes and hood sampling intentionally change.
The accepted cabin, drivetrain, wheels, hardware and painted door positions
must remain exact. This compares actual vertices and node matrices, not inputs.
"""
import argparse,hashlib,json,sys,fnmatch
from pathlib import Path
import bpy
import numpy as np


def snapshot(path,all_meshes=False):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));bpy.context.view_layer.update()
    parts={};pivots={}
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH' and (all_meshes or ob.get('part_category') in ['interior','underbody','tires','wheels','brakes','mechanisms','doors']):
            nm=ob.matrix_world.to_3x3().inverted().transposed()
            parts[ob.name]=dict(points=np.asarray([tuple(ob.matrix_world@v.co) for v in ob.data.vertices]),faces=[tuple(f.vertices) for f in ob.data.polygons],normals=np.asarray([tuple((nm@n.vector).normalized()) for n in ob.data.corner_normals]))
        if 'pivot_axis' in ob:
            pivots[ob.name]=dict(matrix=[list(row) for row in ob.matrix_world],axis=ob['pivot_axis'],range=list(ob['range_degrees']))
    return parts,pivots


def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--all-meshes',action='store_true');p.add_argument('--allow-part',action='append',default=[])
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);before,source=Path(a.before),Path(a.source)
    old,pivots=snapshot(before,a.all_meshes);new,current=snapshot(source,a.all_meshes);rows={};errors=[];allowed=[]
    def permitted(name):return any(fnmatch.fnmatchcase(name,pattern) for pattern in a.allow_part)
    for name,r in old.items():
        q=new.get(name);same=q is not None and r['points'].shape==q['points'].shape
        error=float(np.max(np.abs(q['points']-r['points']))) if same else None
        topology=same and q['faces']==r['faces']
        normal_error=float(np.max(np.abs(q['normals']-r['normals']))) if topology else None
        rows[name]=dict(maximum_coordinate_delta_m=error,topology_identical=topology,maximum_normal_component_delta=normal_error)
        if error is None or error>1e-7 or not topology or a.all_meshes and normal_error>1e-6:
            (allowed if permitted(name) else errors).append(name)
    added=sorted(set(new)-set(old))
    for name in added:
        (allowed if permitted(name) else errors).append(name)
    if current!=pivots:errors.append('Pivot transforms, axes or ranges changed')
    report=dict(passed=not errors,errors=errors,accepted_parts=len(rows)-len([n for n in allowed if n in old]),accepted_pivots=len(pivots),pivots_identical=current==pivots,parts=rows,allowed_changed_parts=allowed,added_parts=added,allowed_patterns=a.allow_part,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),before_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),scope='Actual world vertices, polygon connectivity and pivot contracts; explicitly listed repairs excluded from exact equality; appearance and articulation are separate checks')
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2));print('SUV_PRESERVATION',report['passed'],len(rows),'parts',errors)
    if errors:raise AssertionError(errors)


if __name__=='__main__':main()
