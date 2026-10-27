"""Outdoor product lighting; final geometry is exclusively an exported GLB."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from kit import gpu
from dimensions import *
from views import SHOTS,TITLE
from kit.tiling import world_uv


def dress_street():
    """Optional main-branch library context; never part of Ground exports."""
    specs=[('fire-hydrant','FireHydrant.glb',(-5.15,-17.5,.148),90),
           ('mailbox','Mailbox.glb',(4.75,-28.9,ROAD_EDGE),-90),
           ('trash-cart','TrashCart.glb',(4.68,-19.8,.148),-90),
           ('street-signs','StreetSigns.glb',(5.25,-12,.148),0),
           ('street-light','StreetLight.glb',(-5.40,13,.148),90)]
    added=[];provenance=[]
    for folder,name,loc,yaw in specs:
        source=Path('..')/folder/'export'/name
        check=Path('build/context-props.json')
        status=json.loads(check.read_text()) if check.exists() else {}
        if not source.exists() or status.get(folder,{}).get('returncode',1):continue
        before=set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
        objects=set(bpy.data.objects)-before
        root=bpy.data.objects.new('Context_'+folder,None);bpy.context.scene.collection.objects.link(root)
        for ob in objects:
            if ob.parent not in objects:ob.parent=root
        root.location=loc;root.rotation_euler.z=math.radians(yaw)
        added.extend(objects);added.append(root)
        provenance.append(dict(source=str(source.resolve()),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),location=loc,yaw=yaw))
        if folder=='street-light':
            for ob in objects:
                if ob.type!='MESH':continue
                for mat in ob.data.materials:
                    if mat and mat.use_nodes:
                        for node in mat.node_tree.nodes:
                            if node.type=='BSDF_PRINCIPLED':node.inputs['Emission Strength'].default_value=0
    return added,provenance


def human():
    # Neutral 1.8 m silhouette, only a scale aid, never part of the export.
    mat=bpy.data.materials.new('Scale figure');mat.diffuse_color=(.08,.105,.11,1)
    obs=[]
    def capsule(name,a,b,r):
        a,b=Vector(a),Vector(b);mid=(a+b)/2
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=mid)
        ob=bpy.context.object;ob.name=name;ob.scale=(r,r,(b-a).length/2+r)
        ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();ob.data.materials.append(mat);obs.append(ob)
    x,y,z=6.75,-10.4,CURB_HEIGHT+(6.75-WALK_IN)*WALK_SLOPE
    def p(a,b,c):return (x+a,y+b,z+c)
    capsule('Human torso',p(0,0,.93),p(0,0,1.43),.15)
    capsule('Human head',p(0,0,1.63),p(0,0,1.68),.12)
    for side in (-1,1):
        capsule('Human leg',p(side*.09,0,.075),p(side*.09,0,.89),.075)
        capsule('Human arm',p(side*.20,0,.92),p(side*.20,0,1.40),.055)
    return obs


def presentation_grade(mat):
    """Distant context only, outside the exported sample's rectangular bounds.

    The delivered lawn is never covered. Rim heights meet the sample and fade
    toward the procedural horizon, avoiding a floating rectangular display mat.
    """
    bounds=(CORE+3*LENGTH,CORE+6*LENGTH)
    def section(p):
        p=abs(p)
        if p<=ASPHALT_HALF:return road_z(p)-.003
        if p<=FACE:return 0
        if p<=BACK:return CURB_HEIGHT-.003
        if p<=WALK_IN:return CURB_HEIGHT-.007
        if p<=WALK_OUT:return CURB_HEIGHT+(p-WALK_IN)*WALK_SLOPE-.003
        return YARD_GRADE-.005+.004*(p-WALK_OUT)
    for axis in (0,1):
        extent=bounds[axis];other=bounds[1-axis]
        stops=sorted(set([-other,-CORE,-WALK_OUT,-WALK_IN,-BACK,-FACE,-ASPHALT_HALF,0,ASPHALT_HALF,FACE,BACK,WALK_IN,WALK_OUT,CORE,other]+([-2000,-other-2,other+2,2000] if axis==1 else [])))
        for sign in (-1,1):
            verts=[];faces=[]
            for offset in (0,2,2000):
                for p in stops:
                    z=section(p)
                    if axis==0 and WALK_OUT<abs(p)<CORE:
                        depth=CORE-WALK_OUT;t=(abs(p)-WALK_OUT)/depth;h=t*t*(3-2*t)
                        z=YARD_GRADE-.005+.004*depth*(t+t*t-t*t*t)+h*.004*(extent-WALK_OUT-depth)
                    if axis==0 and abs(p)>=CORE:z=YARD_GRADE-.005+.004*(extent-WALK_OUT)
                    if axis==1 and abs(p)>bounds[0]:
                        blend=min(1,(abs(p)-bounds[0])/2)
                        rim=YARD_GRADE-.005+.004*(bounds[0]-WALK_OUT)
                        z=rim*(1-blend)+.14*blend
                    if offset>0:z=.14
                    v=[0,0,z];v[axis]=sign*(extent+offset);v[1-axis]=p;verts.append(v)
            w=len(stops)
            for j in range(2):
                for i in range(w-1):
                    a=j*w+i
                    for f in ((a,a+1,a+w+1),(a,a+w+1,a+w)):
                        pp=[Vector(verts[k]) for k in f]
                        faces.append(f if (pp[1]-pp[0]).cross(pp[2]-pp[0]).z>0 else tuple(reversed(f)))
            me=bpy.data.meshes.new('Distant context');me.from_pydata(verts,[],faces);me.materials.append(mat)
            ob=bpy.data.objects.new('Distant lawn outside sample',me);bpy.context.collection.objects.link(ob)
            world_uv(ob,LAWN_TILE)
            attr=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
            for c in attr.data:c.color=(.95,.95,.95,1)


def setup(engine,samples,grade=True):
    sc=bpy.context.scene;sc.render.engine=engine
    if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
    sc.world=bpy.data.worlds.new('Original procedural daylight');sc.world.use_nodes=True
    ns=sc.world.node_tree.nodes;ns.clear();sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(38);sky.sun_rotation=math.radians(205);sky.altitude=.1;sky.air_density=1.0;sky.aerosol_density=.35;sky.sun_disc=False
    bg=ns.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.08
    out=ns.new('ShaderNodeOutputWorld');sc.world.node_tree.links.new(sky.outputs['Color'],bg.inputs['Color']);sc.world.node_tree.links.new(bg.outputs[0],out.inputs[0])
    # Explicit solar disk gives the same crisp side daylight in Cycles/Eevee.
    direction=Vector((math.cos(math.radians(38))*math.cos(math.radians(205)),math.cos(math.radians(38))*math.sin(math.radians(205)),math.sin(math.radians(38))))
    ld=bpy.data.lights.new('Side sun / 38 degrees','SUN');lo=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(lo);ld.use_nodes=False;ld.energy=12.;ld.angle=math.radians(.53)
    lo.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
    # Neutral fallback for the isolated tile boards; street context uses lawn.
    mat=bpy.data.materials.new('Neutral presentation substrate');mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.12,.12,.12,1);bs.inputs['Roughness'].default_value=.95
    # Delivered lawn modules fill the former raised neutral grade. Only the
    # distant horizon backdrop lies outside the exported sample, below all
    # paving and below the inlet basin; it reuses the imported lawn maps.
    bpy.ops.mesh.primitive_plane_add(size=10000,location=(0,0,-.36));floor=bpy.context.object;floor.name='Distant lawn backdrop'
    lawn=bpy.data.materials.get('Lawn') if grade else None
    floor.data.materials.append(lawn or mat)
    if lawn:
        presentation_grade(lawn)
        world_uv(floor,LAWN_TILE)
        attr=floor.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for c in attr.data:c.color=(.95,.95,.95,1)
    camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(camera);sc.camera=camera
    camera.data.clip_start=.03;camera.data.clip_end=10000;camera.data.sensor_fit='HORIZONTAL';camera.data.sensor_width=36
    # Preserve saturated material colors; AgX lifted federal yellow to peach.
    sc.view_settings.view_transform='Khronos PBR Neutral';sc.view_settings.look='None';sc.view_settings.exposure=-.5
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=False
    return camera


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--stage',default='final',choices=['final','source']);p.add_argument('--out',type=Path,required=True);p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=64);p.add_argument('--engine',default='CYCLES');p.add_argument('--shots');p.add_argument('--camera-file',type=Path)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.stage=='final':
        assert a.source.suffix=='.glb'
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.source.resolve()))
    else:
        assert a.source.suffix=='.blend';bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
        assert bpy.context.scene.get('ground_source_stage')
    camera=setup(a.engine,a.samples,grade=a.source.stem!='GroundTiles');sc=bpy.context.scene
    defs={n:v['shot'] for n,v in json.loads(a.camera_file.read_text()).items()} if a.camera_file else SHOTS
    names=a.shots.split(',') if a.shots else [n for n in defs if not n.startswith('tile_')]
    a.out.mkdir(parents=True,exist_ok=True);meta_path=a.out/'shots.json'
    meta=json.loads(meta_path.read_text()) if meta_path.exists() else {}
    digest=hashlib.sha256(a.source.read_bytes()).hexdigest()
    for name in names:
        shot=defs[name];camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler();camera.rotation_euler.rotate_axis('Z',shot.get('roll',0))
        camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP'
        camera.data.ortho_scale=shot.get('ortho',10);camera.data.lens=shot.get('lens',45)
        sc.render.resolution_x=a.width;sc.render.resolution_y=round(a.width/shot.get('aspect',1.5));sc.render.resolution_percentage=100
        hs=human() if shot.get('human') else []
        props,prop_meta=dress_street() if shot.get('dress') else ([],[])
        sc.render.filepath=str((a.out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        for ob in hs+props:bpy.data.objects.remove(ob,do_unlink=True)
        meta[name]=dict(stage=a.stage,source=str(a.source.resolve()),source_sha256=digest,engine=a.engine,samples=a.samples,shot=shot,lighting=dict(sun_elevation_degrees=38,sun_azimuth_degrees=205,sun_energy=12,sky_strength=.08,view_transform=sc.view_settings.view_transform,exposure=sc.view_settings.exposure))
        meta[name]['context_props']=prop_meta
        meta_path.write_text(json.dumps(meta,indent=2))

if __name__=='__main__':main()
