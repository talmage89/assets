"""Outdoor review of exported baked utilities; original library context only."""
import argparse,hashlib,json,math,sys,random
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit import gpu,model as G
from plan import SEEDS

def file_sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()



def append(path):
    with bpy.data.libraries.load(str(path.resolve()),link=False) as (src,dst):dst.objects=src.objects
    obs=[o for o in dst.objects if o]
    for o in obs:bpy.context.collection.objects.link(o)
    return obs


def copy_tree(root,name,loc,yaw=0,scale=(1,1,1)):
    original=[root]+list(root.children_recursive);copies={}
    for o in original:
        cp=o.copy();bpy.context.collection.objects.link(cp);copies[o]=cp
    for o,cp in copies.items():
        cp.parent=copies.get(o.parent);cp.matrix_basis=o.matrix_basis.copy();cp.name=name+'__'+o.name
    rt=copies[root]
    # glTF roots may use quaternion rotation. Writing rotation_euler.z on
    # those roots silently leaves the imported pose unchanged. Compose the
    # actual matrix, preserving any original glTF axis conversion instead.
    rt.matrix_world=Matrix.Translation(loc)@Matrix.Rotation(math.radians(yaw),4,'Z')@Matrix.Diagonal((*scale,1))@root.matrix_world
    return list(copies.values())


def context(meta):
    plan=meta['plan'];all_context=[];provenance=[]
    house_lib={};house_fits=[]
    for row in meta['houses']:
        typ=row['type']
        if typ not in house_lib:
            path=Path('build/context',typ+'-look.blend')
            obs=set(append(path))
            roots=[o for o in obs if o.parent is None];assert len(roots)==1,(typ,[o.name for o in roots])
            house_lib[typ]=(roots[0],obs)
            provenance.append(dict(path=str(path),sha256=file_sha(path)))
        root,_=house_lib[typ]
        placed_house=copy_tree(root,row['name'],row['location'],row['yaw']);all_context.extend(placed_house)
        bpy.context.view_layer.update()
        # Verify the visible imported context itself, not another copy of
        # the intended placement math. Roof-guy endpoints must hit its roof.
        from mathutils.bvhtree import BVHTree
        vs=[];fs=[]
        for o in placed_house:
            if o.type!='MESH':continue
            offset=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices)
            o.data.calc_loop_triangles();fs.extend(tuple(offset+i for i in t.vertices) for t in o.data.loop_triangles)
        surface=BVHTree.FromPolygons(vs,fs,all_triangles=True)
        transform=Matrix.Translation(row['location'])@Matrix.Rotation(math.radians(row['yaw']),4,'Z')
        errors=[]
        for point in row['attachment']['roof_anchors']:
            expected=transform@Vector(point);hit=surface.ray_cast(Vector((expected.x,expected.y,30)),Vector((0,0,-1)),40)[0]
            assert hit is not None,(row['name'],'Missing visible roof under mast guy')
            error=(expected-hit).length;assert error<.0002,(row['name'],error,tuple(expected),tuple(hit))
            errors.append(error)
        house_fits.append(dict(house=row['name'],roof_anchor_surface_errors_m=errors))
    # Continue the neighborhood beyond both ends of the utility demonstration.
    # No field horizon, tilted house row, or artificial road end is visible.
    rng=random.Random(plan['seed']+407)
    for side in (-1,1):
        for i,yy in enumerate(list(range(-190,-5,29))+list(range(round(plan['length']+20),round(plan['length']+235),29))):
            typ=list(house_lib)[i%len(house_lib)];rt=house_lib[typ][0]
            all_context.extend(copy_tree(rt,f'Neighbor_{side}_{i}',(side*(21+rng.uniform(-1.8,1.8)),yy,.16764),90 if side<0 else -90))
        for i,yy in enumerate(range(-100,round(plan['length']+150),36)):
            typ=list(house_lib)[(i+1)%len(house_lib)]
            all_context.extend(copy_tree(house_lib[typ][0],f'Next block_{side}_{i}',(side*59,yy,.16764),90 if side<0 else -90))
    for rt,obs in house_lib.values():
        for o in obs:bpy.data.objects.remove(o,do_unlink=True)
    ground=append(Path('build/context/ground.blend'));lib={o.name:o for o in ground if o.parent is None}
    length=plan['length'];count=math.ceil((length+500)/6.096)
    for i in range(count):
        y=-230+i*6.096
        all_context.extend(copy_tree(lib['Road_Straight_A'],f'Road_{i}',(0,y,0)))
    for side in (-1,1):
        yaw=180 if side==-1 else 0
        for i in range(math.ceil((length+500)/3.048)):
            y=-230+i*3.048
            all_context.extend(copy_tree(lib['Curb_Straight'],f'Curb_{side}_{i}',(side*4.1148,y,0),yaw))
        for i in range(math.ceil((length+500)/1.524)):
            y=-230+i*1.524
            all_context.extend(copy_tree(lib['Sidewalk_A'],f'Walk_{side}_{i}',(side*6.096,y,0),yaw))
    lawn=lib['Lawn_Field']
    all_context.extend(copy_tree(lawn,'Neighborhood grade',(0,length/2,-.02),scale=(5000,5000,1)))
    # Yards meet the native walk's back edge at its actual .16764 m grade.
    # The low subgrade stays under the road; a single raised infinite plane
    # would cover the road crown and make the paving disappear.
    for side in (-1,1):
        all_context.extend(copy_tree(lawn,'Raised residential yards',(side*(2500+7.62),length/2,.16764),scale=(5000,5000,1)))
    # A continuous grass verge sits between actual curb and sidewalk modules.
    for side in (-1,1):
        all_context.extend(copy_tree(lawn,'Planting strip',(side*5.1054,length/2,.159),scale=(1.8288,length+500,1)))
    for o in ground:bpy.data.objects.remove(o,do_unlink=True)
    for species in ('maple','oak'):
        tree=append(Path('build/context',species+'.blend'));root=next(o for o in tree if o.parent is None)
        for i,y in enumerate(range(-180,round(length+230),31 if plan['seed']!=103 else 43)):
            if i%2 != (species=='oak'):continue
            for side in (-1,1):
                # Alternate curb-side and yard trees. Where crowns reach the
                # corridor, keep the trunk between poles; no pole-sized hedge.
                xx=side*(5.15 if i%4==0 else 12.7 if i%4==1 else 32+rng.uniform(-3,3))
                yy=y+side*7
                if side<0 and abs(xx)<6 and -15<yy<length+15:xx=-12.7
                if side<0 and abs(xx)<6 and any(abs(yy-p['location'][1])<8 for p in plan['poles']):yy+=13
                scale=rng.uniform(.87,1.07)
                all_context.extend(copy_tree(root,f'{species}_{side}_{i}',(xx,yy,.159 if abs(xx)<6 else .16764),i*63+side*29,(scale,scale,scale)))
        for i,yy in enumerate(range(-240,round(length+330),27)):
            for side in (-1,1):
                xx=side*(96+rng.uniform(-10,13));all_context.extend(copy_tree(root,f'Wooded yards_{side}_{i}',(xx,yy,.16764),rng.uniform(0,360)))
        for i,xx in enumerate(range(-125,140,19)):
            for end in (-1,1):
                yy=-230 if end<0 else length+285
                all_context.extend(copy_tree(root,f'Beyond street_{end}_{i}',(xx+rng.uniform(-6,6),yy+rng.uniform(-12,12),.16764),rng.uniform(0,360)))
        for o in tree:bpy.data.objects.remove(o,do_unlink=True)
    pickup=append(Path('build/context/pickup.blend'));root=next(o for o in pickup if o.parent is None)
    # Original family's factory colors, applied to presentation instances only.
    paints={};palette=[('Atlantic',(.012,.037,.071),.12),('Porcelain',(.78,.79,.76),0),('Graphite',(.160,.153,.141),.42)]
    for i,y in enumerate(range(-60,round(length+120),37)):
        xx=(-1 if i%2 else 1)*2.55;zz=.00635+(3.6576-abs(xx))/48;yaw=180 if i%2 else 0
        placed=copy_tree(root,'Parked pickup '+str(i),(xx,y,zz),yaw)
        placed[0].matrix_world=Matrix.Translation((xx,y,zz))@Matrix.Rotation(math.atan(math.copysign(1/48,xx)),4,'Y')@Matrix.Rotation(math.radians(yaw),4,'Z')@root.matrix_world
        for ob in placed:
            if ob.type!='MESH':continue
            for slot in ob.material_slots:
                original=slot.material
                if not original or not original.use_nodes or not original.node_tree.nodes.get('Paint tint'):continue
                key=(original.name,i%len(palette))
                if key not in paints:
                    name,color,metal=palette[i%len(palette)];m=original.copy();m.name='Context '+name+' factory paint'
                    m.node_tree.nodes['Paint tint'].outputs[0].default_value=(*color,1)
                    m.node_tree.nodes['Paint metallic'].outputs[0].default_value=metal;paints[key]=m
                slot.link='OBJECT';slot.material=paints[key]
        all_context.extend(placed)
    for o in pickup:bpy.data.objects.remove(o,do_unlink=True)
    # Mount the original family's head only, without its municipal steel pole.
    light=append(Path('build/context/light.blend'));head=[]
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('light_dimensions',HERE.parents[1]/'street-light/src/dimensions.py');D=module_from_spec(spec);spec.loader.exec_module(D)
    for o in light:
        if o.type=='MESH' and min((o.matrix_world@Vector(p)).z for p in o.bound_box)>D.FIXTURE_BASE-.07:
            head.append(o)
    for s in plan['poles']:
        if not s.get('light'):continue
        # Light arm local -Y turns toward the roadway, +X.
        target=Vector(meta['sockets'][s['name']]['LightHead'])
        for o in head:
            cp=o.copy();cp.data=o.data;bpy.context.collection.objects.link(cp);cp.parent=None
            transform=Matrix.Translation(target)@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(Vector((0,-D.BACK,-D.ARM_END)))
            cp.matrix_world=transform@o.matrix_world;all_context.append(cp)
    for o in light:bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.view_layer.update()
    provenance.append(dict(scope='Actual posed visible house mesh / mast roof-guy anchor fits',house_fits=house_fits))
    return all_context,provenance


def setup(samples,engine='CYCLES',overcast=False):
    sc=bpy.context.scene;sc.render.engine=engine
    sc.render.threads_mode='FIXED';sc.render.threads=4;sc.render.use_persistent_data=False
    if engine=='CYCLES':
        gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=False;sc.cycles.adaptive_threshold=.01
        sc.cycles.transparent_max_bounces=32;sc.cycles.max_bounces=10
        # Denoise surfaces while retaining the actual Cycles samples in a
        # narrow wire mask. This prevents the denoiser erasing subpixel tubes;
        # it does not widen a wire, change its coverage or paint a line.
        for ob in sc.objects:
            if ob.name.startswith('Conductors_'):ob.pass_index=1
        layer=sc.view_layers[0];layer.use_pass_object_index=True;layer.pass_alpha_threshold=0;layer.cycles.denoising_store_passes=True
        group=bpy.data.node_groups.new('Surface denoise, original wire samples','CompositorNodeTree')
        group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
        sc.compositing_node_group=group;ns,ls=group.nodes,group.links
        render=ns.new('CompositorNodeRLayers');denoise=ns.new('CompositorNodeDenoise')
        ls.new(render.outputs['Image'],denoise.inputs['Image']);ls.new(render.outputs['Denoising Albedo'],denoise.inputs['Albedo']);ls.new(render.outputs['Denoising Normal'],denoise.inputs['Normal'])
        mask=ns.new('CompositorNodeIDMask');mask.inputs['Index'].default_value=1;mask.inputs['Anti-Alias'].default_value=True;ls.new(render.outputs['Object Index'],mask.inputs[0])
        expand=ns.new('CompositorNodeDilateErode');expand.inputs['Type'].default_value='Distance';expand.inputs['Size'].default_value=2;ls.new(mask.outputs[0],expand.inputs[0])
        mix=ns.new('ShaderNodeMix');mix.data_type='RGBA';mix.blend_type='MIX';ls.new(expand.outputs[0],mix.inputs[0]);ls.new(denoise.outputs['Image'],mix.inputs[6]);ls.new(render.outputs['Image'],mix.inputs[7])
        out=ns.new('NodeGroupOutput');ls.new(mix.outputs[2],out.inputs['Image'])
    world=bpy.data.worlds.new('Original procedural sky');world.use_nodes=True;sc.world=world
    ns,ls=world.node_tree.nodes,world.node_tree.links;ns.clear()
    sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(32);sky.sun_rotation=math.radians(210);sky.sun_disc=False;sky.aerosol_density=.5
    bg=ns.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.09 if not overcast else .3
    sat=ns.new('ShaderNodeHueSaturation');sat.name='Sky chroma';sat.inputs['Saturation'].default_value=1
    ls.new(sky.outputs[0],sat.inputs['Color'])
    out=ns.new('ShaderNodeOutputWorld');ls.new(sat.outputs[0],bg.inputs[0]);ls.new(bg.outputs[0],out.inputs[0])
    ld=bpy.data.lights.new('Afternoon sun','SUN');ob=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(ob)
    ld.energy=4.0 if not overcast else .7;ld.color=(1,.86,.69);ld.angle=math.radians(.8 if not overcast else 14)
    direction=Vector((-.90,.30,-.40));ob.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
    incoming=-direction.normalized();sky.sun_elevation=math.asin(incoming.z);sky.sun_rotation=math.atan2(incoming.y,incoming.x)
    cam=bpy.data.objects.new('Utility review camera',bpy.data.cameras.new('Utility review camera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.data.clip_end=2000;cam.data.clip_start=.02
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=-.35
    sc.render.image_settings.file_format='PNG';sc.render.film_transparent=False
    return cam


def match_light(shot):
    """Estimated sun/sky from each reference's cast shadows and cloud cover."""
    sc=bpy.context.scene;sun=next(o for o in sc.objects if o.type=='LIGHT' and o.data.type=='SUN')
    direction=shot.get('sun_direction',(-.6,-.2,-.9));sun.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler()
    sun.data.color=shot.get('sun_color',(1,1,1));sun.data.energy=shot.get('sun_energy',2.5);sun.data.angle=math.radians(shot.get('sun_angle',1.2))
    sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY')
    incoming=-Vector(direction).normalized();sky.sun_elevation=math.asin(incoming.z);sky.sun_rotation=math.atan2(incoming.y,incoming.x)
    sky.aerosol_density=shot.get('aerosol',.65)
    sc.world.node_tree.nodes['Sky chroma'].inputs['Saturation'].default_value=shot.get('sky_saturation',1)
    next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=shot.get('sky_strength',.22)


def dusk(meta):
    sc=bpy.context.scene
    sun=next(o for o in sc.objects if o.type=='LIGHT' and o.data.type=='SUN');sun.data.energy=0
    sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_elevation=math.radians(-4);sky.sun_rotation=math.radians(245)
    bg=next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Strength'].default_value=.65
    sc.view_settings.exposure=1.1
    for i,s in enumerate(meta['plan']['poles']):
        if not s.get('light'):continue
        q=Vector(meta['sockets'][s['name']]['LightHead'])+Vector((.18,0,-.08))
        ld=bpy.data.lights.new('Powered utility luminaire','AREA');ld.energy=580;ld.color=(1,.60,.27);ld.shape='DISK';ld.size=.55
        o=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(o);o.location=q
    # Emission is a presentation state on the library's own glazing/lenses.
    for m in bpy.data.materials:
        if not m.use_nodes:continue
        bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bs:continue
        if 'glass' in m.name.lower() and 'alder' not in m.name.lower():
            bs.inputs['Emission Color'].default_value=(1,.43,.12,1);bs.inputs['Emission Strength'].default_value=.55
        if any(n in m.name.lower() for n in ('lens','emissive','diffuser')) and 'alder' not in m.name.lower():
            bs.inputs['Emission Color'].default_value=(1,.66,.30,1);bs.inputs['Emission Strength'].default_value=7


def shots(meta):
    plan=meta['plan'];p=plan['poles'][1]['location'];x,y,z=p;h=plan['poles'][1]['height'];comm=plan['poles'][1]['communication']
    first=meta['houses'][0];q=first['sockets']['ServiceDrop']
    house_rotation=Matrix.Rotation(math.radians(first['yaw']),3,'Z')
    service_camera=Vector(q)+house_rotation@Vector((-5,-5,1.0))
    return dict(
      hero=dict(location=(-7.0,y-26,1.84764),target=(-2,y+25,7.4),lens=35,aspect=1.6),
      street=dict(location=(6.8,3,1.84764),target=(-3,55,7),lens=40,aspect=1.6),
      above=dict(location=(60,-55,68),target=(0,plan['length']/2,3),lens=42,aspect=1.6),
      transformer=dict(location=(x-2.6,y-5.0,h-1.6),target=(x,y-.2,h-1.25),lens=62,aspect=1.25),
      crossarm=dict(location=(x+2.2,y-4.4,h+.5),target=(x,y+.1,h-.4),lens=65,aspect=1.4),
      communication=dict(location=(x-1.8,y-3.0,comm-.05),target=(x-.2,y,comm-.25),lens=65,aspect=1.4),
      deadend=dict(location=(-13,-16,2.4),target=(-5.05,-2.4,4.7),lens=35,aspect=1.3),
      anchor=dict(location=(-6.25,-8.7,.8),target=(-5.05,-6.25,.34),lens=48,aspect=1.4),
      service=dict(location=tuple(service_camera),target=(q[0],q[1],q[2]-1.4),lens=40,aspect=1.4),
      base=dict(location=(x+.9,y-1.6,.65),target=(x,y,.5),lens=55,aspect=1.2),
      tags=dict(location=(x-1.25,y-2.1,1.8+z),target=(x,y,1.50+z),lens=50,aspect=1.2),
      distance=dict(location=(-8,-55,1.85),target=(-5,90,7.9),lens=50,aspect=1.8),
      distance_filtered=dict(location=(-8,-55,1.85),target=(-5,90,7.9),lens=50,aspect=1.8),
      dusk=dict(location=(-7.0,y-26,1.84764),target=(-2,y+25,7.4),lens=35,aspect=1.6),
      bank=dict(location=(x-3.6,plan['poles'][3]['location'][1]-6,h-.8),target=(-5.05,plan['poles'][3]['location'][1],h-1.3),lens=60,aspect=1.4),
      riser=dict(location=(x-3.5,plan['poles'][4]['location'][1]+4,4.5),target=(-5.05,plan['poles'][4]['location'][1],4.9),lens=28,aspect=1.1),
    )


def render_run(seed,a,names):
    bpy.ops.wm.read_factory_settings(use_empty=True);source=Path('export',f'UtilityStreet-{seed}.gltf')
    from deliver import bundle
    source_hash=bundle(source)
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()));meta=json.loads(source.with_suffix('.json').read_text())
    contexts,provenance=context(meta)
    if a.validate_only:
        Path(f'build/render-context-{seed}.json').write_text(json.dumps(provenance,indent=2));print('VISIBLE CONTEXT FIT PASS',seed);return
    cam=setup(a.samples,a.engine)
    views=shots(meta)
    if a.camera_file:
        calibrated=json.loads(Path(a.camera_file).read_text());views={k:v['shot'] for k,v in calibrated.items() if v.get('seed',101)==seed}
        names=list(views)
    output=a.out/str(seed) if not a.camera_file else a.out;output.mkdir(parents=True,exist_ok=True)
    sc=bpy.context.scene;report_path=output/'provenance.json'
    reports=json.loads(report_path.read_text()) if report_path.exists() else {}
    recipe=hashlib.sha256(b''.join((HERE/n).read_bytes() for n in ('render.py','ribbon.py'))).hexdigest()
    for name in names:
        shot=views[name];cam.location=shot['location'];cam.rotation_euler=(Vector(shot['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
        if name in ('hero','street','dusk'):
            bpy.context.view_layer.update()
            result=sc.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((cam.location.x,cam.location.y,25)),Vector((0,0,-1)))
            assert result[0] and 'Walk_' in result[4].name,(name,result[4].name if result[0] else None)
            cam.location.z=result[1].z+1.68
            shot={**shot,'location':list(cam.location),'measured_eye_above_pavement_m':1.68,'pavement_hit':list(result[1])}
        cam.rotation_euler.rotate_axis('Z',shot.get('roll',0));cam.data.lens=shot.get('lens',40)
        sc.view_settings.exposure=shot.get('exposure',-.35)
        if name=='dusk':
            dusk(meta)
            if a.engine=='CYCLES':sc.cycles.samples=max(a.samples,128)
        elif a.camera_file:match_light(shot)
        sc.render.resolution_x=shot.get('width_px',a.width);sc.render.resolution_y=round(sc.render.resolution_x/shot.get('aspect',1.6));sc.render.resolution_percentage=100
        temporary=None;hidden=[]
        if name=='distance_filtered':
            bpy.context.view_layer.update()
            from ribbon import inspection
            temporary=inspection(meta,cam,a.width,sc.render.resolution_y)
            for o in sc.objects:
                if o.name.startswith('Conductors_'):o.visible_camera=False;hidden.append(o)
        path=output/(name+'.png');sc.render.filepath=str(path.resolve());bpy.ops.render.render(write_still=True)
        assert bundle(source)==source_hash,'Source changed during render'
        reports[name]=dict(source=str(source),sha256=source_hash,recipe_sha256=recipe,camera=shot,engine=a.engine,context=provenance,
            scope='Exported Utility external glTF / baked shared maps; original library source-look context, presentation only')
        if temporary:
            reports[name]['scope']+='; camera-evaluated .85px ribbons with compensated coverage replace tubes for this comparison only'
            bpy.data.objects.remove(temporary,do_unlink=True)
            for o in hidden:o.visible_camera=True
        (output/'provenance.json').write_text(json.dumps(reports,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--out',type=Path,default=Path('renders/checkpoint'))
    p.add_argument('--width',type=int,default=1280);p.add_argument('--samples',type=int,default=32);p.add_argument('--engine',default='CYCLES')
    p.add_argument('--seeds',default='101,102,103,104');p.add_argument('--shots');p.add_argument('--camera-file');p.add_argument('--validate-only',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    for seed in map(int,a.seeds.split(',')):
        names=a.shots.split(',') if a.shots else ([n for n in shots(json.loads(Path(f'build/street-{seed}.json').read_text())) if n not in ('bank','riser')] if seed==101 else ['street','above','bank','riser'] if seed==103 else ['street','above'])
        render_run(seed,a,names)
