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


def ground(meta):
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
