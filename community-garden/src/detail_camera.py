"""Fit tomato detail cameras in actual aisles of the freshly imported sites.

Opaque triangle ray tests conservatively count masked cards as solid. These
measure foreground obstruction, not photographic quality or plant density.
"""
import argparse,hashlib,itertools,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from render import bundle,views


def recipe():
    return hashlib.sha256((HERE/'detail_views.py').read_bytes()+Path(__file__).read_bytes()).hexdigest()


def prepare(seed):
    source=Path(f'export/final/Site_{seed}.gltf');plan=json.loads(Path(f'build/garden-{seed}.json').read_text())['plan']
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));bpy.context.view_layer.update()
    x,y,_=views(plan)['tomato']['target'];target_xy=Vector((x,y,0))
    roots=[o for o in bpy.context.scene.objects if o.get('kind')=='plant' and o.get('species')=='tomato']
    root=min(roots,key=lambda o:(Vector((o.matrix_world.translation.x,o.matrix_world.translation.y,0))-target_xy).length)
    pp=[o.matrix_world@v.co for o in [root,*root.children_recursive] if o.type=='MESH' for v in o.data.vertices]
    lo=Vector(tuple(min(p[i] for p in pp) for i in range(3)));hi=Vector(tuple(max(p[i] for p in pp) for i in range(3)))
    target=Vector((x,y,(lo.z+hi.z)/2));corners=[Vector(p) for p in itertools.product(*zip(lo,hi))]
    candidates=[Vector((x+r*math.cos(a),y+r*math.sin(a),1.65)) for r in (2.2,2.6,3.0,3.4,3.8,4.2) for a in [math.radians(j) for j in range(0,360,5)]]
    W,D=plan['size'];deps=bpy.context.evaluated_depsgraph_get();ranked=[]
    for camera in candidates:
        if abs(camera.x)>W/2-.12 or abs(camera.y)>D/2-.12:continue
        if any(abs(camera.x-b['center'][0])<b['width']/2+.08 and abs(camera.y-b['center'][1])<b['depth']/2+.08 for b in plan['plots']):continue
        forward=(target-camera).normalized();right=forward.cross(Vector((0,0,1))).normalized();up=right.cross(forward).normalized()
        lens=50.
        for p in corners:
            q=p-camera;depth=q.dot(forward)
            if depth<=0:lens=0;break
            lens=min(lens,16.2*depth/max(abs(q.dot(right)),1e-7),16.2*depth/max(abs(q.dot(up)),1e-7))
        if lens<26:continue
        blocked=0
        for u,z in itertools.product((-.7,-.35,0,.35,.7),(.18,.45,.72,.99,1.26)):
            aim=Vector((x,y,lo.z+min(z,hi.z-lo.z-.1)))+right*u;ray=aim-camera;distance=ray.length;direction=ray.normalized()
            entry=0.;exit_distance=distance
            for axis in range(3):
                if abs(direction[axis])<1e-8:continue
                a,b=sorted(((lo[axis]-camera[axis])/direction[axis],(hi[axis]-camera[axis])/direction[axis]));entry=max(entry,a);exit_distance=min(exit_distance,b)
            # Rays outside the target box still test a conservative foreground
            # interval; rays into it stop just before the actual canopy box.
            limit=max(.25,entry-.06) if entry<=exit_distance else max(.25,distance-1.0)
            hit,point,normal,index,ob,matrix=bpy.context.scene.ray_cast(deps,camera,direction,distance=limit)
            blocked+=bool(hit)
        direction=(camera-target).normalized();score=round(-100*blocked-direction.y*.7-abs(lens-40)*.03-abs((camera-target).length-3)*.02,5)
        ranked.append((score,camera,lens,blocked))
    assert ranked,('No aisle camera candidates',seed)
    score,camera,lens,blocked=max(ranked,key=lambda r:r[0]);assert blocked==0,('No unobstructed detail camera',seed,blocked)
    rounded=lambda p:[round(float(v),6) for v in p]
    shot=dict(location=rounded(camera),target=rounded(target),lens=round(lens,6),aspect=1.0,sky_strength=.35,exposure=.10)
    result=dict(source=str(source),bundle_sha256=bundle(source),recipe_sha256=recipe(),camera=shot,target_root=root.name,canopy_bounds_m=[rounded(lo),rounded(hi)],aisle_candidates_measured=len(ranked),foreground_rays=25,foreground_hits=blocked,scope='actual site triangles; plan footprint clearance and conservative alpha-card occlusion; no plant moves')
    print('DETAIL CAMERA',seed,shot,'foreground hits',blocked,flush=True);return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--seeds',nargs='+',type=int,default=[117,229,341]);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);Path('build/detail-cameras.json').write_text(json.dumps({str(s):prepare(s) for s in a.seeds},indent=2))

if __name__=='__main__':main()
