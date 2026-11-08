"""Car-family face/corner and exact optical-intersection audit for the bus."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE),str(ROOT),str(ROOT/'cars/src')]
from sedan_front_check import measure
from sedan_surface_check import intersects

def triangles(ob):
    ob.data.calc_loop_triangles()
    return [ob.matrix_world@v.co for v in ob.data.vertices],[tuple(t.vertices) for t in ob.data.loop_triangles]

def optical_seating(covers):
    """Measure cover setback against the independent, un-routed dense mold."""
    mold=bpy.data.objects.get('Dense front mold')
    if mold is None:return None
    ps,fs=triangles(mold);body=BVHTree.FromPolygons(ps,fs,all_triangles=True)
    rows={}
    for cover in covers:
        ps,fs=triangles(cover);glass=BVHTree.FromPolygons(ps,fs,all_triangles=True)
        center=sum(p.x for p in ps)/len(ps);height=sum(p.z for p in ps)/len(ps);samples=[]
        for dx in [-.12,0,.12]:
            start=Vector((center+dx,-6.5,height));direction=Vector((0,1,0))
            a=body.ray_cast(start,direction,1)[0];c=glass.ray_cast(start,direction,1)[0]
            samples.append(dict(x_m=center+dx,z_m=height,
                uncut_mold_hit_m=list(a) if a is not None else None,
                cover_hit_m=list(c) if c is not None else None,
                setback_m=c.y-a.y if a is not None and c is not None else None))
        rows[cover.name]=samples
    return dict(samples=rows,scope='Actual front rays on independently generated uncut dense mold and finite game cover; positive Y difference is recessed. Does not substitute for visual judging of the molded surround.')

def imported_parts(source,delivery):
    # The unchanged car helper supplies exact imported triangles and normals.
    # Its sedan-specific name filter is adapted in an ignored source copy;
    # neither the real bus source nor any accepted car file is changed.
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!='SchoolBus':continue
        ob['asset_set']='Sedan'
        ob['part_category']={'shell':'fascia','chassis':'underbody'}.get(ob['part_category'],ob['part_category'])
    temporary=source.parent/'front-attribution.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(temporary.resolve()))
    from sedan_surface_proof import delivery_parts
    return delivery_parts(temporary.resolve(),delivery.resolve())

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--delivery')
    p.add_argument('--out',required=True);p.add_argument('--diagnose',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source)
    if a.delivery:obs,correspondence=imported_parts(source,Path(a.delivery))
    else:
        bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
        obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')=='SchoolBus']
        correspondence=None
    selected=[o for o in obs if o.name=='Compound hood shell' or o.name.startswith(('Headlamp','Glass sealed headlamp','Bonded headlamp','Lamp front lowbeam','Grille','Recessed grille','Seated grille'))]
    rows={o.name:measure(o) for o in selected};errors=[n for n,r in rows.items() if not r['passed']]
    hood=next(o for o in selected if o.name=='Compound hood shell')
    points,faces=triangles(hood);tree=BVHTree.FromPolygons(points,faces,all_triangles=True)
    roof_probes=[]
    for sign in [-1,1]:
        for x in [1.045,1.055,1.065,1.075]:
            for y in [-5.815,-5.805,-5.795]:
                hit=tree.ray_cast(Vector((sign*x,y,3)),Vector((0,0,-1)))[0]
                roof_probes.append(dict(xy_m=[sign*x,y],actual_hood_hit_m=list(hit) if hit is not None else None))
    if any(r['actual_hood_hit_m'] is None for r in roof_probes):errors.append('Open fender roof behind optical pocket')
    crossing={}
    for cover in [o for o in selected if o.name.startswith('Glass sealed headlamp')]:
        points,faces=triangles(cover);roles=cover.data.attributes.get('sheet_role')
        outer=[tuple(t.vertices) for t in cover.data.loop_triangles if roles is None or roles.data[t.polygon_index].value==0]
        tree=BVHTree.FromPolygons(points,outer,all_triangles=True);hits={}
        for ob in selected:
            if ob==cover or ob.name.startswith(('Glass','Bonded')):continue
            if ob.name!='Compound hood shell' and not ob.name.startswith(('Headlamp','Lamp front')):continue
            qs,fs=triangles(ob);other=BVHTree.FromPolygons(qs,fs,all_triangles=True)
            count=sum(intersects([points[i] for i in outer[x]],[qs[i] for i in fs[y]]) for x,y in tree.overlap(other))
            if count:hits[ob.name]=count
        crossing[cover.name]=hits
        if hits:errors.append(cover.name+' optical/body crossings')
    result=dict(passed=not errors,errors=errors,parts=rows,lens_crossings=crossing,
                optical_seating=optical_seating([o for o in selected if o.name.startswith('Glass sealed headlamp')]) if not a.delivery else None,
                optical_rear_roof_probes=roof_probes,
                stage='fresh imported glTF triangles' if a.delivery else 'source construction',
                correspondence=correspondence,source=str(source),delivery=a.delivery,
                scope='Unchanged car all-face/corner/area audit and exact triangle intersections; gasket mounting contact excluded')
    Path(a.out).write_text(json.dumps(result,indent=2));print('BUS_FRONT_CHECK',result['stage'],errors,crossing,flush=True)
    if errors and not a.diagnose:raise SystemExit(1)
if __name__=='__main__':main()
