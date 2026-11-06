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
    optical={}
    for name in ['Headlamp opening-1','Headlamp opening1']:
        cover=bpy.data.objects[name];raw=list(cover['aperture_samples'])
        ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu,nv=cover['form_columns'],cover['form_rows']
        raw=list(cover['aperture_chart_samples']);chart=[Vector((raw[i],raw[i+1])) for i in range(0,len(raw),2)]
        raw=list(cover['optical_patch_normals']);ns=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
        areas=[];blocked=[]
        for j in range(nv-1):
            for i in range(nu-1):
                indices=[j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i]
                q=[chart[k] for k in indices]
                areas.append(sum(a.x*c.y-c.x*a.y for a,c in zip(q,q[1:]+q[:1]))*.5)
        orientation=1 if sum(areas)>0 else -1
        for j in range(1,nv-1):
            for i in range(1,nu-1):
                q=ps[j*nu+i];n=ns[j*nu+i];hit,_,fi,_=tree.ray_cast(q+n*.05,-n,.065)
                if hit is not None:blocked.append(dict(part=names[fi][0],point_m=list(hit)))
        optical[name]=dict(minimum_oriented_chart_cell_area=min(a*orientation for a in areas),
            cells=len(areas),interior_rays=(nu-2)*(nv-2),paint_occlusions=blocked,
            method='Every cover cell must preserve orientation in its construction chart; 65 mm normal rays from 50 mm outside interior cover vertices must see no painted obstruction')
    report=dict(passed=not hits and samples>1000 and all(row['minimum_oriented_chart_cell_area']>1e-8 and not row['paint_occlusions'] for row in optical.values()),method='5 mm grid of rays through the actual mouth polygon, inset 8 mm from its measured rim; exterior paint only, through the recessed well depth plus 10 mm',samples=samples,paint_occlusions=len(hits),occlusions=hits,front_cover_charts=optical,scope='Physical aperture correctness on the source, not export serialization')
    Path(a.out).write_text(json.dumps(report,indent=2));print('S240_GRILLE_APERTURE',samples,'rays,',len(hits),'paint occlusions')
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
