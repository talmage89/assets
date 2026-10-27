"""Measure actual checkpoint vertices and distances; no shipping claims."""
import argparse,json,sys,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
import pickup_spec as S

def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]
def box(obs):
    ps=[p for ob in obs for p in points(ob)]
    lo=[min(p[k] for p in ps) for k in range(3)];hi=[max(p[k] for p in ps) for k in range(3)]
    return dict(min=lo,max=hi,size=[b-a for a,b in zip(lo,hi)])
def edge_gap(a,b):
    ps=points(a);end=max(p.y for p in ps)
    selected=[p for p in ps if abs(p.y-end)<1e-6 and .62<p.z<1.30]
    bv=BVHTree.FromPolygons(points(b),[list(p.vertices) for p in b.data.polygons])
    ds=[bv.find_nearest(p)[3] for p in selected]
    return dict(samples=len(ds),min_m=min(ds),max_m=max(ds))

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve()
    bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o]
    total=0;categories={};parts={};roots={}
    for ob in obs:
        ob.data.calc_loop_triangles();n=len(ob.data.loop_triangles);total+=n;parts[ob.name]=n
        cat=ob['part_category'];categories[cat]=categories.get(cat,0)+n
        parent=ob.parent.name;roots[parent]=roots.get(parent,0)+n
    b=box(obs);pivots={n:list(bpy.data.objects[n].matrix_world.translation) for n in ['Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR']}
    wb=abs(pivots['Wheel_FL'][1]-pivots['Wheel_RL'][1]);track=abs(pivots['Wheel_FL'][0]-pivots['Wheel_FR'][0])
    tires={n:box([bpy.data.objects[n]]) for n in ['Tire_FL','Tire_FR','Tire_RL','Tire_RR']}
    gaps={side:edge_gap(bpy.data.objects['Door skin_F'+side],bpy.data.objects['Door skin_R'+side]) for side in ['L','R']}
    arch=[]
    for side in ['L','R']:
        for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            lip=bpy.data.objects['Arch return_'+end+side];tire=bpy.data.objects['Tire_'+end+side]
            z=max(p.z for p in points(lip));tz=max(p.z for p in points(tire))
            arch.append(dict(wheel=end+side,opening_top_m=z,tire_top_m=tz,vertical_gap_m=z-tz))
    floor=box([bpy.data.objects['Pickup bed floor']])
    cab=box([bpy.data.objects['Cab rear lower']]);bed=box([bpy.data.objects['Bed outer_L']])
    cab_gap=bed['min'][1]-cab['max'][1]
    report=dict(stage='body form only',source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                bounds_m=b,triangles=total,triangles_per_category=categories,triangles_per_mesh=parts,triangles_per_parent=roots,
                materials=sorted({m.name for ob in obs for m in ob.data.materials if m}),
                wheel_centers_m=pivots,wheelbase_m=wb,track_m=track,tire_bounds_m=tires,door_seam_distances=gaps,
                arch_vertical_clearances=arch,bed_floor_bounds_m=floor,cab_bed_y_gap_m=cab_gap,
                pending=['ground clearance: axle/frame not yet built','continuous rolling tire deformation','all swept-motion clearance',
                         'UV, bake, GLB and delivery budgets','paint/glass/light material delivery'])
    errors=[]
    if total>70000:errors.append('Triangle budget')
    if abs(wb-S.WHEELBASE)>1e-5 or abs(track-S.TRACK)>1e-5:errors.append('Wheelbase/track')
    if abs(b['size'][1]-S.LENGTH)>.002:errors.append('Length')
    if abs(b['size'][0]-S.WIDTH)>.008:errors.append('Body width')
    if abs(b['size'][2]-S.HEIGHT)>.002:errors.append('Height')
    for value in gaps.values():
        if value['min_m']<.004 or value['max_m']>.0051:errors.append('Door seam gap')
    for value in tires.values():
        if abs(value['min'][2])>1e-5:errors.append('Tire ground contact')
    report.update(errors=errors,passed=not errors)
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['triangles','bounds_m','wheelbase_m','track_m','door_seam_distances','cab_bed_y_gap_m','errors','passed']},indent=2))
    if errors:raise RuntimeError('Checkpoint form checks failed')
if __name__=='__main__':main()
