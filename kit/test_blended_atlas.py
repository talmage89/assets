"""Real no-GPU export/import coverage regression, preserving legacy MASK fixture."""
import sys,runpy,json
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import export,verify,gltf
runpy.run_path(str(ROOT/'kit/test_atlas.py'))
b=ROOT/'build/atlas-test';cfg=runpy.run_path(str(b/'config.py'));cfg={k:v for k,v in cfg.items() if not k.startswith('__')}
cfg['TILED_MESHES']['*_Fabric']['alpha_mode']='BLEND'
config=b/'blend-config.py';config.write_text('\n'.join(k+'='+repr(v) for k,v in cfg.items()))
sys.argv=['blender','--','--source',str(b/'finalized.blend'),'--textures',str(b/'textures'),'--asset','TileFixture','--out',str(b/'blend.glb'),'--report',str(b/'blend.json'),'--config',str(config)];export.main()
sys.argv=['blender','--','--source',str(b/'blend.glb'),'--expected',str(b/'blend.json'),'--config',str(config),'--out',str(b/'blend-verify.json'),'--size','512'];verify.main()
doc=gltf.GLB(b/'blend.glb').json
assert [m['alphaMode'] for m in doc['materials'] if m.get('alphaMode')=='BLEND']==['BLEND']
assert len(doc['images'])==3
print('PASS: BLEND coverage survives real export/re-import and shares the same three images; MASK fixture still passes')
