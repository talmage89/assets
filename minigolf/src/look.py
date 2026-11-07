"""Authored UVs and physical traffic/exposure masks on the actual course skin."""
import json,math,shutil
from pathlib import Path
import bpy
from mathutils import Vector
from kit import tiling
from textures import RECTS
from plan import center

def materials():
 out=Path('export/textures');out.mkdir(parents=True,exist_ok=True)
 for ch in ('BaseColor','Normal','ORM'):shutil.copyfile(Path('textures/ship')/f'T_Minigolf_{ch}.png',out/f'T_Minigolf_{ch}.png')
 atlas=tiling.material('Minigolf',out,tint=True);states={}
 for name in ('Concrete','Asphalt','Lawn'):
  states['grass' if name=='Lawn' else name.lower()]=tiling.material(name,Path('../ground/textures/ship'),tint=True)
 states['wood']=tiling.material('WoodPrivacy',Path('../fences/textures/ship'),tint=True)
 m=atlas.copy();m.name='Minigolf_Lamp';b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Emission Strength'].default_value=6
 tex=next(n for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name);m.node_tree.links.new(tex.outputs[0],b.inputs['Emission Color']);states['lamp']=m
 for name in ('water','glass'):
  m=atlas.copy();m.name='Minigolf_'+name;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Transmission Weight'].default_value=.35 if name=='water' else .75;b.inputs['IOR'].default_value=1.333 if name=='water' else 1.5
  states[name]=m
 return atlas,states

def assign(ob,atlas,states):
 data=ob.data;old=list(data.materials);uv=data.uv_layers.active;vcol=data.color_attributes.get('Tint') or data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER')
 data.color_attributes.active_color=vcol
 owner=ob.parent;h=None
 while owner:
  if owner.get('hole_spec'):h=json.loads(owner['hole_spec']);break
  owner=owner.parent
 course=ob.parent
 while course and not course.get('course_kind'):course=course.parent
 age=.9 if course and course.get('course_kind')=='classic' else .42
 bounds=[(min(v.co[k] for v in data.vertices),max(v.co[k] for v in data.vertices)) for k in range(3)]
 assignments=[];keys=[]
 for p in data.polygons:
  key=old[p.material_index].name.removeprefix('Quick_');keys.append(key)
  assignments.append(states.get('lamp',atlas) if any(n in ob.name for n in ('Floodlight lens','Service porch light','Opal sign face')) else states.get(key,atlas))
 distinct=list(dict.fromkeys(assignments));data.materials.clear()
 for m in distinct:data.materials.append(m)
 for poly,key,material in zip(data.polygons,keys,assignments):
  poly.material_index=distinct.index(material);axes=sorted(range(3),key=lambda k:abs(poly.normal[k]))[:2];axes.sort()
  rect=RECTS[key];u0,v0,u1,v1=rect;pad=8/2048
  for li in poly.loop_indices:
   q=data.vertices[data.loops[li].vertex_index].co;world=ob.matrix_world@q
   tint=[1.,1.,1.]
   if key.startswith('carpet') and h and ob.name.startswith('Carpet playing face'):
    t=q.y/h['length']+.5;cx,_=center(h,t)
    u=.5+(q.x-cx)/3.66;v=t
    traffic=math.exp(-((q.x-cx)/.34)**2)*math.sin(math.pi*max(0,min(1,t)))**.5
    cup=math.exp(-((q.x-cx)**2+((t-.88)*h['length'])**2)/.13)
    tee=math.exp(-((q.x-cx)**2+((t-.08)*h['length'])**2)/.18)
    worn=age*min(1,traffic*.67+cup*.8+tee*.7)
    tint=[.33+.52*worn,.72+.20*worn,.48+.10*worn]
   elif key in ('concrete','asphalt','grass','wood'):
    coverage={'concrete':3.048,'asphalt':6.096,'grass':3.048,'wood':2.4}[key]
    # Reused family maps retain their meter-based repeat and real response.
    uv.data[li].uv=(world[axes[0]]/coverage,world[axes[1]]/coverage)
    if key=='wood':
     uv.data[li].uv=(q[axes[0]]/.16,q[axes[1]]/2.4)
    tint=[.83,.82,.77] if key=='concrete' else [1,1,1]
    vcol.data[li].color=(*tint,1);continue
   else:
    # Each construction part is an authored chart. Dominant-face projection
    # prevents collapse on thin vertical rails and cast faces. Atlas reuse
    # is intentional; no unique-atlas zero-overlap claim applies.
    u=(q[axes[0]]-bounds[axes[0]][0])/max(.0001,bounds[axes[0]][1]-bounds[axes[0]][0]);v=(q[axes[1]]-bounds[axes[1]][0])/max(.0001,bounds[axes[1]][1]-bounds[axes[1]][0])
    if key in ('rock','rocklight'):
     wet=math.exp(-((world.x-2)/1.3)**2-((world.y-9.5)/1.8)**2)*max(0,min(1,(2.5-world.z)/2))
     algae=wet*.65+(.35 if -.25<world.z<.14 else 0)
     tint=[1-.55*algae,1-.40*algae,1-.59*algae]
    elif key in ('red','ivory','navy','white'):
     exposure=max(0,-(ob.matrix_world.to_3x3()@poly.normal).y)*age
     tint=[1,1-exposure*.07,1-exposure*.15]
   uv.data[li].uv=(u0+pad+max(0,min(1,u))*(u1-u0-2*pad),v0+pad+max(0,min(1,v))*(v1-v0-2*pad))
   vcol.data[li].color=(*tint,1)
