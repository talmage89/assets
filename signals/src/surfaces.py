"""Shared baked trims. Assign before component consolidation so local causes
stay attached to their construction. Repeated trim UVs are intentional.
"""
from pathlib import Path
import math
import bpy
from mathutils import Vector
from kit.tiling import material
from textures import ROLES
ATLAS=None
LIT_STRENGTH=6.0

def setup():
 global ATLAS
 from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
 get_settings_group()
 ATLAS=material('Signals',Path('textures/ship'));ATLAS.name='Signals_Atlas'
 for node in ATLAS.node_tree.nodes:
  if node.type=='NORMAL_MAP':node.inputs['Strength'].default_value=.15
 # Visors are a gauge sheet with turned front hem. Interior uses black trim.
 ATLAS.use_backface_culling=False
 return ATLAS

def tile(role,u,v):
 i=ROLES.index(role);row,col=divmod(i,4)
 return ((col+.018+.964*u)/4,(row+.035+.93*v)/8)

def assign(o):
 if o.type!='MESH' or not ATLAS:return
 if o.data.uv_layers.active:o.data.uv_layers.active.name='UVMap'
 original=list(o.data.materials)
 if not original:return
 # Preserve swappable states and names; each obtains the same family image set.
 if any(m and (m.name.startswith('SharedLens') or m.name.startswith('SharedNames') or m.name.startswith('IlluminatedName')) for m in original):return
 uv=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap')
 pts=[v.co for v in o.data.vertices];lo=Vector(tuple(min(p[k] for p in pts) for k in range(3)));hi=Vector(tuple(max(p[k] for p in pts) for k in range(3)));size=hi-lo
 for f in o.data.polygons:
  ma=original[f.material_index];role=ma.get('trim_role',ma.name.replace('Form_',''))
  if role not in ROLES:role='white' if 'emiss' in ma.name.lower() else 'steel'
  n=f.normal;axes=(0,2) if abs(n.y)>=abs(n.x) else (1,2)
  if abs(n.z)>.65:axes=(0,1)
  name=o.name
  if name.startswith(('Anchor nut','Jam nut','Leveling nut','Anchor rod','Plate washer','Base plate')):role='rust' if role=='steel' else 'zinc_base'
  if name.startswith('Round concrete'):role='concrete_form'
  if name.startswith('Folded aluminum door'):role='cabinet_lower'
  if name.startswith(('Inspection sticker','APS service sticker')):role='sticker'
  if name.startswith('Accessible button'):role='button_worn'
  # Upward faces at real bird-perching surfaces; only the top side is marked.
  if n.z>.60 and name.startswith(('Cambered tapered','Compound cast','Pedestrian hood roof')):
   if role+'_top' in ROLES:role+='_top'
  for li in f.loop_indices:
   p=o.data.vertices[o.data.loops[li].vertex_index].co
   q=[max(0,min(1,(p[k]-lo[k])/max(size[k],1e-7))) for k in axes]
   if role=='panel':
    unit=0 if name.startswith('Controller generated') else 2 if name.startswith('Detector cards') else 3 if name.startswith('Power panel') else 1
    q=[(unit%2+q[0])/2,(1-unit//2+q[1])/2]
   if name.startswith('Maintenance record'):q[0]=1-q[0]
   if name.startswith('Tapered shaft') and abs(n.z)<.5:
    q=[(math.atan2(p.y,p.x)/math.tau+1)%1,(p.z-lo.z)/max(size.z,1e-7)]
    # Keep each facet on its own side of the cylindrical wrap seam.
    angles=[(math.atan2(o.data.vertices[o.data.loops[j].vertex_index].co.y,o.data.vertices[o.data.loops[j].vertex_index].co.x)/math.tau+1)%1 for j in f.loop_indices]
    if max(angles)-min(angles)>.5 and q[0]<.5:q[0]=1
   uv.data[li].uv=tile(role,*q)
 o.data.materials.clear();o.data.materials.append(ATLAS)
 for f in o.data.polygons:f.material_index=0

def lenses(graphics):
 folder=Path('textures/ship');mats=[]
 for lit in (False,True):
  m=bpy.data.materials.new('SharedLens_'+('Lit' if lit else 'Off'));m.use_nodes=True;m.use_backface_culling=False
  ns=m.node_tree.nodes;ls=m.node_tree.links;p=ns.get('Principled BSDF')
  em=ns.new('ShaderNodeTexImage');em.image=bpy.data.images.load(str((folder/'T_Signals_Emissive.png').resolve()),check_existing=True)
  mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;factor=.0007 if lit else .012;mix.inputs[2].default_value=(factor,factor,factor,1);ls.new(em.outputs['Color'],mix.inputs[1]);ls.new(mix.outputs[0],p.inputs['Base Color']);ls.new(em.outputs['Alpha'],p.inputs['Alpha']);m.surface_render_method='DITHERED'
  if lit:ls.new(em.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=LIT_STRENGTH
  p.inputs['Roughness'].default_value=.18
  mats.append(m)
 return mats

def lens_uv(o):
 if o.get('signal_lens'):o.data.uv_layers.active.name='UVMap'
