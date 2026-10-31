"""Cape source look-development; no bake or delivery-map writes.

All accepted shared maps remain read-only. Cedar and cement use an original
small two-region preview tile, planned as one additional 512-square set.
"""
import json
import math
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
import bmesh
from mathutils import Vector
from kit import tiling
from lookdev import materials
from textures import SETS
from cape_surfaces import shingle_tile,layer


def prepare(source,out):
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));bpy.context.view_layer.update()
    meta=json.loads(source.with_suffix('.json').read_text())
    from cape_age import add
    add(meta);mats=materials(Path('textures/source'))
    from ranch_fields import trim_orm
    trim_folder=Path('build/ranch/materials/trim')
    if not (trim_folder/'T_RanchTrim_ORM.png').exists():trim_orm(trim_folder,Path('textures/source/T_HouseTrim_ORM.png'))
    for node in mats['Trim'].node_tree.nodes:
        if node.type=='TEX_IMAGE' and node.image and '_ORM' in node.image.name:
            node.image=bpy.data.images.load(str((trim_folder/'T_RanchTrim_ORM.png').resolve()),check_existing=True);node.image.colorspace_settings.name='Non-Color'
    from ranch_lookdev import roof_material
    mats['Shingles']=roof_material(out.parent/'materials'/'roof',meta['spec']['roof_age'])
    from ranch_fields import brick
    brick_folder=out.parent/'materials'/'brick';brick(brick_folder,'tan')
    mats['Veneer']=tiling.material('RanchBrick',brick_folder,tint=True)
    next(n for n in mats['Veneer'].node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.45
    skin=meta['spec']['siding'];preview=out.parent/'materials'/'shingles'
    if skin in ('wood','vinyl','aluminum'):
        next(n for n in mats['Siding'].node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.15
    if skin in ('cedar','cement'):
        shingle_tile(preview);mats['Siding']=tiling.material('CapeShingle',preview,tint=True)
        ns=mats['Siding'].node_tree.nodes;ls=mats['Siding'].node_tree.links
        coord=ns.new('ShaderNodeTexCoord');sep=ns.new('ShaderNodeSeparateXYZ');ls.new(coord.outputs['UV'],sep.inputs[0])
        fract=ns.new('ShaderNodeMath');fract.operation='FRACT';ls.new(sep.outputs['Y'],fract.inputs[0])
        scale=ns.new('ShaderNodeMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=.5;ls.new(fract.outputs[0],scale.inputs[0])
        offset=ns.new('ShaderNodeMath');offset.operation='ADD';offset.inputs[1].default_value=.5 if skin=='cement' else 0;ls.new(scale.outputs[0],offset.inputs[0])
        uvout=ns.new('ShaderNodeCombineXYZ');ls.new(sep.outputs['X'],uvout.inputs[0]);ls.new(offset.outputs[0],uvout.inputs[1])
        for node in ns:
            if node.type=='TEX_IMAGE':ls.new(uvout.outputs[0],node.inputs['Vector'])
    p=mats['Glass'].node_tree.nodes.get('Principled BSDF');nodes=mats['Glass'].node_tree
    for socket in ('Base Color','Roughness'):
        for link in list(p.inputs[socket].links):nodes.links.remove(link)
    p.inputs['Base Color'].default_value=(.95,.97,.95,1);p.inputs['Roughness'].default_value=.035
    total=0;before_total=0;used_roles=set()
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or not ob.get('asset_set'):continue
        if ob.get('component')=='foundation':
            # Wall-section clipping repeats identical foundation prisms below
            # multiple facade regions. Retain each oriented surface once.
            bm=bmesh.new();bm.from_mesh(ob.data);seen=set();duplicates=[]
            for f in bm.faces:
                key=(tuple(sorted(tuple(round(float(x),6) for x in v.co) for v in f.verts)),tuple(round(float(x),5) for x in f.normal),f.material_index)
                if key in seen:duplicates.append(f)
                else:seen.add(key)
            if duplicates:bmesh.ops.delete(bm,geom=duplicates,context='FACES')
            loose=[v for v in bm.verts if not v.link_faces]
            if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
            bm.to_mesh(ob.data);bm.free();ob.data.update()
        from cape_profile import courses
        courses(ob,skin,meta)
        me=ob.data;me.calc_loop_triangles();before_total+=len(me.loop_triangles)
        # Only causal low-wall and upper-roof sample rows. No dense all-face grid.
        if ob.get('component') in ('wall','foundation','roof'):
            bm=bmesh.new();bm.from_mesh(me);block=next((v for v in meta['blocks'] if v['name']==ob.get('block')),meta['blocks'][0])
            levels=[block['floor']-.12,block['floor']+.06,block['floor']+.24,block['floor']+.40] if ob.get('component')!='roof' else [block['eave']+.35,block['eave']+.90,block['eave']+1.7,block['eave']+2.4]
            if meta['spec']['dormers']==3:levels=levels[::2]
            if meta['spec']['dormers']==3 and ob.get('component')=='wall':levels=levels[:1]
            for z in levels:bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,z),plane_no=(0,0,1))
            bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.triangulate(bm,faces=list(bm.faces))
            loose=[v for v in bm.verts if not v.link_faces]
            if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
            bm.to_mesh(me);bm.free();me.update()
        roles=[m.name.replace('House_','') for m in me.materials]
        for i,role in enumerate(roles):me.materials[i]=mats[role]
        attr=me.color_attributes['Tint'];uv=me.uv_layers.active;world=[ob.matrix_world@v.co for v in me.vertices]
        comp=ob.get('component');opening=next((o for o in meta['openings'] if ob.name.startswith(o['id'])),None)
        block_name=ob.get('block') or (opening['block'] if opening else 'Main')
        block=next((v for v in meta['blocks'] if v['name']==block_name),meta['blocks'][0]);vr={};normal={}
        for poly in me.polygons:
            role=roles[poly.material_index];n=(ob.matrix_world.to_3x3()@poly.normal).normalized()
            used_roles.add(role)
            for vi in poly.vertices:
                vr[vi]=role
                if vi not in normal or n.z>.4 or abs(n.z)<.3:normal[vi]=n
            axis=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=axis];pts=[world[i] for i in poly.vertices]
            if role=='Trim':axes.sort(key=lambda k:max(p[k] for p in pts)-min(p[k] for p in pts),reverse=True)
            lo=min(p[axes[1]] for p in pts);hi=max(p[axes[1]] for p in pts)
            strip=6 if role=='Glass' else (5 if comp in ('flashing','valley','roof_vent','storm_window') else (2 if comp=='eave_rake_soffit' and n.z<-.6 else 0))
            if ob.name=='Aged_GrayWoodAtSillNoses':
                strip=3;axes.reverse();lo=min(p[axes[1]] for p in pts);hi=max(p[axes[1]] for p in pts)
            for li in poly.loop_indices:
                p=world[me.loops[li].vertex_index]
                if role in ('Trim','Glass'):
                    u=p[axes[0]]/4
                    if ob.name=='Aged_GrayWoodAtSillNoses':u*=8
                    if strip==5:u=.78+.20*(p[axes[0]]%4)/4
                    uv.data[li].uv=(u,(strip+.04+(p[axes[1]]-lo)/max(.5,(hi-lo)/.92))/8)
                elif role=='Shingles' and abs(n.z)>.3:
                    xy=(p.x,p.y/max(.2,abs(n.z))) if abs(n.y)>=abs(n.x) else (p.y,p.x/max(.2,abs(n.z)))
                    uv.data[li].uv=(xy[0]/4.8768,xy[1]/2.4384)
                elif role=='Siding' and skin in ('cedar','cement'):
                    # Preview uses half-tile addressing; ordinary split charts wait
                    # for delivery, just as the ranch's source roof did.
                    uv.data[li].uv=(p[axes[0]]/1.2192, p[axes[1]]/(.762 if skin=='cedar' else .5588))
                elif role=='Siding' and skin in ('wood','vinyl','aluminum'):
                    vv=-p[axes[1]]/2.4384
                    if skin=='aluminum':
                        center=-sum(q[axes[1]] for q in pts)/len(pts)/2.4384
                        vv+=(1e-6 if center>vv else -1e-6 if center<vv else 0)
                    uv.data[li].uv=(p[axes[0]]/2.4384,vv)
                else:uv.data[li].uv=(p[axes[0]]/SETS.get(role,SETS['Trim'])[1],(p[axes[1]]+(.3048 if role=='Concrete' else 0))/SETS.get(role,SETS['Trim'])[1])
        rest=me.attributes.new(name='CapeRest',type='FLOAT_VECTOR',domain='POINT')
        context=me.attributes.new(name='CapeContext',type='FLOAT_VECTOR',domain='POINT')
        fasteners=me.attributes.new(name='CapeFasteners',type='FLOAT_VECTOR',domain='POINT')
        fields={key:me.attributes.new(name='Cape'+key,type='FLOAT',domain='POINT') for key in ('Water','Wet','Wood','Oxide','Rust','Cheek','GutterAxis','Peel')}
        for v in me.vertices:
            role=vr[v.index];p=world[v.index];c=Vector(attr.data[v.index].color[:3])
            if role=='Glass':c=Vector((1,1,1))
            if role=='Veneer':c=Vector((.61,.464,.625))
            if role=='Concrete':c=Vector((.82,.81,.78))
            if role=='Concrete' and comp=='foundation_marks':c*=.87
            if role=='Shingles':
                c=Vector(dict(green_black=(.61,.65,.53),warm_charcoal=(.72,.72,.67),weathered_wood=(.94,.84,.66),dark_brown=(.75,.61,.44))[meta['spec']['shingle_color']])
                c=Vector((c.x*.98,c.y/.965,c.z*.98/.90))*(.105/.17)
            low=min(.6096,block['floor']-.0762) if block['floor']>=.4 else max(.04,block['floor']-.205)
            if block['name'].startswith('Dormer') or block['name']=='RearShed':
                main=meta['blocks'][0];low=main['eave']+main['pitch']*min(p.y-main['y0'],main['y1']-p.y)
            shade_eave=block['eave']
            face=ob.get('face',opening['face'] if opening else None)
            gable_end=face in (('left','right') if block['ridge_axis']=='X' else ('front','back'))
            if block['roof']=='gable' and gable_end and comp in ('wall','window','storm_window'):
                distance=min(p.y-block['y0'],block['y1']-p.y) if block['ridge_axis']=='X' else min(p.x-block['x0'],block['x1']-p.x)
                shade_eave+=block['pitch']*distance
            rest.data[v.index].vector=p;context.data[v.index].vector=(low,shade_eave,1 if meta['spec']['roof_age']=='tired' else .15)
            water=math.exp(-((p.x-meta['door_x'])/1.2)**2)*math.exp(-((p.y-meta['blocks'][0]['y0'])/.6)**2)
            rust=0
            for d in meta['drains']:
                q=Vector(d['centerline'][3]);water=max(water,math.exp(-((p.x-q.x)**2+(p.y-q.y)**2)/.28))
                for q in map(Vector,d['gutter']):
                    below=q.z-p.z
                    if 0<below<.65:rust=max(rust,math.exp(-((p.x-q.x)**2+(p.y-q.y)**2)/.018)*math.exp(-below/.32)*.6)
            fasteners.data[v.index].vector=(0,0,-10)
            wet=opening['z'] if comp=='window' and opening else -10
            external=True;peel=0
            if opening:
                from plan import wall_frame
                from types import SimpleNamespace
                origin,t,outward,length=wall_frame(SimpleNamespace(**block,width=block['x1']-block['x0'],depth=block['y1']-block['y0']),opening['face'])
                external=(p.x-origin[0])*outward[0]+(p.y-origin[1])*outward[1]>-.045
                fasteners.data[v.index].vector=(origin[0]+opening['u'] if abs(outward[1])>.5 else origin[1]+opening['u'],opening['w']/2-.012,opening['z']+opening['h']-.012)
                if comp=='window' and external:
                    depth=(p.x-origin[0])*outward[0]+(p.y-origin[1])*outward[1]
                    along=(p.x-origin[0])*t[0]+(p.y-origin[1])*t[1]-opening['u']
                    near_sill=max(0,1-abs(p.z-opening['z'])/.045)
                    nose=max(0,min(1,(depth-.068)/.045))
                    ends=math.exp(-((abs(along)-opening['w']/2)/.10)**2)
                    sash_joint=math.exp(-((depth-.035)/.014)**2)
                    peel=near_sill*max(nose,ends*.85,sash_joint*.7)
            wood=role=='Trim' and comp in ('window','corner_posts','water_table','eave_rake_soffit','porch_structure','door_frame') and max(c)>.3 and external
            cheek=0
            for d in meta['blocks']:
                if d['name'].startswith('Dormer'):
                    cheek=max(cheek,math.exp(-min((p.x-d['x0'])**2,(p.x-d['x1'])**2)/.06)*max(0,min(1,(p.y-d['y0']+.1)/.2))*max(0,min(1,(d['y1']+.15-p.y)/.3)))
            if comp in ('drainage','eave_rake_soffit') and block['name'] in ('Main','Wing','Garage'):rust=1
            for key,value in dict(Water=water,Wet=wet,Wood=float(wood),Oxide=float(comp=='storm_window'),Rust=rust,Cheek=cheek,GutterAxis=float(block['ridge_axis']=='X'),Peel=peel).items():fields[key].data[v.index].value=value
            attr.data[v.index].color=(*c,1)
        me.calc_loop_triangles();total+=len(me.loop_triangles)
    for role,mat in mats.items():layer(mat,role,meta)
    meta.update(triangles=total,stage='Cape source look-development checkpoint / original causal fields / no bake',source_triangles=before_total,preview_siding_set=skin in ('cedar','cement'),materials=len(used_roles),material_roles=sorted(used_roles),wear_method='meter-scale rest attributes and procedural source nodes; delivery transfer pending')
    out.parent.mkdir(parents=True,exist_ok=True);out.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
    print('CAPE_SOURCE',meta['seed'],total);return meta


if __name__=='__main__':
    import sys
    for seed in map(int,sys.argv[sys.argv.index('--')+1:] or range(31,37)):
        prepare(Path(f'build/cape/form-{seed}.blend'),Path(f'build/cape/house-{seed}.blend'))
