"""All-visible-surface curvature and reflected stripes, source or shipped GLB.

Curvature measures positions. Stripes use authored shading normals, and retain
the delivered tangent map for a GLB. These are independent of studio approval.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import gpu
from hatch_views import SHOTS
from hatch_render import stripes
import hatch_curvature_map as C
from hatch_round4_render import camera


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
    p.add_argument('--mode',choices=['curvature','horizontal','vertical'],required=True);p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=24)
    p.add_argument('--shots',default='front_three_quarter,rear_three_quarter,side,front,rear,lamp_unlit,wheel,grille,rear_quarter')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    final=source.suffix=='.glb'
    if final:
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source))
    else:bpy.ops.wm.open_mainfile(filepath=str(source))
    sc=bpy.context.scene
    if a.mode=='curvature':
        if final:
            # glTF splits vertices at UV/normal boundaries. Weld coincident
            # positions solely for the geometric diagnostic, never the export.
            for ob in sc.objects:
                if ob.type!='MESH':continue
                bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.to_mesh(ob.data);bm.free()
        report=C.apply();report.update(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),stage='imported GLB' if final else 'procedural source')
        (out/'curvature.json').write_text(json.dumps(report,indent=2))
        sc.render.engine='BLENDER_WORKBENCH';sh=sc.display.shading;sh.light='FLAT';sh.color_type='VERTEX';sh.show_shadows=False;sh.show_cavity=False;sh.show_specular_highlight=False;sh.show_object_outline=False
        sc.display.render_aa='32';sc.world=bpy.data.worlds.new('H120 diagnostic');sc.world.color=(.04,.04,.04)
        sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0
    else:
        stripes(sc,a.mode)
        for mat in bpy.data.materials:
            if not mat.use_nodes:continue
            nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
            if bs is None:continue
            for so in ['Base Color','Roughness','Metallic','Coat Weight','Emission Strength','Transmission Weight']:
                for link in list(bs.inputs[so].links):nt.links.remove(link)
            bs.inputs['Base Color'].default_value=(.20,.20,.20,1);bs.inputs['Metallic'].default_value=.85;bs.inputs['Roughness'].default_value=.045;bs.inputs['Coat Weight'].default_value=0;bs.inputs['Emission Strength'].default_value=0;bs.inputs['Transmission Weight'].default_value=0
        sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=6
        sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.2
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
    meta={}
    for name in a.shots.split(','):
        shot=SHOTS[name];camera(sc,shot,a.width);key=a.mode+'_'+name
        sc.render.filepath=str((out/(key+'.png')).resolve());bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        meta[key]=dict(shot,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),mode=a.mode,width=a.width)
        (out/(a.mode+'-shots.json')).write_text(json.dumps(meta,indent=2))
        print('H120_SURFACE_PROOF',key,flush=True)
    from hatch_detail_review import sheet
    sheet(out,list(meta),out/(a.mode+'-contact.jpg'),3,(600,430))
if __name__=='__main__':main()
