"""Bus gallery imports the delivery; source probes are explicitly labeled."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
import gpu as display_gpu
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(HERE),str(ROOT),str(ROOT/'cars/src')]
from kit import gpu,model as G
from kit.studio import human
from views import SHOTS

def material(name,color,rough=.7):
    m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;return m

def setup(width,samples,engine):
    sc=bpy.context.scene;sc.render.engine=engine
    if engine=='CYCLES':gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.max_bounces=10;sc.cycles.transmission_bounces=8;sc.cycles.transparent_max_bounces=16
    sc.world=bpy.data.worlds.new('Procedural low school sun');sc.world.use_nodes=True;nt=sc.world.node_tree
    sky=nt.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False;sky.sun_elevation=math.radians(18);sky.sun_rotation=math.radians(225)
    cloud=nt.nodes.new('ShaderNodeMixRGB');cloud.name='Reference cloud';cloud.inputs[0].default_value=0;cloud.inputs[2].default_value=(.60,.63,.64,1)
    nt.links.new(sky.outputs[0],cloud.inputs[1]);nt.links.new(cloud.outputs[0],nt.nodes['Background'].inputs['Color']);nt.nodes['Background'].inputs['Strength'].default_value=.18
    ld=bpy.data.lights.new('Low raking sun','SUN');ld.energy=3.0;ld.angle=math.radians(.8);ld.color=(1,.94,.84)
    sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun);sun.rotation_euler=Vector((.60,.80,-.33)).to_track_quat('-Z','Y').to_euler()
    G.box('Checkpoint asphalt',(0,0,-.030),(1000,1000,.06),material('Asphalt',(.047,.052,.052)),0)
    screen=G.box('Side studio backdrop',(10,0,0),(.04,40,20),material('Charcoal studio backdrop',(.035,.040,.038),.88),0)
    screen.hide_render=True
    cam=bpy.data.objects.new('Bus checkpoint camera',bpy.data.cameras.new('Bus checkpoint camera'));sc.collection.objects.link(cam);sc.camera=cam;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.clip_start=.025;cam.data.clip_end=10000
    sc.render.resolution_x=width;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.25
    return cam

def pose(shot):
    bpy.context.view_layer.update();vals={}
    for name in ['Entrance_front','Entrance_rear','Emergency_rear','Stop_arm','Crossing_arm','Roof_hatch_front','Roof_hatch_rear']:
        ob=bpy.data.objects.get(name)
        if ob:vals[ob]=ob.matrix_world.copy()
    def rotate(name,axis,degrees):
        ob=bpy.data.objects[name];rest=vals[ob];p=rest.translation
        ob.matrix_world=Matrix.Translation(p)@Matrix.Rotation(math.radians(degrees),4,axis)@Matrix.Translation(-p)@rest
    if shot.get('pose')=='entrance':
        rotate('Entrance_front','Z',95);rotate('Entrance_rear','Z',-95)
    if shot.get('pose')=='warning':
        rotate('Stop_arm','Z',-90);rotate('Crossing_arm','Z',-90)
    if shot.get('pose')=='hatches':
        for name in ['Roof_hatch_front','Roof_hatch_rear']:rotate(name,'X',-65)
    if shot.get('pose')=='rear_exit':rotate('Emergency_rear','Z',100)
    for m in bpy.data.materials:
        if not m.use_nodes:continue
        bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bs:continue
        if m.get('lamp_lit_strength'):
            active=shot.get('dome') if m.name=='Bus dome' else shot.get('lit') if m.name in ['Bus warning_red','Bus strobe'] else False
            bs.inputs['Emission Strength'].default_value=m['lamp_lit_strength'] if active else 0
    if any('Lamps' in m.name for m in bpy.data.materials):
        from lamp_states import apply
        apply(red=shot.get('lit',False),strobe=shot.get('lit',False),dome=shot.get('dome',False))
    return vals

def imported(path):
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    objects=list(set(bpy.context.scene.objects)-before)
    if path.stem.startswith('C75-') and bpy.context.scene.render.engine=='CYCLES':
        # Queued/fleet buses get the same pane lighting as the lead bus.
        # Restrict this to their own bindings, leaving native campus data alone.
        from glass_lighting import install
        install({m for ob in objects if ob.type=='MESH' for m in ob.data.materials if m})
    return objects

def eevee_finite_panes():
    """Apply the car sheet approximation once per closed, finite bus pane.

    Its rear surface must not add a second sheet Fresnel/TIR response to an
    unrefracted transparent ray. Delivery geometry and Cycles stay physical.
    """
    # Source glazing links its transmission mask; this default only lets the
    # unchanged car adapter identify that transmissive surface in a preview.
    for mat in bpy.data.materials:
        if mat.get('vehicle_glass'):
            bs=mat.node_tree.nodes.get('SURFACE')
            if bs:bs.inputs['Transmission Weight'].default_value=1
    from delivery_materials import eevee_glass
    eevee_glass()
    for mat in bpy.data.materials:
        if not mat.use_nodes:continue
        nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bs or bs.inputs['Transmission Weight'].default_value<=0:continue
        out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');front=out.inputs['Surface'].links[0].from_socket
        rear=nt.nodes.new('ShaderNodeBsdfTransparent');geo=nt.nodes.new('ShaderNodeNewGeometry');mix=nt.nodes.new('ShaderNodeMixShader')
        nt.links.new(geo.outputs['Backfacing'],mix.inputs[0]);nt.links.new(front,mix.inputs[1]);nt.links.new(rear.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs['Surface'])

def digest(path):
    if path.suffix!='.gltf':return hashlib.sha256(path.read_bytes()).hexdigest()
    d=json.loads(path.read_text());fs=[path]+[path.parent/i['uri'] for k in ['buffers','images'] for i in d.get(k,[])]
    return hashlib.sha256(b''.join(hashlib.sha256(f.read_bytes()).digest() for f in fs)).hexdigest()

def render(a):
    path=Path(a.source).resolve();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if path.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(path))
    else:imported(path)
    if a.engine=='BLENDER_EEVEE':
        eevee_finite_panes();bpy.context.scene.eevee.taa_render_samples=max(32 if path.suffix=='.blend' else 192,a.samples);bpy.context.scene.eevee.use_raytracing=True
    else:
        from glass_lighting import install
        install()
    for ob in bpy.context.scene.objects:
        if ob.get('bake_only'):ob.hide_render=True
    cam=setup(a.width,a.samples,a.engine);sc=bpy.context.scene;receipts={}
    shots=SHOTS if a.shots=='all' else {n:SHOTS[n] for n in a.shots.split(',')}
    if a.calibration:shots={n:d['shot'] for n,d in json.loads(Path(a.calibration).read_text()).items()}
    for name,s in shots.items():
        temp=[];vals=pose(s)
        # Horizontal orthographic elevations use the full-height studio card;
        # their parallel rays below Z=0 otherwise see an unlit ground edge.
        bpy.data.objects['Checkpoint asphalt'].hide_render=bool(name=='hero' and a.school) or name in ['front','side','rear']
        screen=bpy.data.objects['Side studio backdrop'];screen.hide_render=name not in ['front','side','rear']
        if not screen.hide_render:
            direction=Vector((s['location'][0],s['location'][1],0)).normalized()
            screen.location=-direction*10
            screen.rotation_euler=direction.to_track_quat('X','Z').to_euler()
        sun=bpy.data.objects['Low raking sun'];cloud=sc.world.node_tree.nodes['Reference cloud'];bg=sc.world.node_tree.nodes['Background']
        sun.data.energy=3.0;cloud.inputs[0].default_value=0;bg.inputs[1].default_value=.18;sc.view_settings.exposure=-.25
        sun.rotation_euler=Vector((.60,.80,-.33)).to_track_quat('-Z','Y').to_euler()
        if name in ['service_front','service_side','service_rear','vision_front']:
            sun.data.energy=0;cloud.inputs[0].default_value=1;cloud.inputs[2].default_value=(.60,.60,.60,1);bg.inputs[1].default_value=.60
            from lighting_context import flags
            temp+=flags(s['location'],side_reflection=name=='service_rear')
        if name in ['aisle','aisle_daylight']:
            # An interior daylight exposure, with a broad bright sky through
            # the real panes. No fill lamps are hidden inside the cabin.
            sun.data.energy=.75;cloud.inputs[0].default_value=.75;bg.inputs[1].default_value=2.5
        if 'exposure' in s:sc.view_settings.exposure=s['exposure']
        sc.view_settings.use_white_balance='whitepoint' in s
        if 'whitepoint' in s:sc.view_settings.white_balance_whitepoint=s['whitepoint']
        if s.get('fleet'):
            for seed,dx in [(102,-4.1),(103,4.1)]:
                obs=imported(path.parent/f'C75-{seed}.gltf')
                for ob in obs:
                    if ob.parent is None:ob.location.x+=dx
                temp+=obs
        if s.get('human'):
            adults=human();temp+=adults
            for ob in adults:ob.location+=Vector((-2.5,-3.1,0))
            children=human();temp+=children
            for ob in children:
                ob.location*=1.1/1.8;ob.scale*=1.1/1.8;ob.location+=Vector((-2.5,-4.0,0))
        if name=='hero' and a.school:
            from school_stage import place
            obs,receipt=place(Path(a.school).resolve(),path,imported,digest,ROOT)
            temp+=obs;receipts['school']=receipt
            sun.rotation_euler=Vector((-.60,.80,-.33)).to_track_quat('-Z','Y').to_euler()
        cam.location=s['location'];cam.rotation_euler=(Vector(s['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',s.get('roll',0))
        cam.data.type='ORTHO' if 'ortho' in s else 'PERSP';cam.data.ortho_scale=s.get('ortho',14);cam.data.lens=s['lens']
        sc.render.resolution_y=round(a.width/s.get('aspect',1.78));sc.render.filepath=str((out/f'{name}.png').resolve())
        sc.render.film_transparent=s.get('background')=='transparent'
        bpy.context.view_layer.update();bpy.ops.render.render(write_still=True)
        receipts[name]=dict(camera=s,source=str(path.relative_to(ROOT)),sha256=digest(path),stage='source' if path.suffix=='.blend' else 'export',engine=a.engine,width=a.width,samples=a.samples,
            engine_samples=sc.cycles.samples if a.engine=='CYCLES' else sc.eevee.taa_render_samples,
            posed_nodes={ob.name:dict(matrix_world=[list(row) for row in ob.matrix_world],rotation_delta_degrees=math.degrees((ob.matrix_world.to_quaternion()@rest.to_quaternion().inverted()).angle)) for ob,rest in vals.items() if (ob.matrix_world.to_quaternion()@rest.to_quaternion().inverted()).angle>1e-5},
            glass='Car-family thin-sheet Fresnel fallback, applied once per finite pane with transparent rear surface' if a.engine=='BLENDER_EEVEE' else 'Cycles camera refraction; parallel-pane colored shadow transmission',
            background_context='Original charcoal horizon flags approximating the photographed tree enclosure' if name.startswith(('service_','vision_')) else 'Full-height neutral charcoal studio wall' if name in ['front','side','rear'] else 'Procedural environment',
            graphics_backend=display_gpu.platform.renderer_get() if a.engine=='BLENDER_EEVEE' else None,
            lighting=dict(sun_energy=sun.data.energy,sun_rotation=list(sun.rotation_euler),sky=bg.inputs[1].default_value,cloud_mix=cloud.inputs[0].default_value,exposure=sc.view_settings.exposure,
                          white_balance_whitepoint=s.get('whitepoint'),white_balance_neutral='Light gray ceiling; adaptation to daylight through the accepted tinted glass' if 'whitepoint' in s else None))
        if s.get('fleet'):receipts[name]['fleet_inputs']={str(seed):digest(path.parent/f'C75-{seed}.gltf') for seed in [101,102,103]}
        if s.get('human'):
            def height(obs):
                zs=[(ob.matrix_world@v.co).z for ob in obs for v in ob.data.vertices]
                return max(zs)-min(zs)
            receipts[name]['measured_human_heights_m']=dict(adult=height(adults),child=height(children))
        (out/'provenance.json').write_text(json.dumps(receipts,indent=2))
        for ob,r in vals.items():ob.matrix_world=r
        for ob in temp:bpy.data.objects.remove(ob,do_unlink=True)

def checkpoint_batch(a):
    """One GPU turn, fresh scenes for every stage; CPU audits run in Make first."""
    import seethrough
    base=HERE.parent;saved=sys.argv
    try:
        sys.argv=[saved[0],'--','--source',a.source,'--parts',str(base/'build/finalized.blend'),'--out',str(base/'renders/seethrough'),'--width','1400']
        seethrough.main()
    finally:sys.argv=saved
    phases=[
        dict(source=a.source,out=a.out,shots='all',school=a.school,calibration=None,engine='CYCLES'),
        dict(source=a.source,out=str(base/'renders/matches'),shots='all',school=None,calibration=str(base/'build/calibration.json'),engine='CYCLES'),
        dict(source=str(base/'build/bus-101.blend'),out=str(base/'renders/source-matches'),shots='all',school=None,calibration=str(base/'build/calibration.json'),engine='CYCLES'),
        dict(source=a.source,out=str(base/'renders/eevee'),shots='hero',school=None,calibration=None,engine='BLENDER_EEVEE')]
    for phase in phases:
        values=vars(a).copy();values.update(phase);render(argparse.Namespace(**values))
    from reflection_lines import render as stripes
    for label,source,part in [('export-full',Path(a.source),None),('export',Path(a.source),'hood'),
                              ('source',base/'build/bus-101.blend','hood'),('dense',base/'build/bus-101.blend','dense')]:
        stripes(source,base/'renders/curvature'/label,width=1200,samples=32,part=part)
    archive=ROOT/'build/bus-round3/before/export/C75-101.gltf'
    if archive.exists():
        original=ROOT/'build/bus-round3/before-cameras.json'
        if original.exists():
            values=vars(a).copy();values.update(source=str(archive),out=str(base/'renders/round3-before'),
                shots='all',school=None,calibration=str(original),engine='CYCLES')
            render(argparse.Namespace(**values))
        values=vars(a).copy();values.update(source=str(archive),out=str(base/'renders/round3-before/details'),
            shots='lamp_detail,hood_surface',school=None,calibration=None,engine='CYCLES')
        render(argparse.Namespace(**values))
    probe=ROOT/'build/bus-round3/fair-optics-low.blend'
    if probe.exists():
        values=vars(a).copy();values.update(source=str(probe),out=str(base/'renders/round3-optics-source'),
            shots='front_detail,lamp_detail,hood_surface',school=None,calibration=None,engine='CYCLES')
        render(argparse.Namespace(**values))

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--shots',default='all');p.add_argument('--width',type=int,default=1400);p.add_argument('--samples',type=int,default=48);p.add_argument('--engine',default='CYCLES');p.add_argument('--school');p.add_argument('--calibration');p.add_argument('--checkpoint-batch',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);checkpoint_batch(a) if a.checkpoint_batch else render(a)
if __name__=='__main__':main()
