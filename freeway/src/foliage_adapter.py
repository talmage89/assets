"""Native tree-family thin-leaf response, reading exported baked images only.

Stock glTF MASK PBR is the fallback. Like the tree family's final renderer,
this presentation restores its documented two-sided/translucent leaf shader.
No source geometry, procedural leaf field or replacement image is loaded.
"""
import importlib.util
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]

def install():
 spec=importlib.util.spec_from_file_location('freeway_native_leaf_response',ROOT/'trees/src/leaf_material.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
 replacements={};rows=[]
 for mat in list(bpy.data.materials):
  if not mat.name.startswith(('PinOak','RedMaple')) or 'Trunk' in mat.name or not mat.use_nodes:continue
  images={c:next((n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and c in n.image.name),None) for c in ('BaseColor','Normal','ORM')}
  if not all(images.values()):continue
  kwargs=dict(name='Pin oak glossy summer foliage',specular=.18,normal_strength=.85,back_multiplier=(1.40,1.45,1.20,1),back_saturation=.78,transmission=.32) if mat.name.startswith('PinOak') else {}
  replacements[mat]=native.material(images['BaseColor'],images['Normal'],images['ORM'],**kwargs)
  rows.append(dict(imported_material=mat.name,images={k:v.name for k,v in images.items()},profile='native pin oak' if kwargs else 'native red maple'))
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  for i,mat in enumerate(ob.data.materials):
   if mat in replacements:ob.data.materials[i]=replacements[mat]
 return rows
