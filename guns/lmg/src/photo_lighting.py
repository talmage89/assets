"""Procedural light fits to the reference's visible reflection cards.

One lighting setup per photograph, shared by all measured finishes in that
photograph. No per-part lighting or image-space color remapping.
"""
FITS={
 'used_photo':dict(world=.23,key=7,fill=1.7,key_size=(.18,.8),fill_size=(.55,1.1),key_position=(-.70,.20,.85),fill_position=(-.65,.20,.25),color=(.83,.91,1.0)),
 'used_right_photo':dict(world=.6,key=28,fill=4,key_size=(.45,1.2),fill_size=(.7,1.1),key_position=(-.70,.20,.45),fill_position=(-.65,.20,.25),color=(.83,.91,1.0)),
 'paint_receiver_photo':dict(world=.003,key=14,fill=.2,key_size=(.7,1.3),fill_size=(.5,1.0),key_position=(-.4,.2,.8),fill_position=(-.6,-.15,.3),color=(.83,.91,1.0)),
 'handguard_finish_photo':dict(world=.2,key=28,fill=4,key_size=(1.2,1.2),fill_size=(1,1),key_position=(.65,.35,.2),fill_position=(-.6,.3,.2),color=(.90,.94,1.0)),
 'stock_finish_photo':dict(world=.025,key=18,fill=2,key_size=(.5,1.0),fill_size=(1.3,1.3),key_position=(-.7,-.2,.18),fill_position=(.6,-.1,.3),color=(.90,.94,1.0)),
 'box_finish_photo':dict(world=.18,key=15,fill=3,key_size=(.8,1.2),fill_size=(.6,1.2),key_position=(-.3,.4,-.4),fill_position=(-.6,-.2,-.05),color=(1,.98,.94)),
}
def apply(scene,shot):
 import bpy
 from mathutils import Vector
 name=shot.get('light_fit')
 if name not in FITS:return
 fit=FITS[name]
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=fit['world']
 for ob in scene.objects:
  if ob.type!='LIGHT' or 'final_energy' not in ob:continue
  if ob.name=='Key softbox':
   ob.location=fit['key_position'];ob.data.energy=fit['key'];ob.data.size,ob.data.size_y=fit['key_size'];ob.data.color=fit['color']
  elif ob.name=='Camera fill':
   ob.location=fit['fill_position'];ob.data.energy=fit['fill'];ob.data.size,ob.data.size_y=fit['fill_size'];ob.data.color=(1,1,1)
  elif ob.name=='Right rim strip' and name=='used_photo':
   ob.location=(-.32,.14,.65);ob.data.energy=2;ob.data.size=.035;ob.data.size_y=.7;ob.data.color=fit['color']
  elif ob.name=='Right rim strip' and name=='used_right_photo':
   ob.location=(0,1.05,.1);ob.data.energy=18;ob.data.size=1.0;ob.data.size_y=.5;ob.data.color=fit['color']
  elif ob.name=='Left rim strip' and name=='used_photo':
   ob.location=(-.10,-.015,-.06);ob.data.energy=.10;ob.data.size=.12;ob.data.size_y=.15;ob.data.color=fit['color']
  else:ob.data.energy=0
  target=(0,-.015,-.035) if ob.name=='Left rim strip' and name=='used_photo' else (0,.10,.10)
  ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
