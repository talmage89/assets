"""Configured rigid-motion sweeps, measured against evaluated solid surfaces.

BVH triangle crossings select candidate pairs. Candidate vertices and edge
intervals inside the other solid measure penetration; ray parity rejects empty
space inside concave or hollow parts. Tolerance is meters. Intended contacts are
explicit (moving-prefix, fixed-prefix) allow-list entries, with reasons in config.
This is a sampled angular/linear sweep, not a continuous collision proof.
"""
import argparse,json,math,runpy,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree


def owned(ob,node):
    while ob:
        if ob==node:return True
        ob=ob.parent
    return False


def surface(ob):
    evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
    points=[evaluated.matrix_world@v.co for v in mesh.vertices]
    faces=[tuple(t.vertices) for t in mesh.loop_triangles];evaluated.to_mesh_clear()
    lo=Vector(tuple(min(p[k] for p in points) for k in range(3)));hi=Vector(tuple(max(p[k] for p in points) for k in range(3)))
    return dict(tree=BVHTree.FromPolygons(points,faces,all_triangles=True),points=points,faces=faces,lo=lo,hi=hi)


def inside(tree,p):
    votes=0
    for vector in ((.82731,.41973,.37319),(-.31291,.87213,.37619),(.21917,-.39813,.89023)):
        direction=Vector(vector).normalized();count=0;start=p.copy()
        epsilon=1e-6*(1+max(abs(v) for v in p))
        for _ in range(128):
            hit=tree.ray_cast(start,direction)
            if hit[0] is None:break
            count+=1;start=hit[0]+direction*epsilon
        else:raise RuntimeError('Ray parity did not terminate')
        votes+=count%2
    return votes>=2


def penetration(a,b,tolerance):
    if any(min(a['hi'][k],b['hi'][k])-max(a['lo'][k],b['lo'][k])<=tolerance for k in range(3)):return 0.0,0
    pairs=a['tree'].overlap(b['tree']);depth=0.0
    def measure(point,other):
        nonlocal depth
        if any(point[k]<other['lo'][k] or point[k]>other['hi'][k] for k in range(3)):return
        nearest=other['tree'].find_nearest(point)
        if nearest[0] is not None and (point-nearest[0]).dot(nearest[1])<0 and nearest[3]>depth and inside(other['tree'],point):depth=nearest[3]
    for current,other,indices in [(a,b,{x for x,y in pairs}),(b,a,{y for x,y in pairs})]:
        if not pairs:
            # Complete containment has no boundary crossings.
            for point in current['points'][::max(1,len(current['points'])//12)]:measure(point,other)
            continue
        edges=set();vertices=set()
        for index in indices:
            triangle=current['faces'][index];vertices.update(triangle)
            edges.update(tuple(sorted((triangle[i],triangle[(i+1)%3]))) for i in range(3))
        for index in vertices:measure(current['points'][index],other)
        for u,v in edges:
            p=current['points'][u];q=current['points'][v];length=(q-p).length
            if length<1e-9:continue
            direction=(q-p)/length;distances=[0.0,length];cursor=0.0
            for _ in range(64):
                hit=other['tree'].ray_cast(p+direction*(cursor+1e-7),direction,length-cursor)
                if hit[0] is None:break
                cursor=(hit[0]-p).dot(direction)
                if cursor>=length:break
                distances.append(cursor)
            distances.sort()
            for left,right in zip(distances,distances[1:]):
                if right-left>2*tolerance:measure(p+direction*((left+right)*.5),other)
    return depth,len(pairs)


def sweep(config):
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'asset_set' in o and not o.get('allow_boundary',False)]
    result={'passed':True,'motions':[],'method':'BVH crossings + solid parity / edge interval penetration','units':'meters'}
    for spec in config.get('MOTIONS',[]):
        pivot=bpy.data.objects.get(spec['node'])
        if pivot is None:raise ValueError('Missing motion node '+spec['node'])
        rest=pivot.matrix_basis.copy();moving=[o for o in meshes if owned(o,pivot)]
        if not moving:raise ValueError('Motion node owns no tagged solid meshes: '+spec['node'])
        fixed=[o for o in meshes if o not in moving and not any(o.name.startswith(p) for p in spec.get('exclude_fixed',[]))]
        stationary={o.name:surface(o) for o in fixed}
        low,high=spec['range'];step=spec['step'];count=math.ceil(abs(high-low)/step)
        samples=[low+(high-low)*i/count for i in range(count+1)] if count else [low]
        tolerance=spec.get('tolerance_m',.0005);violations={};maximum=0.0;allowed=set()
        for value in samples:
            pivot.matrix_basis=rest
            delta=Matrix.Rotation(math.radians(value),4,spec['axis']) if spec.get('kind','rotation')=='rotation' else Matrix.Translation(Vector(tuple(value if k=='XYZ'.index(spec['axis']) else 0 for k in range(3))))
            pivot.matrix_basis=rest@delta;bpy.context.view_layer.update()
            for ob in moving:
                current=surface(ob)
                for fixed_ob in fixed:
                    contact=next((rule for rule in spec.get('allow',[]) if ob.name.startswith(rule['moving']) and fixed_ob.name.startswith(rule['fixed'])),None)
                    if contact:
                        allowed.add((contact['moving'],contact['fixed'],contact['reason']));continue
                    depth,crossings=penetration(current,stationary[fixed_ob.name],tolerance)
                    maximum=max(maximum,depth)
                    if depth>tolerance:
                        key=(ob.name,fixed_ob.name)
                        if key not in violations or depth>violations[key]['depth_m']:violations[key]=dict(moving=ob.name,fixed=fixed_ob.name,value=value,depth_m=depth,triangle_crossings=crossings)
        pivot.matrix_basis=rest;bpy.context.view_layer.update()
        row=dict(node=spec['node'],range=spec['range'],step=step,samples=len(samples),tolerance_m=tolerance,max_penetration_m=maximum,
                 allowed_contacts=[dict(moving=a,fixed=b,reason=c) for a,b,c in sorted(allowed)],violations=list(violations.values()))
        result['motions'].append(row);result['passed'] &= not bool(violations)
        print('MOTION',spec['node'],len(samples),'samples',maximum,'m',len(violations),'violations',flush=True)
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--config',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    result=sweep(runpy.run_path(a.config));Path(a.out).write_text(json.dumps(result,indent=2))
    if not result['passed']:raise RuntimeError('Motion interpenetration: see '+a.out)

if __name__=='__main__':main()
