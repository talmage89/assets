"""Cycles checkpoint views import only published glTF, never the source blend."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit import model as G
from kit.gpu import enable
from kit.studio import human


def camera(sc,pos,target,lens=40,ortho=None,roll=0):
    ob=bpy.data.objects.new('ReviewCamera',bpy.data.cameras.new('ReviewCamera'));sc.collection.objects.link(ob);sc.camera=ob
    ob.location=pos;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.rotation_euler.rotate_axis('Z',roll)
    ob.data.lens=lens;ob.data.sensor_width=36;ob.data.sensor_fit='HORIZONTAL'
    if ortho:ob.data.type='ORTHO';ob.data.ortho_scale=ortho
    return ob


def stage(source,width,samples,aspect=1.5):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));sc=bpy.context.scene;sc.render.engine='CYCLES';enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.seed=41
    sc.render.resolution_x=width;sc.render.resolution_y=round(width/aspect);sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG';sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.25
    world=bpy.data.worlds.new('Procedural daylight');world.use_nodes=True;sc.world=world
    nodes=world.node_tree.nodes;sky=nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(21);sky.sun_rotation=math.radians(220);sky.sun_disc=False
    world.node_tree.links.new(sky.outputs[0],nodes['Background'].inputs[0]);nodes['Background'].inputs[1].default_value=.22
    sun=bpy.data.objects.new('Raking sun 21 degrees',bpy.data.lights.new('Raking sun','SUN'));sc.collection.objects.link(sun);sun.data.energy=3.0;sun.data.angle=math.radians(.8);sun.rotation_euler=Vector((.65,.73,-.40)).to_track_quat('-Z','Y').to_euler()
    return sc


def plane(z=0,size=22):
    mat=bpy.data.materials.new('Review neutral ground');mat.diffuse_color=(.21,.23,.21,1)
    mat.use_nodes=True;mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.21,.23,.21,1)
    G.box('Review ground',(0,0,z-.05),(240,240,.10),mat,0)


def scale_people(pos=(-1,-2,0)):
    obs=human()
    for o in obs:o.location+=Vector((pos[0]+1.03,pos[1]-.24,pos[2]))
    bpy.context.view_layer.update()
    # All mesh coordinates transformed uniformly about the original human origin.
    # 1.1 m child is a scale marker, not an anatomical child model.
    for o in obs:
        c=o.copy();c.data=o.data.copy();bpy.context.collection.objects.link(c);c.name='ChildScale_'+o.name
        factor=1.1/1.8
        # Original human geometry is authored about (-1.03,.24); use world frame.
        for v in c.data.vertices:v.co=(o.matrix_world@v.co-Vector(pos))*factor+Vector((pos[0]+.75,pos[1],pos[2]))
        c.matrix_world=Matrix.Identity(4)


def zones(sc,plan):
    mats=[]
    for i,z in enumerate(plan['zones']):
        mat=bpy.data.materials.new('Zone '+z['group']);mat.diffuse_color=[(.02,.55,.85,1),(.95,.24,.02,1),(.75,.15,.65,1),(.80,.65,.03,1)][i%4]
        mat.use_nodes=True;mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=mat.diffuse_color
        a,b,c,d=z['rect'];pts=[(a,b,.035),(c,b,.035),(c,d,.035),(a,d,.035),(a,b,.035)]
        G.tube('Review use zone '+z['name'],pts,.034,mat,6)


def save(sc,out,source,shot):
    out.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True)
    doc=json.loads(source.read_text());files=[source]+[source.parent/r['uri'] for k in ('buffers','images') for r in doc.get(k,[]) if r.get('uri')]
    stage_name='look-dev / exported glTF / shared baked maps' if any('T_PlayMetal' in im.get('uri','') for im in doc.get('images',[])) else 'before / exported glTF / quick form materials'
    bundle=hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()
    labels=[]
    if shot=='pieces':
        from bpy_extras.object_utils import world_to_camera_view
        for ob in sc.objects:
            if ob.type=='EMPTY' and ob.get('module'):
                uv=world_to_camera_view(sc,sc.camera,ob.matrix_world.translation)
                labels.append(dict(name=ob['module'],pixel=[uv.x*sc.render.resolution_x,(1-uv.y)*sc.render.resolution_y+18]))
    out.with_suffix('.json').write_text(json.dumps(dict(piece_labels=labels,stage=stage_name,source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),resource_bundle_sha256=bundle,shot=shot,engine='CYCLES',width=sc.render.resolution_x,samples=sc.cycles.samples,camera_location=list(sc.camera.location),camera_matrix_world=[list(row) for row in sc.camera.matrix_world],camera_type=sc.camera.data.type,orthographic_scale=sc.camera.data.ortho_scale,lens_mm=sc.camera.data.lens,exposure=sc.view_settings.exposure),indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--out',type=Path,default=Path('renders/checkpoint'));p.add_argument('--width',type=int,default=1200);p.add_argument('--samples',type=int,default=24);p.add_argument('--seeds',default='101,202,303');p.add_argument('--shots',default='all');p.add_argument('--matches',action='store_true');p.add_argument('--export-root',type=Path,default=Path('export'));p.add_argument('--no-setting',action='store_true');p.add_argument('--resume',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.matches:
        from kit.photo_match import verify
        verify('build/cameras.json')
        for name,row in json.loads(Path('build/cameras.json').read_text()).items():
            source=a.export_root/row['source'];shot=row['shot'];sc=stage(source,a.width,a.samples,shot['aspect']);sc.view_settings.exposure=shot.get('exposure',-.25)
            if not a.no_setting:
                from setting import context
                context(json.loads(source.with_suffix('.json').read_text()))
            sun=next(o for o in sc.objects if o.type=='LIGHT' and o.data.type=='SUN')
            if 'swings' in name:sun.data.energy=.15;sc.world.node_tree.nodes['Background'].inputs[1].default_value=.32
            elif 'stair' in name:sun.data.energy=.35;sc.world.node_tree.nodes['Background'].inputs[1].default_value=.28
            else:sun.data.energy=2.2
            camera(sc,shot['location'],shot['target'],shot['lens'],roll=shot['roll']);save(sc,a.out/'matches'/f'{name}.png',source,name)

        return
    wanted=set(a.shots.split(','))
    def want(n):return 'all' in wanted or n in wanted
    for seed in map(int,a.seeds.split(',')):
        plan=json.loads((a.export_root/f'Playground-{seed}.json').read_text());source=a.export_root/f'Playground-{seed}.gltf';x0,y0,x1,y1=plan['surface'];cx=(x0+x1)/2;cy=(y0+y1)/2
        for shot in ('hero','above'):
            if not want(shot):continue
            if a.resume and (a.out/str(seed)/(shot+'.png')).exists():continue
            sc=stage(source,a.width,a.samples)
            if not a.no_setting:
                from setting import context
                context(plan)
            if shot=='hero':
                pos={1996:(-6,-11,1.65),2005:(7,-11,1.65),2013:(-8,-15.4,1.65)}[plan['year']]
                camera(sc,pos,(1,.5,1.55),40)
            else:
                # Hide canopy/trees only in measured plan, to reveal access and zones.
                for o in sc.objects:
                    if ('Library_' in o.name and ('Maple' in o.name or 'Oak' in o.name)) or 'shade tree' in o.name or 'park grove' in o.name:o.hide_render=True
                bounds={1996:(-10.1,-7.6,19.5,10.0),2005:(-16.8,-6.0,12.35,8.0),2013:(-9.6,-13.4,20.55,8.8)}[plan['year']]
                ax,ay,bx,by=bounds;cx=(ax+bx)/2;cy=(ay+by)/2
                zones(sc,plan);camera(sc,(cx,cy,48),(cx,cy,0),40,ortho=max(bx-ax,by-ay)*1.13)
                sc.render.resolution_y=round(a.width*.90)
            save(sc,a.out/str(seed)/(shot+'.png'),source,shot)
    specs={
      'arch-swing':('Playground-202.gltf',(-6.5,-9,1.65),(-11.1,1,1.1),40,None,1.5),
      'swing-seat':('Playground-202.gltf',(-11.2,-.3,.73),(-12.19,1,.43),65,None,1.4),
      'bucket-seat':('Playground-202.gltf',(-9,-.4,1.05),(-10.01,1,.78),65,None,1.4),
      'tube-junction':('Playground-303.gltf',(8.6,-1.1,1.2),(6.90,1.2192,.55),55,None,1.4),
      'rubber-wear':('Playground-303.gltf',(6.8,-.2,.70),(7.32,1.2192,-.005),50,None,1.4),
      'stairs':('Playground-101.gltf',(-4.3,-2.8,1.85),(-1.65,0,.85),48,None,1.4),
      'transfer':('Playground-202.gltf',(2,-3.4,1.5),(0,-1.15,.45),52,None,1.4),
      'swing-hollow':('Playground-202.gltf',(-10.5,-2.9,1.5),(-12.19,1,-.025),50,None,1.4),
      'pieces':('PlaygroundPieces.gltf',(21,-20,45),(21,15,0),45,53,1.15),
      'clamp-deck':('Playground-101.gltf',(-1.56,-1.75,1.87),(-.50,-.49,1.22),65,None,1.4),
      'slide-entrance':('Playground-101.gltf',(1.35,-3,1.75),(0,-1.5,1.16),55,None,1.4),
      'slide-exit':('Playground-101.gltf',(1.5,-5.8,.85),(0,-3.55,.21),55,None,1.4),
      'swing-hanger':('Playground-202.gltf',(-12.2,-.35,2.17),(-12.52,1,2.18),65,None,1.4),
      'climber':('Playground-202.gltf',(3.7,-2.5,1.55),(1.219,-.2,.82),50,None,1.4),
      'molded-sections':('SlideSpiral72.gltf',(4,-5,2.5),(1,-.2,1),45,None,1.4),
      'scale':('Playground-303.gltf',(-7,-14,1.65),(0,-.3,1.1),40,None,1.5),
      'swing':('Playground-101.gltf',(11,-6,2.5),(9,1,1.2),45,None,1.5),
    }
    for shot,(filename,pos,target,lens,ortho,aspect) in specs.items():
        if not want(shot):continue
        if a.resume and (a.out/(shot+'.png')).exists():continue
        source=a.export_root/filename;sc=stage(source,a.width,a.samples,aspect)
        if filename.startswith('Playground-') and not a.no_setting:
            from setting import context
            context(json.loads(source.with_suffix('.json').read_text()))
        if not filename.startswith('Playground-') and shot!='pieces':plane(z=-2.1 if shot=='swing-hanger' else 0)
        if shot=='scale':scale_people((-2.5,-4.8,0))
        if shot=='pieces':plane(size=110);sc.render.resolution_x=a.width*2;sc.render.resolution_y=round(a.width*2/1.15)
        camera(sc,pos,target,lens,ortho);save(sc,a.out/(shot+'.png'),source,shot)

if __name__=='__main__':main()
