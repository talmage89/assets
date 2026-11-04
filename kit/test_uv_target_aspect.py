"""Non-square source images must not squash a reserved delivery UV region."""
import sys,json
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import model,materials,finalize
out=ROOT/'build/uv-target-aspect';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
n=materials.Nodes('UV aspect source');mat=n.finish((.1,.08,.05),.8,0)
image=bpy.data.images.new('Tall procedural source',width=128,height=512)
texture=mat.node_tree.nodes.new('ShaderNodeTexImage');texture.image=image;texture.name='Preserve this source';mat.node_tree.nodes.active=texture
ob=model.box('Cube',(0,0,.5),(1,1,1),mat,0);ob['asset_set']='Aspect'
for edge in ob.data.edges:edge.use_seam=True
bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
cfg=out/'config.py';cfg.write_text("UV_ATLAS_RECT=(.02,.52,.98,.98)\nUV_USE_TARGET_ASPECT=True\nUV_UNWRAP_METHOD='ANGLE_BASED'\nUV_NORMALIZE_ISLAND_SCALE=True\n")
sys.argv=['blender','--','--source',str(out/'source.blend'),'--out',str(out/'final.blend'),'--report',str(out/'uv.json'),'--config',str(cfg),'--size','512','--target-density','1000']
finalize.main()
ob=bpy.data.objects['Cube'];m=ob.data;m.calc_loop_triangles();uv=m.uv_layers['BakeUV'];ratios=[]
for tri in m.loop_triangles:
    p=np.array([m.vertices[i].co[:] for i in tri.vertices]);q=np.array([uv.data[i].uv[:] for i in tri.loops])
    e=p[1]-p[0];f=p[2]-p[0];ex=e/np.linalg.norm(e);ey=f-ex*np.dot(f,ex);ey/=np.linalg.norm(ey)
    j=(q[1:]-q[0]).T@np.linalg.inv(np.array([[e@ex,f@ex],[e@ey,f@ey]]));s=np.linalg.svd(j,compute_uv=False);ratios.append(s[0]/s[1])
assert max(ratios)<1.03,ratios
restored=ob.data.materials[0].node_tree.nodes['Preserve this source'].image
assert restored.name=='Tall procedural source' and list(restored.size)==[128,512]
assert not any(i.name.startswith('UV target region aspect') for i in bpy.data.images)
assert json.loads((out/'uv.json').read_text())['overlap_pairs']==0
print('PASS: reserved non-square target is isotropic; original tall image restored; no UV overlaps. Worst anisotropy',max(ratios))

# Smart UV uses the same image-aspect machinery during averaging and packing.
# A rectangular print must retain its physical metric in a square atlas.
bpy.ops.wm.read_factory_settings(use_empty=True)
n=materials.Nodes('Printed source');mat=n.finish((.2,.2,.2),.5,0)
image=bpy.data.images.new('Wide original print',width=512,height=128)
texture=mat.node_tree.nodes.new('ShaderNodeTexImage');texture.image=image
texture.name='Preserve original print';mat.node_tree.nodes.active=texture
ob=model.plane_uv('Print',[(0,0,0),(.12,0,0),(.12,0,.03),(0,0,.03)],mat);ob['asset_set']='Aspect'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'print-source.blend'))
cfg.write_text('UV_USE_TARGET_ASPECT=True\nUV_NORMALIZE_ISLAND_SCALE=True\n')
sys.argv=['blender','--','--source',str(out/'print-source.blend'),'--out',str(out/'print-final.blend'),'--report',str(out/'print-uv.json'),'--config',str(cfg),'--size','512','--target-density','10000']
finalize.main()
ob=bpy.data.objects['Print'];m=ob.data;m.calc_loop_triangles();layer=m.uv_layers['BakeUV'];ratios=[]
for tri in m.loop_triangles:
    p=np.array([[m.vertices[i].co.x,m.vertices[i].co.z] for i in tri.vertices])
    q=np.array([layer.data[i].uv[:] for i in tri.loops])
    s=np.linalg.svd((q[1:]-q[0]).T@np.linalg.inv((p[1:]-p[0]).T),compute_uv=False)
    ratios.append(s[0]/s[1])
assert max(ratios)<1.001,ratios
assert list(m.materials[0].node_tree.nodes['Preserve original print'].image.size)==[512,128]
assert not any(i.name.startswith('UV target region aspect') for i in bpy.data.images)
print('PASS: square Smart UV atlas preserves physical print axes and restores its original artwork.',max(ratios))
