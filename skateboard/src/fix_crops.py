"""Native-pixel crops of the old and revised exported assets, same cameras."""
from pathlib import Path
import json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import review_sheet
OUT=Path('renders/fixes');OUT.mkdir(parents=True,exist_ok=True)
# No enlargement: every crop retains at least 800 pixels of the actual render.
FIXES={
 '01-grip-tooth':('season','grip_macro',(0,0,1440,1067)),
 '01-grip-frayed-edge':('season','grip_edge',(0,0,1440,1029)),
 '02-no-center-tag':('season','hero',(320,180,1240,980)),
 '03-transverse-slides':('season','hero_bottom',(320,100,1320,950)),
 '03-beat-slides':('beat','hero_bottom',(320,100,1320,950)),
 '04-hanger-grind-and-cast':('season','truck',(0,0,1440,1067)),
 '04-cast-inner':('season','truck_inner',(0,0,1440,1067)),
 '05-wheel-tread-sidewall':('season','wheel_bearing',(0,0,1440,1108)),
 '05-beat-flat':('beat','wheel_profile',(0,0,1440,1108)),
}
manifest={}
for name,(state,shot,rect) in FIXES.items():
    paths=[];metas=[]
    for stage in ('before','after'):
        src=OUT/stage/state/(shot+'.png');im=Image.open(src)
        assert im.width==1440 and rect[2]<=im.width and rect[3]<=im.height,(src,im.size)
        dst=OUT/(name+'-'+stage+'.png');im.crop(rect).save(dst);paths.append(dst)
        meta=json.loads((src.parent/'shots.json').read_text())[shot];metas.append(meta)
    for key in ('location','target','lens','ortho','aspect','invert','exposure'):
        assert metas[0].get(key)==metas[1].get(key),(name,key)
    width=rect[2]-rect[0];assert width>=800
    review_sheet([paths],OUT/(name+'-before-after.jpg'),width=width*2+56,title=name+' / before left / after right / native pixels')
    manifest[name]=dict(state=state,shot=shot,crop=rect,panel_width=width,before_glb_sha256=metas[0]['sha256'],after_glb_sha256=metas[1]['sha256'])
(OUT/'crops.json').write_text(json.dumps(manifest,indent=2))
print('Nine same-camera comparisons, native crop widths:',[v['panel_width'] for v in manifest.values()])
