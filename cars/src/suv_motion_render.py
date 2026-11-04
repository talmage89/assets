"""Source articulation views with sampled actual-vertex paths.

Orange lines are tracked vertices, not swept-volume boundaries. Numerical
solid clearance is independently established by suv_motion.py on both meshes.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G,studio
from suv_mechanics import update_supports


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--width',type=int,default=1600);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    src=Path(a.source);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    metadata={}
    for view,eye,target in [('front',(7,-9,4.4),(0,-.1,1.0)),('rear',(-7,9,4.6),(0,.2,1.0))]:
        bpy.ops.wm.open_mainfile(filepath=str(src.resolve()));sc=bpy.context.scene
        camera=studio.add_studio(scale=2.5)
        for ob in sc.objects:
            if ob.get('studio') and ob.type=='MESH':ob.hide_render=True
        for mat in bpy.data.materials:
            mat.diffuse_color=(.25,.32,.34,1) if mat.get('vehicle_paint') else (.06,.07,.08,1)
        trace=studio.studio_mat('Sampled vertex path',(.95,.28,.045),.6);trace.diffuse_color=(.95,.28,.045,1)
        moving={**{f'Door_{end}{side}':60*(-1 if side=='R' else 1) for end in ['F','R'] for side in ['L','R']},'Hood':-65,'Liftgate':75}
        records={}
        for name,angle in moving.items():
            pivot=bpy.data.objects[name];rest=pivot.matrix_basis.copy();mesh_name='Hood outer' if name=='Hood' else 'Liftgate outer' if name=='Liftgate' else 'Door '+name[-2]+'_'+name[-1]
            ob=bpy.data.objects[mesh_name];ps=[ob.matrix_world@v.co for v in ob.data.vertices]
            if name.startswith('Door'):
                end=max(p.y for p in ps);tips=[min((p for p in ps if p.y>end-.03),key=lambda p:p.z),max((p for p in ps if p.y>end-.03),key=lambda p:p.z)]
            elif name=='Hood':tips=[min((p for p in ps if p.x*sign>.4),key=lambda p:p.y) for sign in [-1,1]]
            else:tips=[min((p for p in ps if p.x*sign>.4),key=lambda p:p.z) for sign in [-1,1]]
            local=[pivot.matrix_world.inverted()@tip for tip in tips]
            for i,point in enumerate(local):
                path=[]
                for j in range(31):
                    pivot.matrix_basis=rest@Matrix.Rotation(math.radians(angle*j/30),4,pivot['pivot_axis']);bpy.context.view_layer.update();path.append(pivot.matrix_world@point)
                line=G.tube(name+' sampled path '+str(i),path,.002,trace,4);line['studio']=True
            pivot.matrix_basis=rest@Matrix.Rotation(math.radians(angle),4,pivot['pivot_axis']);bpy.context.view_layer.update()
            records[name]=dict(angle_degrees=angle,tracked_vertices=[list(t) for t in tips],samples=31)
        update_supports();camera.location=eye;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=70;camera.data.sensor_width=36;camera.data.sensor_fit='HORIZONTAL'
        sc.render.engine='BLENDER_WORKBENCH';sh=sc.display.shading;sh.light='STUDIO';sh.color_type='MATERIAL';sh.show_cavity=True;sh.cavity_type='BOTH';sh.show_object_outline=False;sh.background_type='WORLD'
        sc.render.film_transparent=True;sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/1.65);sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.display.render_aa='32';sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0
        name='sweeps_'+view;sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        metadata[name]=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),stage='Source; actual vertex trajectories, not swept volumes',parts=records)
    (out/'sweeps.json').write_text(json.dumps(metadata,indent=2))

if __name__=='__main__':main()
