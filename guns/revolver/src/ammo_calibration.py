"""Separate neutral ammunition value views; the nose must be camera-visible."""
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parents[2])]
from final_shots import configure_scene as gun_scene,prepare_shot as gun_shot
from presentation import digest as gun_digest
FINAL_STAGE=True
RENDER_STAGE='exported canonical atlas / neutral ammunition comparison'
DEFAULT_SHOTS='cartridge_values,primer_values'
SHOTS={
 'cartridge_values':dict(location=(.085,.045,.025),target=(0,.020,0),lens=65,aspect=1.4,exposure=-.30,background='transparent'),
 'primer_values':dict(location=(.018,-.065,.012),target=(0,.001,0),lens=70,aspect=1.4,exposure=-.30,background='transparent')}
PHOTO_POSES={}
def floor_height(source):return -.07
def recipe_digest():
 return hashlib.sha256(HERE.joinpath('ammo_calibration.py').read_bytes()+gun_digest().encode()).hexdigest()
def configure_scene(scene,source):gun_scene(scene,source)
def prepare_shot(scene,shot):
 gun_shot(scene,shot)
 # Broad neutral room response, without the hero's concentrated bright cards.
 background=scene.world.node_tree.nodes['Background']
 background.inputs['Color'].default_value=(.7,.7,.7,1)
 background.inputs['Strength'].default_value=.18 if shot['location'][1]<0 else 1.1
 for ob in scene.objects:
  if ob.name.startswith('Studio black reflection flag'):ob.hide_render=True
  if ob.type=='LIGHT' and 'baseline_energy' in ob:ob.data.energy=ob['baseline_energy']*.25
if __name__=='__main__':
 import interface
 from guns.common.render import main
 main(sys.modules[__name__],interface)
 out=Path(sys.argv[sys.argv.index('--out')+1]);p=out/'shots.json';rows=json.loads(p.read_text())
 for row in rows.values():row['ammo_calibration_sha256']=recipe_digest()
 p.write_text(json.dumps(rows,indent=2))
