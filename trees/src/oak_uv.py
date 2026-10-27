"""Oak union seams: triangulate, find internal folds, isolate affected patches.

Only UV seams change. The shared finalizer still owns density, packing and
independent overlap validation. Source/game vertices and triangles are retained.
"""
import argparse,sys,json
from pathlib import Path
import bpy,bmesh
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit import uv
p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--out');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
ob=bpy.data.objects['Trunk and branches'];bm=bmesh.new();bm.from_mesh(ob.data)
bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
for f in bm.faces:
    if f.calc_area()<1e-5:
        for e in f.edges:e.seam=True
bm.to_mesh(ob.data);bm.free()
me=ob.data;layer=me.uv_layers.get('BakeUV') or me.uv_layers.new(name='BakeUV');me.uv_layers.active=layer
bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
edge_lookup={tuple(sorted(e.vertices)):e for e in me.edges}
# Match the finalizer's delivery aspect during the diagnostic unwrap too.
# Different source-image aspect can change the tiny union-patch solution.
aspect=bpy.data.images.new('Oak seam diagnostic aspect',width=2048,height=1003)
restore=[];helpers=[]
for mat in me.materials:
    if not mat or not mat.use_nodes:continue
    nt=mat.node_tree;active=nt.nodes.active
    for node in nt.nodes:
        if node.type=='TEX_IMAGE':restore.append((node,node.image));node.image=aspect
    helper=nt.nodes.new('ShaderNodeTexImage');helper.image=aspect;nt.nodes.active=helper;helpers.append((nt,helper,active))
passes=[]
for iteration in range(8):
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.unwrap(method='ANGLE_BASED',margin=0);bpy.ops.object.mode_set(mode='OBJECT')
    me=ob.data;layer=me.uv_layers['BakeUV']
    edge_lookup={tuple(sorted(e.vertices)):e for e in me.edges}
    # Authored seams define the provisional islands. Equal canonical UVs on
    # separate tiny triangles must not accidentally stitch them for this probe.
    parents=list(range(len(me.polygons)));edge_faces={}
    def find(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    for f in me.polygons:
        for key in f.edge_keys:
            key=tuple(sorted(key))
            if edge_lookup[key].use_seam:continue
            if key in edge_faces:parents[find(f.index)]=find(edge_faces[key])
            else:edge_faces[key]=f.index
    faces={}
    for f in me.polygons:faces.setdefault(find(f.index),[]).append(f)
    bad=set();pair_count=0
    for group in faces.values():
        tris=[(f,[tuple(layer.data[i].uv) for i in f.loop_indices]) for f in group]
        boxes=[(min(p[0] for p in t),max(p[0] for p in t),min(p[1] for p in t),max(p[1] for p in t)) for _,t in tris]
        order=sorted(range(len(tris)),key=lambda i:boxes[i][0])
        for ii,i in enumerate(order):
            A=boxes[i]
            for j in order[ii+1:]:
                B=boxes[j]
                if B[0]>=A[1]-1e-10:break
                if B[2]>=A[3]-1e-10 or A[2]>=B[3]-1e-10:continue
                if uv.intersection_area(tris[i][1],tris[j][1])>1e-12:
                    bad.update((tris[i][0].index,tris[j][0].index));pair_count+=1
    passes.append(dict(pass_index=iteration,internal_fold_pairs=pair_count,faces_isolated=len(bad)))
    if not bad:break
    for index in bad:
        for key in me.polygons[index].edge_keys:edge_lookup[tuple(sorted(key))].use_seam=True
else:raise RuntimeError('Oak union UV folds did not converge')
for node,original in restore:node.image=original
for nt,helper,active in helpers:nt.nodes.remove(helper);nt.nodes.active=active
bpy.data.images.remove(aspect)
priority=me.attributes['BarkUVPriority'];owners=me.attributes['GrowthOwner']
for f in me.polygons:
    if owners.data[f.index].value==0 and .75<f.center.z<2.05:priority.data[f.index].value=12.0
    # Micron-wide Boolean slivers can quantize to one UV coordinate after
    # packing. Their own isolated islands need enough precision to retain
    # nonzero area, even when the chest band takes most of the allocation.
    if f.area<1e-8:priority.data[f.index].value=max(priority.data[f.index].value,24.0)
Path(a.out).with_suffix('.json').write_text(json.dumps(dict(passed=True,seam_passes=passes,scope='Internal folds before final packing; final atlas overlap/density checked separately'),indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
