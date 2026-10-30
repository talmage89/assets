"""One procedural light rig per reference, shared by every measured finish.

Area-card energies were fitted with linear-light diagnostic renders of the
actual exported GLB. The final comparisons are rendered again in Cycles;
there is no image-space correction or per-part light linking.
"""
from light_fits import FITS

def apply(scene,shot):
 import bpy
 from mathutils import Vector
 for ob in scene.objects:
  if ob.type=='LIGHT' and ob.name.startswith('Photo reflection card'):ob.hide_render=True
 background=scene.world.node_tree.nodes['Background']
 background.inputs['Color'].default_value=(.25,.25,.25,1)
 name=shot.get('light_fit')
 if name not in FITS:return
 fit=FITS[name];color=fit['color']
 for ob in scene.objects:
  if ob.type=='LIGHT':ob.data.energy=0
 background.inputs['Strength'].default_value=fit['world']
 background.inputs['Color'].default_value=(*[.25*c for c in fit.get('world_color',color)],1)
 for i,card in enumerate(fit['lights']):
  key='Photo reflection card %02d'%i
  ob=scene.objects.get(key)
  if ob is None:
   data=bpy.data.lights.new(key,'AREA');data.shape='RECTANGLE'
   ob=bpy.data.objects.new(key,data);scene.collection.objects.link(ob)
  ob.hide_render=False;ob.location=card['position'];ob.data.energy=card['power']
  ob.data.size,ob.data.size_y=card['size'];ob.data.color=card.get('color',color)
  ob.rotation_euler=(Vector(card.get('target',(0,.10,.07)))-ob.location).to_track_quat('-Z','Y').to_euler()
 shot['physical_light_fit']=fit
