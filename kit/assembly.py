"""Measure declared static supports on evaluated triangle surfaces, not nominal dimensions.

Edge ray intersections prove surface crossings; otherwise report the minimum
sampled vertex-to-triangle distance in both directions (an upper bound on the
continuous minimum). This is a physical support check, separate from GLB
serialization. Do not use it as a swept motion/collision checker.
"""
import argparse,json,sys,runpy
from pathlib import Path
import bpy
from mathutils.bvhtree import BVHTree

def surface(ob):
    dg=bpy.context.evaluated_depsgraph_get();ev=ob.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles()
    vs=[ob.matrix_world@v.co for v in me.vertices];fs=[tuple(t.vertices) for t in me.loop_triangles];es=[tuple(e.vertices) for e in me.edges]
    tree=BVHTree.FromPolygons(vs,fs,all_triangles=True);ev.to_mesh_clear();return vs,es,tree

def distance(a,b):
    av,ae,at=surface(a);bv,be,bt=surface(b)
    for vs,es,tree in [(av,ae,bt),(bv,be,at)]:
        for i,j in es:
            v=vs[j]-vs[i];length=v.length
            if length>1e-10 and tree.ray_cast(vs[i],v/length,length+1e-8)[0] is not None:return 0.0,'triangle-surface intersection'
    return min([bt.find_nearest(v)[3] for v in av]+[at.find_nearest(v)[3] for v in bv]),'sampled vertex-to-triangle upper bound'

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--config',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()));cfg=runpy.run_path(a.config);rows=[];errors=[]
    for left,right,limit in cfg['CONTACTS']:
        x=bpy.data.objects.get(left);y=bpy.data.objects.get(right)
        if x is None or y is None:errors.append('Missing contact member '+left+' / '+right);continue
        d,method=distance(x,y);rows.append(dict(parts=[left,right],distance_m=d,limit_m=limit,method=method))
        if d>limit:errors.append(f'Unsupported {left} / {right}: {d} m')
    out=dict(passed=not errors,source=a.source,scope='physical evaluated source/game surfaces; serialization checked separately',contacts=rows,errors=errors)
    Path(a.out).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
    if errors:raise RuntimeError('Assembly support checks failed')
if __name__=='__main__':main()
