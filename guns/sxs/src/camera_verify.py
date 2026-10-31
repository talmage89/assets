"""Independent Blender projection verification, including actual crop shifts."""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
BASE=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--calibration',default=str(BASE/'build/cameras.json'))
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
sc=bpy.context.scene
cam=bpy.data.objects.new('Camera verification',bpy.data.cameras.new('Camera verification'));sc.collection.objects.link(cam)
cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36
for name,row in json.loads(Path(args.calibration).read_text()).items():
 s=row['shot'];w=row['crop'][2]-row['crop'][0];h=row['crop'][3]-row['crop'][1]
 sc.render.resolution_x=w;sc.render.resolution_y=h;sc.render.resolution_percentage=100
 cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',s['roll']);cam.data.lens=s['lens']
 cam.data.shift_x=s.get('shift_x',0);cam.data.shift_y=s.get('shift_y',0);bpy.context.view_layer.update()
 errors=[]
 for p,expected in zip(row['landmarks_world_m'],row['projected_pixels']):
  v=world_to_camera_view(sc,cam,Vector(p));errors.append(math.dist((v.x*w,(1-v.y)*h),expected))
 assert max(errors)<.05,(name,max(errors))
 print('CAMERA VERIFIED',name,'maximum projection disagreement',max(errors),'px')
