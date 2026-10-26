"""Project delivered vertices into the recorded whole-object studio cameras.

This measures actual GLB geometry after posing, independently of raster output.
Detail crops are intentional; whole-module, scale and assembled views must fit.
"""
import argparse,json,hashlib,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Euler
from bpy_extras.object_utils import world_to_camera_view
FULL={'hero_closed','hero_open','front','side','back','top','gate','gate_back','pieces','posts','scale','corner_good','corner_rails'}
ROOT=Path(__file__).resolve().parents[1]

def check(folder):
    metadata=json.loads((folder/'shots.json').read_text());groups={}
    for name,shot in metadata.items():
        if name in FULL:groups.setdefault(shot['source'],[]).append((name,shot))
    rows=[]
    for source,shots in groups.items():
        path=Path(source);digest=hashlib.sha256(path.read_bytes()).hexdigest()
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path));scene=bpy.context.scene;obs=scene.objects
        rest={o.name:o.matrix_basis.copy() for o in obs};camera=bpy.data.objects.new('Frame proof camera',bpy.data.cameras.new('Frame proof camera'));scene.collection.objects.link(camera)
        for name,shot in shots:
            assert shot['stage']=='final' and shot['source_sha256']==digest
            for n,mat in rest.items():obs[n].matrix_basis=mat
            for n,pose in shot.get('parts',{}).items():
                if 'translation' in pose:obs[n].location+=Vector(pose['translation'])
                if 'rotation_degrees' in pose:
                    obs[n].rotation_mode='XYZ';obs[n].rotation_euler.rotate(Euler(tuple(math.radians(x) for x in pose['rotation_degrees'])))
            scene.render.resolution_x=shot['width'];scene.render.resolution_y=shot['height'];camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
            camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.ortho_scale=shot.get('ortho',1);camera.data.lens=shot.get('lens',70);camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36
            bpy.context.view_layer.update();points=[]
            for ob in obs:
                if ob.type!='MESH' or 'asset_set' not in ob:continue
                hidden=ob.get('bake_only',False) or any(ob.name.startswith(p) for p in shot.get('hide',[])) or ob.get('asset_set') in shot.get('hide_sets',[])
                parent=ob.parent
                while parent:
                    hidden|=parent.name in shot.get('hide_assemblies',[]);parent=parent.parent
                if hidden:continue
                points.extend(world_to_camera_view(scene,camera,ob.matrix_world@v.co) for v in ob.data.vertices)
            lo=[min(p[i] for p in points) for i in (0,1)];hi=[max(p[i] for p in points) for i in (0,1)];behind=min(p.z for p in points)<=0
            passed=not behind and min(lo)>=-.003 and max(hi)<=1.003
            rows.append(dict(shot=name,folder=str(folder),source=source,projected_min=lo,projected_max=hi,vertices=len(points),passed=passed))
    return rows
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--cycles-only',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);rows=[]
for root in (ROOT,ROOT/'picket',ROOT/'chain-link'):
    for sub in (('final',) if a.cycles_only else ('final','final-eevee','assembly')):rows.extend(check(root/'renders'/sub))
report=dict(passed=all(r['passed'] for r in rows),views=rows);Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if not report['passed']:raise RuntimeError('Whole-object studio view crops delivered geometry')
