"""B24 viewpoints, with close-up strip camera and true optical aimed view."""
DEFAULT_SHOTS='right,left,side,top,front,aimed,bolt_open,deployed,folded,grip,optic,crown,wrist,port,rear_cocked,rear_fired,bottom,bipod_detail,rings'
SHOTS={
 'right':dict(location=(1.55,-.55,.78),target=(0,.20,.05),lens=55,aspect=1.8),
 'left':dict(location=(-1.6,-.52,.66),target=(0,.20,.05),lens=55,aspect=1.8),
 'side':dict(location=(2,.25,.055),target=(0,.25,.055),ortho=1.24,aspect=2.7),
 'top':dict(location=(0,.25,2),target=(0,.25,0),ortho=1.24,roll=1.5707963268,aspect=2.7),
 'front':dict(location=(0,2,.065),target=(0,.1,.065),ortho=.30,aspect=1),
 'aimed':dict(location=(0,-.2139,.113),target=(0,.3,.113),lens=42,aimed=True,aspect=1.35),
 'bolt_open':dict(location=(.46,-.18,.30),target=(0,.07,.066),lens=65,aspect=1.5,action='Fire',frame=70),
 'deployed':dict(location=(1.55,-.55,.65),target=(0,.20,-.02),lens=55,aspect=1.8,action='BipodDeploy',frame=78),
 'folded':dict(location=(.60,.64,-.22),target=(0,.44,.005),lens=65,aspect=1.6,action='Idle',frame=0),
 'grip':dict(location=(.30,-.25,.17),target=(0,-.024,.022),lens=66,aspect=1.35),
 'optic':dict(location=(.31,-.28,.27),target=(0,.01,.113),lens=65,aspect=1.5),
 'crown':dict(location=(.06,1.01,.11),target=(0,.817,.065),lens=80,aspect=1.3),
 'magazine':dict(location=(.17,-.215,.115),target=(0,0,-.038),lens=60,aspect=1.2),
 'case':dict(location=(.082,-.065,.065),target=(0,.026,0),lens=68,aspect=1.3),
 'case_mouth':dict(location=(.045,.13,.032),target=(0,.049,0),lens=80,aspect=1.3),
 'wrist':dict(location=(.26,-.41,.25),target=(0,-.105,.042),lens=65,aspect=1.55),
 'port':dict(location=(.28,.12,.20),target=(0,.132,.048),lens=78,aspect=1.5,action='Fire',frame=70),
 'rear_cocked':dict(location=(.17,-.28,.14),target=(0,-.01,.061),lens=80,aspect=1.3),
 'rear_fired':dict(location=(.17,-.28,.14),target=(0,-.01,.061),lens=80,aspect=1.3,action='Fire',frame=10),
 'bottom':dict(location=(.30,-.12,-.14),target=(0,.055,.002),lens=65,aspect=1.55,action='Idle',frame=0),
 'bipod_detail':dict(location=(.46,.70,-.09),target=(0,.43,-.12),lens=45,aspect=1.3,action='BipodDeploy',frame=78),
 'rings':dict(location=(-.20,.18,.20),target=(0,.123,.106),lens=78,aspect=1.5),
}
STRIP_SHOT=dict(location=(.72,-.28,.30),target=(0,.09,.03),lens=45,aspect=1.35)
PHOTO_POSES={'right_photo':{},'profile_right':{},'left_photo':{},'wrist_photo':{},'open_photo':dict(action='Fire',frame=70)}
RENDER_STAGE='Form checkpoint: exported GLB, quick constant materials'
def floor_height(source):return -.12
def configure_scene(scene,source):
 import bpy
 # Scale the pistol-family studio lights to this long asset without changing
 # the shared renderer or the other guns' presentation.
 for ob in scene.objects:
  if ob.name=='Studio seamless':
   for v in ob.data.vertices:
    v.co.x*=2;v.co.y*=4
    if v.co.z>1:v.co.z*=3
  if ob.type=='LIGHT':
   ob.location*=3.3;ob.data.energy*=10.89
   if ob.data.type=='AREA':ob.data.size*=3.3
 if scene.render.engine=='BLENDER_WORKBENCH':scene.display.shading.single_color=(.56,.59,.62)
 if scene.render.engine=='CYCLES':
  from mathutils import Vector
  for name,loc,target,power,size in [
    ('Port soft fill',(.24,.12,.23),(0,.13,.045),12,.22),
    ('Underside fill',(-.20,.38,-.10),(0,.30,.01),5,.35)]:
   light=bpy.data.lights.new(name,'AREA');light.energy=power;light.shape='DISK';light.size=size
   ob=bpy.data.objects.new(name,light);scene.collection.objects.link(ob);ob.location=loc
   ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()

def prepare_shot(scene,s):
 scene.camera.data.dof.use_dof=False
 s.setdefault('exposure',-1.8)
 if 'time_s' in s:
  s['exposure']=.4
  if s.get('action','').startswith('Bipod'):
   s.update(location=(.57,.13,.20),target=(0,.46,-.08),lens=45)
