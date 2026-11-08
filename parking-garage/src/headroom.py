"""Independent imported overhead rays, including tee bottoms and diffusers."""
import math
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import numpy as np
from mathutils import Vector
from check import tree,measured_height
from plan import FLOOR


def measure(meshes,p,floors):
    hard=[o for o in meshes if o.name!='Cause-driven service history' and '__Gate__Arm' not in o.name]
    overhead=tree(hard,lambda m:not any(s in m.name.lower() for s in ('glass','groundparking')))
    xs=set(float(x) for x in np.linspace(-p['length']/2+1,p['length']/2-1,43))
    for ob in hard:
        for tri in ob.data.loop_triangles:
            if (ob.matrix_world.to_3x3()@tri.normal).z>-.5:continue
            ps=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices];cut=[]
            for a,b in zip(ps,ps[1:]+ps[:1]):
                if abs(a.y-p['flat_y'])<1e-6:cut.append(a.x)
                if (a.y-p['flat_y'])*(b.y-p['flat_y'])<0:cut.append(a.x+(b.x-a.x)*(p['flat_y']-a.y)/(b.y-a.y))
            if len(cut)>=2:
                x=(min(cut)+max(cut))/2
                if -p['length']/2+1<x<p['length']/2-1:xs.add(x)
    aisle=[]
    for lev in range(p['levels']-1):
        for x in sorted(xs):
            floor=measured_height(floors,(x,p['flat_y'],lev*FLOOR+.05))
            if floor is None:continue
            hit=overhead.ray_cast(Vector((x,p['flat_y'],floor+.18)),Vector((0,0,1)),FLOOR+1)
            if hit[0] is not None:aisle.append(hit[0].z-floor)
    van=[];samples=[]
    for row in p['paths']:
        if row['name'] not in ('Drive_Entry_to_L1','Drive_L1_to_Exit'):continue
        for a,b in zip(row['points'],row['points'][1:]):
            a,b=Vector(a),Vector(b);delta=b-a
            if delta.xy.length<1e-6:continue
            normal=Vector((-delta.y,delta.x,0)).normalized();steps=max(1,math.ceil(delta.length/.25))
            samples.extend(a.lerp(b,j/steps)+normal*offset for j in range(steps+1) for offset in (-1.2,0,1.2))
    for s in p['stalls']:
        if not s.get('van'):continue
        samples.extend(Vector((s['x']+dx,s['y']+dy,s['z'])) for dx in (-s['width']/2+.25,0,s['width']/2-.25) for dy in (-s['depth']/2+.5,0,s['depth']/2-.5))
    for point in samples:
        floor=measured_height(floors,point);assert floor is not None,('Van floor missing',list(point))
        hit=overhead.ray_cast(Vector((point.x,point.y,floor+.18)),Vector((0,0,1)),FLOOR+1)
        if hit[0] is not None:van.append(hit[0].z-floor)
    assert min(aisle)>=2.1336,(p['seed'],'aisle clearance',min(aisle))
    assert min(van)>=2.4892-.0001,(p['seed'],'van route clearance',min(van))
    return dict(aisle_samples=len(aisle),aisle_min_m=min(aisle),van_samples=len(samples),van_route_min_m=min(van),
        method='Upward rays from actual imported floor planes; regular stations and every downward face aisle section. Gate arm excluded; concrete, housings and physical diffusers included. Discrete samples, not continuous clearance certification.')


if __name__=='__main__':
    import bpy,json
    from pathlib import Path
    from check import floor_planes
    rows=[]
    for seed in (101,202):
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(f'export/form/ParkingGarageForm-{seed}.gltf').resolve()));bpy.context.view_layer.update()
        meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];p=json.loads(Path(f'build/lookdev/garage-{seed}.json').read_text())
        for ob in meshes:ob.data.calc_loop_triangles()
        row=dict(seed=seed,**measure(meshes,p,floor_planes(meshes)));rows.append(row);print('FORM HEADROOM',row,flush=True)
    Path('build/lookdev/form-headroom.json').write_text(json.dumps(rows,indent=2)+'\n')
