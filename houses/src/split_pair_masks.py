"""Rasterize actual source/export silhouettes for the two bake-loss cameras.

This is geometry projection only: no lighting or shaded render is involved.
It excludes the presentation ground from the whole-house error measurement.
"""
import hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from delivery_io import bundle_hash

for folder in (Path('renders/split/source-matches'),Path('renders/split/final-matches')):
    records=json.loads((folder/'provenance.json').read_text());result={}
    for name,row in records.items():
        source=Path(row['source'])
        if source.suffix=='.gltf':
            bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));digest=bundle_hash(source)
        else:
            bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));digest=hashlib.sha256(source.read_bytes()).hexdigest()
        assert digest==row['source_sha256']
        width,height=Image.open(folder/(name+'.png')).size;sc=bpy.context.scene;sc.render.resolution_x=width;sc.render.resolution_y=height;sc.render.resolution_percentage=100;sc.render.pixel_aspect_x=sc.render.pixel_aspect_y=1
        data=bpy.data.cameras.new('Mask camera');camera=bpy.data.objects.new('Mask camera',data);sc.collection.objects.link(camera);sc.camera=camera
        data.sensor_fit='HORIZONTAL';data.sensor_width=36;data.clip_start=.03;data.clip_end=3000
        shot=row['camera'];camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0));data.lens=shot.get('lens',45);data.type='ORTHO' if 'ortho' in shot else 'PERSP'
        if 'ortho' in shot:data.ortho_scale=shot['ortho']
        bpy.context.view_layer.update();mask=Image.new('L',(width,height));draw=ImageDraw.Draw(mask);triangles=0
        for ob in sc.objects:
            if ob.type!='MESH' or not ob.get('asset_set'):continue
            ob.data.calc_loop_triangles()
            projected=[world_to_camera_view(sc,camera,ob.matrix_world@v.co) for v in ob.data.vertices]
            for tri in ob.data.loop_triangles:
                points=[projected[i] for i in tri.vertices]
                if all(p.z>0 for p in points):draw.polygon([(p.x*width,(1-p.y)*height) for p in points],fill=255);triangles+=1
        path=folder/(name+'-mask.png');mask.save(path);result[name]=dict(source_sha256=digest,render_recipe_sha256=row['recipe_sha256'],mask_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),triangles=triangles)
    (folder/'masks.json').write_text(json.dumps(result,indent=2))
print('SPLIT_PAIR_MASKS actual asset triangles; presentation context excluded')
