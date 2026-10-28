"""Measured form / serialized animation checkpoint audit; no UV or bake claim."""
import argparse,sys,json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit import weapon,motion
sys.path.insert(0,str(Path(__file__).parent))
from contacts import measure

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='build/pistol.blend');p.add_argument('--out',default='build/check.json');p.add_argument('--motion',action='store_true');p.add_argument('--dense-source',action='store_true',help='Audit sculpt geometry; game triangle budget does not apply');p.add_argument('--step',type=float,default=.5);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 source=Path(a.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source))
 arm=bpy.data.objects['PistolArmature'];weapon.pose(arm,None,0)
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and 'bone' in o and o.parent==arm]
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 low=Vector(tuple(min(v[k] for v in points) for k in range(3)));high=Vector(tuple(max(v[k] for v in points) for k in range(3)))
 dims=high-low;counts={o.name:sum(len(f.vertices)-2 for f in o.data.polygons) for o in parts}
 bad={};boundaries={}
 for o in parts:
  bm=bmesh.new();bm.from_mesh(o.data)
  edges=sum(not e.is_manifold for e in bm.edges);bm.free()
  if edges:boundaries[o.name]=edges
  if edges and not o.get('allow_boundary'):bad[o.name]=edges
 sockets={o.name:list(o.matrix_world.translation) for o in bpy.context.scene.objects if o.name.startswith('Socket_')}
 clips=[t.name for t in arm.animation_data.nla_tracks]
 result=dict(stage='dense sculpt source; no game triangle budget' if a.dense_source else 'form checkpoint; UV/bake/final delivery checks deferred',bounds_m=dict(low=list(low),high=list(high),size=list(dims)),
       triangles=sum(counts.values()),per_part=counts,materials=len({m.name for o in parts for m in o.data.materials if m}),
       sockets_blender_m=sockets,clips=clips,bones=list(arm.data.bones.keys()),nonmanifold=bad,declared_boundaries=boundaries)
 tube=bpy.data.objects['Barrel_Tube']
 barrel_length=max(v.co.y for v in tube.data.vertices)-min(v.co.y for v in tube.data.vertices)
 result['barrel_length_m']=barrel_length
 result['slide_width_m']=max(v.co.x for v in bpy.data.objects['Slide_Shell'].data.vertices)-min(v.co.x for v in bpy.data.objects['Slide_Shell'].data.vertices)

 def section(ob,z):
  ob.data.calc_loop_triangles();pts=[]
  for tri in ob.data.loop_triangles:
   v=[ob.matrix_world@ob.data.vertices[i].co for i in tri.vertices]
   for p,q in zip(v,v[1:]+v[:1]):
    if (p.z-z)*(q.z-z)<0:pts.append(p+(q-p)*((z-p.z)/(q.z-p.z)))
  return dict(x_min=min(p.x for p in pts),x_max=max(p.x for p in pts),y_min=min(p.y for p in pts),y_max=max(p.y for p in pts))
 g=bpy.data.objects['Frame_Grip'];mid=section(g,-.020);lower=section(g,-.036);upper=section(g,-.012)
 center=lambda r:(r['y_min']+r['y_max'])/2
 mold=motion.surface(g)['tree']
 def hit(start,direction):
  r=mold.ray_cast(Vector(start),Vector(direction),.3);assert r[0] is not None;return r[0]
 rear=hit((0,.04,.009),(0,-1,0));front=hit((0,.04,.009),(0,1,0))
 bottom=hit((.0055,.050,.010),(0,0,-1));top=hit((.0055,.050,.010),(0,0,1))
 centerbottom=hit((0,.050,.010),(0,0,-1))
 outerfront=hit((0,.100,.009),(0,-1,0));outerbottom=hit((0,.050,-.030),(0,0,1))
 shoe=motion.surface(bpy.data.objects['Trigger_Shoe'])['tree'];trigger=shoe.ray_cast(Vector((.002,.100,.017)),Vector((0,-1,0)),.2)[0]
 reach=trigger.y-section(g,.017)['y_min']
 slideob=bpy.data.objects['Slide_Shell'];result['form_measurements']=dict(
  slide_height_m=max(v.co.z for v in slideob.data.vertices)-min(v.co.z for v in slideob.data.vertices),
  slide_length_m=max(v.co.y for v in slideob.data.vertices)-min(v.co.y for v in slideob.data.vertices),
  grip_mid_width_m=mid['x_max']-mid['x_min'],grip_mid_depth_m=mid['y_max']-mid['y_min'],
  grip_rake_degrees=math.degrees(math.atan((center(upper)-center(lower))/.024)),
  guard_inner_length_at_mid_m=front.y-rear.y,guard_inner_height_m=top.z-bottom.z,
  guard_front_wall_m=outerfront.y-front.y,guard_bottom_wall_m=centerbottom.z-outerbottom.z,
  trigger_reach_at_17mm_m=reach,sections=dict(lower=lower,mid=mid,upper=upper))
 sights=[o for o in parts if o.name.startswith('Sight_Dovetail')]
 centers=sorted((min(v.co.y for v in o.data.vertices)+max(v.co.y for v in o.data.vertices))/2 for o in sights)
 result['form_measurements']['sight_radius_m']=centers[-1]-centers[0]
 # Actual local surround samples, rather than an extrusion thickness labeled
 # as stand-off. The front/bottom wrap of the grip is intentionally excluded.
 release=motion.surface(bpy.data.objects['MagRelease_Button'])
 stand=[]
 for y,z in ((.0095,.010),(.0165,.0182)):
  point=hit((-.025,y,z),(1,0,0));distance=point.x-release['lo'].x
  stand.append(dict(surround_point_m=list(point),stand_proud_m=distance))
 result['form_measurements']['mag_release_stand_proud']=stand
 gauges=[]
 for z in (.024,.017,.007):
  front=shoe.ray_cast(Vector((.002,.100,z)),Vector((0,-1,0)),.2)[0]
  back=shoe.ray_cast(Vector((.002,.030,z)),Vector((0,1,0)),.2)[0]
  gauges.append(dict(z_m=z,side_thickness_m=front.y-back.y))
 result['form_measurements']['trigger_shoe_gauges']=gauges
 skin=[]
 for y,z in ((.022,.0355),(.030,.0350),(.038,.0340)):
  point=hit((-.025,y,z),(1,0,0))
  assert point.x<-.0136,('stop cavity breaks exterior skin',list(point))
  skin.append(list(point))
 result['form_measurements']['stop_stem_exterior_skin_samples_m']=skin

 # A real sightline through the witness hole must see brass before barrel steel.
 start=Vector((0,.036,.070));direction=Vector((0,0,-1));hits=[]
 for ob in parts:
  location,normal,index,distance=motion.surface(ob)['tree'].ray_cast(start,direction,.03)
  if location is not None:hits.append((distance,ob.name))
 hits.sort();result['chamber_witness_first_surface']=dict(distance_m=hits[0][0],part=hits[0][1])
 errors=[]
 if not hits[0][1].startswith('ChamberRound'):errors.append('witness hole does not see chambered brass')
 if abs(barrel_length-.102)>.00005:errors.append('barrel visual length')
 for index,want in enumerate((.032,.1843,.128)):
  if abs(dims[index]-want)>.0005:errors.append(f'envelope axis {index}: {dims[index]} vs {want}')
 if not a.dense_source and not 25000<=sum(counts.values())<=35000:errors.append('triangle budget')
 if bad:errors.append('nonmanifold solids')
 fm=result['form_measurements']
 for key,lo,hi in [('grip_mid_width_m',.0295,.0310),('grip_mid_depth_m',.0495,.0515),
                   ('grip_rake_degrees',21.5,22.5),('guard_inner_length_at_mid_m',.032,.036),
                   ('guard_inner_height_m',.026,.028),('guard_front_wall_m',.0058,.0075),
                   ('guard_bottom_wall_m',.0058,.0075),('slide_length_m',.1739,.1741),
                   ('sight_radius_m',.1519,.1521)]:
  if not lo<=fm[key]<=hi:errors.append(f'{key}: {fm[key]} outside [{lo}, {hi}]')
 result['measurement_planes']=dict(guard_opening_x_m=.0055,guard_bar_center_gauge_x_m=0,
     guard_front_center_gauge_x_m=0,grip_sections_z_m=[-.036,-.020,-.012])
 result['required_contacts']=measure(arm)
 if a.motion:
  allow=[dict(a='Barrel_Tube',b='ChamberRound',reason='chambered round inside the visual chamber',max_penetration_m=.0006),
         dict(a='Barrel_Hood',b='ChamberRound',reason='chambered round in chamber bore',max_penetration_m=.0006),
         dict(a='Magazine_FeedLip',b='Magazine_TopRound',reason='feed lips retain top round at surface',max_penetration_m=.00015),
         dict(a='Magazine_Body',b='Magazine_TopRound',reason='feed lip retained round in upper magazine',max_penetration_m=.00015),
         dict(a='Magazine_Body',b='Magazine_SecondRound',reason='reserve round inside magazine shell',max_penetration_m=.00015),
         dict(a='Magazine_Follower',b='Magazine_SecondRound',reason='follower supports cartridges',max_penetration_m=.00015)]
  result['motion']=motion.sweep_clips(arm,clips,step_frames=a.step,tolerance_m=.0002,allow=allow)
  if not result['motion']['passed']:errors.append('motion crossings')
 result['errors']=errors;result['passed']=not errors
 Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('per_part','motion')},indent=2))
 if errors:raise RuntimeError(', '.join(errors))
if __name__=='__main__':main()
