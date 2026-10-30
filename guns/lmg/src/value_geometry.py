"""Save posed actual imported triangles for the whole-part image audits."""
import json,sys,hashlib
from pathlib import Path
import bpy,numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W,weapon_verify as V

def capture(path,source,pose_key=None):
 xyz=[];uv=[];ids=[];names=[]
 dg=bpy.context.evaluated_depsgraph_get()
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or not ob.get('asset_set'):continue
  arm=next((o for o in bpy.context.scene.objects if o.type=='ARMATURE'),None)
  if arm and ob.get('bone') and min(abs(v) for v in arm.pose.bones[ob['bone']].matrix.to_scale())<.001:continue
  name=ob.get('part_name',ob.name);ev=ob.evaluated_get(dg);data=ev.to_mesh();data.calc_loop_triangles();layer=data.uv_layers.active
  ammunition=name.startswith('Belt_Round')
  if ammunition:
   base_y=min((ev.matrix_world@v.co).y for v in data.vertices);names.extend([name+'_Case',name+'_Jacket']);case_id=len(names)-1;jacket_id=len(names)
  else:names.append(name)
  for tri in data.loop_triangles:
   points=[tuple(ev.matrix_world@data.vertices[i].co) for i in tri.vertices]
   xyz.append(points);uv.append([tuple(layer.data[i].uv) for i in tri.loops]);ids.append((jacket_id if sum(p[1] for p in points)/3-base_y>.0445 else case_id) if ammunition else len(names))
  ev.to_mesh_clear()
 np.savez_compressed(path,xyz=np.asarray(xyz),uv=np.asarray(uv),ids=np.asarray(ids),names=np.asarray(names),sha256=np.asarray(hashlib.sha256(source.read_bytes()).hexdigest()),pose_key=np.asarray(json.dumps(pose_key,sort_keys=True)))

out=BASE/'build/image-geometry';out.mkdir(parents=True,exist_ok=True)
from delivery import split_imported
V.import_glb(BASE/'export/lmg.glb');split_imported(bpy.context.scene,BASE/'build/delivery/finalized.blend')
snapshot=BASE/'build/image-import.blend';bpy.ops.wm.save_as_mainfile(filepath=str(snapshot))
for folder in ('beauty','photos'):
 meta=BASE/'renders/final'/folder/'shots.json'
 if not meta.exists():continue
 for name,shot in json.loads(meta.read_text()).items():
  if hashlib.sha256(Path(shot['source']).read_bytes()).hexdigest()!=shot['sha256']:continue
  if name in ('scale','aimed','aimed_macro'):continue
  bpy.ops.wm.open_mainfile(filepath=str(snapshot))
  arm=bpy.data.objects['HarrowArmature'];W.pose(arm,shot.get('action','Idle'),shot.get('frame',0))
  keep={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
  for bone,(clip,f) in shot.get('layers',{}).items():
   W.pose(arm,clip,f);keep[bone]=arm.pose.bones[bone].matrix_basis.copy()
  arm.animation_data.action=None
  for b in arm.pose.bones:b.matrix_basis=keep[b.name]
  bpy.context.view_layer.update()
  if shot.get('hide_box'):
   for ob in list(bpy.context.scene.objects):
    if ob.name.startswith(('Box_','Belt_')):bpy.data.objects.remove(ob,do_unlink=True)
  if shot.get('inspection_parts'):
   for ob in list(bpy.context.scene.objects):
    if ob.type=='MESH' and not ob.get('part_name',ob.name).startswith(tuple(shot['inspection_parts'])):bpy.data.objects.remove(ob,do_unlink=True)
  capture(out/(name+'.npz'),BASE/'export/lmg.glb',{k:shot.get(k) for k in ('action','frame','layers','hide_box','inspection_parts','diagnostic_isolate')})
for name in ('cartridge','case','link'):
 V.import_glb(BASE/'export'/(name+'.glb'))
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':ob['asset_set']='LMG';ob['part_name']=name.title()
 capture(out/(name+'.npz'),BASE/'export'/(name+'.glb'))
print('CAPTURED ACTUAL IMPORTED IMAGE GEOMETRY',flush=True)
