"""Cycles/Eevee evidence from freshly imported external strip deliveries.

Native road/curb/sidewalk/lawn are presentation context. No source-scene
geometry or replacement facade shaders enter these judgments.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from mathutils import Vector,Matrix
from geometry import root,mesh
from render import setup,tone,load_context
from ground_adapter import FLOW
from strip_plan import PROOF_SEEDS
from context import bundle


def sha(path):
    path=Path(path)
    if path.suffix=='.gltf':return bundle(path.resolve())['sha256']
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def recipe():
    files=[HERE/n for n in ('strip_render.py','strip_presentation.py','render.py','presentation.py','paving.py','strip_photo_matches.py')]
    files += [HERE.parents[1]/'houses/src/render.py',HERE.parents[1]/'cars/src/delivery_materials.py']
    return hashlib.sha256(b''.join(p.read_bytes() for p in files)).hexdigest()


def ground(p):
    source=HERE.parents[1]/'ground/export/Ground.glb';before=set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(source));added=set(bpy.context.scene.objects)-before
    library={o.name:o for o in added if o.parent not in added};rt=root('StripGroundContext',kind='CONTEXT');count=0
    def place(kind,loc,yaw=90):
        nonlocal count
        src=library[kind];copies={o:o.copy() for o in (src,*src.children_recursive)}
        for ob,cp in copies.items():
            bpy.context.collection.objects.link(cp);cp.parent=copies.get(ob.parent,rt);cp.matrix_basis=ob.matrix_basis.copy()
        cp=copies[src];cp.location=loc;cp.rotation_mode='XYZ';cp.rotation_euler=(0,0,math.radians(yaw));count+=1
        return cp
    W,D=p['lot'];edge=-D/2;cy=edge-7.4676
    for i in range(-round(W/12.192)-18,round(W/12.192)+19):
        x=i*6.096
        place(('Road_Straight_A','Road_Straight_B','Road_Straight_C')[i%3],(x,cy,FLOW))
        for dx in (-1.524,1.524):
            place('Curb_Straight',(x+dx,cy-4.1148,FLOW),-90)
            place('Lawn_Strip',(x+dx,cy-4.2672,FLOW),-90)
        for dx in (-2.286,-.762,.762,2.286):place('Sidewalk_A',(x+dx,cy-6.096,FLOW),-90)
        # Continue the native near edge outside the center's own front interface.
        def outside(kind,center,native,y):
            lo=center-native/2;hi=center+native/2
            for a,b in ((lo,min(hi,-W/2)),(max(lo,W/2),hi)):
                if b-a<.0001:continue
                cp=place(kind,((a+b)/2,y,FLOW),90);cp.scale.y=(b-a)/native
        for dx in (-1.524,1.524):
            outside('Curb_Straight',x+dx,3.048,cy+4.1148)
            outside('Lawn_Strip',x+dx,3.048,cy+4.2672)
        for dx in (-2.286,-.762,.762,2.286):outside('Sidewalk_A',x+dx,1.524,cy+6.096)
    # Native material and UV density on context lawn, with its actual requested
    # vertex-color input. Four disjoint regions leave road and property clear.
    lawn=next(mat for ob in added if ob.type=='MESH' for mat in ob.data.materials if mat.name.startswith('Lawn'))
    from kit.tiling import world_uv
    for x0,x1,y0,y1,z in ((-1000,1000,-1000,1000,FLOW-.03),(-450,450,-450,cy-7.62,-.006),(-450,-W/2,edge+.16,450,-.006),(W/2,450,edge+.16,450,-.006),(-W/2,W/2,D/2,450,-.006)):
        ob=mesh('Context native lawn',[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],[(0,1,2,3)],lawn,rt,False);world_uv(ob,3.048)
        for node in lawn.node_tree.nodes:
            if node.type=='VERTEX_COLOR':
                attr=ob.data.color_attributes.new(name=node.layer_name or 'Color',type='FLOAT_COLOR',domain='POINT')
                for value in attr.data:value.color=(1,1,1,1)
                ob.data.color_attributes.active_color=attr
    for ob in added:bpy.data.objects.remove(ob,do_unlink=True)
    return dict(source='ground/export/Ground.glb',sha256=sha(source),placed_modules=count,scope='Native shared ground geometry/maps; presentation only')


def views(p):
    W,D=p['lot'];b=p['building'];f=b['front'];left=b['left'];right=left+b['width'];bay=p['modules'][2];x=bay['origin'][0]
    result=dict(
        hero=dict(location=(-W/2+1.5,f-18,1.6),target=(left+b['width']*.22,f,1.6),lens=35,aspect=1.90,shift_y=.10),
        street=dict(location=(-W*.85,-D/2-14.0,1.6),target=(0,f+b['depth']*.50,1.6),lens=40,aspect=2.6,shift_y=.025,shift_x=-.06),
        above=dict(location=(-W*.74,-D*.93,69),target=(0,0,0),lens=40,aspect=1.6),
        storefront=dict(location=(x+3.1,f-23,1.75),target=(x,f-1,2.6),lens=82,aspect=1.5),
        walk=dict(location=(left+4.5,f-1.7,1.65),target=(left+25,f-1.45,1.65),lens=38,aspect=1.65),
        tower=dict(location=(left+7.0,f-12.2,1.7),target=(left+1.8,f-2.7,3.6),lens=45,aspect=1.15),
        endcap=dict(location=(left-12,f-10,1.7),target=(left,f+4.5,2.45),lens=45,aspect=1.55),
        stalls=dict(location=(x+3,f-19,2.8),target=(x,f-6.0,.12),lens=50,aspect=1.55),
        dusk=dict(location=(-W/2+1.5,f-18,1.6),target=(left+b['width']*.22,f,1.6),lens=35,aspect=1.90,shift_y=.10,dusk=True,sun_energy=0,sky_strength=.40,exposure=2.2),
        pylon=dict(location=(p['sign_center'][0]+6,p['sign_center'][1]-10,1.9),target=(*p['sign_center'],4.05),lens=48,aspect=1.0),
        rear=dict(location=(left-3,b['rear']+13,5.3),target=(left+14,b['rear'],2.1),lens=42,aspect=1.75,sun_direction=(.45,-.65,-1)),
        services=dict(location=(right+7,b['rear']+4,2.0),target=(right,b['rear']-2.2,1.7),lens=45,aspect=1.5,sun_direction=(-.65,-.45,-1)),
    )
    kind=(p['seed']-201)%4
    result['street']=(
        dict(location=(-W*.35,-D/2-16,1.6),target=(left+b['width']*.50,f+2,1.6),lens=35,aspect=2.10,shift_y=.045),
        dict(location=(W*.56,-D/2-17,1.6),target=(-W*.06,f+2,1.6),lens=42,aspect=1.85,shift_y=.035),
        dict(location=(-W/2-13,-D*.32,1.6),target=(left+6,f+2,1.6),lens=38,aspect=1.75,shift_y=.08),
        dict(location=(-W*.32,-D/2-16,1.6),target=(left+b['width']*.55,f+1,1.6),lens=38,aspect=2.10,shift_y=.06),
    )[kind]
    for name,loc in (('front',(0,f-80,3)),('side',(right+80,f+5,3)),('back',(0,b['rear']+80,3)),('top',(0,.001,150))):
        result[name]=dict(location=loc,target=(0,0,0) if name=='top' else (left+b['width']/2,f+b['depth']/2,3),ortho=max(W,D)+9,aspect=1.35 if name=='top' else 3.3)
    return result


def scale(p):
    repo=HERE.parents[1];files=[Path('build/strip/context/station-101.glb'),Path('build/strip/context/split.glb'),repo/'cars/export/AlderC150.glb']
    stall=min((s for s in p['stalls'] if s['row']==1 and not s['accessible']),key=lambda s:abs((s['x0']+s['x1'])/2-12))
    truck=((stall['x0']+stall['x1'])/2,(stall['y0']+stall['y1'])/2,0)
    anchors=((93,5,0),(135,-9,0),truck);records=[]
    for file,loc in zip(files,anchors):
        load_context(file,loc);records.append(dict(path=str(file),sha256=sha(file)))
    house=json.loads(files[1].with_suffix('.json').read_text());drive=house['driveway'];hx,hy,_=anchors[1]
    drive_hole=(hx+drive['x']-drive['width']/2-.02,hx+drive['x']+drive['width']/2+.02,hy+drive['front']-.02,hy+drive['back']+.02)
    gas=json.loads(files[0].with_suffix('.json').read_text());gw,gd=gas['lot'];gx,gy,_=anchors[0]
    gas_hole=(gx-gw/2-3.81,gx+gw/2+.01,gy-gd/2-3.81,gy+gd/2+.01)
    # The split's descending drive must stay visible below presentation grade.
    # Upper lawn also yields to the station's own native low curb/walk skins.
    from kit.tiling import world_uv
    for ob in [o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Context native lawn')]:
        q=[v.co for v in ob.data.vertices];x0=min(v.x for v in q);x1=max(v.x for v in q);y0=min(v.y for v in q);y1=max(v.y for v in q);z=q[0].z
        holes=[drive_hole]+([gas_hole] if z>-.1 else [])
        xs=sorted({x0,x1,*[v for r in holes for v in r[:2] if x0<v<x1]});ys=sorted({y0,y1,*[v for r in holes for v in r[2:] if y0<v<y1]})
        verts=[];faces=[]
        for a,b in zip(xs,xs[1:]):
            for c,d in zip(ys,ys[1:]):
                if any(lo<(a+b)/2<hi and front<(c+d)/2<back for lo,hi,front,back in holes):continue
                i=len(verts);verts.extend(((a,c,z),(b,c,z),(b,d,z),(a,d,z)));faces.append((i,i+1,i+2,i+3))
        mat=ob.data.materials[0];data=bpy.data.meshes.new('Context cut lawn');data.from_pydata(verts,[],faces);data.materials.append(mat);ob.data=data;world_uv(ob,3.048)
        for node in mat.node_tree.nodes:
            if node.type=='VERTEX_COLOR':
                attr=data.color_attributes.get(node.layer_name or 'Color') or data.color_attributes.new(name=node.layer_name or 'Color',type='FLOAT_COLOR',domain='POINT')
                for value in attr.data:value.color=(1,1,1,1)
                data.color_attributes.active_color=attr
    return dict(location=(-95,-130,90),target=(35,0,0),ortho=210,aspect=2.1),records


def above_frame(camera,assets):
    """Recenter, then fit conservative imported bounds into a six-percent frame.

Positive-depth projected bounds contain every point of their convex boxes;
therefore all actual exported vertices stay within these reported bounds.
"""
    from bpy_extras.object_utils import world_to_camera_view
    points=[ob.matrix_world@Vector(corner) for ob in assets if ob.type=='MESH' for corner in ob.bound_box]
    scene=bpy.context.scene;aspect=scene.render.resolution_x/scene.render.resolution_y
    for _ in range(5):
        bpy.context.view_layer.update();q=[world_to_camera_view(scene,camera,v) for v in points]
        assert min(v.z for v in q)>0
        lo=[min(v[k] for v in q) for k in (0,1)];hi=[max(v[k] for v in q) for k in (0,1)]
        camera.data.shift_x+=(lo[0]+hi[0])/2-.5
        camera.data.shift_y+=((lo[1]+hi[1])/2-.5)/aspect
        factor=min(.88/(hi[0]-lo[0]),.88/(hi[1]-lo[1]));camera.data.lens*=factor
        if abs(factor-1)<.0001 and max(abs((a+b)/2-.5) for a,b in zip(lo,hi))<.0001:break
    bpy.context.view_layer.update();q=[world_to_camera_view(scene,camera,v) for v in points]
    lo=[min(v[k] for v in q) for k in (0,1)];hi=[max(v[k] for v in q) for k in (0,1)]
    assert min(lo)>.059 and max(hi)<.941,(lo,hi)
    return dict(min_uv=lo,max_uv=hi,minimum_margin=.06,imported_bounding_corners=len(points),scope='Conservative imported mesh bounds, wholly positive camera depth; every contained exported vertex fits')


def render(seed=201,folder=Path('build/strip'),out=Path('renders/strip/checkpoint'),names=None,width=1440,samples=32,cameras=None,engine='CYCLES',with_scale=False,source_override=None):
    path=source_override or (Path(f'export/CommercialStrip-{seed}.gltf') if Path(folder).name=='strip-look' else Path(folder)/f'strip-{seed}.glb');source_digest=sha(path);render_recipe=recipe();meta=json.loads(path.with_suffix('.json').read_text())
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()));assets=set(bpy.context.scene.objects)
    from strip_presentation import ready,neighborhood,cars
    ground_record=neighborhood(meta) if ready() else ground(meta)
    context=cars(meta) if meta.get('look') and not cameras else []
    context_objects=set(bpy.context.scene.objects)-assets
    camera=setup(samples,engine);shots=views(meta)
    if with_scale:
        shots['scale']={**shots['storefront'],'human':True}
        import importlib.util
        spec=importlib.util.spec_from_file_location('_strip_human',HERE.parents[1]/'houses/src/render.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.human((meta['modules'][2]['origin'][0]-2,meta['building']['front']-1,.1524))
    figures=[o for o in bpy.context.scene.objects if o.name.startswith(('Scale ','Human '))]
    if cameras:shots={name:row['shot'] for name,row in cameras.items()}
    names=names or list(shots)
    if with_scale:names=[name for name in names if name!='scale']+['scale']
    out=Path(out);out.mkdir(parents=True,exist_ok=True);records={}
    for name in names:
        for ob in context_objects:
            if ob.type in ('MESH','LIGHT'):ob.hide_render=name in ('front','side','back','top') and not ob.name.startswith('Context native lawn')
        for figure in figures:figure.hide_render=name!='scale'
        parked=bpy.data.objects.get('ParkedVehicles')
        if parked:
            for ob in parked.children_recursive:ob.hide_render=name not in ('hero','street','above','dusk')
        assert sha(path)==source_digest and recipe()==render_recipe,'Source/recipe changed during render; rerun from a stable export'
        shot=dict(shots[name]);camera.location=shot['location'];camera.rotation_euler=(Vector(shot['target'])-camera.location).to_track_quat('-Z','Y').to_euler()
        if shot.get('roll'):camera.rotation_euler.rotate_axis('Z',shot['roll'])
        camera.data.type='ORTHO' if 'ortho' in shot else 'PERSP';camera.data.lens=shot.get('lens',40);camera.data.shift_y=shot.get('shift_y',0);camera.data.shift_x=shot.get('shift_x',0)
        if 'ortho' in shot:camera.data.ortho_scale=shot['ortho']
        sc=bpy.context.scene;sc.render.resolution_x=width;sc.render.resolution_y=round(width/shot.get('aspect',1.5));sc.render.resolution_percentage=100;sc.render.film_transparent=shot.get('background')=='transparent'
        eye=None;framing=None
        if name in ('hero','street') and not cameras:
            bpy.context.view_layer.update();hit,point,_,_,ob,_=sc.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((camera.location.x,camera.location.y,100)),Vector((0,0,-1)))
            assert hit,'Eye camera has no ground beneath it'
            camera.location.z=point.z+1.6;target=Vector(shot['target']);target.z=camera.location.z
            camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();shot['location']=list(camera.location);shot['target']=list(target)
            eye=dict(height_m=camera.location.z-point.z,surface=ob.name)
        if name=='above':
            framing=above_frame(camera,assets);shot.update(lens=camera.data.lens,shift_x=camera.data.shift_x,shift_y=camera.data.shift_y)
        direction=shot.get('sun_direction',(-1.0,.30,-.75))
        sun=bpy.data.objects['Sun'];sun.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler();sun.data.energy=shot.get('sun_energy',6.0);sun.data.angle=math.radians(shot.get('sun_angle',.65))
        sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY');sky.sun_elevation=math.radians(-3) if shot.get('dusk') else math.atan2(-direction[2],math.hypot(*direction[:2]));sky.sun_rotation=math.atan2(-direction[1],-direction[0])
        bg=next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Strength'].default_value=shot.get('sky_strength',.035)
        sc.world.node_tree.nodes['Sky chroma'].inputs['Saturation'].default_value=shot.get('sky_saturation',1)
        sc.view_settings.exposure=shot.get('exposure',.25)
        if engine=='BLENDER_EEVEE' and not bpy.data.objects.get('Strip bounce cache'):
            bpy.ops.object.lightprobe_add(type='VOLUME',location=(0,meta['building']['front'],2.3));probe=bpy.context.object;probe.name='Strip bounce cache';probe.scale=(meta['building']['width']/2+1,9,3)
            probe.data.resolution_x=24;probe.data.resolution_y=8;probe.data.resolution_z=4;probe.data.bake_samples=32
            probe.data.capture_world=True;probe.data.capture_indirect=True;probe.data.capture_emission=True
            bpy.ops.object.lightprobe_cache_bake(subset='ALL')
        target=out/(name+'.png');sc.render.filepath=str(target.resolve());bpy.ops.render.render(write_still=True)
        if name=='scale':
            q=[o.matrix_world@v.co for o in figures for v in o.data.vertices];height=max(v.z for v in q)-min(v.z for v in q);assert abs(height-1.8)<.001
            target.with_suffix('.scale.json').write_text(json.dumps(dict(measured_height_m=height,minimum_z_m=min(v.z for v in q),scope='Actual imported-scene silhouette vertices'),indent=2)+'\n')
        if name=='hero':tone(target,camera,[ob for ob in assets if ob.type=='MESH' and ob.parent and ob.parent.name.startswith(('BuildingStatic','Bay_','Tower_','EndCap_'))])
        assert sha(path)==source_digest and recipe()==render_recipe,'Source/recipe changed during rendering'
        records[name]=dict(source=str(path),sha256=source_digest,image_sha256=sha(target),shot=shot,engine=engine,width=width,samples=samples,eye=eye,framing=framing,ground=ground_record,context=context,stage=meta['stage'],recipe_sha256=render_recipe,comparison=dict(calibration_sha256=sha('build/strip/cameras.json'),balanced_photo_sha256=sha(cameras[name]['photo'])) if cameras else None)
    provenance=out/'provenance.json';old=json.loads(provenance.read_text()) if provenance.exists() else {};old.update(records);provenance.write_text(json.dumps(old,indent=2)+'\n')
    return records


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--seed',type=int,default=201);a.add_argument('--source-root',type=Path,default=Path('build/strip'));a.add_argument('--out',type=Path,default=Path('renders/strip/checkpoint'));a.add_argument('--shots',default='hero,storefront,walk,tower,endcap,pylon,rear,services,stalls,dusk');a.add_argument('--width',type=int,default=1440);a.add_argument('--samples',type=int,default=32);a.add_argument('--family',action='store_true');a.add_argument('--scale',action='store_true');a.add_argument('--matches',action='store_true');a.add_argument('--engine',default='CYCLES');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.matches:
        from kit.photo_match import verify
        from strip_photo_matches import PAIR_SEEDS,LIGHTING
        path=Path('build/strip/cameras.json');verify(path);cameras=json.loads(path.read_text())
        for name in PAIR_SEEDS:cameras[name]['shot'].update(LIGHTING[name])
        for seed in dict.fromkeys(PAIR_SEEDS.values()):
            selected={name:cameras[name] for name,value in PAIR_SEEDS.items() if value==seed}
            render(seed,a.source_root,Path('renders/strip/matches'),list(selected),a.width,a.samples,selected,a.engine)
    else:
        names=a.shots.split(',')+(['scale'] if a.scale else [])
        render(a.seed,a.source_root,a.out,names,a.width,a.samples,engine=a.engine,with_scale=a.scale)
        if a.family:
            for seed in PROOF_SEEDS:render(seed,a.source_root,a.out/'seeds'/str(seed),['above','street'],a.width,a.samples,engine=a.engine)
