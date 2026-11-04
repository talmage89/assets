"""Fixed physical patches on the actual split source, before any bake.

The aluminum white-paint control is explicit. All other cases retain the
proof seed's authored palette. No rendered pixel receives postprocessing.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path[:0]=[str(Path(__file__).resolve().parents[2]),str(Path(__file__).resolve().parent)]
from render import setup
from cape_reflections import scenery
from split_render import grade

CASES={
 **{f'brick{s}':dict(seed=s,role='Veneer',exposure=e) for s,e in ((51,.95),(53,-.20),(54,-.65),(55,.80),(56,.40))},
 'stone52':dict(seed=52,role='Veneer',exposure=-.20,overcast=True),
 'battens':dict(seed=52,role='Siding',exposure=.15,overcast=True),
 'blue_lap':dict(seed=53,role='Siding',exposure=-.80,overcast=True),
 'vinyl':dict(seed=55,role='Siding',exposure=.55),
 'garage':dict(seed=51,role='Trim',exposure=.20),
 'roof':dict(seed=51,role='Shingles',exposure=-.55),
 'driveway':dict(seed=51,role='Concrete',exposure=1.40),
 'wood':dict(seed=51,role='Siding',exposure=-.90,sky=.14),
 'aluminum':dict(seed=53,role='Siding',exposure=1.15,paint=(.61,.60,.55)),
 'concrete':dict(seed=51,role='Concrete',exposure=.20,sky=.008),
 'trim':dict(seed=51,role='Trim',exposure=-1.15),
 'glass':dict(seed=51,role='Glass',exposure=-.88,overcast=True),
}
CASES['brick55']['sky']=.08
CASES['brick56']['sun_direction']=(-.5,-.8,-1)


def recipe():
    root=Path(__file__).resolve().parent
    return hashlib.sha256(b''.join((root/n).read_bytes() for n in ('split_value_render.py','split_render.py','cape_value_render.py','cape_render.py','cape_reflections.py','ranch_render.py','render.py'))).hexdigest()


def material_mask(path,camera,wanted):
    """First-hit material IDs, never a threshold on displayed pixel values."""
    from mathutils.bvhtree import BVHTree
    import numpy as np
    from PIL import Image
    vs=[];fs=[];keep=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.hide_render or not ob.visible_camera:continue
        me=ob.data;me.calc_loop_triangles();off=len(vs);vs.extend(ob.matrix_world@v.co for v in me.vertices)
        for t in me.loop_triangles:
            fs.append(tuple(off+i for i in t.vertices));keep.append(bool(ob.get('asset_set')) and me.materials[t.material_index].name.split('.')[0]==wanted)
    tree=BVHTree.FromPolygons(vs,fs,all_triangles=True);sc=bpy.context.scene;w=sc.render.resolution_x;h=sc.render.resolution_y
    mask=np.zeros((h,w),dtype='uint8');bpy.context.view_layer.update();basis=camera.matrix_world.to_3x3();right=basis.col[0];up=basis.col[1];forward=-basis.col[2]
    for y in range(round(h*.12),round(h*.88)):
        start=camera.location+up*((.5-(y+.5)/h)*camera.data.ortho_scale*h/w)
        for x in range(round(w*.12),round(w*.88)):
            origin=start+right*(((x+.5)/w-.5)*camera.data.ortho_scale)
            hit=tree.ray_cast(origin,forward,10)
            if hit[2] is not None and keep[hit[2]]:mask[y,x]=255
    Image.fromarray(mask).save(path);return int((mask>0).sum())


def render(folder,names,width=600,samples=24):
    folder.mkdir(parents=True,exist_ok=True);records=json.loads((folder/'patches.json').read_text()) if (folder/'patches.json').exists() else {}
    refs=json.loads(Path('build/split/material-photos.json').read_text())
    for name in names:
        if name in ('aluminum','glass'):
            from split_context import cape_control
            cape_control(34 if name=='aluminum' else 36)
            from cape_value_render import render as retained_cape
            retained_cape(folder,width,samples,[name])
            row=json.loads((folder/'patches.json').read_text())[name];row['recipe_sha256']=recipe();row['map_sha256']=row['material_sha256']
            row['reuse_control']='Accepted Cape white aluminum / original 4 in profile. The split wide blue 8 in profile is separately measured as blue_lap.' if name=='aluminum' else 'Accepted Cape glass / identical IOR 1.52, roughness .010, clear white tint, no normal. Reflection distribution depends on room and scenery; split street/bay views are separately reviewed.'
            records[name]=row;(folder/'patches.json').write_text(json.dumps(records,indent=2));continue
        case=CASES[name];source=Path(f"build/split/house-{case['seed']}.blend");bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));meta=json.loads(source.with_suffix('.json').read_text())
        m=meta['blocks'][0];wing=next((b for b in meta['blocks'] if b['name']=='Wing'),m);role=case['role']
        wanted={'Veneer':'SplitStone' if meta['spec']['veneer']=='stone' else 'SplitBrick','Siding':'SplitPaintedBoards' if meta['spec']['siding']=='battens' else 'HouseSiding','Shingles':'RanchRoof','Trim':'HouseTrim','Concrete':'HouseConcrete','Glass':'HouseGlass'}[role]
        if case.get('paint'):
            for ob in bpy.context.scene.objects:
                if ob.type!='MESH' or not ob.get('asset_set'):continue
                c=ob.data.color_attributes.get('Tint');seen=set()
                for p in ob.data.polygons:
                    if ob.data.materials[p.material_index].name.split('.')[0]!=wanted:continue
                    for i in p.vertices:
                        if i not in seen:c.data[i].color=(*case['paint'],1);seen.add(i)
        normal=Vector((0,-1,0));span=.9
        if name.startswith('brick'):
            b=m;target=Vector((m['x0']+(m['x1']-m['x0'])*.34,m['y0']-.073,m['floor']+.30));span=3.6
            if name=='brick53':span=4.8
            if name=='brick54':b=wing;target=Vector(((b['x0']+b['x1'])/2,b['y1']+.073,meta['levels']['upper']+.54));span=1.6;normal=Vector((0,1,0))
            if name=='brick55':target=Vector((m['x0']+(m['x1']-m['x0'])*.34,m['y0']-.073,.78));span=1.0
            if name=='brick56':target=Vector(((wing['x0']+wing['x1'])/2,wing['y1']+.073,1.15));span=7.;normal=Vector((0,1,0))
        elif name=='stone52':target=Vector(((wing['x0']+wing['x1'])/2,wing['y0']-.073,.45));span=1.70
        elif name in ('battens','blue_lap','vinyl','wood','aluminum'):
            target=Vector(((wing['x0']+wing['x1'])/2,wing['y0']-.014,meta['levels']['upper']+.50));span=.70
            if name=='aluminum':span=.83
            if name=='wood':span=.70
            if name=='blue_lap':span=.90
            if name=='vinyl':
                target.x=m['x0']+(m['x1']-m['x0'])*.35;target.z=meta['levels']['upper']+.40;span=1.4
        elif name=='garage':
            opening=next(o for o in meta['openings'] if o['kind']=='garage');b=next(b for b in meta['blocks'] if b['name']==opening['block'])
            target=Vector((b['x0']+opening['u'],b['y0']+.20,opening['z']+.70));span=2.8
        elif name=='roof':
            y=m['y0']+2.;target=Vector((m['x0']+2.2,y,m['eave']+m['pitch']*2));normal=Vector((0,-m['pitch'],1)).normalized();span=3.0
        elif name=='driveway':
            d=meta['driveway'];y=d['front']+3.0;z=d['back_z']-.01+(d['front_z']-d['back_z']+.01)*(d['back']-1.25-y)/(d['back']-1.25-d['front'])
            target=Vector((d['x'],y,z));normal=Vector((0,0,1));span=3.0
        elif name=='concrete':target=Vector((m['x0']+.7,m['y0']+.023,.15));span=.14
        elif name in ('trim','glass'):
            o=next(o for o in meta['openings'] if o['face']=='front' and o['kind']=='window');x=m['x0']+o['u']
            target=Vector((meta['door_x']-.9144/2-.03 if name=='trim' else x,m['y0']-.082 if name=='trim' else m['y0']-.10,meta['levels']['living']+.80 if name=='trim' else o['z']+.28));span=.080 if name=='trim' else .12
        camera=setup('CYCLES',samples);grade(meta);scenery(meta,phase=case.get('reflection_phase'));camera.location=target+normal*5;camera.rotation_euler=(-normal).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.sensor_fit='HORIZONTAL';camera.data.ortho_scale=span
        photo_box=refs[name]['box'];aspect=(photo_box[2]-photo_box[0])/(photo_box[3]-photo_box[1]);aspect=min(5,max(.55,aspect))
        sc=bpy.context.scene;sc.render.resolution_x=width;sc.render.resolution_y=round(width/aspect);sc.render.resolution_percentage=100;sc.view_settings.exposure=case['exposure']
        sc.view_settings.use_white_balance=True;sc.view_settings.white_balance_temperature=6500
        sun_direction=case.get('sun_direction',(.5,-.8 if normal.y>.5 else .8,-1))
        bpy.data.objects['Afternoon sun'].rotation_euler=Vector(sun_direction).to_track_quat('-Z','Y').to_euler()
        bg=next(n for n in sc.world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Strength'].default_value=case.get('sky',.12)
        if case.get('overcast'):
            for link in list(bg.inputs['Color'].links):sc.world.node_tree.links.remove(link)
            bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=1
            bpy.data.objects['Afternoon sun'].data.energy=.35;bpy.data.objects['Afternoon sun'].data.angle=.6
        sc.render.filepath=str((folder/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
        count=material_mask(folder/(name+'-mask.png'),camera,wanted)
        records[name]=dict(seed=case['seed'],source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),metadata_sha256=hashlib.sha256(source.with_suffix('.json').read_bytes()).hexdigest(),recipe_sha256=recipe(),target_m=list(target),normal=list(normal),span_m=span,box=[width*.12,sc.render.resolution_y*.12,width*.88,sc.render.resolution_y*.88],material=wanted,material_pixels=count,mask='Independent first-hit triangle/material IDs',paint_control=case.get('paint'),exposure_ev=case['exposure'],white_balance_kelvin=6500,sky_strength=1 if case.get('overcast') else case.get('sky',.12),sun_energy=.35 if case.get('overcast') else 3.7,engine='CYCLES',stage='Source checkpoint before bake')
        records[name]['map_sha256']={str(Path(bpy.path.abspath(im.filepath)).resolve()):hashlib.sha256(Path(bpy.path.abspath(im.filepath)).read_bytes()).hexdigest() for im in bpy.data.images if im.filepath and Path(bpy.path.abspath(im.filepath)).is_file()}
        records[name].update(sun_direction=sun_direction,reflection_phase=case.get('reflection_phase'))
        (folder/'patches.json').write_text(json.dumps(records,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('renders/split/lookdev/values'));p.add_argument('--names',default=','.join(CASES));p.add_argument('--width',type=int,default=600);p.add_argument('--samples',type=int,default=24);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);render(a.out,a.names.split(','),a.width,a.samples)
