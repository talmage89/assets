"""Independent facet, normal-continuity and back-containment measurements.

The delivery mode uses freshly imported GLB triangles/normals. Source geometry
supplies part names and face roles only, never replacement delivery surfaces.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_ray_tri
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from sedan_surface_proof import CATEGORIES,delivery_parts


def intersects(a,c):
    for source,dest in [(a,c),(c,a)]:
        for p,q in zip(source,source[1:]+source[:1]):
            d=q-p;length=d.length
            if length<1e-12:continue
            h=intersect_ray_tri(*dest,d/length,p,True)
            if h is not None and 1e-8<(h-p).length<length-1e-8:return True
    return False


def measure(ob):
    me=ob.data;me.calc_loop_triangles();matrix=ob.matrix_world;nm=matrix.to_3x3().inverted().transposed()
    ps=[matrix@v.co for v in me.vertices];roles=me.attributes.get('sheet_role');outside=[];inside=[];dots=[];negative=[];by_point={}
    for tri in me.loop_triangles:
        role=roles.data[tri.polygon_index].value if roles else 0
        if role==1:inside.append(tuple(tri.vertices))
        if role!=0:continue
        ids=tuple(tri.vertices);outside.append(ids);a,c,d=[ps[i] for i in ids];cross=(c-a).cross(d-a);area=cross.length*.5
        if area<1e-12:continue
        exact=me.attributes.get('DeliveryNormal')
        ns=[(nm@(exact.data[i].vector if exact else me.corner_normals[i].vector)).normalized() for i in tri.loops]
        dot=cross.normalized().dot(sum(ns,Vector()).normalized());dots.append(dot)
        if dot<0:negative.append(dict(area_m2=area,dot=dot,center_m=list((a+c+d)/3)))
        for i,n in zip(ids,ns):by_point.setdefault(tuple(round(v,7) for v in ps[i]),[]).append(n)
    continuous=ob.get('part_category') in ['body','doors','fascia','pillars','glass'] or ob.name.startswith(('Headlamp opening','Taillamp opening'))
    jump=0.
    if continuous:
        for ns in by_point.values():
            for n in ns[1:]:jump=max(jump,float((n-ns[0]).length))
    row=dict(triangles=len(me.loop_triangles),outside_triangles=len(outside),
        geometric_to_corner_normal_dot_percentiles=np.percentile(dots,[0,1,50,99,100]).tolist() if dots else [],
        reversed_facets=len(negative),reversed_area_m2=sum(x['area_m2'] for x in negative),
        significant_reversed_area_m2=sum(x['area_m2'] for x in negative if x['area_m2']>=1e-8),
        reversed_examples=negative[:8],maximum_shared_corner_normal_difference=jump)
    if inside and outside and ob.get('part_category') in ['body','doors','fascia']:
        tree=BVHTree.FromPolygons(ps,outside,all_triangles=True);back=BVHTree.FromPolygons(ps,inside,all_triangles=True)
        crossing=[];minimum=1.
        for oi,bi in tree.overlap(back):
            if intersects([ps[i] for i in outside[oi]],[ps[i] for i in inside[bi]]):crossing.append((oi,bi))
        for ids in inside:
            q=[ps[i] for i in ids]
            for p in q+[sum(q,Vector())/3]+[(a+c)/2 for a,c in zip(q,q[1:]+q[:1])]:
                hit,n,_,_=tree.find_nearest(p);minimum=min(minimum,-(p-hit).dot(n))
        row['back']=dict(triangles=len(inside),minimum_sampled_depth_m=minimum,exact_triangle_crossings=len(crossing),crossing_examples=crossing[:8])
    row['passed']=(not continuous or (row['significant_reversed_area_m2']==0 and jump<1e-3)) and ('back' not in row or (row['back']['exact_triangle_crossings']==0 and row['back']['minimum_sampled_depth_m']>=-1e-6))
    return row


def grille_measure(obs):
    """Measure mirror pairs on the actual vanes, including imported delivery."""
    from mathutils.kdtree import KDTree
    vanes={int(o.name.rsplit(' ',1)[-1]):o for o in obs if 'Low wide grille opening cascade vane ' in o.name}
    if len(vanes)!=17:raise ValueError('Missing manufactured grille vanes')
    pairs=[]
    for index in range(9):
        a,b=vanes[index],vanes[16-index]
        target=[b.matrix_world@v.co for v in b.data.vertices];tree=KDTree(len(target))
        for i,p in enumerate(target):tree.insert(p,i)
        tree.balance();errors=[]
        for v in a.data.vertices:
            p=a.matrix_world@v.co;p.x=-p.x;errors.append(tree.find(p)[2])
        pairs.append(dict(vanes=[a.name,b.name],maximum_mirrored_vertex_error_m=max(errors)))
    return dict(passed=max(r['maximum_mirrored_vertex_error_m'] for r in pairs)<1e-5,
        pairs=pairs,scope='Actual vane vertices reflected across the vehicle center plane; no authored die constants substituted for measurements')


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--glb');p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    triangle=[Vector(p) for p in [(0,0,0),(1,0,0),(0,1,0)]]
    assert intersects(triangle,[Vector(p) for p in [(.2,.2,-.1),(.8,.2,.1),(.2,.8,-.1)]])
    assert not intersects(triangle,[p-Vector((0,0,.1)) for p in triangle])
    if a.glb:obs,correspondence=delivery_parts(Path(a.source).resolve(),Path(a.glb).resolve())
    else:
        bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));correspondence=None
        obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_category') in CATEGORIES]
    rows={o.name:measure(o) for o in obs};failed=[name for name,row in rows.items() if not row['passed']]
    grille=grille_measure(obs)
    if not grille['passed']:failed.append('Grille mirror curvature')
    report=dict(passed=not failed,failed_parts=failed,parts=rows,delivery_correspondence=correspondence,
        grille_curvature=grille,
        source_sha256=hashlib.sha256(Path(a.source).read_bytes()).hexdigest(),glb_sha256=hashlib.sha256(Path(a.glb).read_bytes()).hexdigest() if a.glb else None,
        scope='Actual triangle winding versus exported corner normals, normal continuity at shared positions, and exact back/outer triangle crossings; source and delivery checked independently',
        numerical_sliver_area_m2=1e-8,shared_normal_difference_tolerance=1e-3)
    Path(a.out).write_text(json.dumps(report,indent=2));print('S240_SURFACE_CHECK',len(rows),'parts; failures:',failed)
    if failed:raise SystemExit(1)
if __name__=='__main__':main()
