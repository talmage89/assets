"""Measure actual painted occlusion across the grille mouth, beyond its center."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import convex_hull_2d

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    blank=bpy.data.objects['Low wide grille opening'];raw=list(blank['well_mouth_samples'])
    mouth=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];flat=[Vector((v.x,v.z)) for v in mouth]
    polygon=[flat[i] for i in convex_hull_2d(flat)]
    if sum(a.x*b.y-b.x*a.y for a,b in zip(polygon,polygon[1:]+polygon[:1]))<0:polygon.reverse()
    points=[];triangles=[];names=[]
    for ob in bpy.context.scene.objects:
        roles=ob.data.attributes.get('sheet_role') if ob.type=='MESH' else None
        if roles is None or ob.get('part_category') not in ['body','doors','fascia','pillars']:continue
        start=len(points);points.extend(ob.matrix_world@v.co for v in ob.data.vertices);ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            if roles.data[tri.polygon_index].value!=0:continue
            triangles.append(tuple(start+i for i in tri.vertices));names.append((ob.name,tri.index))
    tree=BVHTree.FromPolygons(points,triangles,all_triangles=True);hits=[];samples=0
    lo=[min(v[k] for v in polygon) for k in range(2)];hi=[max(v[k] for v in polygon) for k in range(2)]
    step=.005;margin=.008;limit=max(v.y for v in mouth)+blank['well_depth_m']+.010
    def inside(q):
        return all((b.x-a.x)*(q.y-a.y)-(b.y-a.y)*(q.x-a.x)>margin*(b-a).length for a,b in zip(polygon,polygon[1:]+polygon[:1]))
    for i in range(int((hi[0]-lo[0])/step)+1):
        for j in range(int((hi[1]-lo[1])/step)+1):
            q=Vector((lo[0]+(i+.5)*step,lo[1]+(j+.5)*step))
            if not inside(q):continue
            samples+=1;hit,_,fi,_=tree.ray_cast(Vector((q.x,-4,q.y)),Vector((0,1,0)),6)
            if hit is not None and hit.y<limit:hits.append(dict(part=names[fi][0],triangle=names[fi][1],point_m=list(hit)))
    report=dict(passed=not hits and samples>1000,method='5 mm grid of rays through the actual mouth polygon, inset 8 mm from its measured rim; exterior paint only, through the recessed well depth plus 10 mm',samples=samples,paint_occlusions=len(hits),occlusions=hits,scope='Physical aperture correctness on the source, not export serialization')
    Path(a.out).write_text(json.dumps(report,indent=2));print('S240_GRILLE_APERTURE',samples,'rays,',len(hits),'paint occlusions')
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
