"""Nine actual exported surface rays per fixed measurement rectangle."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from mathutils import Vector
from strip_measure import CASES
rows={};provenance=json.loads(Path('renders/strip/matches/provenance.json').read_text())
for name,case in CASES.items():
    bpy.ops.wm.read_factory_settings(use_empty=True);row=provenance[case['pair']];shot=row['shot'];bpy.ops.import_scene.gltf(filepath=str(Path(row['source']).resolve()))
    cam=bpy.data.objects.new('Measurement camera',bpy.data.cameras.new('Measurement camera'));bpy.context.scene.collection.objects.link(cam);bpy.context.scene.camera=cam
    cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',shot.get('roll',0));cam.data.lens=shot['lens'];cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.shift_x=shot.get('shift_x',0);cam.data.shift_y=shot.get('shift_y',0)
    scene=bpy.context.scene;scene.render.resolution_x=row['width'];scene.render.resolution_y=round(row['width']/shot['aspect']);bpy.context.view_layer.update();frame=cam.data.view_frame(scene=scene);samples=[]
    x0,y0,x1,y1=case['render_box']
    for fy in (.2,.5,.8):
        for fx in (.2,.5,.8):
            x=x0+(x1-x0)*fx;y=y0+(y1-y0)*fy;q=frame[2].lerp(frame[1],x).lerp(frame[3].lerp(frame[0],x),1-y)
            hit,p,n,index,ob,_=scene.ray_cast(bpy.context.evaluated_depsgraph_get(),cam.location,cam.matrix_world.to_3x3()@q.normalized());assert hit,(name,x,y,'No source surface')
            mat=ob.data.materials[ob.data.polygons[index].material_index].name
            allowed=(case['material'],'StripTenantInks','CommercialEquipment')
            assert mat in allowed and n.z>.98,(name,x,y,mat,tuple(n),tuple(p))
            expect=.1524 if case['material']=='CommercialConcrete' else 0
            assert abs(p.z-expect)<.01,(name,'Wrong floor level',tuple(p))
            samples.append(dict(pixel_fraction=(x,y),material=mat,position=list(p)))
    rows[name]=dict(samples=samples,render_box=case['render_box'],image_sha256=row['image_sha256'])
Path('build/strip-look/value-surface-check.json').write_text(json.dumps(dict(passed=True,patches=rows,scope='Nine actual exported surface rays per patch. Alpha deposits/black sealant on the same grade are allowed; columns, walls, glass, curbs and wrong floor heights are rejected.'),indent=2)+'\n');print('STRIP VALUE SURFACES',sum(len(r['samples']) for r in rows.values()),'PASS')
