"""Independent surface/finish rays for fixed appearance measurement patches."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy,numpy as np
from mathutils import Vector
from values import CASES
EXPECTED={'soffit':('CommercialEquipment',0),'concrete':('CommercialConcrete',None),'dark_cabinet':('CommercialEquipment',1),'eifs':('CommercialEIFS',None),'asphalt':('Asphalt',None)}
rows={}
for name,case in CASES.items():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 row=json.loads(Path('renders/look-matches/provenance.json').read_text())[case['pair']];shot=row['camera']
 bpy.ops.import_scene.gltf(filepath=str(Path(row['source']).resolve()));bpy.context.view_layer.update()
 cam=bpy.data.objects.new('Patch ray camera',bpy.data.cameras.new('Patch ray camera'));bpy.context.scene.collection.objects.link(cam);bpy.context.scene.camera=cam
 cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',shot.get('roll',0));cam.data.lens=shot['lens'];cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36
 bpy.context.scene.render.resolution_x=row['width'];bpy.context.scene.render.resolution_y=round(row['width']/shot['aspect']);bpy.context.view_layer.update()
 frame=cam.data.view_frame(scene=bpy.context.scene);x0,y0,x1,y1=case['render_box'];samples=[]
 for fy in (.2,.5,.8):
  for fx in (.2,.5,.8):
   x=x0+(x1-x0)*fx;y=y0+(y1-y0)*fy;q=frame[2].lerp(frame[1],x).lerp(frame[3].lerp(frame[0],x),1-y)
   hit,p,_,index,o,_=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),cam.location,cam.matrix_world.to_3x3()@q.normalized());assert hit,(name,x,y)
   poly=o.data.polygons[index];mat=o.data.materials[poly.material_index].name
   xyz=np.array([o.matrix_world@o.data.vertices[i].co for i in poly.vertices]).T;w=np.linalg.lstsq(np.vstack((xyz,np.ones(3))),np.r_[np.array(p),1],rcond=None)[0]
   uv=sum((o.data.uv_layers[0].data[li].uv*float(v) for li,v in zip(poly.loop_indices,w)),Vector((0,0)));cell=int(uv.y*8)*4+int(uv.x*4)
   expected,finish=EXPECTED[name];assert mat==expected and (finish is None or cell==finish),(name,x,y,mat,cell)
   samples.append(dict(pixel_fraction=(x,y),material=mat,finish_cell=cell if finish is not None else None,position=list(p)))
 rows[name]=dict(samples=samples,source_bundle_sha256=row['sha256'],image_sha256=row['image_sha256'],render_box=case['render_box'])
Path('build/value-surface-check.json').write_text(json.dumps(dict(passed=True,patches=rows,scope='Nine independent actual exported surface/finish rays per fixed display-value ROI; no pixel fitting or material substitution'),indent=2));print('VALUE_SURFACES',len(rows)*9,'verified')
