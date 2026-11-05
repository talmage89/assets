"""Independent strip-center form builds; never writes station artifacts."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from geometry import *
from strip_plan import generate,PROOF_SEEDS
from strip_graphics import generate as graphics,install
from strip_building import bay,endcap,tower,ladder,coping,meter_bank
from strip_site import site,pylon,plant


def build(seed,folder=Path('build/strip'),overrides=None,plants=True,look=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    import geometry
    geometry.SHARED_GRAPHICS=False;reset_prints()
    p=generate(seed,overrides);p['look']=look;b=p['building']
    palette(dict(primary=(.095,.125,.12),accent=(.35,.19,.09),light=(.70,.67,.59)),b['wall_color'])
    # Quick physical-value palette; the form gate deliberately does not build
    # the commercial material fields or modify the gas station's shared maps.
    M['Lamp'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=25
    ink,layout=install(Path('build/strip/signs-look' if look else 'build/strip/signs'),look=look);modules={}
    row=[m for m in p['modules'] if not m['wing']]
    if p['towers']=='ends':positions=[b['left']+1.8,b['left']+b['width']-1.8];tower_tenants=[row[0]['tenant'],row[-1]['tenant']]
    elif p['towers']=='center':positions=[b['left']+b['width']/2];tower_tenants=[None]
    else:positions=[p['elbow']['bounds'][0]-5.0];tower_tenants=[row[-1]['tenant']]
    hosted=set(key for key in tower_tenants if key)
    for i,m in enumerate(p['modules']):
        nextm=p['modules'][i+1] if i+1<len(p['modules']) else None
        # End caps / the return-wing closure own the outer wall. A final
        # demising wall here duplicates their exterior skin below 2.94m.
        m['partition']=bool(nextm) and not (m['lease_group']==nextm['lease_group'] and m['yaw']==nextm['yaw'])
        prev=p['modules'][i-1] if i else None
        m['open_left']=bool(prev and prev['lease_group']==m['lease_group'] and prev['yaw']==m['yaw'])
        m['corner_end']=bool(nextm and not m['wing'] and nextm['wing'])
        m['end_column']=(nextm is None or m['yaw']!=nextm['yaw']) and not m['corner_end']
        m['wrap_side']=(-1 if i==0 and p['endcaps'][0]=='wrap' else 1 if i==len(p['modules'])-1 and p['endcaps'][1]=='wrap' and not p['elbow'] else 0)
        m['hosted_sign']=not m['wing'] and m['tenant'] in hosted
        group=[q for q in p['modules'] if q['lease_group']==m['lease_group'] and q['yaw']==m['yaw']]
        m['sign_leader']=m==group[0]
        m['sign_offset']=(len(group)-1)*m['width']/2
        if p['towers']=='center':
            center=positions[0];xx=m['origin'][0]
            if abs(xx-center)<m['width']:
                m['sign_width']=m['width']-2.45
                m['sign_offset']=-.90 if xx<center else .90
        modules[m['id']]=bay(m,p,ink,layout)
    endcap('EndCap_Left',b['left']+.1016,p,ink=ink,layout=layout)
    if not p['elbow']:endcap('EndCap_Right',b['left']+b['width']-.1016,p,outward=1,ink=ink,layout=layout)
    else:
        x0,x1,y0,y1=p['elbow']['bounds'];r=root('ElbowStorage',kind='Elbow');r['reusable_module']=True
        box('Elbow floor',((x0+x1)/2,(y0+y1)/2,.0762),(x1-x0,y1-y0,.1524),'Concrete',r,.003)
        box('Elbow rear masonry',((x0+x1)/2,y1-.1016,b['parapet']/2),(x1-x0,.2032,b['parapet']),'Wall',r,.004)
        box('Elbow outer return',(x1-.1016,(y0+y1)/2,b['parapet']/2),(.2032,y1-y0,b['parapet']),'Wall',r,.004)
        box('Elbow membrane',((x0+x1)/2,(y0+y1)/2,b['roof']),(x1-x0,y1-y0-.30,.045),'Roof',r,0)
        # Wing outer end wall and coping close the short leg without a duplicate
        # inside end wall between the elbow and its tenant's storage.
        d=b['depth'];ww=p['modules'][0]['width'];yy=y0-2*ww
        end=endcap('EndCap_Return',0,{**p,'building':{**b,'front':-d/2}},outward=1,ink=ink,layout=layout)
        end.location=((x0+x1)/2,yy+.1016,0);end.rotation_euler.z=0
        box('Elbow east coping',(x1,(y0+y1)/2,b['parapet']+.018),(.30,y1-y0,.036),'Trim',r,.003)
        box('Elbow rear coping',((x0+x1)/2,y1,b['parapet']+.018),(d,.30,.036),'Trim',r,.003)
    for i,(x,tenant) in enumerate(zip(positions,tower_tenants)):tower('Tower_'+str(i+1),x,p,tenant,ink,layout)
    ladder(p);meter_bank(p,ink,layout);site(p,modules,ink,layout);pylon(p,ink,layout)
    world=root('StripCenter_'+str(seed),kind='StripCenter')
    for ob in list(bpy.context.scene.objects):
        if ob!=world and ob.parent is None:ob.parent=world;ob['reusable_module']=True
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    # Sub-4mm edge breaks on mullions, straps, seams and panel rims belong in
    # the eventual shared trim normal, not eight copies of bevel triangles.
    # Keep cabinet, upholstery, masonry-base and casting silhouette radii.
    for ob in bpy.context.scene.objects:
        for mod in list(ob.modifiers):
            if mod.type=='BEVEL' and mod.width<=.0041:ob.modifiers.remove(mod)
    if look:
        from strip_age import add
        from strip_surfaces import apply
        add(p,modules,ink,layout);apply(p,ink,layout)
    finish_prints(folder/f'addresses-{seed}.png');finalize();bpy.context.view_layer.update()
    if plants:p['landscape']=plant(p,world)
    else:p['landscape']=dict(instances=0,scope='No botanical instances for diagnostic repeat')
    bpy.context.view_layer.update();path=folder/f'strip-{seed}.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(path.resolve()),compress=True)
    if look:
        from kit.tiling import export
        export(path.with_suffix('.glb'))
    else:bpy.ops.export_scene.gltf(filepath=str(path.with_suffix('.glb').resolve()),export_format='GLB',export_extras=True,export_apply=False,export_yup=True,export_texcoords=True,export_normals=True,export_tangents=False,export_materials='EXPORT',export_cameras=False,export_lights=False)
    counts={};meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    for ob in meshes:
        owner=ob.parent
        while owner and owner.parent!=world:owner=owner.parent
        key=owner.name if owner else ob.name;counts[key]=counts.get(key,0)+sum(len(f.vertices)-2 for f in ob.data.polygons)
    p.update(triangles=counts,total_triangles=sum(counts.values()),unique_mesh_triangles=sum(sum(len(f.vertices)-2 for f in me.polygons) for me in {o.data for o in meshes}),
             materials=len({mat for o in meshes for mat in o.data.materials}),glb_bytes=path.with_suffix('.glb').stat().st_size,glb_sha256=hashlib.sha256(path.with_suffix('.glb').read_bytes()).hexdigest())
    p['building_triangles']=sum(n for key,n in counts.items() if key.startswith(('Bay_','EndCap_','Tower_','Elbow','RoofLadder','MeterBank')))
    p['moving_parts']={o.name:dict(position=list(o.matrix_world.translation),axis=o['pivot_axis'],range=list(o['range_degrees'])) for o in bpy.context.scene.objects if o.get('pivot_axis')}
    p['sockets']={o.name:list(o.matrix_world.translation) for o in bpy.context.scene.objects if o.get('socket_kind')}
    path.with_suffix('.json').write_text(json.dumps(p,indent=2)+'\n')
    print('STRIP',seed,p['building_triangles'],'building;',p['total_triangles'],'placed triangles;',p['glb_bytes'],'bytes',flush=True)
    print(counts,flush=True)
    return p


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--seeds',default=','.join(map(str,PROOF_SEEDS)));a.add_argument('--out',type=Path,default=Path('build/strip'));a.add_argument('--plan',type=Path);a.add_argument('--no-plants',action='store_true');a.add_argument('--look',action='store_true');a=a.parse_args(sys.argv[sys.argv.index('--')+1:])
    graphics(Path('build/strip/signs-look' if a.look else 'build/strip/signs'),look=a.look)
    for seed in map(int,a.seeds.split(',')):build(seed,a.out,json.loads(a.plan.read_text()) if a.plan else None,not a.no_plants,a.look)
