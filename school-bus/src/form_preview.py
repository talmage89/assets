"""Fast serial Workbench form views; no bake or delivery claim."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from views import SHOTS

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True)
    p.add_argument('--out',required=True);p.add_argument('--shots',default='front_detail,side')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
    sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH'
    sc.display.shading.light='STUDIO';sc.display.shading.studiolight_rotate_z=.55
    sc.display.shading.color_type='MATERIAL';sc.display.shading.show_shadows=True
    sc.display.shading.show_cavity=True;sc.display.shading.cavity_type='BOTH'
    sc.display.shading.background_type='WORLD'
    if sc.world is None:sc.world=bpy.data.worlds.new('Form world')
    sc.world.color=(.15,.15,.15)
    for ob in sc.objects:
        if ob.get('bake_only'):ob.hide_render=True
    cam=bpy.data.objects.new('Form camera',bpy.data.cameras.new('Form camera'))
    sc.collection.objects.link(cam);sc.camera=cam;cam.data.clip_start=.02
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    sc.render.image_settings.file_format='PNG';sc.render.resolution_percentage=100
    for name in a.shots.split(','):
        s=SHOTS[name];cam.location=s['location']
        cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.data.type='ORTHO' if 'ortho' in s else 'PERSP'
        cam.data.lens=s['lens'];cam.data.ortho_scale=s.get('ortho',14)
        sc.render.resolution_x=1000;sc.render.resolution_y=round(1000/s['aspect'])
        sc.render.filepath=str((out/f'{name}.png').resolve())
        bpy.ops.render.render(write_still=True)
    (out/'source.json').write_text(json.dumps(dict(source=a.source,stage='Workbench source form preview')))

if __name__=='__main__':main()
