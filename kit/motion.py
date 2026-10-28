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


def sweep_clips(armature, names, *, step_frames=1, tolerance_m=.0002, allow=()):
    """Sample complete authored actions on separately bound rigid source parts.

    Uses the same evaluated-solid penetration test as pivot sweeps. Same-bone
    surfaces form one manufactured assembly and are omitted; every cross-bone
    pair is checked unless an explicit prefix pair documents intended contact.
    Includes action endpoints and authored keyframes, even at fractional times.
    """
    from kit.weapon import pose, fcurves
    if step_frames<=0:raise ValueError('step_frames must be positive')
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'
            and o.parent==armature and 'bone' in o and not o.get('allow_boundary',False)]
    if not meshes:raise ValueError('No rigid weapon source parts')
    result=dict(passed=True,method='evaluated skin surfaces; BVH + solid parity / edge intervals',
                units='meters',step_frames=step_frames,tolerance_m=tolerance_m,clips=[])
    pairs=[];allowed=[]
    for i,a in enumerate(meshes):
        for b in meshes[i+1:]:
            if a['bone']==b['bone']:continue
            rule=next((r for r in allow if
                (a.name.startswith(r['a']) and b.name.startswith(r['b'])) or
                (b.name.startswith(r['a']) and a.name.startswith(r['b']))),None)
            if rule:
                allowed.append(dict(a=a.name,b=b.name,reason=rule['reason'],
                                    max_penetration_m=rule.get('max_penetration_m')))
                # Legacy exceptions remain available. New rigid assemblies can
                # bound an intentional overlap instead of removing its test.
                if 'max_penetration_m' not in rule:continue
            pairs.append((a,b,rule))
    result['allowed_contacts']=allowed;result['cross_bone_pairs']=len(pairs)
    # Long holds and identical poses in different clips need only one solid test.
    # Pair-relative bone matrices also avoid repeating an inspect's rigid Root turn.
    pair_cache={};surface_cache={};tested=0
    rest_action=armature.animation_data.action if armature.animation_data else None
    rest_frame=bpy.context.scene.frame_current
    try:
        for name in names:
            action=bpy.data.actions[name];lo,hi=map(float,action.frame_range)
            count=math.ceil((hi-lo)/step_frames)
            frames={lo,hi,*[lo+i*step_frames for i in range(count)]}
            frames.update(float(k.co.x) for fc in fcurves(action) for k in fc.keyframe_points)
            violations={};maximum=0.0
            for frame in sorted(frames):
                pose(armature,name,frame)
                matrices={b.name:b.matrix.copy() for b in armature.pose.bones}
                surfaces={}
                for o in meshes:
                    key=(o.name,tuple(round(v,9) for row in matrices[o['bone']] for v in row))
                    if key not in surface_cache:surface_cache[key]=surface(o)
                    surfaces[o.name]=surface_cache[key]
                for a,b,rule in pairs:
                    sa,sb=surfaces[a.name],surfaces[b.name]
                    limit=rule['max_penetration_m'] if rule else tolerance_m
                    measure_tolerance=min(tolerance_m,limit)
                    if any(min(sa['hi'][k],sb['hi'][k])-max(sa['lo'][k],sb['lo'][k])<=measure_tolerance for k in range(3)):continue
                    ma,mb=matrices[a['bone']],matrices[b['bone']]
                    relative=ma.inverted_safe()@mb
                    key=(a.name,b.name,tuple(round(v,8) for row in relative for v in row))
                    if key not in pair_cache:
                        pair_cache[key]=penetration(sa,sb,measure_tolerance);tested+=1
                    depth,crossings=pair_cache[key];maximum=max(maximum,depth)
                    if depth>limit:
                        key=(a.name,b.name)
                        if key not in violations or depth>violations[key]['depth_m']:
                            violations[key]=dict(a=a.name,b=b.name,frame=frame,depth_m=depth,limit_m=limit,triangle_crossings=crossings)
            row=dict(clip=name,range_frames=[lo,hi],samples=len(frames),
                     max_penetration_m=maximum,violations=list(violations.values()))
            result['clips'].append(row);result['passed'] &= not bool(violations)
            print('CLIP MOTION',name,len(frames),'samples',maximum,'m',len(violations),'violations',flush=True)
    finally:
        pose(armature,rest_action.name if rest_action else None,rest_frame)
    result['unique_solid_tests']=tested
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--config',required=True);p.add_argument('--out',required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    result=sweep(runpy.run_path(a.config));Path(a.out).write_text(json.dumps(result,indent=2))
    if not result['passed']:raise RuntimeError('Motion interpenetration: see '+a.out)

if __name__=='__main__':main()
