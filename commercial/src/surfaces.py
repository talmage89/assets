"""Shared baked PBR charts, original graphics and cause-local vertex weather.

Every source mesh receives its charts before static module consolidation.
Manufactured grain stays in the maps; only low-frequency age is sampled to
stock glTF COLOR_0. Reference images are never read here.
"""
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from kit import tiling,model as G
from geometry import M,own
from textures import CELLS,TRIM,SETS

FOLDER=Path('textures/ship')


def cell_rect(name):
 i=CELLS[name];row,col=divmod(i,4);g=8/2048
 return (col/4+g,row/8+g,(col+1)/4-g,(row+1)/8-g)


def pbr(name,folder=FOLDER,tint=True,pair=False):
 if not pair:return tiling.material(name,folder,tint=tint)
 ma=bpy.data.materials.new(name);ma.use_nodes=True;ma['tiling_vertex_tint']=tint
 ns,ls=ma.node_tree.nodes,ma.node_tree.links;p=ns.get('Principled BSDF')
 for channel in ('BaseColor','Normal'):
  tex=ns.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str((folder/f'T_{name}_{channel}.png').resolve()),check_existing=True)
  tex.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
  if channel=='BaseColor':
   color=tex.outputs['Color']
   if tint:
    vc=ns.new('ShaderNodeVertexColor');vc.layer_name='Tint';mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
    ls.new(color,mix.inputs[1]);ls.new(vc.outputs['Color'],mix.inputs[2]);color=mix.outputs[0]
   ls.new(color,p.inputs['Base Color'])
  else:
   nm=ns.new('ShaderNodeNormalMap');ls.new(tex.outputs['Color'],nm.inputs['Color']);ls.new(nm.outputs[0],p.inputs['Normal'])
 p.inputs['Roughness'].default_value=.93 if name.endswith('Roof') else .88;ma.use_backface_culling=True
 return ma


def shared_text(name,string,p,size,mat,parent,align='CENTER',yaw=0):
 catalogue=json.loads((FOLDER/'graphics.json').read_text());data=catalogue[string]
 mark=string.startswith('@');h=size if mark else size*data['pixel_height']/data['font_size'];w=h*data['aspect']
 # Wordmarks have equal geometry so either brand selects another UV cell.
 px,py,pz=p
 if align=='LEFT':px+=w/2
 ob=own(G.plane_uv(name,[(px-w/2,py,pz-h/2),(px+w/2,py,pz-h/2),(px+w/2,py,pz+h/2),(px-w/2,py,pz+h/2)],M['White']),parent,False)
 uv=ob.data.uv_layers.active;r=data['rect'];tc=[(r[0],r[1]),(r[2],r[1]),(r[2],r[3]),(r[0],r[3])]
 for poly in ob.data.polygons:
  for li in poly.loop_indices:uv.data[li].uv=tc[ob.data.loops[li].vertex_index]
 ob.rotation_euler.z=math.radians(yaw);ob['graphic']=True;ob['graphic_role']=mat;ob['graphic_string']=string
 return ob


def tint_layer(ob,values):
 attr=ob.data.color_attributes.get('Tint') or ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
 for c,rgb in zip(attr.data,values):c.color=(*rgb,1)
 ob.data.color_attributes.active_color=attr


def subdivide(ob,wall=False,fascia=False):
 """Cut planar manufacture faces only; retain bevel rims and source normals."""
 if not wall and not fascia:return
 me=ob.data;bm=bmesh.new();bm.from_mesh(me);lo=[min(v.co[k] for v in bm.verts) for k in range(3)];hi=[max(v.co[k] for v in bm.verts) for k in range(3)]
 axes=[k for k in range(3) if hi[k]-lo[k]>.35]
 for axis in axes:
  if axis==2:
   cuts=[lo[2]+a for a in (.10,.24,.42,.68)]
   cuts+=[hi[2]-a for a in (.12,.32,.65)]
  else:
   step=.80 if wall else .61;cuts=[lo[axis]+i*step for i in range(1,math.ceil((hi[axis]-lo[axis])/step))]
  for q in cuts:
   if not lo[axis]+.005<q<hi[axis]-.005:continue
   point=[0,0,0];point[axis]=q;normal=[0,0,0];normal[axis]=1
   bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=point,plane_no=normal,clear_inner=False,clear_outer=False)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8);bm.to_mesh(me);bm.free();me.update()


def charts(ob,role,cell=None,strip=None,coverage=1):
 me=ob.data;uv=me.uv_layers.active or me.uv_layers.new(name='UVMap');uv.name='UVMap'
 if ob.get('swept_wear'):
  r=cell_rect(cell);stations=len(me.vertices)//2
  for loop in me.loops:
   i=loop.vertex_index;uv.data[loop.index].uv=(r[0]+(i%2)*(r[2]-r[0]),r[1]+(i//2)/(stations-1)*(r[3]-r[1]))
  return
 # Construction coordinates, before the entire station is quarter-turned.
 coords=[ob.matrix_world@v.co for v in me.vertices]
 bbox=[[min(p[k] for p in coords),max(p[k] for p in coords)] for k in range(3)]
 for poly in me.polygons:
  normal=ob.matrix_world.to_3x3()@poly.normal;axis=max(range(3),key=lambda k:abs(normal[k]))
  axes=[(1,2),(0,2),(0,1)][axis]
  # Right-handed tangent charts on both front and rear wall faces.
  sign=-1 if (axis==0 and normal.x<0) or (axis==1 and normal.y>0) or (axis==2 and normal.z<0) else 1
  for li in poly.loop_indices:
   q=coords[me.loops[li].vertex_index];u=q[axes[0]]*sign;v=q[axes[1]]
   if cell:
    r=cell_rect(cell);a,b=axes;den=max(.000001,bbox[a][1]-bbox[a][0]);dv=max(.000001,bbox[b][1]-bbox[b][0])
    if role=='Soil':
     bounds={k:(min(coords[i][k] for i in poly.vertices),max(coords[i][k] for i in poly.vertices)) for k in axes}
     den=max(.000001,bounds[a][1]-bounds[a][0]);dv=max(.000001,bounds[b][1]-bounds[b][0])
     uu=(q[a]-bounds[a][0])/den;vv=(q[b]-bounds[b][0])/dv
    else:
     uu=(q[a]-bbox[a][0])/den;vv=(q[b]-bbox[b][0])/dv
    if sign<0:uu=1-uu
    uv.data[li].uv=(r[0]+uu*(r[2]-r[0]),r[1]+vv*(r[3]-r[1]))
   elif strip is not None:
    b=axes[1];vv=(v-bbox[b][0])/max(.000001,bbox[b][1]-bbox[b][0]);g=8/2048
    uv.data[li].uv=(u/2.4384,strip/8+g+vv*(1/8-2*g))
   else:uv.data[li].uv=(u/coverage,v/coverage)


def graphic_chart(ob,key,lit=False):
 catalogue=json.loads((FOLDER/'graphics.json').read_text());r=catalogue[key]['rect']
 uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='UVMap');uv.name='UVMap'
 em=ob.data.uv_layers.get('EmissionUV') or ob.data.uv_layers.new(name='EmissionUV')
 blank=catalogue['Blank']['rect'];off=((blank[0]+blank[2])/2,(blank[1]+blank[3])/2)
 if not ob.get('graphic'):
  charts(ob,'Wear' if key.startswith('Wear:') else 'Lamp',cell=ob.get('wear_cell')) if ob.get('swept_wear') else None
  # Every small face fits its swatch; the wide wear quads use true corner UVs.
  coords=[v.co for v in ob.data.vertices]
  for poly in ob.data.polygons:
   axis=max(range(3),key=lambda k:abs(poly.normal[k]));axes=[(1,2),(0,2),(0,1)][axis]
   ids=range(len(coords)) if key.startswith('Wear:') else poly.vertices
   bounds=[(min(coords[i][a] for i in ids),max(coords[i][a] for i in ids)) for a in axes]
   for li in poly.loop_indices:
    i=ob.data.loops[li].vertex_index
    if ob.get('swept_wear'):u=i%2;v=(i//2)/(len(coords)//2-1)
    else:u,v=[(coords[i][a]-lo)/max(hi-lo,1e-8) for a,(lo,hi) in zip(axes,bounds)]
    if ob.get('wear_flip'):u=1-u
    uv.data[li].uv=(r[0]+u*(r[2]-r[0]),r[1]+v*(r[3]-r[1]))
 for li in range(len(ob.data.loops)):em.data[li].uv=uv.data[li].uv if lit else off
 ob.data.uv_layers.active=uv


def weather(q,name,role,ob,meta):
 x,y,z=q;b=meta['building'];amount=0
 # Low grade splash follows roughness in a narrow decaying zone, not a band.
 if role in ('Wall','Concrete') and not any(t in name for t in ('floor','ceiling','shelf','worktop')):
  reach=.31+.09*math.sin(x*4.1+y*1.8)+.04*math.sin(x*13+y*7)
  amount=.38*max(0,1-max(0,z-.05)/reach)
 if role=='Wall':
  # Runoff starts at the actual coping joints and dies down the wall.
  top=b['parapet'];u=x if 'Side' not in name and 'wainscot' not in name else y
  joint=abs((u+b['width']/2-.20+1.2192)%2.4384-1.2192)
  strength=.78+.22*math.sin(math.floor((u+b['width']/2-.20)/2.4384)*2.37+meta['seed'])**2
  amount+=.30*strength*math.exp(-(joint/.14)**2)*math.exp(-max(0,top-z)/.62)
  if z<.5:amount+=.13*(.5+.5*math.sin(u*9.1))**4*max(0,1-z/.5)
 if 'Fascia' in name:
  u=x if ob.dimensions.x>ob.dimensions.y else y
  seams=abs((u+1.2192)%2.4384-1.2192);amount+=.48*math.exp(-(seams/.16)**2)
 if any(s in name for s in ('Hydraulic','Dispenser plinth','Square canopy column','Column base','Pipe bollard','Column U guard')):
  localz=ob.matrix_world.inverted()@Vector(q)
  bottom=min((ob.matrix_world@v.co).z for v in ob.data.vertices)
  amount+=.46*math.exp(-max(0,z-bottom)/.18)
 if 'Roof membrane' in name:
  edge=min(abs(abs(x-b['center_x'])-b['width']/2),abs(y-b['front']),abs(y-b['front']-b['depth']))
  amount+=.33*math.exp(-edge/.40)
 factor=max(.26,1-min(.68,amount)*.72)
 if any(s in name for s in ('parking stripe','stall boundary','hatching','Wheelchair')):
  factor*=.65+.20*(.5+.5*math.sin(x*21+y*37))
 if ob.get('repair'):factor*=.52
 return factor


def apply(meta):
 """Install the actual shipping materials before module consolidation."""
 # Seed Blender's complete native settings group before kit.material adds AO.
 # The 5.2 importer also expects its optional iridescence/thickness sockets.
 from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
 get_settings_group()
 mats={r:pbr('Commercial'+r,pair=c==2) for r,(size,cov,c) in SETS.items()}
 ground=Path(__file__).resolve().parents[2]/'ground/textures/ship'
 for r in ('Asphalt','Lawn'):mats[r]=pbr(r,ground)
 nt=mats['Asphalt'].node_tree;p=nt.nodes.get('Principled BSDF');source=p.inputs['Roughness'].links[0].from_socket
 multiply=nt.nodes.new('ShaderNodeMath');multiply.operation='MULTIPLY';multiply.inputs[1].default_value=.88;nt.links.new(source,multiply.inputs[0]);nt.links.new(multiply.outputs[0],p.inputs['Roughness'])
 # Smooth CMU shares the same image, with a distinct physical normal response.
 mats['SmoothCMU']=mats['CMU'].copy();mats['SmoothCMU'].name='CommercialSmoothCMU'
 next(n for n in mats['SmoothCMU'].node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.20
 mats['Glass']=bpy.data.materials.new('CommercialGlass');mats['Glass'].use_nodes=True;mats['Glass']['tiling_vertex_tint']=False
 p=mats['Glass'].node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.94,.97,.96,1);p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.52;p.inputs['Roughness'].default_value=.025
 ma=bpy.data.materials.new('CommercialGraphics');ma.use_nodes=True;ma['tiling_vertex_tint']=False
 ns,ls=ma.node_tree.nodes,ma.node_tree.links;pp=ns.get('Principled BSDF');tex=ns.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str((FOLDER/'T_CommercialGraphics_BaseColor.png').resolve()),check_existing=True)
 ls.new(tex.outputs['Color'],pp.inputs['Base Color']);ls.new(tex.outputs['Alpha'],pp.inputs['Alpha'])
 pp.inputs['Roughness'].default_value=.55;ma.surface_render_method='DITHERED';ma.use_backface_culling=False
 emi=ns.new('ShaderNodeTexImage');emi.image=bpy.data.images.load(str((FOLDER/'T_CommercialGraphics_Emission.png').resolve()),check_existing=True);emi.image.colorspace_settings.name='sRGB'
 u=ns.new('ShaderNodeUVMap');u.uv_map='EmissionUV';ls.new(u.outputs['UV'],emi.inputs['Vector']);ls.new(emi.outputs['Color'],pp.inputs['Emission Color']);pp.inputs['Emission Strength'].default_value=300
 mats['Graphics']=ma
 rows={};bpy.context.view_layer.update()
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
 dg=bpy.context.evaluated_depsgraph_get();evaluated=[]
 for ob in objects:
  if ob.get('wear_cell') or ob.get('graphic'):continue
  evaluated.append((ob,bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True)))
 for ob,data in evaluated:ob.data=data;ob.modifiers.clear()
 for index,ob in enumerate(objects):
  if index%400==0:print('SURFACES',index,'/',len(objects),ob.name,flush=True)
  old=ob.data.materials[0];role=old.name.removeprefix('Form_').split('.')[0];name=ob.name
  if ob.get('wear_cell'):
   ob.data.materials.clear();ob.data.materials.append(mats['Graphics']);graphic_chart(ob,'Wear:'+ob['wear_cell']);continue
  if ob.get('graphic'):
   role=ob['graphic_role'];lit=role in ('Light','Logo') and any(t in name for t in ('Canopy','Store brand','Price brand'))
   ob.data.materials.clear();ob.data.materials.append(mats['Graphics']);graphic_chart(ob,ob['graphic_string'],lit);continue
  if role=='Primary' and any(q in name for q in ('Store brand backing','Price brand backing')):
   ob.data.materials.clear();ob.data.materials.append(mats['Graphics']);graphic_chart(ob,'BrandRillway' if meta['brand']=='rillway' else 'BrandLatchline',True);continue
  # Evaluate manufacturing bevels before causal planar sampling.
  wall=role=='Wall';fascia='Fascia' in name
  subdivide(ob,wall,fascia)
  if role=='Soil':
   bm=bmesh.new();bm.from_mesh(ob.data)
   for axis in (0,1):
    lo=min(v.co[axis] for v in bm.verts);hi=max(v.co[axis] for v in bm.verts)
    for i in range(1,math.ceil((hi-lo)/.65)):
     co=[0,0,0];co[axis]=lo+i*.65;no=[0,0,0];no[axis]=1
     bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=co,plane_no=no)
   bm.to_mesh(ob.data);bm.free();ob.data.update()
  module=ob.parent;in_dispenser=False
  while module:
   if module.get('module_kind')=='Dispenser':in_dispenser=True;break
   module=module.parent
  material=mats['Equipment'];cell=role if role in CELLS else 'Black' if role=='Trim' else 'White';strip=None;coverage=1;col=(1,1,1)
  if wall:
   style=meta['building']['wall'];key='Brick' if style=='brick' else 'EIFS' if style=='eifs' else 'CMU' if style=='split_cmu' or 'wainscot' in name or 'Pilaster precast foot' in name else 'SmoothCMU'
   material=mats[key];cell=None;coverage=SETS['CMU' if key=='SmoothCMU' else key][1]
  elif role in ('Concrete','Asphalt','Green'):
   material=mats['Lawn' if role=='Green' else role];cell=None;coverage=6.096 if role=='Asphalt' else 1.524 if role=='Concrete' else 3.048
  elif role=='Roof':material=mats['Roof'];cell=None;coverage=SETS['Roof'][1]
  elif ob.get('rust_finish'):cell='Rust'
  elif ob.get('package') is not None:cell='Package'+str(ob['package'])
  elif role=='Glass':material=mats['Glass'];cell=None
  elif role in ('Lamp','LED','Logo','Light'):
   key='PriceLED' if role=='LED' else 'CanopyLamp' if 'luminaire' in name else 'InteriorLamp' if 'Ceiling' in name else 'WallPackLamp' if 'pack lens' in name else 'LotLamp' if name.startswith('Light lens') else 'InteriorLamp'
   ob.data.materials.clear();ob.data.materials.append(mats['Graphics']);graphic_chart(ob,key,True);continue
  elif role=='Trim':cell='Black'
  if material==mats['Equipment'] and role in ('Primary','Accent'):
   cell='Primary';target=M[role].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value[:3];col=tuple(a/.86 for a in target)
  if 'Soffit cladding' in name:col=(.78,.69,.56)
  if role in ('Primary','Accent') and any(s in name for s in ('Fascia','backing','crown','Entry canopy fascia')):
   front=ob.matrix_world.to_3x3()@Vector((0,-1,0));angle=math.radians(meta['yaw']);south=max(0,-(front.x*math.sin(angle)+front.y*math.cos(angle)))
   fade=.35*south;col=tuple(c*(1-.18*fade)+.055*fade for c in col)
  ob.data.materials.clear();ob.data.materials.append(material)
  if role in ('Asphalt','Concrete'):
   from paving import cut,tint
   if ob.name.startswith('Lot asphalt'):cut(ob,.55)
   elif ob.name.startswith('Fuel apron'):cut(ob,.90)
   charts(ob,role,cell,strip,coverage);tint(ob,meta,role)
   rows[name]=dict(role=role,material=material.name,cell=cell,strip=strip);continue
  charts(ob,role,cell,strip,coverage)
  values=[]
  for vertex in ob.data.vertices:
   q=ob.matrix_world@vertex.co;f=weather(q,name,role,ob,meta)
   values.append(tuple(min(1,c*f) for c in col))
  tint_layer(ob,values);rows[name]=dict(role=role,material=material.name,cell=cell,strip=strip)
 meta['surface_assignment']=rows;meta['stage']='shared baked PBR look checkpoint; exported maps and causal COLOR_0'
 return mats
