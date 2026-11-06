"""True-distance optical fixture, using two imported reusable game heads."""
import sys,math,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from render import setup
from setting import load,clone
from kit import model as G
from deliver import bundle

def main(width=1600,samples=32):
 source=Path('export/parts/Head_three.gltf');out=Path('renders/checkpoint/optics');out.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.read_factory_settings(use_empty=True);lib,obs=load(source);r=next(iter(lib.values()))
 cases=[]
 for i,x in enumerate((-1.,1.)):
  rt=clone(r,'Lit' if i==0 else 'Dark',(x,0,7));lenses=[]
  for o in rt.children_recursive:
   if o.get('signal_lens'):
    on=i==0 and o.get('signal_kind')=='red';o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(bpy.data.materials['SharedLens_Lit' if on else 'SharedLens_Off']);lenses.append(o)
  cases.append((rt,lenses))
 for o in obs:bpy.data.objects.remove(o,do_unlink=True)
 # Presentation-only test rig has physically supported heads, all original.
 ma=bpy.data.materials.new('Comparison rig');ma.diffuse_color=(.08,.08,.075,1)
 for x in (-1.,1.):G.cylinder('Fixture vertical',(x,0,0),(x,0,7.04),.03,ma,12)
 G.mesh('Ground',[(-300,-300,0),(300,-300,0),(300,300,0),(-300,300,0)],[(0,1,2,3)],ma)
 cam,sun,bg,sky=setup(samples);sc=bpy.context.scene;cam.data.lens=50
 bpy.context.view_layer.update();centers=[]
 for rt,lenses in cases:
  lens=next(o for o in lenses if o.get('signal_kind')=='red');pts=[lens.matrix_world@v.co for v in lens.data.vertices];centers.append((lens,sum(pts,Vector())/len(pts)))
 reports=[]
 for distance in (30,100):
  mid=(centers[0][1]+centers[1][1])/2;dy=math.sqrt(distance**2-(mid.z-1.18)**2-1)
  cam.location=(mid.x,mid.y-dy,1.18);cam.rotation_euler=(mid-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
  sc.render.resolution_x=width;sc.render.resolution_y=round(width*.5625);sc.render.resolution_percentage=100;sc.render.filepath=str((out/f'{distance}m.png').resolve())
  bpy.ops.render.render(write_still=True);rows=[]
  for lens,center in centers:
   coords=[world_to_camera_view(sc,cam,lens.matrix_world@v.co) for v in lens.data.vertices]
   rows.append(dict(lens=lens.name,distance_m=(center-cam.location).length,rect_pixels=[min(p.x for p in coords)*width,(1-max(p.y for p in coords))*sc.render.resolution_y,max(p.x for p in coords)*width,(1-min(p.y for p in coords))*sc.render.resolution_y]))
  reports.append(dict(distance=distance,heads=rows));(out/f'{distance}m.json').write_text(json.dumps(dict(source=str(source),bundle_sha256=bundle(source),heads=rows,engine='CYCLES',width=width,samples=samples),indent=2))
 Path('build/lens-distances.json').write_text(json.dumps(reports,indent=2))
if __name__=='__main__':main()
