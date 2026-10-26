"""No-GPU fixture: unique islands plus deliberately repeated alpha tile UVs.

Runs real finalize/export/verify, proves MASK/double-sided/shared-image delivery,
and confirms an out-of-rectangle card is rejected. All outputs stay in build/.
"""
import sys,json,runpy
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import model as G,finalize,export,verify,atlas
from kit.image_io import write_png
b=ROOT/'build/atlas-test';b.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
r=G.pivot('TileFixture',(0,0,0));r['static_root']=True;r['asset_set']='TileFixture'
mat=bpy.data.materials.new('Fixture')
o=G.box('Frame',(-.5,0,.5),(1,.1,1),mat,0);G.attach(o,r,asset_set='TileFixture')
verts=[];faces=[]
for x in (.1,.6):
 i=len(verts);verts.extend([(x,-.06,0),(x+.5,-.06,0),(x+.5,-.06,1),(x,-.06,1)]);faces.append(tuple(range(i,i+4)))
o=G.mesh('Sheet_Fabric',verts,faces,mat);G.attach(o,r,asset_set='TileFixture');o['allow_boundary']=True;o['export_part']='Sheet_Fabric'
layer=o.data.uv_layers.new(name='BakeUV')
for face in o.data.polygons:
 for i,uv in zip(face.loop_indices,[(.01,.01),(.25,.01),(.25,.25),(.01,.25)]):layer.data[i].uv=uv
cfg=dict(BUDGETS={'TileFixture':100},BOUNDS={'TileFixture':dict(size=(2.1,.11,1),tolerance=(.001,.001,.001))},
 TILED_MESHES={'*_Fabric':dict(rect=(.01,.01,.25,.25),alpha_cutoff=.5,double_sided=True,density_min=100,density_max=200)},
 UV_ATLAS_RECT=(.28,.28,.99,.99),UV_MIN_COVERAGE=.2,UV_DENSITY_BANDS=dict(reference_size=512,p5_min=1,median_min=1,median_max=1000,p95_max=2000))
config=b/'config.py';config.write_text('\n'.join(k+'='+repr(v) for k,v in cfg.items()))
bpy.context.scene['quality']='game';bpy.ops.wm.save_as_mainfile(filepath=str(b/'source.blend'))
def args(script,values):sys.argv=['blender','--',*values]
args('finalize',['--source',str(b/'source.blend'),'--config',str(config),'--out',str(b/'finalized.blend'),'--report',str(b/'uv.json'),'--size','512','--target-density','1000']);finalize.main()
xx=np.arange(512)[None,:]/511;yy=np.arange(512)[:,None]/511
bc=np.zeros((512,512,4));bc[:,:,:3]=np.stack(np.broadcast_arrays(xx,yy,xx*.2+.2),axis=2);bc[:,:,3]=1
bc[384:512,:128,3]=((np.arange(128)[:,None]//8+np.arange(128)[None,:]//8)%2)
tex=b/'textures';tex.mkdir(exist_ok=True)
write_png(tex/'T_TileFixture_BaseColor.png',bc);write_png(tex/'T_TileFixture_Normal.png',np.full((512,512,3),(.5,.5,1)));write_png(tex/'T_TileFixture_ORM.png',np.full((512,512,3),(1,.6,.8)))
args('export',['--source',str(b/'finalized.blend'),'--textures',str(tex),'--asset','TileFixture','--out',str(b/'fixture.glb'),'--report',str(b/'export.json'),'--config',str(config)]);export.main()
args('verify',['--source',str(b/'fixture.glb'),'--expected',str(b/'export.json'),'--config',str(config),'--out',str(b/'verify.json'),'--size','512']);verify.main()
o=bpy.data.objects['Sheet_Fabric'];layer=o.data.uv_layers['UVMap'];layer.data[0].uv=(.6,.6)
assert not atlas.tile_report([o],cfg,512,'UVMap')['passed'],'Tile escaped its reserved region without a failure'
print('PASS: tiled MASK export shares three images; unique UVs checked; escaped tile rejected')
