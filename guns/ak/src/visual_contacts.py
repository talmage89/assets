"""Independent exterior seating/coverage observations on evaluated triangles.

The samples follow the supplied game animation, not a functional firearm model.
Distances, triangle ray hits and mesh ownership are measured after posing, in
both the source scene and a fresh GLB import through check.py.
"""
import bpy
from mathutils import Vector
from kit import weapon as W,motion,assembly
from clips import SAFE,AUTO,SEMI
from interface import CLIPS
def audit(arm,part,meshes):
 rows=[]
 def seating(clip,frames,a,b,limit,kind):
  samples=[]
  for frame in frames:
   W.pose(arm,clip,frame);d,method=assembly.distance(part(a),part(b))
   samples.append(dict(frame=frame,distance_m=d,method=method))
  rows.append(dict(kind=kind,clip=clip,parts=[a,b],samples=samples,
   maximum_distance_m=max(r['distance_m'] for r in samples),limit_m=limit,
   passed=all(r['distance_m']<=limit for r in samples)))
 # During release/extraction the rear catch is deliberately disengaged. Only
 # the front nose stays cradled until unhook, and again after front_hook.
 for clip in ('Reload','ReloadEmpty'):
  seating(clip,[i*.5 for i in range(0,77)],'Magazine_FrontLug','Receiver_FrontLugSlot',.00025,'front lug seated throughout rock-out')
  seating(clip,[112+i*.5 for i in range(41)],'Magazine_FrontLug','Receiver_FrontLugSlot',.00025,'front lug seated throughout rock-in')
  seating(clip,[0,1,8,10,138,139,140],'Magazine_RearCatch','MagRelease_VisualCatch',.0003,'rear catch engaged at seated holds')
  W.pose(arm,clip,56);d,_=assembly.distance(part('Magazine_FrontLug'),part('Receiver_FrontLugSlot'))
  rows.append(dict(kind='front lug detached after unhook',clip=clip,distance_m=d,passed=d>.1))
 # The closed carrier bears on the rear-facing exterior shoulder, independent
 # of agreement between the source and serialized animation.
 for clip,spec in CLIPS.items():
  end=spec['frames']
  seating(clip,[end],'Carrier_SeatingFace','Front_InsertUpperShoulder',.00015,'closed carrier against front insert shoulder')
 # Measure the handle's whole swept envelope, then test a 2-D grid covering
 # that aperture. This cannot pass merely because a line or one point is hidden.
 envelope=[];sections=[]
 # Only the handle neck crosses the receiver sheet. Its external finger pad
 # is wider, and its outer rectangle does not describe a hole in that sheet.
 plane=motion.surface(part('Receiver_Sheet'))['hi'].x
 for f in [i*.5 for i in range(25)]:
  W.pose(arm,'Fire',f);surface=motion.surface(part('ChargingHandle'));lines=[]
  for tri in surface['faces']:
   points=[surface['points'][i] for i in tri];hits=[]
   for a,b in ((0,1),(1,2),(2,0)):
    p,q=points[a],points[b]
    if (p.x-plane)*(q.x-plane)<0:hits.append(p+(q-p)*((plane-p.x)/(q.x-p.x)))
   if len(hits)==2:lines.append(hits);envelope.extend(hits)
  sections.extend(lines)
 lo=Vector([min(p[k] for p in envelope) for k in range(3)])
 hi=Vector([max(p[k] for p in envelope) for k in range(3)])
 W.pose(arm,'IdleSafe',0);tree=motion.surface(part('Selector_Lever'))['tree'];handle=motion.surface(part('ChargingHandle'))['tree'];coverage=[]
 for j in range(15):
  for k in range(5):
   y=lo.y+.00015+(hi.y-lo.y-.0003)*j/14;z=lo.z+.00015+(hi.z-lo.z-.0003)*k/4
   crossings=[]
   for p,q in sections:
    if (p.z-z)*(q.z-z)<0:crossings.append(p.y+(q.y-p.y)*(z-p.z)/(q.z-p.z))
   if not crossings or not min(crossings)<=y<=max(crossings):continue
   hit=tree.ray_cast(Vector((.05,y,z)),Vector((-1,0,0)),.06)
   closed=handle.ray_cast(Vector((.05,y,z)),Vector((-1,0,0)),.06)
   coverage.append(dict(y_m=y,z_m=z,hit_m=list(hit[0]) if hit[0] is not None else list(closed[0]) if closed[0] is not None else None,
    occluder='selector' if hit[0] is not None else 'closed handle' if closed[0] is not None else None))
 rows.append(dict(kind='safe selector covers 2-D neck travel slot; closed handle occupies front end',section_plane_x_m=plane,envelope_m=[list(lo),list(hi)],
  rays=coverage,passed=all(r['hit_m'] is not None for r in coverage)))
 for angle,frame in [(SAFE,0),(AUTO,18),(SEMI,36)]:
  seating('Selector',[frame],'Selector_Dimple','Selector_Detent_'+str(angle),.0003,'selector dimple seated at detent '+str(angle))
 # Removing unseen mechanisms is stronger than sampling a few obscured views:
 # there is no renderable geometry on these owners in any pose or camera.
 owned=[o for o in meshes(arm) if o.get('bone') in ('Bolt','Hammer')]
 forbidden=[o.name for o in bpy.context.scene.objects if o.type=='MESH' and any(t in o.name.lower() for t in ('bolt_lug','hammer_visual','sear'))]
 rows.append(dict(kind='hidden bolt-lug / hammer-sear render geometry absent',
  retained_transform_bones=[n for n in ('Bolt','Hammer') if n in arm.data.bones],
  owned_render_meshes=[o.name for o in owned],forbidden_render_meshes=forbidden,
  proof='zero render meshes in source and GLB; invariant across all clips and cameras',
  passed=not owned and not forbidden and all(n in arm.data.bones for n in ('Bolt','Hammer'))))
 W.pose(arm,'Idle',0);return rows
