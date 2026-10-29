"""Keep the accepted standalone ammunition lighting, with current baked GLBs."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from mathutils import Vector
from guns.common.render import main
import final_shots,interface
configure_gun=final_shots.configure_scene

def configure_scene(scene,source):
 configure_gun(scene,source)
 scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.16,.16,.16,1)
 scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6
 cards={
  'Key softbox':((-.65,.18,.40),24,.55,1.25),
  'Camera fill':((.65,.20,.13),22,.55,1.20),
  'Right rim strip':((.25,.85,.42),8,.12,1.0),
  'Left rim strip':((-.30,-.30,.38),6,.13,.8),
  'Overhead reflection card':((0,.22,.85),5,.32,1.0),
  'Lever top strip':((.05,.20,.8),10,.6,.15),
  'Lever action fill':((.32,.12,.26),2,.30,.30),
  'Lever rear edge':((-.24,-.35,.25),6,.3,.5)}
 for name,(location,power,width,height) in cards.items():
  ob=scene.objects[name];ob.location=location;ob.data.energy=power
  ob.data.size=width;ob.data.size_y=height
  ob.rotation_euler=(Vector((0,.20,.02))-ob.location).to_track_quat('-Z','Y').to_euler()
 for ob in scene.objects:
  if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True

final_shots.configure_scene=configure_scene
if __name__=='__main__':main(final_shots,interface)
