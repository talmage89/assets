"""Town context from original exported libraries; never part of delivery."""
import math,json,random,hashlib
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
from kit import model as G
ROOT=Path(__file__).resolve().parents[2]

class Library:
 def __init__(self):self.cache={};self.dependencies={};self.paint={}
 def load(self,path):
  path=Path(path)
  if path in self.cache:return self.cache[path]
  # Match the houses' source/context import accommodation: the source tile
  # writer has a minimal AO group; the 5.2 importer needs its full interface.
  group=bpy.data.node_groups.get('glTF Material Output')
  if group and not any(q.name=='Iridescence Factor' for q in group.interface.items_tree):group.name='ApartmentsSource_Occlusion'
  before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
  objects=list(set(bpy.context.scene.objects)-before);bpy.context.view_layer.update()
  if path.parent.parent.name=='cars':
   for ob in objects:
    if ob.type!='MESH':continue
    for ma in ob.data.materials:
     if ma and ma.use_nodes:
      bs=next((n for n in ma.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
      if bs:bs.inputs['Emission Strength'].default_value=0
  if path.parent.parent.name=='street-light':
   for ob in objects:
    if ob.type!='MESH':continue
    for ma in ob.data.materials:
     if not ma or not ma.use_nodes:continue
     bs=next((n for n in ma.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
     if bs and bs.inputs['Emission Strength'].default_value>0:
      ma['presentation_emission_default']=bs.inputs['Emission Strength'].default_value;bs.inputs['Emission Strength'].default_value=0
  for ob in objects:ob.hide_render=True;ob.hide_set(True)
  self.cache[path]=objects;self.dependencies[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest();return objects
 def place(self,path,name,p=(0,0,0),yaw=0,select=None,scale=(1,1,1)):
  objects=self.load(path);selected=objects;base=Matrix.Identity(4)
  if select:
   anchor=next((o for o in objects if o.name.split('.')[0]==select),None)
   if anchor is None:raise ValueError((str(path),select,[o.name for o in objects if o.parent not in objects]))
   selected=[anchor,*anchor.children_recursive];base=anchor.matrix_world.inverted()
  root=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(root)
  root.location=p;root.rotation_euler.z=math.radians(yaw);root.scale=scale;root['presentation_only']=True;root['presentation_family']=path.parent.parent.name
  copies={o:o.copy() for o in selected}
  for ob,cp in copies.items():
   bpy.context.collection.objects.link(cp);cp.name=name+'__'+ob.name;cp.parent=copies.get(ob.parent,root)
   cp.matrix_basis=ob.matrix_basis.copy() if ob.parent in copies else base@ob.matrix_world
   cp.hide_render=False;cp.hide_set(False)
  if path.parent.parent.name=='ground' and scale!=(1,1,1):
   from context import ground_charts
   bpy.context.view_layer.update()
   for cp in copies.values():ground_charts(cp)
  return root
 def factory(self,root,index):
  for ob in root.children_recursive:
   if ob.type!='MESH':continue
   for slot in ob.material_slots:
    original=slot.material
    if original.get('paint_decode')!='reference_plus_coverage_delta':continue
    colors=json.loads(original['paint_colors']);names=[n for n in ('Carbon','Aluminum','Porcelain','Atlantic','Graphite') if n in colors]
    preset=names[index%len(names)];key=(original.name,preset)
    if key not in self.paint:
     ma=original.copy();ma.name='Presentation factory '+preset+' '+original.name;nt=ma.node_tree
     bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
     delta=nt.nodes.new('ShaderNodeCombineXYZ')
     for socket,a,b in zip(delta.inputs,colors[preset],original['paint_reference_color']):socket.default_value=a-b
     scale=nt.nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';nt.links.new(delta.outputs[0],scale.inputs[0]);nt.links.new(tex.outputs['Alpha'],scale.inputs['Scale'])
     add=nt.nodes.new('ShaderNodeVectorMath');add.operation='ADD';nt.links.new(tex.outputs['Color'],add.inputs[0]);nt.links.new(scale.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],bs.inputs['Base Color'])
     for key2,a,b in (('Coat Weight',.90,.10),('Coat Roughness',-.35,.385)):
      node=nt.nodes.new('ShaderNodeMath');node.operation='MULTIPLY_ADD';node.inputs[1].default_value=a;node.inputs[2].default_value=b
      nt.links.new(tex.outputs['Alpha'],node.inputs[0]);nt.links.new(node.outputs[0],bs.inputs[key2])
     self.paint[key]=ma
    slot.link='OBJECT';slot.material=self.paint[key]
 def clear(self):
  for objects in self.cache.values():
   for ob in objects:
    if ob.name in bpy.data.objects:bpy.data.objects.remove(ob,do_unlink=True)


def point_light(name,p,power=50,color=(1,.72,.42),radius=.25):
 ld=bpy.data.lights.new(name,'POINT');ld.energy=power;ld.color=color;ld.shadow_soft_size=radius
 ob=bpy.data.objects.new(name,ld);bpy.context.collection.objects.link(ob);ob.location=p;return ob


def dress(meta,stem):
 p=meta['plan'];is_complex=stem.startswith('Complex');is_row=stem.startswith('Row');lib=Library();rng=random.Random(p['seed']+914)
 single=stem.startswith('Building')
 if single:
  lib.dependencies.update(match_context(meta,stem,plants=False))
  p=dict(seed=p['seed'],building=p,lot=(100,86),buildings=[dict(origin=(0,0,0),yaw=0)])
  is_complex=True
 if not (is_complex or is_row):return lib.dependencies
 W,D=p['lot'] if is_complex else (p['count']*p['width']+12,p['depth']+34)
 depth=p.get('depth',0);south=-D/2-8.8 if is_complex else -depth/2-11.2;north=D/2+9 if is_complex else depth/2+22
 ground=ROOT/'ground/export/Ground.glb'
 def street(y):
  # Repeat manufactured pieces at their native length. Length-scaling whole
  # curb/slab meshes also scales their expansion joints into visible gaps.
  for j in range(-29,30):
   lib.place(ground,'Town road',(j*6.096,y,-.172),90,'Road_Straight_'+('ABC'[j%3]))
  for sy in (-1,1):
   for j in range(-59,60):
    lib.place(ground,'Town curb',(j*3.048,y+sy*4.13,-.008),90 if sy<0 else 270,'Curb_Straight')
   if not (is_row and y==south and sy>0):
    for j in range(-118,119):lib.place(ground,'Town sidewalk',(j*1.524,y+sy*6.1,0),90,'Sidewalk_A')
 street(south);street(north)
 # Extend the town's rear and opposite frontages with the accepted houses.
 for j in range(-4,5):
  for sy,yy,yaw in ((-1,south-23,180),(1,north+23,0)):
   house=ROOT/'houses/export'/('Hearthfield-27.gltf' if (j+sy)%2 else 'Hearthfield-2.gltf')
   lib.place(house,f'Neighbor house {sy} {j}',(j*27+sy*4,yy,0),yaw)
 if is_row:
  for sx in (-1,1):
   for j in range(3):lib.place(ROOT/'houses/export'/('Hearthfield-27.gltf' if j%2 else 'Hearthfield-2.gltf'),'Along-block neighbor',(sx*(W/2+18+j*29),0,0),0)
 else:
  for sx in (-1,1):
   for j in range(-3,4):
    lib.place(ROOT/'houses/export'/('Hearthfield-27.gltf' if j%2 else 'Hearthfield-2.gltf'),'Beyond side lawns',(sx*(W/2+33),j*24,0),sx*90)
 tree=ROOT/'trees/export/RedMaple.glb';shrub=ROOT/'shrubs/export/Shrubs.glb'
 # Fill authored site markers with actual atlas-bearing library assets.
 markers=[o for o in bpy.context.scene.objects if o.get('presentation_kind')]
 cars=[ROOT/'cars/export'/n for n in ('AlderC150.glb','AlderX220.glb','AlderH120.glb')]
 for j,marker in enumerate(markers):
  kind=marker['presentation_kind'];xf=marker.matrix_world.copy();pos=xf.translation;yaw=math.degrees(xf.to_euler().z)
  path=cars[j%3] if kind=='car' else tree if kind=='tree' else shrub
  if kind=='shrub' and 'Island_shrub' not in marker.name:continue
  if kind=='car' and is_complex:
   b=p['building'];hero_x=p['buildings'][0]['origin'][0]+b['modules'][0]['origin'][0]-21
   if math.hypot(pos.x-hero_x,pos.y+12)<15:continue
  if kind=='car' and is_row:path=cars[2 if 'vehicle_1' in marker.name else 1]
  rt=lib.place(path,'Site '+marker.name,pos,yaw,select='Boxwood' if kind=='shrub' else None)
  if kind=='car':rt.matrix_world=xf;lib.factory(rt,j)
  if kind=='tree':rt.scale=(1.15,1.15,1.15)
 from landscaping import foundations
 foundations(lib,p,ROOT,stem)
 # Mature court canopies are independent of the smaller mixed borders.
 if is_complex:
  for j,(x,y) in enumerate([(-W*.43,20),(W*.28,14),(-W*.30,-15),(W*.32,-16),(0,D*.38),(-W*.1,-D*.36)]):
   lib.place(tree,'Court canopy '+str(j),(x,y,0),j*57,scale=(1.35,1.35,1.35))
 for j in range(-4,5):
  for yy in (south-11,north+11):lib.place(tree,'Street canopy',(j*26+8,yy,0),j*39,scale=(1.2,1.2,1.2))
 if is_row:
  for sx in (-1,1):
   for j in range(3):lib.place(tree,'Along-block canopy',(sx*(W/2+9+j*29),-depth/2-3.5,0),j*53,scale=(1.15,1.15,1.15))
 # Pole parts use the utility family's exact baked atlas and native framing.
 utility=Path('build/context/utility.glb')
 for yy in (south-5.1,north+5.1):
  poles=[lib.place(utility,'Utility tangent',(j*42,yy,.0),90,select='Tangent') for j in range(-3,4)]
  bpy.context.view_layer.update()
  cablemat=bpy.data.materials.new('Presentation conductor');cablemat.diffuse_color=(.025,.03,.025,1)
  for aa,bb in zip(poles,poles[1:]):
   for key in ('Primary_A','Primary_B','Primary_C','Neutral','CommStrand'):
    def anchor(root):return next(o for o in root.children_recursive if o.name.split('__')[-1].split('.')[0].endswith('_'+key))
    a,b=anchor(aa),anchor(bb);p0,p1=a.matrix_world.translation,b.matrix_world.translation
    pts=[p0.lerp(p1,t)-Vector((0,0,.70*4*t*(1-t))) for t in [k/24 for k in range(25)]]
    G.tube('Utility catenary',pts,float(a.get('diameter_m',.0101))/2,cablemat,6)
 for yy,yaw in ((south+(6.15 if is_row else 4.9),0),(north-4.9,180)):
  for j in range(-3,4):lib.place(ROOT/'street-light/export/StreetLight.glb','Town street light',(j*39+7,yy,0),yaw)
 if is_complex:
  for sx in (-1,0,1):
   for sy in (-1,1):lib.place(ROOT/'street-light/export/StreetLight.glb','Lot street light',(sx*W/3,sy*11.4,0),0 if sy>0 else 180)
 # Continuous, metric PBR turf around the public street and private parcels.
 # It supports neighbor roots at grade and closes the formerly flat backdrop.
 objects=lib.load(ground);turf=next(m for o in objects if o.type=='MESH' for m in o.data.materials if m.name.startswith('Lawn'))
 from kit.tiling import world_uv
 excluded=[(-220,220,yy-4.13,yy+4.13) for yy in (south,north)]
 if single:
  bw,bd=p['building']['width'],p['building']['depth'];edge=-bd/2-4.3
  excluded.extend([(-bw/2-.4,bw/2+.4,-bd/2-2,bd/2+2),(-75,75,edge-25,edge+3.5)])
 else:excluded.append((-W/2,W/2,-D/2,D/2) if is_complex else (-W/2,W/2,-depth/2-17,depth/2+10))
 xs=sorted({-220,220,*[v for q in excluded for v in q[:2]]});ys=sorted({-220,220,*[v for q in excluded for v in q[2:]]})
 for x0,x1 in zip(xs,xs[1:]):
  for y0,y1 in zip(ys,ys[1:]):
   if any(a<(x0+x1)/2<b and c<(y0+y1)/2<d for a,b,c,d in excluded):continue
   ob=G.box('Town continuous lawn',((x0+x1)/2,(y0+y1)/2,-.058),(x1-x0,y1-y0,.1),turf,0);world_uv(ob,3.048)
   names={n.layer_name or 'Color' for n in turf.node_tree.nodes if n.type=='VERTEX_COLOR'} or {'Color'}
   for name in names:
    attr=ob.data.color_attributes.new(name=name,type='FLOAT_COLOR',domain='POINT');ob.data.color_attributes.active_color=attr
    for v in attr.data:v.color=(.68,.70,.58,1)
 lib.clear();return lib.dependencies


def dusk_lights():
 # Unit room backings are behind their own windows. The warm pools and lenses
 # belong to presentation; shipped routing-mask emission remains unchanged.
 for ma in bpy.data.materials:
  if ma.get('presentation_emission_default') and ma.use_nodes:next(n for n in ma.node_tree.nodes if n.type=='BSDF_PRINCIPLED').inputs['Emission Strength'].default_value=ma['presentation_emission_default']
 for rt in list(bpy.context.scene.objects):
  if rt.get('presentation_only') and rt.name.startswith(('Town street light','Lot street light')):
   socket=next(o for o in rt.children_recursive if o.get('socket_kind')=='engine_light')
   ld=bpy.data.lights.new('Street pool','SPOT');ld.energy=950;ld.color=(1,.78,.47);ld.spot_size=math.radians(112);ld.spot_blend=.72;ld.shadow_soft_size=.18
   lamp=bpy.data.objects.new('Street pool',ld);bpy.context.collection.objects.link(lamp);lamp.matrix_world=socket.matrix_world.copy();lamp.location.z-=.06
 for ob in list(bpy.context.scene.objects):
  if ob.get('socket_kind')=='engine_light' and ob.get('light_kind'):
   point_light(ob['light_kind'].title()+' pool',ob.matrix_world.translation,float(ob['render_power_w']),radius=.09)


def match_context(meta,stem,plants=True):
 """Comparable near-ground materials/planting, outside the asset package."""
 p=meta['plan'];lib=Library();ground=ROOT/'ground/export/Ground.glb'
 if stem.startswith('Building'):
  d,w=p['depth'],p['width'];edge=-d/2-4.3
  if p['seed']!=305:lib.place(ground,'Photo foreground road',(0,edge-4.1,-.172),90,'Road_Straight_A',(1,100/6.096,1))
  lib.place(ground,'Photo curb',(0,edge,-.008),90,'Curb_Straight',(1,100/3.048,1))
  lib.place(ground,'Photo walk',(0,edge+1.0,0),90,'Sidewalk_A',(1,100/1.524,1))
  # Repeated native lawn modules have been flattened in the source family;
  # this single common-phase skin gives the photograph a comparable verge.
  objects=lib.load(ground);ma=next(m for o in objects if o.type=='MESH' for m in o.data.materials if m.name.startswith('Lawn'))
  if p['seed']==305:
   asphalt=next(m for o in objects if o.type=='MESH' for m in o.data.materials if m.name.startswith('Asphalt'))
   lot=G.box('Photo apartment parking',(0,edge-12.5,-.06),(150,25,.10),asphalt,0)
   from kit.tiling import world_uv
   world_uv(lot,6.096);vc=lot.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');lot.data.color_attributes.active_color=vc
   for c in vc.data:c.color=(1.,.98,.94,1)
   vehicles=[ROOT/'cars/export'/name for name in ('AlderC150.glb','AlderX220.glb','AlderH120.glb')]
   for j,x in enumerate((-w*.32,-w*.10,w*.19,w*.39)):
    path=vehicles[j%3]
    if path.exists():lib.factory(lib.place(path,'Photo parked car',(x,edge-3.2,0),0),j+2)
  ob=G.box('Photo front lawn',(0,edge+2.7,-.08),(w+20,3.4,.13),ma,0)
  from kit.tiling import world_uv
  world_uv(ob,3.048);tint=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');ob.data.color_attributes.active_color=tint
  for c in tint.data:c.color=(.7,.72,.6,1)
  if plants:
   from landscaping import foundations
   foundations(lib,p,ROOT,stem)
 else:
  from landscaping import foundations
  foundations(lib,p,ROOT,stem)
  width=p['count']*p['width']+12;edge=-p['depth']/2-11.2
  lib.place(ground,'Photo townhouse public street',(0,edge,-.172),90,'Road_Straight_A',(1,(width+50)/6.096,1))
  for j,marker in enumerate([o for o in bpy.context.scene.objects if o.get('presentation_kind')=='tree']):
   lib.place(ROOT/'trees/export/RedMaple.glb','Photo '+marker.name,marker.matrix_world.translation,j*39)
 lib.clear();return lib.dependencies
