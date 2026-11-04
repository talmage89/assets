"""Unlit geometric H maps beside matched reflection stripes, actual game skin."""
import argparse,sys,json,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import studio,gpu
from sedan_curvature_map import apply,self_test
from sedan_render import SHOTS,stripes

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--width',type=int,default=1100);p.add_argument('--parent',action='store_true');p.add_argument('--maps-only',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    src=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);reports={}
    self_test()
    for mode in ['curvature'] if a.maps_only else ['curvature','horizontal','vertical']:
        bpy.ops.wm.open_mainfile(filepath=str(src))
        if a.parent:
            from sedan_body import master
            for ob in list(bpy.data.objects):bpy.data.objects.remove(ob,do_unlink=True)
            ob,_=master(2);obs=[ob]
        else:obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_category') in ['body','doors','fascia','pillars'] and o.data.attributes.get('sheet_role')]
        for ob in bpy.context.scene.objects:
            if ob.type=='MESH' and ob not in obs:ob.hide_render=True
        sc=bpy.context.scene;camera=studio.add_studio(scale=2.5)
        for ob in sc.objects:
            if ob.get('studio') and ob.type in ['MESH','LIGHT']:ob.hide_render=True
        if mode=='curvature':
            reports=apply(obs,a.parent);sc.render.engine='BLENDER_EEVEE';sc.eevee.taa_render_samples=16
            sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0
        else:
            mat=studio.studio_mat('Clay body',(.28,.29,.30),.065)
            for ob in obs:
                ob.data.materials.clear();ob.data.materials.append(mat)
                for f in ob.data.polygons:f.material_index=0
            stripes(sc,mode);sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=16;sc.cycles.use_denoising=True;sc.cycles.max_bounces=3
            sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.2
        for name in ['front_three_quarter','rear_three_quarter','side','front','rear']:
            shot=SHOTS[name];camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.sensor_width=36;camera.data.sensor_fit='HORIZONTAL';camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.lens=shot.get('lens',58);camera.data.ortho_scale=shot.get('ortho',5.7)
            sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot['aspect']);sc.render.resolution_percentage=100;sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
            sc.render.filepath=str((out/(name+'-'+mode+'.png')).resolve());bpy.ops.render.render(write_still=True)
    # Full measurements remain local, including invalid boundary samples.
    (out/'mean-curvature.json').write_text(json.dumps(dict(method='Signed cotangent H with mixed Voronoi area; real game triangle positions, no authored normals; fixed scale -20,-5,-1,0,1,5,20 m^-1; gray excludes cut boundaries and gauge',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),parts=reports),separators=(',',':')))
if __name__=='__main__':main()
