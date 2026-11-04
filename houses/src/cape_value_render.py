"""Render fixed physical house patches, with explicit auxiliary paint controls.

Primary wood/cedar/roof retain the six proof seeds' colors. Auxiliary siding
comparisons use stated neutral/blue paint controls to compare finish rather
than pretending a white aluminum photograph measures blue paint.
"""
import argparse,json,sys,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from render import setup
from cape_reflections import scenery as reflection_scenery
from cape_reflections import DEFAULT_PHASE
from cape_render import recipe_sha


def material_mask(path,camera,normal,span,name):
    """Independent first-hit material mask; no displayed pixel values select it."""
    import numpy as np
    from PIL import Image
    from mathutils.bvhtree import BVHTree
    wanted={'wood':('HouseSiding',),'vinyl':('HouseSiding',),'aluminum':('HouseSiding',),
        'cedar':('CapeShingle','CapeCedar'),'cement':('CapeShingle','CapeCement'),
        'roof':('RanchRoof',),'concrete':('HouseConcrete',),'trim':('HouseTrim',),
        'brick':('RanchBrick','RanchBrick_tan'),'glass':('HouseGlass',)}[name]
    vertices=[];faces=[];eligible=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.get('asset_set'):continue
        me=ob.data;me.calc_loop_triangles();off=len(vertices);vertices.extend(ob.matrix_world@v.co for v in me.vertices)
        for t in me.loop_triangles:
            faces.append(tuple(off+i for i in t.vertices));eligible.append(me.materials[t.material_index].name.split('.')[0] in wanted)
    tree=BVHTree.FromPolygons(vertices,faces,all_triangles=True);sc=bpy.context.scene;groups={}
    units=[u for u in json.loads(Path('build/cape/materials/shingles/manufacture.json').read_text())['units'] if u['kind']=='cedar'] if name=='cedar' else []
    pixels=np.asarray(Image.open(path.with_name(name+'.png')).convert('RGB'))/255 if units else None
    width=sc.render.resolution_x;height=sc.render.resolution_y;mask=np.zeros((height,width),dtype='uint8')
    bpy.context.view_layer.update();basis=camera.matrix_world.to_3x3();right=basis.col[0];up=basis.col[1];origin=camera.location.copy();direction=-normal
    for y in range(round(height*.12),round(height*.88)):
        start=origin+up*((.5-(y+.5)/height)*span*height/width)
        for x in range(round(width*.12),round(width*.88)):
            p=start+right*(((x+.5)/width-.5)*span);hit=tree.ray_cast(p,direction,10)
            if hit[2] is not None and eligible[hit[2]]:
                mask[y,x]=255
                if units and x%3==0 and y%3==0:
                    q=hit[0];u=q.y%1.2192;r=int((q.z%.762)/.1524);row=int(q.z//.1524)
                    for j,unit in enumerate(units):
                        if unit['row']!=r:continue
                        for period in (-1,0,1):
                            a=unit['u0_m']+period*1.2192;b=unit['u1_m']+period*1.2192
                            v=((q.z+unit['butt_offset_m'])%.1524)/.1524
                            if a+.003<u<b-.003 and .15<v<.55:
                                key=(row,j,int(q.y//1.2192)-period);groups.setdefault(key,[]).append(float(pixels[y,x]@np.array((.2126,.7152,.0722))))
    Image.fromarray(mask).save(path)
    values=[float(np.median(v)) for v in groups.values() if len(v)>=40]
    stats=dict(count=len(values),values=values,median=float(np.median(values)),sd=float(np.std(values)),cv=float(np.std(values)/np.mean(values)),p10=float(np.quantile(values,.1)),p90=float(np.quantile(values,.9))) if values else None
    return int((mask>0).sum()),stats

CASES=dict(wood=dict(seed=36,exposure=-.90,sky=.14),cedar=dict(seed=32,exposure=-.72,white_balance_kelvin=7500),roof=dict(seed=32,exposure=.07),
    vinyl=dict(seed=31,paint=(.46,.47,.45),exposure=.55),aluminum=dict(seed=34,paint=(.61,.60,.55),exposure=1.25),cement=dict(seed=33,paint=(.61,.60,.55),exposure=0.),
    concrete=dict(seed=36,exposure=.20,sky=.008),trim=dict(seed=36,exposure=-1.15),brick=dict(seed=36,exposure=-.7),glass=dict(seed=36,exposure=-.88,overcast=True,white_balance_kelvin=6500))


def render(folder,width,samples,names,final=False):
    folder.mkdir(parents=True,exist_ok=True);patches=json.loads((folder/'patches.json').read_text()) if (folder/'patches.json').exists() else {}
    for name in names:
        s=CASES[name]
        if final:
            from delivery_io import bundle_hash
            source=Path(f"export/HearthfieldCape-{s['seed']}{'-control' if name=='aluminum' else ''}.gltf");bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()));source_digest=bundle_hash(source)
        else:
            source=Path(f"build/cape/house-{s['seed']}.blend");bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));source_digest=hashlib.sha256(source.read_bytes()).hexdigest()
        meta=json.loads(source.with_suffix('.json').read_text());m=meta['blocks'][0]
        if 'paint' in s and meta.get('paint_control')!=list(s['paint']):
            for ob in bpy.context.scene.objects:
                if ob.type!='MESH' or not ob.get('asset_set'):continue
                attr=ob.data.color_attributes.get('Tint') or ob.data.color_attributes.active_color
                if attr is None:continue
                changed=set()
                for p in ob.data.polygons:
                    if ob.data.materials[p.material_index].name.split('.')[0] not in ('CapeShingle','CapeCedar','CapeCement','HouseSiding'):continue
                    for vi in (p.loop_indices if attr.domain=='CORNER' else p.vertices):
                        if vi in changed:continue
                        changed.add(vi)
                        if final:
                            original=meta['spec']['colors']['siding'];c=attr.data[vi].color
                            attr.data[vi].color=(*(min(1,c[k]*s['paint'][k]/original[k]) for k in range(3)),1)
                        else:attr.data[vi].color=(*s['paint'],1)
        camera=setup('CYCLES',samples);reflection_scenery(meta,phase=s.get('reflection_phase'))
        if name=='cedar':
            target=Vector((m['x0']-.012,(m['y0']+m['y1'])/2-1.65,4.1));normal=Vector((-1,0,0));span=.7018421053
        elif name=='roof':
            # The reference contains about fifteen courses, not a granule macro.
            # A wide, shallow patch fits the clear strip above all three dormers.
            y=m['y0']+3.5;target=Vector((m['x0']+2.0,y,m['eave']+m['pitch']*3.5));normal=Vector((0,-m['pitch'],1)).normalized();span=3.0
        elif name in ('trim','glass'):
            o=next(o for o in meta['openings'] if o['face']=='front' and o['kind']=='window');x=m['x0']+o['u']
            target=Vector((x-o['w']/2-.04445 if name=='trim' else x,m['y0']-.082 if name=='trim' else m['y0']-.072,o['z']+.68 if name=='trim' else o['z']+.28));normal=Vector((0,-1,0));span=.080 if name=='trim' else .12
        elif name=='concrete':
            target=Vector((m['x0']+.85,m['y0']+.023,.15));normal=Vector((0,-1,0));span=.14
        elif name=='brick':
            if final:target=Vector(meta['brick_patch_target'])
            else:
                ob=bpy.data.objects['Brick_Chimney'];vs=[ob.matrix_world@v.co for p in ob.data.polygons if ob.data.materials[p.material_index].name in ('HouseVeneer','RanchBrick') for v in [ob.data.vertices[i] for i in p.vertices]]
                lo=Vector(tuple(min(p[i] for p in vs) for i in range(3)));hi=Vector(tuple(max(p[i] for p in vs) for i in range(3)))
                target=Vector(((lo.x+hi.x)/2,lo.y+.001,hi.z-.45))
            normal=Vector((0,-1,0));span=.65
        else:
            target=Vector((m['x0']+(m['x1']-m['x0'])*.25,m['y0']-.013,m['floor']+.43));normal=Vector((0,-1,0));span=.62
            if name=='cement':span=.6816502193;target.z=m['floor']+.8
            if name in ('wood','vinyl','aluminum'):
                span={'wood':.3931888545,'vinyl':1.0620467836,'aluminum':.8302493075}[name]
                target.x=m['x0']+{'wood':.4,'vinyl':.65,'aluminum':.5}[name]
        camera.location=target+normal*5;camera.rotation_euler=(-normal).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.sensor_fit='HORIZONTAL';camera.data.ortho_scale=span
        sc=bpy.context.scene;sc.render.resolution_x=width;sc.render.resolution_y=width//2 if name=='roof' else width;sc.render.resolution_percentage=100
        sc.view_settings.exposure=s['exposure'];sc.view_settings.look='AgX - Medium High Contrast'
        if s.get('white_balance_kelvin'):
            sc.view_settings.use_white_balance=True;sc.view_settings.white_balance_temperature=s['white_balance_kelvin']
        bpy.data.objects['Afternoon sun'].rotation_euler=Vector(s.get('sun_direction',(.5,.8,-1))).to_track_quat('-Z','Y').to_euler()
        next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=s.get('sky',.12)
        if s.get('overcast'):
            bg=next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND')
            for link in list(bg.inputs['Color'].links):sc.world.node_tree.links.remove(link)
            bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=1
            bpy.data.objects['Afternoon sun'].data.energy=.35;bpy.data.objects['Afternoon sun'].data.angle=.6
        sc.render.filepath=str((folder/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        count,unit_stats=material_mask(folder/(name+'-mask.png'),camera,normal,span,name)
        # Entire central square is a prescribed physical patch, not a mask
        # selected from pixel values. Roof avoids both dormer penetrations.
        box=[width*.12,sc.render.resolution_y*.12,width*.88,sc.render.resolution_y*.88]
        patches[name]=dict(image=name,box=box,seed=s['seed'],target_m=list(target),width_m=span*.76,source=str(source),source_sha256=source_digest,metadata_sha256=hashlib.sha256(source.with_suffix('.json').read_bytes()).hexdigest(),render_recipe_sha256=recipe_sha((Path(__file__),)),reflection_phase=list(s.get('reflection_phase',DEFAULT_PHASE)),paint_control=s.get('paint'),exposure_ev=s['exposure'],sky_strength=1 if s.get('overcast') else s.get('sky',.12),overcast=s.get('overcast',False),white_balance_kelvin=s.get('white_balance_kelvin'),engine='CYCLES',stage='delivered shared PBR' if final else 'source')
        patches[name].update(material_mask=name+'-mask.png',measured_material_pixels=count,mask_method='Independent orthographic first-hit rays against asset triangles and material IDs; fixtures excluded without selecting displayed values')
        patches[name]['sun_direction']=s.get('sun_direction',(.5,.8,-1))
        if unit_stats:patches[name]['per_shingle']=unit_stats
    (folder/'patches.json').write_text(json.dumps(patches,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/cape/lookdev/values'));p.add_argument('--width',type=int,default=720);p.add_argument('--samples',type=int,default=32);p.add_argument('--names',default=','.join(CASES));p.add_argument('--final',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);render(a.out,a.width,a.samples,a.names.split(','),a.final)
