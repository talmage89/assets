"""Same-worktree ground-library streets. Presentation only, never exported.

The station supplies its commercial curb cuts and near sidewalk. The road
intersection, opposite curbs, walks and lawns retain the ground family's
geometry, real road crown and delivered materials.
"""
import hashlib,math
from pathlib import Path
import bpy
from geometry import root,mesh
from ground_adapter import FLOW


def _neighborhood_ground(meta):
 repo=Path(__file__).resolve().parents[2];path=repo/'ground/export/Ground.glb'
 before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path))
 library_objects=set(bpy.context.scene.objects)-before;library={o.name:o for o in library_objects if o.parent not in library_objects}
 parent=root('GroundPresentation',yaw=meta['yaw'],kind='CONTEXT');placed=[]
 def place(kind,name,loc,yaw=0,scale=(1,1,1)):
  source=library[kind];copies={}
  for ob in [source,*source.children_recursive]:
   cp=ob.copy();bpy.context.collection.objects.link(cp);copies[ob]=cp;placed.append(cp)
  for ob,cp in copies.items():cp.parent=copies.get(ob.parent,parent);cp.matrix_basis=ob.matrix_basis.copy();cp.name=name+'__'+ob.name
  rt=copies[source];rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw));rt.scale=scale
  from paving import context_road
  for cp in copies.values():context_road(cp,kind)
  return rt
 W,D=meta['lot'];core=8.6868;face=4.1148;back=4.2672;walkin=6.096
 cx=-W/2+1.2192-core;cy=-D/2+1.2192-core
 east=W/2+12.5;north=D/2+12.5;extent=250
 # A real four-corner neighborhood block. Every street continues beyond the
 # photographic frame; native crowns, curbs and walk widths stay unchanged.
 for gx in (cx,east):
  for gy in (cy,north):
   place('Road_Intersection','Neighborhood intersection',(gx,gy,FLOW))
   for yaw in (0,90,180,270):
    if gx==cx and gy==cy and yaw==0:continue
    cs,sn=math.cos(math.radians(yaw)),math.sin(math.radians(yaw))
    loc=(gx+cs*core-sn*core,gy+sn*core+cs*core,FLOW)
    for kind in ('Curb_Corner','Sidewalk_Corner','Lawn_CornerStrip','Lawn_CornerYard'):place(kind,'Neighborhood corner '+kind,loc,yaw)
 def street(axis,center,lo,hi):
  yaw=0 if axis==1 else 270
  def xy(x,y):return (center+x,y,FLOW) if axis==1 else (y,center-x,FLOW)
  def module(kind,label,transverse,start,end,native,side=1):
   # Existing station construction owns its two near curbs/walks.
   near=(axis==1 and center==cx and side==1) or (axis==0 and center==cy and side==-1)
   spans=[(start,end)]
   if near:
    cutlo,cutend=(-D/2+1.2192,D/2) if axis==1 else (-W/2+1.2192,W/2)
    spans=[(start,min(end,cutlo)),(max(start,cutend),end)]
   for a,b in spans:
    if b-a>.001:place(kind,label,xy(transverse,(a+b)/2),yaw+(180 if side<0 else 0),scale=(1,(b-a)/native,1))
  n=math.ceil((hi-lo)/6.096)
  for i in range(n):
   a=lo+i*6.096;b=min(hi,a+6.096);v=(a+b)/2
   place('Road_Straight_A','Neighborhood road',xy(0,v),yaw,scale=(1,(b-a)/6.096,1))
   for side in (-1,1):
    for j in range(2):module('Curb_Straight','Neighborhood curb',side*face,a+(b-a)*j/2,a+(b-a)*(j+1)/2,3.048,side)
    module('Lawn_Strip','Neighborhood verge',side*back,a,b,3.048,side)
    for j in range(4):module('Sidewalk_A','Neighborhood walk',side*walkin,a+(b-a)*j/4,a+(b-a)*(j+1)/4,1.524,side)
 for x in (cx,east):
  for lo,hi in ((-extent,cy-core),(cy+core,north-core),(north+core,extent)):street(1,x,lo,hi)
 for y in (cy,north):
  for lo,hi in ((-extent,cx-core),(cx+core,east-core),(east+core,extent)):street(0,y,lo,hi)
 # Adjacent private lawn, kept out of the road and station. It uses the
 # library's exact material; no pale green scalar backdrop is introduced.
 turf=next(m for ob in library_objects if ob.type=='MESH' for m in ob.data.materials if m.name.startswith('Lawn'))
 from kit.tiling import world_uv
 walkout=7.62
 excluded=[(x-walkout,x+walkout,-250,250) for x in (cx,east)]
 excluded += [(-250,250,y-walkout,y+walkout) for y in (cy,north)]
 excluded += [(x-core,x+core,y-core,y+core) for x in (cx,east) for y in (cy,north)]
 excluded += [(-W/2-3.81,W/2+.005,-D/2-3.81,D/2+.005)]
 # Preserve the split-level's sunken drive in presentation lawns as well.
 from plan import rotate
 import json
 houses=[]
 for i in range(7):
  houses.append(('houses/export/HearthfieldCape-31.gltf' if i%3==0 else 'houses/export/HearthfieldRanch-11.gltf' if i%3==1 else 'houses/export/HearthfieldSplit-51.gltf',(-15+i*27,north+23,0),0))
 for i in range(6):
  houses.append(('houses/export/HearthfieldRanch-11.gltf' if i%2==0 else 'houses/export/HearthfieldCape-31.gltf',(east+21,-15+i*29,0),-90))
 for i in range(5):
  houses.append(('houses/export/HearthfieldSplit-51.gltf',(cx-24,-8+i*28,0),90))
  houses.append(('houses/export/HearthfieldCape-31.gltf',(-6+i*29,cy-21,0),180))
 for relative,location,yaw in houses:
  data=json.loads((repo/relative).with_suffix('.json').read_text());drive=data.get('driveway')
  if drive:
   points=[rotate((x,y),yaw) for x in (drive['x']-drive['width']/2-.07,drive['x']+drive['width']/2+.07) for y in (drive['front']-.07,drive['back']+.07)]
   excluded.append((location[0]+min(q[0] for q in points),location[0]+max(q[0] for q in points),location[1]+min(q[1] for q in points),location[1]+max(q[1] for q in points)))
 xs=sorted({-250,250,*[q for r in excluded for q in r[:2]]});ys=sorted({-250,250,*[q for r in excluded for q in r[2:]]})
 regions=[]
 for x0,x1 in zip(xs,xs[1:]):
  for y0,y1 in zip(ys,ys[1:]):
   if not any(a<(x0+x1)/2<b and c<(y0+y1)/2<d for a,b,c,d in excluded):regions.append((x0,x1,y0,y1))
 for i,(x0,x1,y0,y1) in enumerate(regions):
  ob=mesh('Neighbor lawn '+str(i),[(x0,y0,-.006),(x1,y0,-.006),(x1,y1,-.006),(x0,y1,-.006)],[(0,1,2,3)],turf,parent,False);world_uv(ob,3.048)
  for node in turf.node_tree.nodes:
   if node.type=='VERTEX_COLOR':
    color=ob.data.color_attributes.get(node.layer_name or 'Color') or ob.data.color_attributes.new(name=node.layer_name or 'Color',type='FLOAT_COLOR',domain='POINT')
    for value in color.data:value.color=(1,1,1,1)
    ob.data.color_attributes.active_color=color
 for ob in library_objects:bpy.data.objects.remove(ob,do_unlink=True)
 dressing=[]
 # Import each original once, snapshot its unparented basis, then instance
 # from that immutable template. This avoids a second copy inheriting the
 # first placement's transform and disappearing behind the camera.
 from context import bundle
 placements={}
 for relative,location,yaw in houses:placements.setdefault(relative,[]).append((location,yaw))
 placements['trees/export/PinOak.glb']=[((x,north+12,0),i*43) for i,x in enumerate((-14,15,43,71,101,131,160))]+[((east+12,y,0),i*37) for i,y in enumerate((-15,17,49,80,115,148))]
 placements['trees/export/RedMaple.glb']=[((x,north+38,0),i*51) for i,x in enumerate((-32,0,32,61,93,124,154))]+[((cx-13,y,0),i*31) for i,y in enumerate((2,40,78,114))]
 placements['street-light/export/StreetLight.glb']=[((x,north-5.0,.001),180) for x in (-16,14,46,78,110,142)]+[((east-5.0,y,.001),90) for y in (-18,14,46,78,110,142)]+[((cx-5.0,y,.001),-90) for y in (4,40,76,112)]
 for relative,instances in placements.items():
  source=repo/relative
  if not source.exists():raise FileNotFoundError('Missing read-only presentation export: '+relative)
  before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(source));added=set(bpy.context.scene.objects)-before
  templates={ob:(ob.parent,ob.matrix_basis.copy()) for ob in added}
  for index,(location,yaw) in enumerate(instances):
   copies={ob:ob.copy() for ob in added}
   rt=root('Neighbor_'+Path(relative).stem+'_'+str(index),location,yaw,parent=parent,kind='CONTEXT')
   rt['presentation_neighbor']=True
   for ob,cp in copies.items():
    bpy.context.collection.objects.link(cp);original_parent,basis=templates[ob];cp.parent=copies.get(original_parent,rt);cp.matrix_basis=basis
    cp['presentation_neighbor']=True
  for ob in added:bpy.data.objects.remove(ob,do_unlink=True)
  dressing.append(bundle(source))
 return parent,dict(source='ground/export/Ground.glb',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),placed_modules=len(placed),neighbor_dependencies=dressing,scope='Library street grid and instanced original houses/trees/lights, presentation only; all canonical files immutable')


def _accepted_ground(meta):
 repo=Path(__file__).resolve().parents[2];path=repo/'ground/export/Ground.glb'
 before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path))
 library_objects=set(bpy.context.scene.objects)-before;library={o.name:o for o in library_objects if o.parent not in library_objects}
 parent=root('GroundPresentation',yaw=meta['yaw'],kind='CONTEXT');placed=[]
 def place(kind,name,loc,yaw=0,scale=(1,1,1)):
  source=library[kind];copies={}
  for ob in [source,*source.children_recursive]:
   cp=ob.copy();bpy.context.collection.objects.link(cp);copies[ob]=cp;placed.append(cp)
  for ob,cp in copies.items():cp.parent=copies.get(ob.parent,parent);cp.matrix_basis=ob.matrix_basis.copy();cp.name=name+'__'+ob.name
  rt=copies[source];rt.location=loc;rt.rotation_mode='XYZ';rt.rotation_euler=(0,0,math.radians(yaw));rt.scale=scale
  from paving import context_road
  for cp in copies.values():context_road(cp,kind)
  return rt
 W,D=meta['lot'];core=8.6868;face=4.1148;back=4.2672;walkin=6.096
 cx=-W/2+1.2192-core;cy=-D/2+1.2192-core
 place('Road_Intersection','Street intersection',(cx,cy,FLOW))
 # Four arms grow out of the intersection. The station is the NE lot.
 for yaw in (0,90,180,270):
  cs,sn=math.cos(math.radians(yaw)),math.sin(math.radians(yaw))
  def xy(x,y):return (cx+cs*x-sn*y,cy+sn*x+cs*y,FLOW)
  for i in range(13):
   v=core+(i+.5)*6.096
   place('Road_Straight_A',f'Street{yaw}_{i}',xy(0,v),yaw)
   for side in (-1,1):
    # Existing property interfaces occupy the east side of the N arm and
    # north side of E arm. Every other curb/walk uses actual stock modules.
    near=(yaw==0 and side==1) or (yaw==270 and side==-1)
    pyaw=yaw+(180 if side<0 else 0)
    cutoff=(D/2-cy if yaw==0 else W/2-cx) if near else -1e6
    def segment(kind,label,x,center,length,native):
     lo=max(center-length/2,cutoff);hi=center+length/2
     if hi-lo>.001:place(kind,label,xy(x,(lo+hi)/2),pyaw,scale=(1,(hi-lo)/native,1))
    for j in (-1,1):segment('Curb_Straight',f'Curb{yaw}_{side}_{i}_{j}',side*face,v+j*1.524,3.048,3.048)
    segment('Lawn_Strip',f'Verge{yaw}_{side}_{i}',side*back,v,6.096,3.048)
    for j in (-3,-1,1,3):segment('Sidewalk_A',f'Walk{yaw}_{side}_{i}_{j}',side*walkin,v+j*.762,1.524,1.524)
 for yaw in (90,180,270):
  cs,sn=math.cos(math.radians(yaw)),math.sin(math.radians(yaw));loc=(cx+cs*core-sn*core,cy+sn*core+cs*core,FLOW)
  for kind in ('Curb_Corner','Sidewalk_Corner','Lawn_CornerStrip','Lawn_CornerYard'):place(kind,'Other corner '+str(yaw)+kind,loc,yaw)
 # Adjacent private lawn, kept out of the road and station. It uses the
 # library's exact material; no pale green scalar backdrop is introduced.
 turf=next(m for ob in library_objects if ob.type=='MESH' for m in ob.data.materials if m.name.startswith('Lawn'))
 from kit.tiling import world_uv
 extent=core+13*6.096;walkout=7.62
 excluded=[(cx-walkout,cx+walkout,cy-extent,cy+extent),(cx-extent,cx+extent,cy-walkout,cy+walkout),
           (cx-core,cx+core,cy-core,cy+core),(-W/2-3.81,W/2+.005,-D/2-3.81,D/2+.005)]
 xs=sorted({-250,250,*[q for r in excluded for q in r[:2]]});ys=sorted({-250,250,*[q for r in excluded for q in r[2:]]})
 regions=[]
 for x0,x1 in zip(xs,xs[1:]):
  for y0,y1 in zip(ys,ys[1:]):
   if not any(a<(x0+x1)/2<b and c<(y0+y1)/2<d for a,b,c,d in excluded):regions.append((x0,x1,y0,y1))
 for i,(x0,x1,y0,y1) in enumerate(regions):
  ob=mesh('Neighbor lawn '+str(i),[(x0,y0,-.006),(x1,y0,-.006),(x1,y1,-.006),(x0,y1,-.006)],[(0,1,2,3)],turf,parent,False);world_uv(ob,3.048)
  for node in turf.node_tree.nodes:
   if node.type=='VERTEX_COLOR':
    color=ob.data.color_attributes.get(node.layer_name or 'Color') or ob.data.color_attributes.new(name=node.layer_name or 'Color',type='FLOAT_COLOR',domain='POINT')
    for value in color.data:value.color=(1,1,1,1)
    ob.data.color_attributes.active_color=color
 for ob in library_objects:bpy.data.objects.remove(ob,do_unlink=True)
 dressing=[]
 # Neighboring originals give glass something real to reflect and prevent a
 # bare horizon. Their own exports remain read-only presentation dependencies.
 for relative,locations in (
  ('trees/export/PinOak.glb',[(W/2+18,D/2+18,0),(-W/2+6,D/2+12,0)]),
  ('houses/export/HearthfieldSplit-51.gltf',[(-W/2-28,10,0),(9,D/2+17,0)])):
  source=repo/relative
  if not source.exists():continue
  before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(source));added=set(bpy.context.scene.objects)-before
  anchors=[o for o in added if o.parent not in added]
  for index,location in enumerate(locations):
   copies={ob:(ob if index==0 else ob.copy()) for ob in added}
   if index:
    for cp in copies.values():bpy.context.collection.objects.link(cp)
   rt=root('Neighbor_'+Path(relative).stem+'_'+str(index),location,90 if index==0 else 0,parent=parent,kind='CONTEXT')
   for ob,cp in copies.items():cp.parent=copies.get(ob.parent,rt);cp.matrix_basis=ob.matrix_basis.copy()
  from context import bundle
  dressing.append(bundle(source))
 return parent,dict(source='ground/export/Ground.glb',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),placed_modules=len(placed),neighbor_dependencies=dressing,scope='Library geometry/materials with copied presentation-road color fields; all canonical files immutable')


def ground(meta,neighborhood=False):
 return _neighborhood_ground(meta) if neighborhood else _accepted_ground(meta)
