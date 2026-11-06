"""Measured sampled source-surface motion, separate from glTF serialization.

No surface pairs are silently skipped. Penetrations above 0.5 mm are
reported, separately from the raw/import serialization audit.
"""
import json,math,sys
from pathlib import Path
import bpy
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.motion import surface,penetration,owned

def check(path):
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));result=[]
    roots=[o for o in bpy.context.scene.objects if o.parent is None and o.name not in ('NewsRow','ShelterMissingPanel','BikeRackRow')]
    for root in roots:
        meshes=[o for o in root.children_recursive if o.type=='MESH' and o.get('solid')]
        for pivot in [o for o in root.children_recursive if 'pivot_axis' in o]:
            moving=[o for o in meshes if owned(o,pivot)];fixed=[o for o in meshes if o not in moving];rest=pivot.matrix_basis.copy();cache={o.name:surface(o) for o in fixed};samples=[];violations=[];contacts={}
            lo,hi=pivot['range_degrees'];count=max(1,math.ceil(abs(hi-lo)/10));maximum=0
            for j in range(count+1):
                angle=lo+(hi-lo)*j/count;pivot.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,pivot['pivot_axis']);bpy.context.view_layer.update();samples.append(angle)
                for ob in moving:
                    a=surface(ob)
                    for other in fixed:
                        b=cache[other.name]
                        if any(min(a['hi'][k],b['hi'][k])-max(a['lo'][k],b['lo'][k])<=.0005 for k in range(3)):continue
                        depth,cross=penetration(a,b,.0005);maximum=max(maximum,depth)
                        if depth>.0005:violations.append(dict(moving=ob.name,fixed=other.name,angle=angle,depth_m=depth,crossings=cross))
            pivot.matrix_basis=rest;bpy.context.view_layer.update()
            row=dict(root=root.name,pivot=pivot.name,axis=pivot['pivot_axis'],sampled_degrees=samples,max_penetration_m=maximum,violations=violations);result.append(row);print('MOTION',pivot.name,maximum,len(violations),flush=True)
    return dict(source=path.name,motions=result,passed=not any(r['violations'] for r in result))
if __name__=='__main__':
    paths=[Path(p) for p in sys.argv[sys.argv.index('--')+1:]];reports=[check(p) for p in paths];passed=all(r['passed'] for r in reports);Path('build/motion-check.json').write_text(json.dumps(dict(scope=__doc__,reports=reports,passed=passed),indent=2));assert passed,'Physical surface sweep failed; see build/motion-check.json'
