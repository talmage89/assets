"""Triangle intersections of new open-backed liners with every closure pose.

The general solid-motion check handles closed channels. These liners have no
hidden rear face and no solid parity, so test their actual surface crossings
separately at the same 2-degree angular samples. Intended static mounting on
body/rail surfaces is outside this moving-closure check.
"""
import argparse,hashlib,json,math,runpy,sys
from pathlib import Path
import bpy
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.motion import owned,surface
from sedan_surface_check import intersects


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    source=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    liners=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('allow_boundary') and o.name.startswith(('S240 inner aperture liner','S240 inner rear roof rail','S240 optical back','S240 optical housing'))]
    liner_names={o.name for o in liners};rows=[];violations=[];recorded=set()
    policy=runpy.run_path(str(Path(__file__).with_name('sedan_detail_config.py')))
    for motion in policy['MOTIONS']:
        root=bpy.data.objects[motion['node']];rest=root.matrix_basis.copy()
        members=[o for o in bpy.context.scene.objects if o.type=='MESH' and owned(o,root)]
        fixed={ob.name:surface(ob) for ob in bpy.context.scene.objects if ob.type=='MESH' and not owned(ob,root)}
        moving_liners={o.name for o in liners if owned(o,root)}
        lo,hi=motion['range'];poses=list(range(int(lo),int(hi)+1,int(motion['step'])));pairs=0;crossings=0
        for angle in poses:
            root.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,motion['axis']);bpy.context.view_layer.update()
            for member in members:
                moving=surface(member)
                for name,stationary in fixed.items():
                    if member.name not in moving_liners and name not in liner_names:continue
                    if any(moving['hi'][k]<stationary['lo'][k] or moving['lo'][k]>stationary['hi'][k] for k in range(3)):continue
                    for i,j in moving['tree'].overlap(stationary['tree']):
                        pairs+=1
                        if intersects([moving['points'][k] for k in moving['faces'][i]],[stationary['points'][k] for k in stationary['faces'][j]]):
                            crossings+=1
                            key=(root.name,angle,member.name,name)
                            if key not in recorded:
                                recorded.add(key);violations.append(dict(node=root.name,angle_degrees=angle,moving=member.name,fixed=name))
        root.matrix_basis=rest;bpy.context.view_layer.update()
        rows.append(dict(node=root.name,poses=poses,bvh_candidates=pairs,actual_triangle_crossings=crossings))
        print('RETURN_SWEEP',root.name,len(poses),crossings,flush=True)
    report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),method=__doc__.strip(),liners=len(liners),motions=rows,violations=violations,passed=not any(r['actual_triangle_crossings'] for r in rows))
    Path(a.out).write_text(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit('Liner crosses a moving closure: '+a.out)
if __name__=='__main__':main()
