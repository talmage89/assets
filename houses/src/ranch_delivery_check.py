"""Independent delivery checks, image-cache identity, maps and colonial bytes."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from check_delivery import check
from kit.image_io import read_png
from kit.motion import sweep


def dish_shell(seed):
 ob=bpy.data.objects.get('Legacy_dish')
 if ob is None:return None
 from plan import generate
 from check_mesh import surface
 from mathutils import Vector
 meta=json.loads(Path(f'build/ranch/delivery/game-{seed}.json').read_text())
 m=generate(seed,meta['spec'],house_type='ranch')['blocks'][0]
 x=m.cx+1.;y=m.cy+1.4;z=m.height(x,y)
 mesh=surface([ob]);front=mesh.ray_cast(Vector((x+.17,y-1,z+1.00)),Vector((0,1,0)),2)[0]
 assert front is not None
 back=mesh.ray_cast(front+Vector((0,.0001,0)),Vector((0,1,0)),.01)[0]
 assert back is not None
 gauge=back.y-front.y;edges={}
 for p in ob.data.polygons:
  for edge in p.edge_keys:edges[edge]=edges.get(edge,0)+1
 open_edges=sum(v!=2 for v in edges.values())
 assert open_edges==0 and abs(gauge-.003)<2e-5,(seed,open_edges,gauge)
 return dict(passed=True,measured_y_gauge_m=gauge,boundary_or_nonmanifold_edges=open_edges,scope='Actual front/back surface ray separation and closed sheet topology')


def colonial():
 baseline=Path('build/ranch/delivery/colonial-before.json')
 # Original accepted delivery hashes are retained locally from the handoff.
 if not baseline.exists():return dict(scope='No local pre-build baseline; construction baseline checked separately')
 rows=json.loads(baseline.read_text());result={}
 for file,digest in rows.items():
  path=Path(file)
  if path.parts[0]=='houses':path=Path(*path.parts[1:])
  actual=hashlib.sha256(path.read_bytes()).hexdigest();assert actual==digest,('Colonial changed',str(path))
  result[str(path)]=actual
 return dict(passed=True,files=len(result),sha256=result)


def reuse(seeds):
 bpy.ops.wm.read_factory_settings(use_empty=True);seen={};steps=[]
 paths=[Path(f'export/HearthfieldRanch-{s}.gltf') for s in seeds]
 paths += sorted(Path('export').glob('Hearthfield-*.gltf'))+[paths[0]]
 for path in paths:
  bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
  images=[i for i in bpy.data.images if i.source=='FILE' and i.filepath];by_path={}
  for im in images:
   p=str(Path(bpy.path.abspath(im.filepath)).resolve());assert p not in by_path
   by_path[p]=im
   if p in seen:assert seen[p]==im.as_pointer()
   seen[p]=im.as_pointer()
  steps.append(dict(source=str(path),image_datablocks=len(images)))
 assert len(seen)<=31
 return dict(passed=True,steps=steps,unique_image_datablocks=len(seen),resident_rgba8_pixel_bytes=sum(i.size[0]*i.size[1]*4 for i in images))


def textures():
 rows=[]
 for path in sorted(Path('export/textures').glob('*.png')):
  a=read_png(path);assert np.isfinite(a).all();n=a.shape[0];assert a.shape==(n,n,3)
  if '_Normal' in path.name:assert float(abs(np.linalg.norm(a*2-1,axis=2)-1).max())<.008
  loss=None
  if 'Ranch' in path.name and 'Trim' not in path.name:
   name=path.name.removeprefix('T_').rsplit('_',1)[0];channel=path.stem.rsplit('_',1)[1]
   native=Path('build/ranch/delivery/native')/('roof' if name=='RanchRoof' else name.removeprefix('RanchBrick_'))/('T_RanchRoof_' if name=='RanchRoof' else 'T_RanchBrick_')
   original=read_png(str(native)+channel+'.png')
   loss=dict(mean_absolute=float(abs(a-original).mean()),maximum=float(abs(a-original).max()))
   if channel in ('BaseColor','ORM'):assert loss['mean_absolute']<.025,(str(path),loss)
  rows.append(dict(path=str(path),size=n,png_bytes=path.stat().st_size,gpu_mib=n*n*4/3/1048576,source_vs_ship=loss))
 assert len(rows)==31 and sum(r['gpu_mib'] for r in rows)<=48
 return rows


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seeds',default='11,12,13,14,15,16');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);seeds=list(map(int,a.seeds.split(',')))
 rows=[]
 for seed in seeds:
  row=check(seed,ranch=True)
  assert row['triangles']<=60000,('Ranch delivery triangle ceiling',seed,row['triangles'])
  from ranch_chart_check import check as chart_check
  row['accepted_roof_comparison']=chart_check(seed)
  bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/ranch/delivery/game-{seed}.blend').resolve()))
  row['dish_shell']=dish_shell(seed)
  motions=[dict(node='FrontDoor',axis='Z',range=[0,105],step=3,tolerance_m=.0005),dict(node='PatioDoor',axis='X',kind='translation',range=[0,.8382],step=.04,tolerance_m=.0005)]
  if 'ServiceDoor' in bpy.data.objects:motions.append(dict(node='ServiceDoor',axis='Z',range=[-100,0],step=5,tolerance_m=.0005))
  motion=sweep(dict(MOTIONS=motions));assert motion['passed'];row['motion']=motion;rows.append(row)
 median=float(np.median([r['triangles'] for r in rows]))
 if set(seeds)=={11,12,13,14,15,16}:assert median<=56000,('Ranch median triangle target',median)
 maps=textures();result=dict(passed=True,rows=rows,median_triangles=median,textures=maps,gpu_mib=sum(r['gpu_mib'] for r in maps),colonial=colonial(),image_reuse=reuse(seeds))
 Path('build/ranch/delivery/check.json').write_text(json.dumps(result,indent=2));print('RANCH_DELIVERY_CHECK',[(r['seed'],r['triangles']) for r in rows],result['gpu_mib'],flush=True)
