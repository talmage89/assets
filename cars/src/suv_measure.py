"""Actual source surfaces, plane cuts and static form measurements.

No motion, UV, bake or delivery certification. The kit audit supplies topology;
these rays/cuts independently measure the requested proportions and sections.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import suv_spec as S

def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]
def bounds(obs):
    ps=[p for ob in obs for p in points(ob)]
    lo=[min(p[k] for p in ps) for k in range(3)];hi=[max(p[k] for p in ps) for k in range(3)]
    return dict(min=lo,max=hi,size=[b-a for a,b in zip(lo,hi)])
def mesh_tree(obs):
    ps=[];fs=[]
    for ob in obs:
        offset=len(ps);ps+=points(ob);fs.extend(tuple(offset+i for i in f.vertices) for f in ob.data.polygons)
    return BVHTree.FromPolygons(ps,fs)
def plane_cut(obs,y,axis=1):
    result=[]
    for ob in obs:
        ps=points(ob);ob.data.calc_loop_triangles()
        for tri in ob.data.loop_triangles:
            hits=[];vs=[ps[i] for i in tri.vertices]
            for a,b in zip(vs,vs[1:]+vs[:1]):
                if abs(a[axis]-y)<1e-7:hits.append([a[1-axis],a.z])
                if (a[axis]-y)*(b[axis]-y)<0:
                    p=a+(b-a)*((y-a[axis])/(b[axis]-a[axis]));hits.append([p[1-axis],p.z])
            unique=[]
            for hit in hits:
                if not any(math.dist(hit,h)<1e-7 for h in unique):unique.append(hit)
            if len(unique)==2:result.append(unique)
    return result
