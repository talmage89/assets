"""Capture actual imported triangles, names and UVs for whole-part image masks."""
import sys
from pathlib import Path
import bpy,numpy as np
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/imported-parts.blend'))
arm=bpy.data.objects['R39Armature'];W.pose(arm,'Idle',0)
xyz=[];uv=[];ids=[];names=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or not ob.get('asset_set'):continue
 if min(abs(v) for v in arm.pose.bones[ob['bone']].matrix.to_scale())<.001:continue
 names.append(ob['part_name']);evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());data=evaluated.data
 data.calc_loop_triangles();layer=data.uv_layers.active
 for tri in data.loop_triangles:
  xyz.append([tuple(evaluated.matrix_world@data.vertices[i].co) for i in tri.vertices])
  uv.append([tuple(layer.data[i].uv) for i in tri.loops]);ids.append(len(names))
np.savez_compressed(BASE/'build/value-geometry.npz',xyz=np.asarray(xyz),uv=np.asarray(uv),ids=np.asarray(ids),names=np.asarray(names))
print('VALUE GEOMETRY',len(xyz),'actual imported triangles')

# The standalone is a fresh import with the same embedded atlas. Segment its
# inert case/jacket exterior by the visible exterior station, not its color.
from kit.weapon_verify import import_glb
import_glb(BASE/'export/cartridge.glb')
xyz=[];uv=[];ids=[]
for ob in [o for o in bpy.context.scene.objects if o.type=='MESH']:
 ob.data.calc_loop_triangles();layer=ob.data.uv_layers.active
 for tri in ob.data.loop_triangles:
  points=[tuple(ob.matrix_world@ob.data.vertices[i].co) for i in tri.vertices]
  xyz.append(points);uv.append([tuple(layer.data[i].uv) for i in tri.loops]);ids.append(2 if sum(p[1] for p in points)/3>.0386 else 1)
np.savez_compressed(BASE/'build/value-cartridge.npz',xyz=np.asarray(xyz),uv=np.asarray(uv),ids=np.asarray(ids),names=np.asarray(['Cartridge_Case','Cartridge_Jacket']))
