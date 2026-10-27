"""Checkpoint maps and UVs only. Existing shared images are read-only.

Four independent brick tiles, one roof atlas and one trim ORM add 9 1/3 MiB.
The accepted colonial maps stay byte-identical; planned family total 47 1/3 MiB.
"""
from pathlib import Path
import json
import math
import sys
import numpy as np
import bpy
from mathutils import Vector
from kit import tiling
from kit.image_io import write_png,linear_to_srgb
from textures import SETS,fields
from lookdev import materials,subdivide,weather
from ranch_build import BRICKS


def brick_maps(out,brick_color):
 from ranch_fields import brick
 brick(out,brick_color)


def roof_material(folder,age):
 from ranch_fields import roof
 roof(folder)
 mat=tiling.material('RanchRoof',folder,tint=True)
 ns,ls=mat.node_tree.nodes,mat.node_tree.links
 uv=ns.new('ShaderNodeTexCoord');sep=ns.new('ShaderNodeSeparateXYZ');ls.new(uv.outputs['UV'],sep.inputs[0])
 def mathnode(op,a,b=None):
  node=ns.new('ShaderNodeMath');node.operation=op
  if hasattr(a,'node'):ls.new(a,node.inputs[0])
  else:node.inputs[0].default_value=a
  if b is not None:
   if hasattr(b,'node'):ls.new(b,node.inputs[1])
   else:node.inputs[1].default_value=b
  return node.outputs[0]
 # Source-only atlas addressing: every real roof course and roll gets its
 # own phase, breaking the short tile's large-scale repeat. Final delivery
 # will split metric roof charts at these integer course/roll boundaries.
 row=mathnode('FLOOR',mathnode('MULTIPLY',sep.outputs['Y'],17))
 roll=mathnode('FLOOR',sep.outputs['X'])
 phase=mathnode('MULTIPLY',mathnode('SINE',mathnode('ADD',mathnode('MULTIPLY',row,12.9898),mathnode('MULTIPLY',roll,78.233))),437.15)
 uu=mathnode('FRACT',mathnode('ADD',sep.outputs['X'],phase))
 vv=mathnode('ADD',mathnode('MULTIPLY',mathnode('FRACT',sep.outputs['Y']),.5),.5 if age=='newer' else 0)
 combine=ns.new('ShaderNodeCombineXYZ');ls.new(uu,combine.inputs[0]);ls.new(vv,combine.inputs[1])
 for node in ns:
  if node.type=='TEX_IMAGE':ls.new(combine.outputs[0],node.inputs['Vector'])
 return mat


def prepare(source,out,folder=Path('textures/source')):
 bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));meta=json.loads(source.with_suffix('.json').read_text());mats=materials(folder)
 new=out.parent/'materials'/meta['spec']['brick_color']
 brick_maps(new,meta['spec']['brick_color'])
 mats['Veneer']=tiling.material('RanchBrick',new,tint=True)
 from ranch_fields import trim_orm
 trim_path=out.parent/'materials'/'trim';trim_orm(trim_path,folder/'T_HouseTrim_ORM.png')
 for node in mats['Trim'].node_tree.nodes:
  if node.type=='TEX_IMAGE' and node.image and '_ORM' in node.image.name:
   node.image=bpy.data.images.load(str((trim_path/'T_RanchTrim_ORM.png').resolve()),check_existing=True);node.image.colorspace_settings.name='Non-Color'
 mats['Shingles']=roof_material(out.parent/'materials'/'roof',meta['spec']['roof_age'])
 glass=mats['Glass'];p=glass.node_tree.nodes.get('Principled BSDF')
 for socket in ('Base Color','Roughness'):
  for link in list(p.inputs[socket].links):glass.node_tree.links.remove(link)
 p.inputs['Base Color'].default_value=(.94,.97,.94,1);p.inputs['Roughness'].default_value=.025
 # Keep the same material roles and at most six materials in a house.
 triangles=0;added=0;weathered=0;efflorescent=0;rowlock_uv_samples=0;rowlock_uv_max=0;tint_min=1;tint_max=0
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH':continue
  me=ob.data;me.calc_loop_triangles();before=len(me.loop_triangles);subdivide(ob,meta);me=ob.data
  roles=[m.name.replace('House_','') for m in me.materials]
  for i,role in enumerate(roles):me.materials[i]=mats[role]
  world=[ob.matrix_world@v.co for v in me.vertices];uv=me.uv_layers.active;attr=me.color_attributes['Tint'];normals={};vr={}
  comp=ob.get('component');face=ob.get('face');block=next((v for v in meta['blocks'] if v['name']==ob.get('block')),meta['blocks'][0])
  for poly in me.polygons:
   role=roles[poly.material_index];n=(ob.matrix_world.to_3x3()@poly.normal).normalized()
   for vi in poly.vertices:
    vr[vi]=role
    if vi not in normals or (abs(n.z)<.5 and comp in ('wall','foundation','chimney')):normals[vi]=n
   axis=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=axis];points=[world[i] for i in poly.vertices]
   strip=0
   if role=='Glass':strip=6
   elif comp in ('roof_vent','flashing','valley','aerial'):strip=5
   elif comp=='opening_masonry' and role=='Trim':strip=5
   elif comp=='chimney' and role=='Trim' and max(attr.data[poly.vertices[0]].color[:3])<.24:strip=5
   elif comp=='eave_rake_soffit' and n.z<-.6:strip=2
   elif comp in ('window','storm_window'):
    c=attr.data[poly.vertices[0]].color
    if ob.get('window_system') in ('aluminum','wood_storm','bronze') and (max(abs(c[k]-(.30,.31,.27)[k]) for k in range(3))<.01 or max(abs(c[k]-(.105,.075,.042)[k]) for k in range(3))<.01):strip=5
    elif max(c[:3])<.5 and min(c[:3])>.23:strip=4
    shutter=meta['spec']['colors']['shutter']
    if max(abs(c[k]-shutter[k]*.78) for k in range(3))<.002:strip=1
   if role=='Trim':axes.sort(key=lambda k:max(p[k] for p in points)-min(p[k] for p in points),reverse=True)
   lo=min(p[axes[1]] for p in points);hi=max(p[axes[1]] for p in points)
   for li in poly.loop_indices:
    p=world[me.loops[li].vertex_index]
    if role in ('Trim','Glass'):
     u=p[axes[0]]/4
     if strip==5:u=.78+.20*(p[axes[0]]%4)/4
     uv.data[li].uv=(u,(strip+.04+(p[axes[1]]-lo)/max(.5,(hi-lo)/.92))/8)
    elif role=='Shingles' and abs(n.z)>.3:
     coord=(p.x,p.y/max(.2,abs(n.z))) if abs(n.y)>=abs(n.x) else (p.y,p.x/max(.2,abs(n.z)))
     uv.data[li].uv=(coord[0]/4.8768,coord[1]/2.4384)
    elif role=='Veneer':
     # Meter-aligned modular courses; each tile repeats 6x18 bricks.
     if comp=='opening_masonry':
      # Construction is triangulated before look-dev. Every rowlock
      # retains its eight prism vertices; polygon indices cannot identify
      # units, and per-triangle bounds cause diagonal color discontinuities.
      index=min(poly.vertices)//8;unit=world[index*8:index*8+8]
      aa=sorted(axes,key=lambda k:max(v[k] for v in unit)-min(v[k] for v in unit),reverse=True)
      pmin=[min(v[k] for v in unit) for k in aa];span=[max(v[k] for v in unit)-pmin[j] for j,k in enumerate(aa)]
      uv.data[li].uv=((index%6-.5*((index//6)%2)+.15+.70*(p[aa[0]]-pmin[0])/max(span[0],1e-6))/6,((index//6)%18+.24+.52*(p[aa[1]]-pmin[1])/max(span[1],1e-6))/18)
     else:uv.data[li].uv=(p[axes[0]]/1.2192,p[axes[1]]/1.2192)
    else:uv.data[li].uv=(p[axes[0]]/SETS[role][1],p[axes[1]]/SETS[role][1])
  if comp=='opening_masonry':
   seen={}
   for poly in me.polygons:
    if roles[poly.material_index]!='Veneer':continue
    plane=tuple(round(v,4) for v in poly.normal)
    for li in poly.loop_indices:
     key=(me.loops[li].vertex_index,plane);value=uv.data[li].uv.copy()
     if key in seen:
      rowlock_uv_samples+=1;error=(value-seen[key]).length;rowlock_uv_max=max(rowlock_uv_max,error)
      assert error<1e-6,('Discontinuous rowlock triangle chart',ob.name,key,error)
     seen[key]=value
  for v in me.vertices:
   p=world[v.index];role=vr[v.index];n=normals[v.index];c=Vector(attr.data[v.index].color[:3])
   if role=='Veneer':c=Vector((.72,.72,.72))
   if role=='Glass':c=Vector((1,1,1))
   if role=='Concrete':c=Vector((.8,.8,.8))
   if role=='Shingles':c=Vector(dict(warm_charcoal=(.92,.92,.88),weathered_wood=(1.14,.99,.78),dark_brown=(.92,.72,.51))[meta['spec']['shingle_color']])
   if role=='Shingles':c*=.115/.17
   if role=='Shingles' and meta['spec']['roof_age']=='newer' and meta['spec']['shingle_color']=='warm_charcoal':c*=1.48
   factor,amount,green=weather(p,n,role,comp,meta,ob.get('block'),face)
   if role=='Shingles' and meta['spec']['roof_age']=='newer':factor=Vector((1,1,1));amount=green=0
   if role in ('Veneer','Siding'):
    # Wind-driven splash is strongest near wet grade; salt migration makes
    # pale irregular blooms within the same damp zone, never a level band.
    ripple=.5+.5*math.sin(p.x*6.3+p.y*8.1+.6*math.sin(p.x*17))
    salts=max(0,1-abs(p.z-(block['floor']-.10))/.40)*ripple*.65 if role=='Veneer' else 0
    c=c.lerp(Vector((1.0,.98,.90)),salts);efflorescent+=salts>.03
    for opening in meta['openings']:
     if opening['kind']!='window' or opening['block']!=block['name'] or opening['face']!=face:continue
     axis=0 if face in ('front','back') else 1;origin=block['x0'] if axis==0 else block['y0']
     for sign in (-1,1):
      horiz=p[axis]-(origin+opening['u']+sign*opening['w']*.43);below=opening['z']-p.z
      if 0<below<.85:
       streak=.28*math.exp(-(horiz/(.09+.035*below))**2)*math.exp(-below/.42)
       factor*=Vector((1-streak*.55,1-streak*.64,1-streak*.78))
   if role=='Shingles' and meta['spec']['roof_age']=='tired':
    # Uneven granule loss on exposed slopes, water-carried algae below the
    # shaded ridge. Geometry samples carry these large causal masks.
    ridge=block['eave']+block['pitch']*(block['y1']-block['y0'])/2
    stripes=(.5+.5*math.sin(p.x*4.37+.35*math.sin(p.x*11.7)))**8
    north=max(0,n.y);algae=.55*north*stripes*math.exp(-((p.z-(ridge-.35))/.8)**2)
    factor*=Vector((1-algae*.68,1-algae*.56,1-algae*.73))
    loss=max(0,-n.y)*(.5+.5*math.sin(p.x*2.8+p.y*6.4))*.13;c*=1+loss
   if role=='Trim' and comp in ('corner_posts','eave_rake_soffit','porch_structure','window'):
    gray=sum(c)/3;chalk=.25 if comp!='window' or ob.get('window_system')=='wood_storm' else .04
    c=c.lerp(Vector((gray+.065,gray+.055,gray+.03)),chalk)
   if comp=='eave_rake_soffit':
    # The continuous gutter has real miter/end joints, not a seam
    # every arbitrary noise period. Wet the soffit just beneath those joints.
    seam=max((.30*math.exp(-((p.x-q[0])**2+(p.y-q[1])**2)/.10) for d in meta['drains'] for q in d['gutter']),default=0)*max(0,-n.z)
    factor*=1-seam
   if comp=='porch_steps' and n.z>.5:
    y0=meta['porch']['y0'];wear=math.exp(-((p.x-meta['door_x'])/.40)**2)*(.6+.4*math.sin(p.y*8)**2)
    factor*=Vector((1-.16*wear,1-.18*wear,1-.22*wear))
   result=tuple(c[k]*factor[k] for k in range(3));tint_min=min(tint_min,*result);tint_max=max(tint_max,*result)
   assert 0<=min(result) and max(result)<=1.000001,('Normalized tint range',ob.name,result)
   attr.data[v.index].color=(*result,1);weathered+=amount>.04
  me.calc_loop_triangles();triangles+=len(me.loop_triangles);added+=len(me.loop_triangles)-before
 meta.update(stage='ranch source checkpoint; quick period maps; before bake',triangles=triangles,materials=6,
   weather=dict(vertices_weathered=weathered,efflorescence_vertices=efflorescent,added_triangles=added),
   planned_shared_gpu_mib=47.3333333333,rowlock_uv_continuity=dict(samples=rowlock_uv_samples,max_error=rowlock_uv_max),normalized_tint_range=[tint_min,tint_max],period_source_maps=str(new))
 out.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
 print('RANCH_LOOKDEV',meta['seed'],triangles,meta['weather'])
 return meta
