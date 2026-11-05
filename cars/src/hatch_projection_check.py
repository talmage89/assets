"""Partwise projection rays before baking; reports actual coverage and back hits."""
import argparse,json,sys,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def main():
    p=argparse.ArgumentParser();p.add_argument('--low',required=True);p.add_argument('--high',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.low).resolve()))
    low={};weights=[(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('asset_set')!='Hatch':continue
        matrix=ob.matrix_world.copy();normal=matrix.to_3x3().inverted().transposed();ob.data.calc_loop_triangles();rows=[]
        for tri in ob.data.loop_triangles:
            ps=[matrix@ob.data.vertices[i].co for i in tri.vertices];ns=[normal@ob.data.corner_normals[i].vector for i in tri.loops]
            area=(ps[1]-ps[0]).cross(ps[2]-ps[0]).length*.5
            for w in weights:
                point=sum((p*v for p,v in zip(ps,w)),Vector());n=sum((p*v for p,v in zip(ns,w)),Vector()).normalized()
                rows.append((point,n,area/len(weights)))
        low[ob.name]=rows
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.high).resolve()));results={};missing=[]
    for name,rows in low.items():
        ob=bpy.data.objects.get(name)
        if ob is None:missing.append(name);continue
        ob.data.calc_loop_triangles();points=[ob.matrix_world@v.co for v in ob.data.vertices];faces=[tuple(t.vertices) for t in ob.data.loop_triangles]
        tree=BVHTree.FromPolygons(points,faces,all_triangles=True)
        total=miss=back=0.;maximum=0.;misses=backs=0
        for point,n,area in rows:
            total+=area;hit,hn,_,distance=tree.ray_cast(point+n*.014,-n,.054)
            nearest=tree.find_nearest(point)[3];maximum=max(maximum,nearest)
            if hit is None:miss+=area;misses+=1
            elif hn.dot(n)<0:back+=area;backs+=1
        results[name]=dict(samples=len(rows),surface_m2=total,miss_samples=misses,miss_area_fraction=miss/max(total,1e-12),back_hit_samples=backs,back_hit_area_fraction=back/max(total,1e-12),nearest_distance_max_m=maximum)
    total=sum(v['surface_m2'] for v in results.values())
    report=dict(low_sha256=hashlib.sha256(Path(a.low).read_bytes()).hexdigest(),high_sha256=hashlib.sha256(Path(a.high).read_bytes()).hexdigest(),scope='Interior barycentric samples of every game triangle against its named high source, before UV rasterization; geometric normals identify back hits',cage_m=.014,ray_m=.054,missing_sources=missing,parts=results,
        miss_area_fraction=sum(v['surface_m2']*v['miss_area_fraction'] for v in results.values())/total,back_hit_area_fraction=sum(v['surface_m2']*v['back_hit_area_fraction'] for v in results.values())/total)
    Path(a.out).write_text(json.dumps(report,indent=2))
    print('PROJECTION',report['miss_area_fraction'],report['back_hit_area_fraction'],'missing',missing)
    for name,row in sorted(results.items(),key=lambda x:-(x[1]['miss_area_fraction']+x[1]['back_hit_area_fraction']))[:30]:print(name,row)
if __name__=='__main__':main()
