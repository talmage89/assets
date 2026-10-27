"""Source/export display loss inside an independently projected asset mask."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
from PIL import Image,ImageDraw
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from delivery_io import bundle_hash


def check(seed):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path(f'export/HearthfieldRanch-{seed}.gltf').resolve()))
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];camera=bpy.data.objects.new('LossCamera',bpy.data.cameras.new('LossCamera'));bpy.context.scene.collection.objects.link(camera);camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36
 root=Path(f'renders/ranch/revision2/bake-loss/{seed}');calibration=json.loads(Path(f'build/ranch/revision2/cameras-{seed}.json').read_text());rows={};sc=bpy.context.scene
 provenance={label:json.loads((root/label/'provenance.json').read_text()) for label in ('source','export')}
 for label,records in provenance.items():
  for name,row in records.items():
   source=Path(row['source']);digest=bundle_hash(source) if source.suffix=='.gltf' else hashlib.sha256(source.read_bytes()).hexdigest()
   assert digest==row['source_sha256'],(seed,label,name,'stale geometry')
   assert row['camera']==calibration[name]['shot'],(seed,label,name,'stale camera')
   for file,value in row['material_sha256'].items():assert hashlib.sha256(Path(file).read_bytes()).hexdigest()==value,(seed,file,'stale map')
 for name,data in calibration.items():
  shot=data['shot'];before=Image.open(root/'source'/(name+'.png')).convert('RGB');after=Image.open(root/'export'/(name+'.png')).convert('RGB');assert before.size==after.size
  camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0));camera.data.lens=shot.get('lens',45);sc.render.resolution_x=after.width;sc.render.resolution_y=after.height;sc.render.resolution_percentage=100;bpy.context.view_layer.update()
  mask=Image.new('L',after.size);draw=ImageDraw.Draw(mask)
  for ob in objects:
   points=[]
   for v in ob.data.vertices:
    q=world_to_camera_view(sc,camera,ob.matrix_world@v.co);points.append((q.x*after.width,(1-q.y)*after.height))
   ob.data.calc_loop_triangles()
   for t in ob.data.loop_triangles:draw.polygon([points[i] for i in t.vertices],fill=255)
  keep=np.asarray(mask)>0;a=np.asarray(before)/255.;b=np.asarray(after)/255.;w=np.array((.2126,.7152,.0722));delta=abs((a@w-b@w)[keep]);assert len(delta)>10000
  rows[name]=dict(mask_pixels=int(keep.sum()),mean_absolute_encoded_y=float(delta.mean()),p95_absolute_encoded_y=float(np.quantile(delta,.95)),maximum_absolute_encoded_y=float(delta.max()))
  assert rows[name]['mean_absolute_encoded_y']<.03,(seed,name,rows[name])
  mask.save(root/(name+'-asset-mask.png'))
 print('BAKE_LOSS',seed,{n:round(r['mean_absolute_encoded_y'],6) for n,r in rows.items()},flush=True);return dict(seed=seed,views=rows,provenance_current=True)


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seeds',default='11,12,13,15,16');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);rows=[check(int(s)) for s in a.seeds.split(',')]
 Path('build/ranch/revision2/bake-loss.json').write_text(json.dumps(dict(passed=True,rows=rows,scope='Display Y-prime difference inside exported triangle-union silhouette, shared calibrated cameras; native source versus current delivered PBR. Geometry preservation checked separately.'),indent=2))
