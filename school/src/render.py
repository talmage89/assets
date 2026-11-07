"""Every form view imports the external glTF; no source-scene render shortcut."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix,Euler
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT)]
from kit.gpu import enable
from plans import school,world


def views(p):
    ex,ey=p['entry'];b=next(b for b in p['blocks'] if b['id']==('Finger_A' if p['type']=='finger' else 'Cluster_B' if p['type']=='courtyard' else 'South_Classrooms'))
    face='west' if p['type']=='finger' else 'north' if p['type']=='courtyard' else 'south'
    o=next(o for o in b['openings'] if o['type']=='window' and o['face']==face);pt=world((o['u'],0,0),o['origin'],o['yaw']);nx,ny,_=world((0,-1,0),(0,0),o['yaw']);tx,ty,_=world((1,0,0),(0,0),o['yaw'])
    gym=next(b for b in p['blocks'] if b['kind']=='gym');l,r,f,k=gym['rect']
    door=next(o for o in gym['openings'] if o['type'] in ('double','door'));dp=world((door['u'],0,0),door['origin'],door['yaw'])
    dnx,dny,_=world((0,-1,0),(0,0),door['yaw'])
    result=dict(
      hero=dict(location=(ex-45,ey-57,1.68),target=(ex+6,ey+12,2.50),lens=40,aspect=1.80),
      above=dict(location=(225,-245,210),target=(0,0,0),lens=48,aspect=1.55),
      plan=dict(location=(92,-114,106),target=(0,0,0),lens=45,aspect=1.5),
      rear=dict(location=(68,87,10),target=(8,20,2.0),lens=42,aspect=1.8),
      windows=dict(location=(pt[0]+nx*11+tx*7,pt[1]+ny*11+ty*7,1.68),target=(pt[0]+tx*1.5,pt[1]+ty*1.5,1.95),lens=45,aspect=1.55),
      entry=dict(location=(ex-10,ey-17,1.68),target=(ex,ey,2.0),lens=42,aspect=1.55),
      gym=dict(location=(l-6,f-16,1.68),target=((l+r)/2,f,3.3),lens=40,aspect=1.5),
      door=dict(location=(dp[0]+dnx*4.4-1.4,dp[1]+dny*4.4,1.60),target=(dp[0],dp[1],1.25),lens=48,aspect=1.25),
      roof=dict(location=(r+10,k+13,13),target=((l+r)/2,(f+k)/2,5.5),lens=45,aspect=1.5))
    if p['type']=='finger':result['windows']=dict(location=(pt[0]+nx*6+tx*5,pt[1]+ny*6+ty*5,1.68),target=(pt[0]+tx*1.5,pt[1]+ty*1.5,1.95),lens=35,aspect=1.55)
    result['windows']['light_direction']=(-nx,-ny,-.38)
    result['door']['light_direction']=(-dnx,-dny,-.38)
    result['rear']=dict(location=((-105,55,25) if p['type']=='courtyard' else (105,55,25)),target=((-8,5,1.8) if p['type']=='courtyard' else (8,5,1.8)),lens=35,aspect=1.8)
    if p['type']=='courtyard':
        result['hero']=dict(location=(ex-57,ey-44,1.68),target=(ex+2,ey+9,2.55),lens=40,aspect=1.80)
        result['gym']=dict(location=(l-4,f-10,1.68),target=((l+r)/2,f,3.3),lens=35,aspect=1.5)
    result['hero']=dict(location=p['hero'][0],target=p['hero'][1],lens=40,aspect=1.80)
    # Before/after evidence keeps the checkpoint's world camera unchanged,
    # including when this revision turns a campus toward another frontage.
    old=Path('renders/before')/str(p['seed'])/'provenance.json'
    if old.exists():
        for name in ('hero','above','rear','windows'):
            row=json.loads(old.read_text())[name];result['legacy_'+name]=dict(row['camera'],comparison_light=row['light'])
    # The native silhouette's feet are offset .24m in Y. Seat it on the
    # actual entry-plaza slope, rather than the higher loading curb.
    hz=p['floor']+(.1704-p['floor'])*min(1,.76/(ey-p['bus_curb'][0][1]))
    result['scale']=dict(result['entry'],human=(ex+2,ey-1,hz))
    result['blacktop']=dict(location=(p['blacktop'][1]+14,p['blacktop'][3]+19,14),target=((p['blacktop'][0]+p['blacktop'][1])/2,(p['blacktop'][2]+p['blacktop'][3])/2,0),lens=42,aspect=1.6)
    rotation=Matrix.Rotation(math.radians(p['site_yaw']),4,'Z')
    for name,s in result.items():
        if name in ('above','plan') or name.startswith('legacy_'):continue
        for key in ('location','target','human'):
            if key in s:s[key]=list(rotation@Vector(s[key]))
    return result


def setup(width,samples,light=None):
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=8;sc.cycles.transparent_max_bounces=16;enable()
    worldmat=bpy.data.worlds.new('Procedural school daylight');sc.world=worldmat;worldmat.use_nodes=True
    ns,ls=worldmat.node_tree.nodes,worldmat.node_tree.links;bg=ns.get('Background');sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=math.radians(24);sky.sun_rotation=math.radians(215);sky.altitude=100;sky.air_density=1.1
    sat=ns.new('ShaderNodeHueSaturation');sat.inputs['Saturation'].default_value=.45;ls.new(sky.outputs[0],sat.inputs['Color']);ls.new(sat.outputs[0],bg.inputs[0]);bg.inputs[1].default_value=.08
    ld=bpy.data.lights.new('Raking school sun','SUN');sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun);ld.energy=6;ld.angle=math.radians(.65);ld.color=(1,.97,.93)
    sun.rotation_euler=Vector((.62,.78,-.52)).to_track_quat('-Z','Y').to_euler()
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.30
    if light:
        ld.energy=light.get('energy',3.1);bg.inputs[1].default_value=light.get('sky',.20);ld.angle=math.radians(light.get('softness',1.4))
        sun.rotation_euler=Vector(light.get('direction',(.62,.78,-.52))).to_track_quat('-Z','Y').to_euler()
        sc.view_settings.exposure=light.get('exposure',-.45)
    # The school and static parcel ship in glTF. Native cars and the surrounding
    # neighborhood are intact presentation instances, with separate costs.
    ma=bpy.data.materials.new('Distant ground');ma.use_nodes=True;bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.045,.066,.021,1);bs.inputs['Roughness'].default_value=1
    from kit.model import box
    box('Distant ground',(0,0,-.12),(2400,2400,.10),ma,0)
    cam=bpy.data.objects.new('School review camera',bpy.data.cameras.new('School review camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.clip_end=3000;cam.data.clip_start=.03
    sc.render.resolution_x=width;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    return cam,sun


def digest(path):
    d=json.loads(path.read_text());files=[path]+[path.parent/r['uri'] for k in ('buffers','images') for r in d.get(k,[])];return hashlib.sha256(b''.join(hashlib.sha256(p.read_bytes()).digest() for p in files)).hexdigest()


def render(path,out,width,samples,shots,light=None,engine='CYCLES',plan=None):
    if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    presentation=None
    if plan:
        from neighborhood import context
        presentation=context(plan)
    cam,sun=setup(width,samples,light);sc=bpy.context.scene;sc.render.engine=engine
    if engine=='BLENDER_EEVEE':
        sc.eevee.use_raytracing=True;sc.eevee.ray_tracing_options.resolution_scale='1';sc.eevee.taa_render_samples=samples
        for ma in bpy.data.materials:
            bs=ma.node_tree.nodes.get('Principled BSDF') if ma.use_nodes else None
            if bs and bs.inputs['Transmission Weight'].default_value>0:
                ma.use_raytrace_refraction=True;ma.thickness_mode='SLAB'
                value=ma.node_tree.nodes.new('ShaderNodeValue');value.outputs[0].default_value=.006
                output=next(n for n in ma.node_tree.nodes if n.type=='OUTPUT_MATERIAL');ma.node_tree.links.new(value.outputs[0],output.inputs['Thickness'])
    sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY')
    sky.sun_rotation=math.radians(215+(plan['site_yaw'] if plan else 0))
    from kit.studio import human
    figures=human();rests={o:o.location.copy() for o in figures}
    figure_root=bpy.data.objects.new('Scale silhouette placement',None);sc.collection.objects.link(figure_root)
    figure_root.rotation_euler.z=math.radians(plan['site_yaw'] if plan else 0)
    for ob in figures:ob.parent=figure_root
    out.mkdir(parents=True,exist_ok=True);receipt={}
    default_light=dict(energy=sun.data.energy,sky=sc.world.node_tree.nodes.get('Background').inputs[1].default_value,exposure=sc.view_settings.exposure,angle=sun.data.angle,color=tuple(sun.data.color))
    for name,s in shots.items():
        cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',s.get('roll',0));cam.data.lens=s['lens']
        direction=s.get('light_direction',(light or {}).get('direction',(-.6,-.7,-.30) if name in ('rear','blacktop') else (-.82,.4,-.30)))
        previous=s.get('comparison_light')
        if previous:
            direction=Euler(previous['sun_direction']).to_matrix()@Vector((0,0,-1))
        sun.data.energy=previous['sun_energy'] if previous else default_light['energy']
        sun.data.angle=math.radians(1.4) if previous else default_light['angle']
        sun.data.color=(1,.96,.89) if previous else default_light['color']
        next(n for n in sc.world.node_tree.nodes if n.type=='HUE_SAT').inputs['Saturation'].default_value=1.0 if previous else .45
        sc.world.node_tree.nodes.get('Background').inputs[1].default_value=previous['sky_strength'] if previous else default_light['sky']
        sc.view_settings.exposure=previous['exposure'] if previous else default_light['exposure']
        if plan and not previous:direction=Matrix.Rotation(math.radians(plan['site_yaw']),4,'Z')@Vector(direction)
        sky.sun_rotation=math.radians(215 if previous else 215+(plan['site_yaw'] if plan else 0))
        sun.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler()
        figure_root.location=s.get('human',(0,0,0))
        for ob in figures:
            ob.hide_render='human' not in s;ob.location=rests[ob]
        if engine=='BLENDER_EEVEE':
            # Native library Eevee presentation uses a sky/bounce probe;
            # exported materials and geometry remain unchanged.
            point=Matrix.Rotation(math.radians(plan['site_yaw']),4,'Z')@Vector((*plan['entry'],2.3)) if plan else Vector((0,0,2.3))
            bpy.ops.object.lightprobe_add(type='VOLUME',location=point);probe=bpy.context.object;probe.scale=(50,8,3.4)
            probe.data.resolution_x=14;probe.data.resolution_y=5;probe.data.resolution_z=3;probe.data.bake_samples=32
            probe.data.capture_world=True;probe.data.capture_indirect=True;probe.data.capture_emission=True
            bpy.ops.object.lightprobe_cache_bake(subset='ALL')
        sc.render.resolution_y=round(width/s['aspect']);sc.render.filepath=str((out/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        recipe=hashlib.sha256(b''.join((HERE/f).read_bytes() for f in ('render.py','neighborhood.py'))).hexdigest()
        receipt[name]=dict(source=path.as_posix(),package_sha256=digest(path) if path.suffix=='.gltf' else hashlib.sha256(path.read_bytes()).hexdigest(),presentation_recipe_sha256=recipe,presentation_triangles=presentation.get('placed_presentation_triangles',0) if presentation else 0,two_native_cars_triangles=presentation.get('two_native_cars_triangles',0) if presentation else 0,camera=s,engine=engine,width=width,samples=samples,eye_height_m=s['location'][2],stage=('exported look-dev glTF' if path.suffix=='.gltf' else 'source campus before consolidation/export')+' / canonical baked maps / presentation neighborhood',light=dict(sun_energy=sun.data.energy,sky_strength=sc.world.node_tree.nodes.get('Background').inputs[1].default_value,sun_direction=list(sun.rotation_euler),exposure=sc.view_settings.exposure))
    target=out/'provenance.json';existing=json.loads(target.read_text()) if target.exists() else {};existing.update(receipt);target.write_text(json.dumps(existing,indent=2))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source');ap.add_argument('--seeds',default='101,102,103');ap.add_argument('--out',type=Path,default=Path('renders/checkpoint'));ap.add_argument('--width',type=int,default=1400);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--shots');ap.add_argument('--matches',action='store_true');ap.add_argument('--source-scene',action='store_true');ap.add_argument('--engine',default='CYCLES');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.matches:
        for name,row in json.loads(Path('build/matched-cameras.json').read_text()).items():
            if a.shots and name not in a.shots.split(','):continue
            plan=school(row['seed']);rotation=Matrix.Rotation(math.radians(plan['site_yaw']),4,'Z');shot=dict(row['shot'])
            for key in ('location','target'):shot[key]=list(rotation@Vector(shot[key]))
            path=Path('build' if a.source_scene else 'export')/('Campus-'+str(row['seed'])+('.blend' if a.source_scene else '.gltf'))
            render(path,a.out,a.width,a.samples,{name:shot},row.get('light'),plan=plan)
    else:
        for seed in map(int,a.seeds.split(',')):
            shots=views(school(seed))
            if a.shots:shots={k:v for k,v in shots.items() if k in a.shots.split(',')}
            render(Path('export')/('Campus-'+str(seed)+'.gltf'),a.out/str(seed),a.width,a.samples,shots,engine=a.engine,plan=school(seed))

if __name__=='__main__':main()
