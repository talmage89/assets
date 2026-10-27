"""Measured checkpoint construction: casts on meshes, independent of exporters."""
import math
import bpy
from mathutils import Vector
from plan import wall_frame
from check_mesh import surface


def check(p,meta,obs):
 m,g=p['blocks'];walls=surface([o for o in obs if o.get('component')=='wall']);rows=[]
 roofpoints=[o.matrix_world@v.co for o in obs if o.get('component')=='roof' and o.get('block')=='Main' for v in o.data.vertices]
 front_edge=min(v.y for v in roofpoints)
 # Plain brick pier below a bedroom, clear of its sill and any crawl vent.
 x=m.x0+m.width*(.13 if p['spec']['garage']['side']=='right' else .87)
 hit=walls.ray_cast(Vector((x,m.y0-2,m.floor+.45)),Vector((0,1,0)),3)[0]
 assert hit is not None,'No front wall for overhang measurement'
 clear=hit.y-front_edge
 for opening in meta['openings']:
  ob=next((v for v in obs if v.get('component')=='window' and v.name==opening['id']),None)
  masonry=next((v for v in obs if v.get('opening_id')==opening['id']),None)
  if ob is None or masonry is None:continue
  block=next(v for v in p['blocks'] if v.name==opening['block']);origin,t,n,l=wall_frame(block,opening['face']);normal=Vector((*n,0))
  def point(u,v,z):return Vector((origin[0]+t[0]*u+n[0]*v,origin[1]+t[1]*u+n[1]*v,z))
  u,z,w,h=(opening[k] for k in ('u','z','w','h'))
  frame=surface([ob]);brick=walls.ray_cast(point(u-w/2-.09,.4,z+.1),-normal,.7)[0]
  rail=frame.ray_cast(point(u,.4,z+h-.025),-normal,.9)[0]
  if brick is None or rail is None:raise AssertionError('Unmeasurable masonry frame '+opening['id'])
  setback=(brick-rail).dot(normal);assert .0762<=setback<=.105,('Window setback',opening['id'],setback)
  sill=surface([masonry]);count=math.ceil((w+.1524)/(.2032/3));su=u-(w+.1524)/2+(w+.1524)/count/2
  backs=sill.ray_cast(point(su,-.060,z+.1),Vector((0,0,-1)),.4)[0];fronts=sill.ray_cast(point(su,.100,z+.1),Vector((0,0,-1)),.4)[0]
  assert backs is not None and fronts is not None,'Missing rowlock'
  slope=math.degrees(math.atan2(backs.z-fronts.z,.160));assert 7<slope<10,('Sill slope',slope)
  row=dict(opening=opening['id'],setback_m=setback,sill_slope_degrees=slope)
  # Wainscot stops below the header and correctly has no steel angle above it.
  if p['spec']['wall_mix']!='wainscot':
   a=sill.ray_cast(point(u,.04,z+h+.11),Vector((0,0,-1)),.2)[0];b=sill.ray_cast(point(u,.04,z+h-.10),Vector((0,0,1)),.2)[0]
   gauge=a.z-b.z if a is not None and b is not None else None
   assert gauge is not None and abs(gauge-.004)<2e-6,('Lintel',gauge)
   row['lintel_gauge_m']=gauge
  rows.append(row)
 posts=next(o for o in obs if o.get('component')=='porch_structure');beam=next(o for o in obs if o.get('component')=='porch_beam')
 maxpost=max((posts.matrix_world@v.co).z for v in posts.data.vertices);minbeam=min((beam.matrix_world@v.co).z for v in beam.data.vertices)
 assert abs(maxpost-minbeam)<2e-6,('Post/beam bearing',maxpost,minbeam)
 chimney=next((o for o in obs if o.get('component')=='chimney'),None);shaft=None;flashing={}
 if chimney:
  points=[chimney.matrix_world@v.co for v in chimney.data.vertices]
  if p['spec']['chimney']=='gable':assert abs(min(v.z for v in points))<1e-6,'Chimney grade bearing'
  mid=Vector(tuple((min(q[k] for q in points)+max(q[k] for q in points))/2 for k in range(3)));mid.z=max(q.z for q in points)-.70
  tree=surface([chimney]);spans=[]
  for axis in (Vector((1,0,0)),Vector((0,1,0))):
   a=tree.ray_cast(mid,axis,3)[0];b=tree.ray_cast(mid,-axis,3)[0];assert a is not None and b is not None
   spans.append((a-b).length)
  shaft=sorted(spans);assert abs(shaft[0]-.6096)<1e-5 and .9144<=shaft[1]<=1.524,('Chimney shaft',shaft)
  counter=next(o for o in obs if o.get('flashing_kind')=='counter');fronts=[];backs=[]
  # Each counter piece retains eight prism vertices after triangulation.
  for i in range(0,len(counter.data.vertices),8):
   vv=[counter.matrix_world@v.co for v in counter.data.vertices[i:i+8]]
   for points,dest in ((vv[:4],fronts),(vv[4:],backs)):
    point=sum(points,Vector())/4;nearest=tree.find_nearest(point);dest.append((point-nearest[0]).dot(nearest[1]))
  assert max(abs(v-.001) for v in fronts)<2e-6 and max(abs(v+.002) for v in backs)<2e-6,('Counterflashing bed',fronts,backs)
  aprons=next(o for o in obs if o.get('flashing_kind')=='apron');roof=surface([o for o in obs if o.get('component')=='roof']);gaps=[]
  for poly in aprons.data.polygons:
   if poly.normal.z<.5:continue
   point=sum((aprons.matrix_world@aprons.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices)
   hit=roof.ray_cast(point+Vector((0,0,.1)),Vector((0,0,-1)),.3)[0]
   assert hit is not None,'Flashing misses roof';gaps.append(point.z-hit.z)
  assert min(gaps)>.008 and max(gaps)<.013,('Apron/roof offset',gaps)
  flashing=dict(counter_pieces_measured=len(fronts),outer_offset_max_m=max(fronts),bed_depth_min_m=-max(backs),apron_samples=len(gaps),apron_roof_gap_min_m=min(gaps),apron_roof_gap_max_m=max(gaps))
 # Deep overhang is evaluated against actual veneer, not the structural datum.
 expected=p['spec']['main']['overhang']-.072
 assert abs(clear-expected)<1e-5,('Clear overhang',clear,expected)
 return dict(clear_front_overhang_measured_m=clear,windows=rows,post_beam_gap_measured_m=minbeam-maxpost,chimney_shaft_measured_m=shaft,chimney_flashing_measured=flashing)
