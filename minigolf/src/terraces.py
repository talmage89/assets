"""Original retained banks and connected quarry shell, clipped to public surfaces."""
import math
from geometry import *
from plan import local,center,level,halfwidth
import paths

def clearance(ob,cutter):
 # A spatially disjoint reservation cannot remove rock. Passing it to Exact
 # on the fused concave shell can discard an exterior component instead.
 # Cull using evaluated world bounds, and remove the unused fabrication tool.
 a=[ob.matrix_world@Vector(q) for q in ob.bound_box];b=[cutter.matrix_world@Vector(q) for q in cutter.bound_box]
 if any(max(q[k] for q in a)<min(q[k] for q in b)-1e-5 or max(q[k] for q in b)<min(q[k] for q in a)-1e-5 for k in range(3)):
  bpy.data.objects.remove(cutter,do_unlink=True);return ob
 before=len(ob.data.polygons);name=cutter.name;G.boolean(ob,cutter)
 if ob.get('rock_seed')==1291:print('QUARRY CLEARANCE',name,before,'->',len(ob.data.polygons),flush=True)
 return ob

def build(p,rt):
 # Retaining construction follows the actual slab, with returns. Its crest
 # stays below the playing skin and never projects into the stance walk.
 for h in p['holes']:
  if h.get('crossing'):continue
  side=-paths.side(h);stations=[]
  for j in range(17):
   t=j/16;cx,cy=center(h,t);x=cx+side*(halfwidth(h,t)+.35);xx,yy,_=local(h,x,cy);crest=level(h,x,t)-.035;ground=.015+.065*max(0,yy+7)
   stations.append((xx,yy,ground,crest))
  sections=[]
  for i,(x,y,bottom,top) in enumerate(stations):
   a=Vector(stations[max(0,i-1)][:2]);b=Vector(stations[min(len(stations)-1,i+1)][:2]);d=(b-a).normalized();n=Vector((-d.y,d.x))
   sections.append([(x+n.x*dx,y+n.y*dx,z) for dx,z in ((-.13,bottom-.08),(.13,bottom-.08),(.13,top),(-.13,top))])
  wall=own(G.loft('Carved terrace retaining wall',sections,M['rocklight']),rt);wall['rock_seed']=1000+h['number']
  # Short timber returns key the wall into the graded berm at each end.
  for t in (0,1):
   cx,cy=center(h,t);a=local(h,cx+side*(halfwidth(h,t)+.35),cy,level(h,cx,t)-.12);b=local(h,cx+side*(halfwidth(h,t)+.90),cy,level(h,cx,t)-.12)
   beam('Retaining wall timber return',a,b,.1397,.1397,'wood',rt,edge_radius=0)
 # Carve crosswalk gaps through the retaining crest as well as the rockwork.
 from plan_check import hull
 for wall in [o for o in rt.children if o.name.startswith('Carved terrace retaining wall')]:
  points=[v.co for v in wall.data.vertices];wb=(min(q.x for q in points),max(q.x for q in points),min(q.y for q in points),max(q.y for q in points))
  for _,line,*_ in paths.adventure_links(p):
   poly=hull([q for quad in paths.ribbon(line,1.60) for q in quad]);bb=(min(q[0] for q in poly),max(q[0] for q in poly),min(q[1] for q in poly),max(q[1] for q in poly))
   if wb[1]<bb[0] or wb[0]>bb[1] or wb[3]<bb[2] or wb[2]>bb[3]:continue
   cutter=own(G.profile('Retaining crosswalk opening tool',poly,-1,9,M['black'],axis='Z'),rt)
   bpy.context.view_layer.update();clearance(wall,cutter)
 # Omit buried wall soles after all solid cuts; their shape is retained
 # in the construction source until the openings have been fabricated.
 for wall in [o for o in rt.children if o.name.startswith('Carved terrace retaining wall')]:
  bm=bmesh.new();bm.from_mesh(wall.data);bm.normal_update()
  buried=[f for f in bm.faces if f.normal.z<-.4 and all(v.co.z<.015+.065*max(0,v.co.y+7)-.01 for v in f.verts)]
  bmesh.ops.delete(bm,geom=buried,context='FACES');bm.to_mesh(wall.data);bm.free();wall['solid']=False
  wall.data.materials.clear();wall.data.materials.append(M['rocklight'])
  for face in wall.data.polygons:face.material_index=0
 # The north bank and central outcrops read as one landscape spine. Geometry
 # is cut around green/fixture and path reservations; it is not laid over them.
 shell=rock('Quarry terraced mountain',(0,19.9,.40),(18.0,12.2,4.1),rt,1291,'rocklight')
 for modifier in shell.modifiers:
  if modifier.type=='DECIMATE':modifier.ratio=.50
 # Fuse the existing fall body and west outcrop into this continuous shell.
 for old in list(rt.children_recursive):
  if old.type=='MESH' and old.name.startswith(('Quarry mountain','Western terraced outcrop')):
   bpy.context.view_layer.update();G.boolean(shell,old,'UNION')
 # Public raking-light viewpoint is an actual cut walking ledge, linked to
 # the stream bank; preserve the accepted world camera without burying it.
 walkline=[(-1.7,13.0),(-1.7,15.4),(-1.2,17.0)]
 from plan_check import hull
 pocket=hull([(x+dx,y+dy) for x,y in walkline for dx in (-1.10,1.10) for dy in (-.50,.50)])
 cutter=own(G.profile('Mountain viewing ledge clearance',pocket,-.5,9,M['black'],axis='Z'),rt)
 bpy.context.view_layer.update();clearance(shell,cutter)
 points=[(x,y,.065+.065*max(0,y+7)) for x,y in walkline]
 # Grade-backed 100 mm walk, open at the stream-bank end.
 vs=[]
 for x,y,z in points:vs.extend(((x-.762,y,z),(x+.762,y,z)))
 ob=mesh('Quarry viewing ledge walk',vs,[(0,1,3,2),(2,3,5,4)],'concrete',rt,False);ob['walking_surface']=True
 mod=ob.modifiers.new('Walk slab gauge','SOLIDIFY');mod.thickness=.10;mod.offset=-1;ob['buried_walk_bottom']=True
 # Rock shells use support-plane reservations, wider than the actual top faces.
 from plan_check import hull,strips
 for shell in [o for o in rt.children if o.get('rock_seed') in (1291,)]:
  for h in p['holes']:
   poly=hull([q for quad in strips(h,.48) for q in quad])
   cutter=own(G.profile('Terrace playing clearance tool',poly,-.5,9,M['black'],axis='Z'),rt)
   bpy.context.view_layer.update();clearance(shell,cutter)
  for h in p['holes']:
   line=paths.lane(h)
   poly=hull([q for quad in paths.ribbon(line,1.75) for q in quad])
   cutter=own(G.profile('Terrace walking clearance tool',poly,-.5,9,M['black'],axis='Z'),rt)
   bpy.context.view_layer.update();clearance(shell,cutter)
  routes=[line for _,line,*_ in paths.adventure_links(p)]+[[q[:2] for q in paths.quarry_ledge()]]
  for line in routes:
   poly=hull([q for quad in paths.ribbon(line,1.75) for q in quad])
   cutter=own(G.profile('Terrace connection clearance tool',poly,-.5,9,M['black'],axis='Z'),rt)
   bpy.context.view_layer.update();clearance(shell,cutter)

 # The plan reservations are conservative, but the end caps of a graded
 # slab differ from a planar routing ribbon. Clear the actual authored top
 # footprint, with 130 mm of fabrication allowance, at every public surface.
 for walkob in [o for o in rt.children_recursive if o.type=='MESH' and o.get('walking_surface')]:
  transform=rt.matrix_world.inverted()@walkob.matrix_world
  points=[transform@v.co for v in walkob.data.vertices];xy=[(v.x,v.y) for v in points]
  if not xy or max(x for x,y in xy)<-11 or min(x for x,y in xy)>11 or max(y for x,y in xy)<12 or min(y for x,y in xy)>28:continue
  profile=hull([(x+dx,y+dy) for x,y in xy for dx in (-.13,.13) for dy in (-.13,.13)])
  cutter=own(G.profile('Actual public surface clearance tool',profile,-1,9,M['black'],axis='Z'),rt)
  bpy.context.view_layer.update();clearance(shell,cutter)
 # Boolean tools carry a diagnostic black material. Cut quarry faces are
 # the same carved shotcrete as the outside; never export the tool pigment.
 for rockpart in [o for o in rt.children if o.get('rock_seed')==1291]:
  rockpart.data.materials.clear();rockpart.data.materials.append(M['rocklight'])
  for face in rockpart.data.polygons:face.material_index=0
