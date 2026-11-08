"""Batched Cycles review from fresh external glTF imports, never source blends."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
from geometry import Library,ROOT
from kit import gpu,model as G
from kit.tiling import world_uv


def setup(width,samples):
    sc=bpy.context.scene;sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=samples;sc.cycles.use_denoising=True
    sc.cycles.transparent_max_bounces=24;sc.cycles.max_bounces=7
    sc.world=bpy.data.worlds.new('Clear afternoon');sc.world.use_nodes=True
    ns,ls=sc.world.node_tree.nodes,sc.world.node_tree.links
    sky=ns.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(18);sky.sun_rotation=math.radians(235);sky.sun_disc=False;sky.aerosol_density=.45
    sat=ns.new('ShaderNodeHueSaturation');sat.name='Daylight sky chroma';sat.inputs['Saturation'].default_value=.35
    bg=ns.get('Background');bg.inputs['Strength'].default_value=.10;ls.new(sky.outputs[0],sat.inputs['Color']);ls.new(sat.outputs[0],bg.inputs[0])
    visible=ns.new('ShaderNodeHueSaturation');visible.name='Visible sky chroma';ls.new(sky.outputs[0],visible.inputs['Color'])
    camera_bg=ns.new('ShaderNodeBackground');camera_bg.name='Visible clear sky';camera_bg.inputs['Strength'].default_value=.06;ls.new(visible.outputs[0],camera_bg.inputs['Color'])
    paths=ns.new('ShaderNodeLightPath');specular=ns.new('ShaderNodeMath');specular.operation='MAXIMUM'
    ls.new(paths.outputs['Is Camera Ray'],specular.inputs[0]);ls.new(paths.outputs['Is Glossy Ray'],specular.inputs[1])
    mix=ns.new('ShaderNodeMixShader');ls.new(specular.outputs[0],mix.inputs[0]);ls.new(bg.outputs[0],mix.inputs[1]);ls.new(camera_bg.outputs[0],mix.inputs[2])
    ls.new(mix.outputs[0],next(n for n in ns if n.type=='OUTPUT_WORLD').inputs['Surface'])
    ld=bpy.data.lights.new('Low raking sun','SUN');ld.energy=10;ld.angle=math.radians(.65);ld.color=(1,.94,.83)
    sun=bpy.data.objects.new(ld.name,ld);sc.collection.objects.link(sun);sun.rotation_euler=Vector((.75,.61,-.316)).to_track_quat('-Z','Y').to_euler()
    cam=bpy.data.objects.new('CheckpointCamera',bpy.data.cameras.new('CheckpointCamera'));sc.collection.objects.link(cam);sc.camera=cam
    cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cam.data.clip_start=.03;cam.data.clip_end=2000
    sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=0
    sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
    return cam


def context(plan):
    from town_context import context as town
    return town(plan)


def image_resources():
    """Content-deduplicated images bound by the visible presentation meshes."""
    materials={slot.material for ob in bpy.context.scene.objects if ob.type=='MESH' and not ob.hide_render
               for slot in ob.material_slots if slot.material};images=set();seen=set()
    def visit(tree):
        if tree in seen:return
        seen.add(tree)
        for node in tree.nodes:
            if node.type=='TEX_IMAGE' and node.image:images.add(node.image)
            elif node.type=='GROUP' and node.node_tree:visit(node.node_tree)
    for mat in materials:
        if mat.use_nodes:visit(mat.node_tree)
    result={}
    for im in images:
        data=im.packed_file.data if im.packed_file else Path(bpy.path.abspath(im.filepath)).read_bytes()
        sha=hashlib.sha256(data).hexdigest();w,h=im.size[:]
        result[sha]=dict(name=im.name,sha256=sha,size=[w,h],png_bytes=len(data),mipped_8bpp_mib=w*h*4/3/1048576)
    return sorted(result.values(),key=lambda row:row['sha256'])


def source_finish():
    """Same game geometry/cause colors, original manufacture before GPU bake."""
    for mat in bpy.data.materials:
        if not mat.name.startswith('ManufacturedPBR_Metal'):continue
        ns,ls=mat.node_tree.nodes,mat.node_tree.links
        for node in ns:
            if node.type!='TEX_IMAGE' or not node.image:continue
            name=node.image.name
            channel='BaseColor' if 'BaseColor' in name else 'ORM' if 'ORM' in name else None
            if channel:
                node.image=bpy.data.images.load(str(Path('textures/source',f'T_Manufactured_{channel}.png').resolve()),check_existing=True)
                node.image.colorspace_settings.name='sRGB' if channel=='BaseColor' else 'Non-Color'
        height=ns.new('ShaderNodeTexImage');height.image=bpy.data.images.load(str(Path('textures/source/T_Manufactured_Height.png').resolve()),check_existing=True);height.image.colorspace_settings.name='Non-Color'
        bump=ns.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.012;ls.new(height.outputs['Color'],bump.inputs['Height'])
        bs=next(n for n in ns if n.type=='BSDF_PRINCIPLED');ls.new(bump.outputs['Normal'],bs.inputs['Normal'])


def clear_raking_direction(plan):
    """Choose the 18-degree camera-side sun through the real imported canopy.

    Uses the same measured-visibility approach as Playground's presentation.
    Alpha-card triangles make this a conservative occlusion score.
    """
    bpy.context.view_layer.update();scene=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get()
    lane=-plan['loop_x'];start=-plan['span']/2;probes=[]
    for row in plan['lots']:
        if row['lane']!=lane or row['origin'][1]>start+36:continue
        h=row['home'];point=Vector((row['origin'][0]-row['side']*(h['length']/2+.08),row['origin'][1],1.75))
        probes.append((point,Vector((-row['side'],0,0)),2.0))
    probes += [(Vector((lane+x,start+y,.12)),Vector((0,0,1)),1.0) for x in (-1.2,1.2) for y in (8,18,28)]
    choices=[]
    for az in range(210,331,15):
        angle=math.radians(az);toward=Vector((math.cos(angle),math.sin(angle),math.tan(math.radians(18)))).normalized()
        score=0.;clear=0
        for point,normal,weight in probes:
            incidence=max(0,normal.dot(toward))
            if incidence>.05 and not scene.ray_cast(deps,point,toward,distance=180)[0]:score+=weight*incidence;clear+=1
        choices.append((score,-abs(az-270),az,toward,clear))
    score,_,az,toward,clear=max(choices,key=lambda q:q[:2])
    return dict(direction=list(-toward),weighted_lambert_score=score,clear_probe_count=clear,probe_count=len(probes),sun_azimuth_degrees=az,
                visibility_scope='Imported triangles and surface-normal incidence; conservative for alpha foliage; lane and home-end probes')


def landmark_visibility(points,camera):
    bpy.context.view_layer.update();scene=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();rows=[];origin=Vector(camera)
    for point in points:
        delta=Vector(point)-origin;distance=delta.length
        hit,position,normal,index,ob,xf=scene.ray_cast(deps,origin,delta.normalized(),distance=max(.01,distance-.50))
        rows.append(dict(landmark=point,clear=not hit,occluder=ob.name if hit else None,
                         occluder_distance_m=(position-origin).length if hit else None))
    return dict(anchors=rows,clear_count=sum(r['clear'] for r in rows),anchor_count=len(rows),
                scope='Conservative imported-triangle rays; final 0.50m excludes subject trim and surface contact')


def shot_views(stem,meta):
    p=meta['plan'];wide=stem.startswith('Double');L=p.get('length',10) if p else 10;W=p.get('width',5) if p else 5
    if stem.startswith('Park'):
        span=p['span'];sx,sy=p['size'];old=p['kind']=='old'
        xx=p['loop_x']
        views=dict(hero=dict(location=(-xx-1.50,-span/2+2,1.68),target=(-xx-.3,-span/2+31,1.83),lens=40),
                    above=dict(location=(sx*1.02,-sy*1.05,max(sx,sy)*.95),target=(0,0,0),lens=43,aspect=1.45,light=dict(exposure=1.0,sky_strength=.12,sun_energy=8)),
                    entrance=dict(location=(-xx+11,-span/2-19,1.68),target=(-xx+6,-span/2-7,1.4),lens=48,aspect=1.5),
                    row=dict(location=(-xx+2.3,-span/2+15,1.68),target=(-xx-12,-span/2+23,1.8),lens=40))
        # Preserve the accepted look5 direction despite canopy variation.
        for v in views.values():v.setdefault('light',{})['direction']=(-.6724985241889954,.6724985241889954,-.30901700258255005)
        return views
    if stem.startswith(('Single','Double')):
        return dict(hero=dict(location=(L*.92,-L*1.14,3.6),target=(0,0,1.7),lens=42),
                    front=dict(location=(0,-40,1.8),target=(0,0,1.8),ortho=L+2.7,aspect=2.1),
                    side=dict(location=(40,0,1.9),target=(0,0,1.9),ortho=W+2.0,aspect=1.25),
                    back=dict(location=(0,40,1.8),target=(0,0,1.8),ortho=L+2.7,aspect=2.1),
                    top=dict(location=(0,0,45),target=(0,0,0),ortho=L+2.7,aspect=1.6),
                    skirt=dict(location=(2.7,-W/2-2.4,.78),target=(1.8,-W/2,.50),lens=48,aspect=1.5),
                    entry=dict(location=(-L*.035+.85,-W/2-1.78,2.565),target=(-L*.035,-W/2,1.96),lens=40,aspect=1.3,door_angles=dict(FrontDoor=48,StormDoor=-67)),
                    scale=dict(location=(L*.76,-L*.92,2.5),target=(0,-1.0,1.35),lens=42))
    presets={
      'Deck':((4,-6,2.5),(0,-.1,.80),48),
      'Carport':((7,-7,3.3),(0,0,1.4),45),
      'UtilityService':((1.8,-2.8,1.55),(.2,0,.75),52),
      'SupportFrame':((12,-8,2.3),(0,0,.43),45),
      'EntranceSign':((3.2,-5.7,2.0),(0,0,1.1),50),
      'Modules':((24,-42,37),(0,4,0),45),
      'HomeForms':((45,-78,76),(0,10,1),45)}
    loc,target,lens=presets.get(stem,((3,-5,2),(0,0,.6),45))
    out=dict(detail=dict(location=loc,target=target,lens=lens,aspect=1.6))
    if stem=='SupportFrame':out['piers']=dict(location=(1.5,-2.6,1.05),target=(0,-.94,.35),lens=55,aspect=1.5)
    return out


def render(stem,path,meta,views,out,width,samples,dress=True,source=False):
    from inspection import mirror
    delivery=path;packed=path if path.suffix=='.glb' else mirror(path);archive=(out.parent if out.name=='matches' else out)/'sources'/(path.stem+'.glb')
    archive.parent.mkdir(parents=True,exist_ok=True)
    if not archive.exists() or archive.read_bytes()!=packed.read_bytes():archive.write_bytes(packed.read_bytes())
    path=archive
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    bpy.context.view_layer.update()
    # Imported custom bone-display helpers never appear in product evidence.
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH' and not o.data.materials and 'Icosphere' in o.name:bpy.data.objects.remove(o,do_unlink=True)
    ctx=context(meta['plan']) if stem.startswith('Park') and dress else {}
    if source:source_finish()
    if ctx:
        ctx['image_resources']=image_resources()
        ctx['image_gpu_mib']=sum(im['mipped_8bpp_mib'] for im in ctx['image_resources'])
    cam=setup(width,samples);sc=bpy.context.scene
    automatic_sun=any(not v.get('fixed_camera') and 'direction' not in v.get('light',{}) for v in views.values())
    sun_choice=clear_raking_direction(meta['plan']) if ctx and automatic_sun else None
    if not stem.startswith('Park'):
        from kit.studio import studio_mat
        G.box('Review ground',(0,0,-.10),(1000,1000,.20),studio_mat('Ground',(.13,.14,.11),.95),0)
    provenance=[]
    for name,v in views.items():
        temporary=[];posed={}
        for suffix,angle in v.get('door_angles',{}).items():
            pivot=next(o for o in bpy.context.scene.objects if o.name.endswith('__'+suffix));posed[pivot]=pivot.matrix_basis.copy();pivot.matrix_basis=posed[pivot]@Matrix.Rotation(math.radians(angle),4,'Z')
        light=dict(sun_energy=10,sky_strength=.10,exposure=0,angle_degrees=.65,sky_saturation=.35,camera_sky_strength=.06,camera_sky_saturation=1)
        light.update(v.get('light',{}));automatic=sun_choice is not None and not v.get('fixed_camera') and 'direction' not in v.get('light',{})
        direction=light.get('direction',sun_choice['direction'] if automatic else (.75,.61,-.316));light['direction']=direction
        if v.get('fixed_camera'):light['sky_saturation']=v.get('light',{}).get('sky_saturation',1)
        sun=bpy.data.objects['Low raking sun'];sun.data.energy=light['sun_energy'];sun.data.angle=math.radians(light['angle_degrees'])
        sun.rotation_euler=Vector(direction).to_track_quat('-Z','Y').to_euler()
        sky=next(n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY');dv=Vector(direction).normalized()
        sky.sun_rotation=math.atan2(-dv.y,-dv.x);sky.sun_elevation=math.asin(-dv.z)
        sc.world.node_tree.nodes['Daylight sky chroma'].inputs['Saturation'].default_value=light['sky_saturation']
        sc.world.node_tree.nodes['Visible sky chroma'].inputs['Saturation'].default_value=light['camera_sky_saturation']
        sc.world.node_tree.nodes['Visible clear sky'].inputs['Strength'].default_value=light['camera_sky_strength']
        sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=light['sky_strength']
        sc.view_settings.exposure=light['exposure']
        if name=='scale':
            from kit.studio import human
            humans=human()
            for hh in humans:hh.location+=Vector((-meta['plan']['length']*.17,-meta['plan']['width']/2-1.1,0));temporary.append(hh)
            lib=Library();car=lib.place(ROOT/'cars/export/AlderH120.glb','Scale car',(meta['plan']['length']*.22,-meta['plan']['width']/2-2.7,0),90);lib.factory(car,1);lib.clear();temporary.append(car)
        cam.location=v['location'];cam.rotation_euler=(Vector(v['target'])-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.data.type='ORTHO' if 'ortho' in v else 'PERSP';cam.data.lens=v.get('lens',45);cam.data.ortho_scale=v.get('ortho',20)
        if v.get('roll'):cam.rotation_euler.rotate_axis('Z',v['roll'])
        sc.render.resolution_x=width;sc.render.resolution_y=round(width/v.get('aspect',1.78));sc.render.filepath=str((out/stem/(name+'.png')).resolve());Path(sc.render.filepath).parent.mkdir(parents=True,exist_ok=True)
        if not v.get('fixed_camera') and not stem.startswith('Park') and name in ('hero','detail','front','back','side','top','scale'):
            from bpy_extras.object_utils import world_to_camera_view
            lo,hi=meta['bounds_min'],meta['bounds_max'];corners=[Vector((x,y,z)) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]
            bpy.context.view_layer.update()
            for rt in temporary:
                for ob in [rt,*rt.children_recursive]:
                    if ob.type=='MESH':corners.extend(ob.matrix_world@Vector(c) for c in ob.bound_box)
            center=Vector(v['target'])
            for _ in range(30):
                bpy.context.view_layer.update();projections=[world_to_camera_view(sc,cam,p) for p in corners]
                if all(.035<q.x<.965 and .035<q.y<.965 and q.z>0 for q in projections):break
                if cam.data.type=='ORTHO':cam.data.ortho_scale*=1.06
                else:cam.location=center+(cam.location-center)*1.06
            v=dict(v,location=list(cam.location),ortho=cam.data.ortho_scale) if cam.data.type=='ORTHO' else dict(v,location=list(cam.location))
        if v.get('fixed_matrix'):cam.matrix_world=Matrix(v['fixed_matrix'])
        for subject in v.get('review_subject_nodes',[]):
            ob=bpy.data.objects.get(subject)
            assert ob and any(c.type=='MESH' for c in ob.children_recursive),(name,'Missing imported comparison subject',subject)
        visibility=landmark_visibility(v['review_landmarks'],cam.location) if v.get('review_landmarks') else None
        if v.get('require_visible_landmarks'):
            assert visibility and visibility['clear_count']==visibility['anchor_count'],(name,'Occluded photo-fit anchors',visibility)
        sc.render.engine=v.get('engine','CYCLES')
        bpy.ops.render.render(write_still=True)
        provenance.append(dict(stem=stem,shot=name,camera=v,source=str(path),delivery=str(delivery),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),images=meta['images'],context=ctx,
                               source_manufacture=source,light={**light,'sun_elevation_degrees':math.degrees(math.asin(-dv.z)),'sun_visibility':sun_choice if automatic else None},
                               landmark_visibility=visibility,camera_matrix_world=[list(r) for r in cam.matrix_world],
                               camera_parameters=dict(type=cam.data.type,lens=cam.data.lens,ortho_scale=cam.data.ortho_scale,sensor_width=cam.data.sensor_width,
                                                      resolution=[sc.render.resolution_x,sc.render.resolution_y]),engine=sc.render.engine,width=width,samples=samples))
        for root in temporary:
            for o in [*root.children_recursive,root]:bpy.data.objects.remove(o,do_unlink=True)
        for pivot,rest in posed.items():pivot.matrix_basis=rest
    return provenance


def baseline_renders(folder,receipts,out,width,samples):
    """Render the supplied earlier packages using current cameras AND lights."""
    import importlib.util
    global context
    spec=importlib.util.spec_from_file_location('_checkpoint_before',folder.parent/'legacy_render.py')
    legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy);legacy.HERE=HERE
    previous=context;context=legacy.context;result=[]
    try:
        for stem in ('Park-101','Park-202','SingleWide-120','DoubleWide-228','Deck','Carport'):
            source=folder/('Baseline_'+stem+'.gltf')
            if not source.exists():continue
            chosen=('hero','above') if stem.startswith('Park') else ('hero',) if stem.startswith(('Single','Double')) else ('detail',)
            views={}
            for row in receipts:
                if row['stem']==stem and row['shot'] in chosen:
                    views['baseline_'+row['shot']]=dict(row['camera'],light=row['light'],fixed_camera=True,fixed_matrix=row['camera_matrix_world'],
                        comparison=dict(after_stem=stem,after_shot=row['shot'],requested_same_camera_and_light=True))
            if views:result+=render(stem,source,json.loads(source.with_suffix('.json').read_text()),views,out,width,samples)
    finally:context=previous
    return result


def main():
    a=argparse.ArgumentParser();a.add_argument('--source');a.add_argument('--out',type=Path,default=Path('renders/checkpoint/pass1'))
    a.add_argument('--width',type=int,default=1200);a.add_argument('--samples',type=int,default=24)
    a.add_argument('--only',default='all');a.add_argument('--shots',default='all');a.add_argument('--cameras',type=Path)
    a.add_argument('--before-cameras',type=Path);a.add_argument('--baseline',type=Path);a.add_argument('--no-context',action='store_true')
    a.add_argument('--retain-cameras',type=Path);a.add_argument('--eevee',action='store_true');a.add_argument('--source-finish',action='store_true')
    a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    stems=[*[k for k in json.loads(Path('build/family.json').read_text()) if k.startswith('Park-')],'SingleWide-120','DoubleWide-228','Deck','Carport','UtilityService','EntranceSign','Modules','HomeForms','SupportFrame'] if a.only=='all' else a.only.split(',')
    receipts=[]
    for stem in stems:
        path=Path('export')/(stem+'.gltf');meta=json.loads(path.with_suffix('.json').read_text());views=shot_views(stem,meta)
        if a.shots!='all':views={k:v for k,v in views.items() if k in a.shots.split(',')}
        if a.retain_cameras:
            prior=json.loads(a.retain_cameras.read_text())
            for row in prior:
                if row['stem']==stem and row['shot'] in views:
                    views[row['shot']]=dict(row['camera'],fixed_camera=True,light=row['light'],fixed_matrix=row['camera_matrix_world'])
        if a.eevee and stem=='Park-202':views['eevee']=dict(views['hero'],engine='BLENDER_EEVEE')
        if a.before_cameras and a.before_cameras.exists():
            for row in json.loads(a.before_cameras.read_text()):
                if row['stem']==stem and row['shot'] in ('hero','above'):
                    oldlight={k:v for k,v in row['light'].items() if k in ('sun_energy','sky_strength','exposure','direction','angle_degrees')}
                    views['before_'+row['shot']]=dict(row['camera'],fixed_camera=True,light=oldlight)
                if stem=='Park-101' and row['shot'] in ('single-2009','addition-2007','carport-2015'):
                    from park_matches import transform
                    number={'single-2009':1,'addition-2007':18,'carport-2015':6}[row['shot']]
                    lot=next(q for q in meta['plan']['lots'] if q['number']==number);h=lot['home']
                    offset=(0,0,0) if row['shot']=='single-2009' else (-h['length']*.32,-h['width']/2-1.2,0) if row['shot']=='addition-2007' else (h['length']/2-2.9,-h['width']/2-1.82,0)
                    camera=dict(row['camera']);camera.update(location=transform(lot,camera['location'],offset),target=transform(lot,camera['target'],offset),
                        fixed_camera=True,light=row['camera'].get('light',{}),baseline_reference=dict(stem=row['stem'],shot=row['shot'],camera=row['camera'],module_frame=True))
                    views['before_'+row['shot']]=camera
        if views:receipts+=render(stem,path,meta,views,a.out,a.width,a.samples,not a.no_context,a.source_finish)
    if a.cameras and a.cameras.exists():
        from kit.photo_match import verify
        verify(a.cameras)
        for name,row in json.loads(a.cameras.read_text()).items():
            stem=row['asset'];meta=json.loads(Path('export',stem+'.json').read_text())
            v=row['shot'];v['aspect']=(row['crop'][2]-row['crop'][0])/(row['crop'][3]-row['crop'][1]);v['review_landmarks']=row['landmarks_world_m'];v['review_subject_nodes']=row.get('subject_nodes',[])
            v['light']=(dict(sun_energy=.8,sky_strength=.40,sky_saturation=.06,camera_sky_strength=.40,camera_sky_saturation=.06,angle_degrees=12,direction=(.3,.3,-1),exposure=-.80) if name=='single-2009' else
                        dict(sun_energy=2.0,sky_strength=.30,sky_saturation=.10,camera_sky_strength=.30,camera_sky_saturation=.10,angle_degrees=5,direction=(.6,.6,-1),exposure=.10) if name=='street-2007' else
                        dict(sun_energy=5,sky_strength=.12,sky_saturation=.35,angle_degrees=.65,direction=(.5,.5,-1),exposure=.10))
            receipts+=render(stem,Path('export',stem+'.gltf'),meta,{name:v},a.out/'matches',a.width,a.samples,True,a.source_finish)
    if a.baseline and a.baseline.exists():receipts+=baseline_renders(a.baseline,receipts,a.out,a.width,a.samples)
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'provenance.json').write_text(json.dumps(receipts,indent=2));print('RENDERED',len(receipts),flush=True)

if __name__=='__main__':main()
