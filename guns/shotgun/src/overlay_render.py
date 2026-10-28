"""Render only our exported stock; reference pixels never enter Blender."""
import json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]));sys.path.insert(0,str(Path(__file__).parent))
from guns.common.render import main
import shots,interface
data=json.loads((BASE/'build/cameras.json').read_text())
shots.SHOTS={'stock_'+side:dict(data[side+'_photo']['shot'],background='transparent') for side in ('right','left')}
shots.PHOTO_POSES={}
def prepare(sc,shot):
 for ob in sc.objects:
  if ob.type=='MESH':ob.hide_render=ob.get('part_name',ob.name)!='Stock'
shots.prepare_shot=prepare
if __name__=='__main__':main(shots,interface)
