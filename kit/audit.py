"""Blender scene audit with explicit checkpoint versus final gates.

A look-dev pass must never be reported as final game readiness. Checks use only
asset_set-tagged meshes, excluding studio and comparison annotations.
"""
import argparse, json, math, sys, runpy, hashlib, struct
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector


def bounds(obs):
    points=[ob.matrix_world @ Vector(c) for ob in obs for c in ob.bound_box]
    lo=[min(p[k] for p in points) for k in range(3)]
    hi=[max(p[k] for p in points) for k in range(3)]
    return {'min':lo,'max':hi,'size':[b-a for a,b in zip(lo,hi)]}


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--config',required=True);p.add_argument('--out',required=True);p.add_argument('--stage',choices=['lookdev','final'],default='lookdev')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    cfg=runpy.run_path(a.config);sc=bpy.context.scene;bpy.context.view_layer.update()
    sets={};errors=[];warnings=[]
    for ob in sc.objects:
        if ob.type!='MESH' or 'asset_set' not in ob or ob.get('bake_only'):continue
        sets.setdefault(ob['asset_set'],[]).append(ob)
    report={'stage':a.stage,'source':a.source,'quality':sc.get('quality'),'sets':{},'errors':errors,'warnings':warnings}
    dg=bpy.context.evaluated_depsgraph_get()
    for aset,obs in sets.items():
        digest=hashlib.sha256()
        tris=0;bad_faces=[];invalid=[];uv_missing=[];materials=set();part_counts=[];topology=[]
        for ob in sorted(obs,key=lambda ob:ob.name):
            ev=ob.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles()
            count=len(me.loop_triangles);tris+=count;part_counts.append((count,ob.name))
            digest.update(ob.name.encode())
            for row in ob.matrix_world:
                digest.update(struct.pack('<4f',*row))
            for v in me.vertices:digest.update(struct.pack('<3f',*v.co))
            for t in me.loop_triangles:digest.update(struct.pack('<3I',*t.vertices))
            materials.update(m.name for m in me.materials if m)
            if not me.uv_layers:uv_missing.append(ob.name)
            for v in me.vertices:
                if not all(math.isfinite(x) for x in v.co):invalid.append(ob.name);break
            # Sub-micron slivers created by exact booleans are recorded, not hidden.
            tiny=sum(1 for t in me.loop_triangles if t.area<1e-12)
            if tiny:bad_faces.append((ob.name,tiny))
            if any(p.normal.length<.5 for p in me.polygons):invalid.append(ob.name+' zero normal')
            if not ob.get('allow_boundary',False):
                bm=bmesh.new();bm.from_mesh(me)
                nonmanifold=sum(1 for e in bm.edges if not e.is_manifold)
                volume=bm.calc_volume(signed=True)
                if nonmanifold or volume<=0:topology.append((ob.name,nonmanifold,volume))
                bm.free()
            ev.to_mesh_clear()
        bb=bounds(obs);spec=cfg['BOUNDS'][aset]
        if any(abs(x-y)>tol for x,y,tol in zip(bb['size'],spec['size'],spec['tolerance'])):
            errors.append(f'{aset} dimensions outside configured tolerance: {bb["size"]}')
        if topology:errors.append(f'{aset} non-manifold/inside-out solids: {topology}')
        if invalid:errors.append(f'{aset} invalid coordinates or normals: {invalid}')
        if bad_faces:errors.append(f'{aset} zero-area triangle slivers: {bad_faces}')
        is_game=sc.get('quality')=='game'
        source_budget=cfg.get('SOURCE_BUDGETS',cfg['BUDGETS'])[aset]
        if is_game and tris>source_budget:errors.append(f'{aset} source triangle budget exceeded: {tris}')
        if a.stage=='final':
            if uv_missing:errors.append(f'{aset}: missing UVs')
            if len(materials)>3:errors.append(f'{aset}: material budget exceeded')
        report['sets'][aset]={'triangles':tris,'budget':source_budget,'delivery_budget':cfg['BUDGETS'][aset],
                'budget_enforced':is_game,'geometry_sha256':digest.hexdigest(),'bounds_m':bb,'meshes':len(obs),
                'materials':sorted(materials),'missing_uv_meshes':len(uv_missing),
                'largest_parts':sorted(part_counts,reverse=True)[:12]}
    report['pivots']={ob.name:{'position_m':list(ob.matrix_world.translation),'axis':ob['pivot_axis'],
        'range_degrees':list(ob.get('range_degrees',[]))} for ob in sc.objects if 'pivot_axis' in ob}
    if not sets:errors.append('No tagged asset geometry')
    if a.stage=='lookdev':
        report['pending']=['atlas UV unwrap/pack','UV overlap and texel-density validation',
                           '4096 GPU bake / 2048 delivery textures','normal-map validation',
                           'GLB export and re-import validation','final material/texture/file budgets',
                           'studio renders of re-imported GLB']
    else:
        # This command cannot stand in for export verification. Require its separate evidence.
        report['separate_delivery_evidence']='kit/verify.py checks the exported GLB independently'
    report['passed']=not errors
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    if errors:raise RuntimeError('Scene audit failed; see '+a.out)

if __name__=='__main__':main()
