"""Asset-owned checkpoint cameras, including the exact Eye socket."""
import math
FINAL_STAGE=True
SHOTS={
 'hero':dict(location=(1.50,-.74,.73),target=(0,.23,.005),lens=60,aspect=1.8),
 'side':dict(location=(2,.235,-.018),target=(0,.235,-.018),ortho=1.20,aspect=4),
 'left':dict(location=(-2,.235,-.018),target=(0,.235,-.018),ortho=1.20,aspect=4),
 'top':dict(location=(0,.235,2),target=(0,.235,0),ortho=1.20,aspect=4,roll=math.pi/2),
 'front':dict(location=(0,2,-.023),target=(0,.235,-.023),ortho=.20,aspect=1),
 'rake_right':dict(location=(1.6,1.15,.76),target=(0,.23,0),lens=60,aspect=1.8,raking=1),
 'rake_left':dict(location=(-1.6,-.76,.76),target=(0,.23,0),lens=60,aspect=1.8,raking=-1),
 'open':dict(location=(.18,-.17,.26),target=(0,.13,.052),lens=65,aspect=1.5,action='IdleOpenSpent',frame=0),
 'breech':dict(location=(-.14,-.08,.22),target=(0,.14,.054),lens=72,aspect=1.5,action='IdleOpenLoaded',frame=0),
 'action':dict(location=(.23,-.10,.15),target=(0,.085,.03),lens=70,aspect=1.5),
 'action_left':dict(location=(-.23,-.10,.15),target=(0,.085,.03),lens=70,aspect=1.5),
 'triggers':dict(location=(.23,.055,-.005),target=(0,.055,-.010),lens=75,aspect=1.5),
 'trigger_quarter':dict(location=(-.18,.18,.065),target=(0,.055,-.010),lens=70,aspect=1.5),
 'forend':dict(location=(.25,.39,-.07),target=(0,.27,.02),lens=58,aspect=1.5),
 'stock':dict(location=(.40,-.38,.09),target=(0,-.14,-.03),lens=48,aspect=1.5),
 'muzzle':dict(location=(.08,.94,.10),target=(0,.765,.044),lens=70,aspect=1.5),
 'top_controls':dict(location=(.075,-.10,.25),target=(0,.055,.042),lens=75,aspect=1.5),
 'lumps':dict(location=(.16,.08,-.02),target=(0,.145,.048),lens=60,aspect=1.5,action='IdleOpenEmpty',frame=0),
 'aimed':dict(location=(0,0,0),target=(0,1,0),lens=45,aspect=1.6,aimed=True),
 'shell':dict(location=(.075,-.09,.065),target=(0,.027,0),lens=65,aspect=1.5),
 'hull':dict(location=(.06,.13,.06),target=(0,.03,0),lens=65,aspect=1.5)}
SHOTS.update({
 'action_rake_right':dict(location=(.40,.10,.08),target=(0,.115,.031),lens=85,aspect=1.5,raking=1),
 'action_rake_left':dict(location=(-.40,.10,.08),target=(0,.115,.031),lens=85,aspect=1.5,raking=-1),
 'action_rake_top':dict(location=(.025,.045,.35),target=(0,.115,.035),lens=65,aspect=1.5,raking=1),
 'action_rake_bottom':dict(location=(.04,.12,-.30),target=(0,.115,.015),lens=65,aspect=1.5,raking=-1),
})
for name,shot in SHOTS.items():
 if name not in ('shell','hull'):shot.setdefault('action','Idle');shot.setdefault('frame',0)
DEFAULT_SHOTS=','.join(n for n in SHOTS if n not in ('shell','hull'))
STRIP_SHOT=dict(location=(.52,-.35,.37),target=(0,.10,.005),lens=55,aspect=1.5)
PHOTO_POSES={name:dict(action='Idle',frame=0) for name in (
 'right','left','action','action_left','action_top','action_bottom','forend','forend_side','trigger')}
PHOTO_POSES.update({name:dict(action='IdleOpenEmpty',frame=0,extractor_home=True,
 photo_open_angle=-30,pose_note='empty photographic pose, 30-degree opening; canonical clips unchanged') for name in ('open','barrel_flats')})
PHOTO_POSES['barrel_flats'].update(photo_barrel_isolation=True,pose_note='Detached barrel comparison: fixed action and forend omitted to match reference; exported asset unchanged')
def floor_height(source):return -.15
def configure_scene(sc,source):
 import bpy
 from kit import model as M
 for ob in sc.objects:
  if ob.type=='LIGHT':ob['baseline_energy']=ob.data.energy
 data=bpy.data.lights.new('Underside inspection softbox','AREA');data.shape='DISK';data.size=.38;data.energy=18
 ob=bpy.data.objects.new('Underside inspection softbox',data);sc.collection.objects.link(ob)
 from mathutils import Vector
 ob.location=(0,.25,-.27);ob.rotation_euler=(Vector((0,.20,.025))-ob.location).to_track_quat('-Z','Y').to_euler();ob.hide_render=True
 data=bpy.data.lights.new('Raking strip','AREA');data.shape='RECTANGLE';data.size=.035;data.size_y=1.2;data.energy=32
 ob=bpy.data.objects.new('Raking strip',data);sc.collection.objects.link(ob);ob.hide_render=True
 m=bpy.data.materials.new('Aim gray card');m.use_nodes=True;nt=m.node_tree;nt.nodes.clear()
 e=nt.nodes.new('ShaderNodeEmission');e.inputs[0].default_value=(.24,.24,.24,1);o=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(e.outputs[0],o.inputs['Surface'])
 card=M.box('Aim backdrop',(0,1.1,.07),(4,.003,3),m,0);M.apply(card);card.hide_render=True
 def before_render(scene):
  if scene.get('exact_aim'):scene.render.film_transparent=False;card.hide_render=False
  if scene.get('photo_extractor_home'):
   arm=next(o for o in scene.objects if o.type=='ARMATURE')
   # Freeze the sampled action before pressing the extractor home. An active
   # animation would overwrite the manual pose on the render dependency update.
   frozen={b.name:b.matrix_basis.copy() for b in arm.pose.bones}
   arm.animation_data.action=None
   for name,basis in frozen.items():arm.pose.bones[name].matrix_basis=basis
   bpy.context.view_layer.update()
   barrel=arm.pose.bones['Barrels'];extractor=arm.pose.bones['Extractor']
   if scene.get('photo_open_angle'):
    from mathutils import Matrix
    rest=barrel.bone.matrix_local
    barrel.matrix=Matrix.Translation(rest.translation)@Matrix.Rotation(math.radians(scene['photo_open_angle']),4,'X')@Matrix.Translation(-rest.translation)@rest
    bpy.context.view_layer.update()
   expected=(barrel.matrix@barrel.bone.matrix_local.inverted())@extractor.bone.matrix_local
   extractor.matrix=expected
   bpy.context.view_layer.update()
   assert max(abs(extractor.matrix[i][j]-expected[i][j]) for i in range(4) for j in range(4))<1e-6
 bpy.app.handlers.render_pre.append(before_render)
def prepare_shot(sc,shot):
 import bpy
 from mathutils import Vector
 for ob in sc.objects:
  if ob.type=='MESH' and 'bone' in ob:
   ob.hide_render=bool(shot.get('photo_barrel_isolation')) and ob['bone'] not in ('Barrels','Extractor')
 sign=shot.get('raking',0)
 sc.objects['Underside inspection softbox'].hide_render=not (shot.get('target',(0,0,0))[2]-shot.get('location',(0,0,0))[2]>.035)
 for ob in sc.objects:
  if ob.type=='LIGHT' and 'baseline_energy' in ob:ob.data.energy=ob['baseline_energy']*(.13 if sign else 1)
 strip=sc.objects['Raking strip'];strip.hide_render=not bool(sign)
 if sign:
  strip.location=(sign*.35,.18,-.20 if shot.get('location',(0,0,0))[2]<0 else .26);strip.rotation_euler=(Vector(shot.get('target',(0,.23,.015)))-strip.location).to_track_quat('-Z','Y').to_euler()
 sc['exact_aim']=bool(shot.get('aimed'));sc.objects['Aim backdrop'].hide_render=not sc['exact_aim']
 sc['photo_extractor_home']=bool(shot.get('extractor_home'))
 sc['photo_open_angle']=shot.get('photo_open_angle',0)
