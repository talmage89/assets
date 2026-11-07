"""Authored UVs and physical traffic/exposure masks on the actual course skin."""
import json,math,shutil
from pathlib import Path
import bpy
from mathutils import Vector
from kit import tiling
from textures import RECTS
from plan import center
FENCE_CHARTS=None

def wet_mask(world):
 return math.exp(-((world.x-2)/1.7)**2-((world.y-9.65)/2.3)**2)*max(0,min(1,(3.0-world.z)/.8))

def fence_charts():
 global FENCE_CHARTS
 if FENCE_CHARTS is not None:return FENCE_CHARTS
 # Interior, unpainted lumber pixels in the actual 2048 atlas. The staged
 # post GLB's old charts do not match this delivery and sampled black gaps.
 # Longitudinal V follows the vertical grain of a clean board region.
 path=Path('../fences/textures/ship/T_WoodPrivacy_BaseColor.png')
 FENCE_CHARTS=dict(side=[[350/2048,1-1950/2048],[48/2048,0],[0,400/2048]],end=[[730/2048,1-368/2048],[50/2048,0],[0,26/2048]])
 Path('build/fence-chart-reuse.json').write_text(json.dumps(dict(source=str(path),charts=FENCE_CHARTS,pixel_rectangles=dict(side=[350,1550,398,1950],end=[730,342,780,368]),scope='Interior bare board and end-grain rectangles with positive-Z tangent normals in the unchanged canonical atlas; no black gaps or hardware'),indent=2))
 return FENCE_CHARTS

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
  m=atlas.copy();m.name='Minigolf_'+name;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Transmission Weight'].default_value=1.;b.inputs['IOR'].default_value=1.333 if name=='water' else 1.5
  if name=='glass':
   # Clear thin glazing uses a neutral transmission color. Dark albedo on
   # the old state absorbed almost all light across the two pane surfaces.
   for link in list(m.node_tree.links):
    if link.to_socket==b.inputs['Base Color']:m.node_tree.links.remove(link)
   b.inputs['Base Color'].default_value=(.95,.985,.98,1)
  states[name]=m
 states['fallwater']=states['water']
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
 normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
 assignments=[];keys=[]
 for p in data.polygons:
  key=old[p.material_index].name.removeprefix('Quick_')
  if key in ('rock','rocklight') and wet_mask(ob.matrix_world@p.center)>.25:key='wetrock'
  keys.append(key)
  assignments.append(states.get('lamp',atlas) if any(n in ob.name for n in ('Floodlight lens','Service porch light','Service counter lamp','Opal sign face')) else states.get(key,atlas))
 distinct=list(dict.fromkeys(assignments));data.materials.clear()
 for m in distinct:data.materials.append(m)
 for poly,key,material in zip(data.polygons,keys,assignments):
  # Quantize near-equal face components so adjacent triangles on one 45°
  # manufacturing bevel choose the same chart axes after float32 evaluation.
  poly.material_index=distinct.index(material);axes=sorted(range(3),key=lambda k:round(abs(poly.normal[k]),3))[:2];axes.sort()
  rect=RECTS[key];u0,v0,u1,v1=rect;pad=8/2048
  nw=normal_matrix@poly.normal;wa=sorted(range(3),key=lambda k:round(abs(nw[k]),3))[:2];wa.sort()
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
    shade=math.exp(-((q.x-cx)/.9)**4-(((t-.49)*h['length'])/1.4)**4) if h.get('fixture') else 0
    sunfade=age*(1-.8*shade)
    tint=[.33+.52*worn+.10*sunfade,.72+.20*worn+.05*sunfade,.48+.10*worn+.06*sunfade]
   elif key in ('concrete','asphalt','grass','wood'):
    coverage={'concrete':3.048,'asphalt':6.096,'grass':3.048,'wood':2.4}[key]
    # Reused family maps retain their meter-based repeat and real response.
    uv.data[li].uv=(world[wa[0]]/coverage,world[wa[1]]/coverage)
    if key=='wood':
     # Privacy is a unique atlas, not a seamless wood tile. Reuse actual
     # clean wood charts, avoiding its hardware and unused atlas background.
     spans=[b-a for a,b in bounds];long_axis=max(range(3),key=lambda k:spans[k]);end=long_axis not in axes
     va=max(axes,key=lambda k:spans[k]);ua=next(k for k in axes if k!=va)
     u=(q[ua]-bounds[ua][0])/max(.0001,spans[ua]);v=(q[va]-bounds[va][0])/max(.0001,spans[va])
     origin,du,dv=[Vector(q) for q in fence_charts()['end' if end else 'side']]
     uv.data[li].uv=origin+du*(.04+.92*u)+dv*(.01+.98*v)
    tint=[.83,.82,.77] if key=='concrete' else [1,1,1]
    if ob.get('surface_tint'):tint=[a*b for a,b in zip(tint,ob['surface_tint'])]
    vcol.data[li].color=(*tint,1);continue
   else:
    # Each construction part is an authored chart. Dominant-face projection
    # prevents collapse on thin vertical rails and cast faces. Atlas reuse
    # is intentional; no unique-atlas zero-overlap claim applies.
    u=(q[axes[0]]-bounds[axes[0]][0])/max(.0001,bounds[axes[0]][1]-bounds[axes[0]][0]);v=(q[axes[1]]-bounds[axes[1]][0])/max(.0001,bounds[axes[1]][1]-bounds[axes[1]][0])
    if key=='brick' and ob.name.startswith('Jointed brick border'):
     # One modeled brick samples clay within one atlas brick, not a miniature
     # seven-course wall printed on each individual edging unit.
     u=.02+.20*u;v=.015+.10*v
    if key in ('rock','rocklight','wetrock'):
     wet=wet_mask(world);algae=min(1,wet*.90+(.28 if -.25<world.z<.06 else 0))
     tint=[1-.85*algae,1-.73*algae,1-.88*algae]
     if ob.get('stone_uv_m'):
      tile=ob['stone_uv_m'];middle=ob.matrix_world@poly.center
      u=(world[wa[0]]-math.floor((middle[wa[0]]+1e-7)/tile)*tile)/tile;v=(world[wa[1]]-math.floor((middle[wa[1]]+1e-7)/tile)*tile)/tile
    elif key=='soil' and ob.get('mulch_uv_m'):
     tile=ob['mulch_uv_m'];middle=ob.matrix_world@poly.center
     u=(world.x-math.floor((middle.x+1e-7)/tile)*tile)/tile;v=(world.y-math.floor((middle.y+1e-7)/tile)*tile)/tile
    elif key in ('red','ivory','navy','white','stonepaint'):
     exposure=max(0,-(ob.matrix_world.to_3x3()@poly.normal).y)*age
     tint=[.82+.18*exposure,.78+.22*exposure,.74+.26*exposure]
   uv.data[li].uv=(u0+pad+max(0,min(1,u))*(u1-u0-2*pad),v0+pad+max(0,min(1,v))*(v1-v0-2*pad))
   vcol.data[li].color=(*tint,1)
