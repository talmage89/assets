"""Cape-reused source look development; never publishes delivery maps.

Metric lap geometry reuses the Cape profile sweep on siding faces only.
Existing brick, roof, trim and concrete fields are reused. Macro age follows
grade, orientation, window runoff, eave shelter and vehicle paths.
"""
import json
import math
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector
from lookdev import materials
from lookdev import weather as shared_weather
from ranch_lookdev import roof_material
from split_surfaces import layer
from split_fields import stone_material,COVERAGE as STONE_COVERAGE
from cape_profile import courses
from kit import tiling


def lap_siding_only(ob,skin,meta):
    """Keep masonry on its original plane while sweeping only lap surfaces."""
    if ob.get('component')!='wall' or skin not in ('wood','vinyl','aluminum'):return
    me=ob.data
    # Cape's profile sweep assumes a single wall finish. Use disconnected
    # material subsets to preserve the lower brick/upper siding floor break.
    bm=bmesh.new();bm.from_mesh(me)
    siding=next(i for i,m in enumerate(me.materials) if m.name=='House_Siding')
    non=[f for f in bm.faces if f.material_index!=siding]
    exposure=.2032 if skin=='aluminum' else None
    if not non:bm.free();courses(ob,skin,meta,exposure_m=exposure);return
    copy=bm.copy();bmesh.ops.delete(bm,geom=non,context='FACES')
    bmesh.ops.delete(copy,geom=[f for f in copy.faces if f.material_index==siding],context='FACES')
    bm.to_mesh(me);bm.free();me.update();courses(ob,skin,meta,exposure_m=exposure)
    base=ob.data;join=bmesh.new();join.from_mesh(base)
    extra=bpy.data.meshes.new('Temporary masonry');copy.to_mesh(extra);copy.free();join.from_mesh(extra);join.to_mesh(base);join.free();bpy.data.meshes.remove(extra);base.update()


def prepare(source,out):
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));meta=json.loads(source.with_suffix('.json').read_text());s=meta['spec']
    from plan import generate
    from cape_age import add
    import copy
    if s['roof_age']=='tired' and s['window_update']=='wood_storm':
        age_meta=copy.deepcopy(meta);age_meta['spec']['siding']='wood'
        from split_build import veneer_top
        age_plan=generate(meta['seed'],s,house_type='split');sills=[]
        for o in age_meta['openings']:
            block=next(b for b in age_plan['blocks'] if b.name==o['block']);top=veneer_top(age_plan,block,o['face'])
            # Masonry openings have brick rowlocks, not projecting painted
            # wood noses. The bay also has its own newer faceted seat.
            if o.get('style')=='bay' or (top is not None and top>o['z']):continue
            o['sill_wall_y']=block.y0+o.get('recess',0)
            o['sill_profile']=(.035,.006,.185,-.012)
            o['sill_loss_depth_range']=(.135,.150);sills.append(o)
        age_meta['openings']=sills
        add(age_meta,age_plan,foundation_marks=False)
    mats=materials(Path('textures/source'))
    folder=Path('build/split/materials')
    mats['Shingles']=roof_material(folder/'roof',s['roof_age'])
    from cape_masonry import dielectric,author
    masonry=folder/'masonry';author(masonry)
    mats['Veneer']=stone_material(folder/'stone') if s['veneer']=='stone' else dielectric('CapeBrick',masonry)
    mats['Veneer'].name='SplitStone' if s['veneer']=='stone' else 'SplitBrick'
    mats['Concrete']=dielectric('CapeConcrete',masonry);mats['Concrete'].name='HouseConcrete'
    from ranch_fields import trim_orm
    trim_folder=folder/'trim';trim_orm(trim_folder,Path('textures/source/T_HouseTrim_ORM.png'))
    for node in mats['Trim'].node_tree.nodes:
        if node.type=='TEX_IMAGE' and node.image and '_ORM' in node.image.name:
            node.image=bpy.data.images.load(str((trim_folder/'T_RanchTrim_ORM.png').resolve()),check_existing=True);node.image.colorspace_settings.name='Non-Color'
    if s['siding'] in ('battens','grooved'):
        mats['Siding']=mats['Trim'].copy();mats['Siding'].name='SplitPaintedBoards'
    else:
        next(n for n in mats['Siding'].node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.15
    total=0;used=set()
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.get('asset_set'):continue
        lap_siding_only(ob,s['siding'],meta)
        me=ob.data;roles=[m.name.replace('House_','') for m in me.materials]
        for i,role in enumerate(roles):me.materials[i]=mats[role]
        if not me.uv_layers:me.uv_layers.new(name='UVMap')
        uv=me.uv_layers.active;col=me.color_attributes['Tint'];world=[ob.matrix_world@v.co for v in me.vertices]
        rest=me.attributes.new(name='SplitRest',type='FLOAT_VECTOR',domain='POINT')
        context=me.attributes.new(name='CapeContext',type='FLOAT_VECTOR',domain='POINT')
        cape_rest=me.attributes.new(name='CapeRest',type='FLOAT_VECTOR',domain='POINT')
        fasteners=me.attributes.new(name='CapeFasteners',type='FLOAT_VECTOR',domain='POINT')
        fields={key:me.attributes.new(name='Cape'+key,type='FLOAT',domain='POINT') for key in ('Water','Wet','Wood','Oxide','Rust','Cheek','GutterAxis','Peel')}
        special={key:me.attributes.new(name='Split'+key,type='FLOAT',domain='POINT') for key in ('Garage','Drive','Retaining','Paint','Eave','Flake','Coping','Vinyl')}
        vertex_roles={};normals={};component=ob.get('component')
        opening=next((o for o in meta['openings'] if ob.name.startswith(o['id'])),None)
        block=next((b for b in meta['blocks'] if b['name']==ob.get('block',opening['block'] if opening else 'Main')),meta['blocks'][0])
        for poly in me.polygons:
            role=roles[poly.material_index];used.add(role);n=(ob.matrix_world.to_3x3()@poly.normal).normalized()
            pts=[world[i] for i in poly.vertices];axis=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=axis]
            if role=='Trim':axes.sort(key=lambda k:max(p[k] for p in pts)-min(p[k] for p in pts),reverse=True)
            lo=min(p[axes[1]] for p in pts);hi=max(p[axes[1]] for p in pts)
            strip=6 if role=='Glass' else 2 if component=='eave_rake_soffit' and n.z<-.6 else 5 if component in ('flashing','roof_vent','storm_window','bay_roof') else 0
            if ob.name=='Aged_GrayWoodAtSillNoses':strip=3
            if component=='bay_brackets':strip=5
            if component=='window':
                cc=col.data[poly.vertices[0]].color
                if max(cc[:3])<.01:strip=7
                elif .18<min(cc[:3]) and max(cc[:3])<.5:strip=4
            for i in poly.vertices:vertex_roles[i]=role;normals[i]=n
            for li in poly.loop_indices:
                p=world[me.loops[li].vertex_index]
                if role in ('Trim','Glass') or (role=='Siding' and s['siding'] in ('battens','grooved')):
                    uu=p[axes[0]]/4
                    if strip==5:uu=.78+.20*(uu%1)
                    uv.data[li].uv=(uu,(strip+.04+.90*(p[axes[1]]-lo)/max(.5,hi-lo))/8)
                elif role=='Shingles' and abs(n.z)>.3:
                    coord=(p.x,p.y/abs(n.z)) if abs(n.y)>=abs(n.x) else (p.y,p.x/abs(n.z));uv.data[li].uv=(coord[0]/4.8768,coord[1]/2.4384)
                elif role=='Siding':uv.data[li].uv=(p[axes[0]]/2.4384,-p[axes[1]]/(4.8768 if s['siding']=='aluminum' else 2.4384))
                elif role=='Veneer':
                    if component=='opening_masonry':
                        index=min(poly.vertices)//8;unit=world[index*8:index*8+8]
                        aa=sorted(axes,key=lambda k:max(v[k] for v in unit)-min(v[k] for v in unit),reverse=True)
                        low=[min(v[k] for v in unit) for k in aa];span=[max(v[k] for v in unit)-low[j] for j,k in enumerate(aa)]
                        uv.data[li].uv=((index%3-.5*((index//3)%2)+.15+.70*(p[aa[0]]-low[0])/max(span[0],1e-6))/3,((index//3)%8+.24+.52*(p[aa[1]]-low[1])/max(span[1],1e-6))/8)
                        if s['veneer']=='stone':uv.data[li].uv=((index%3+.14+.72*(p[aa[0]]-low[0])/max(span[0],1e-6))/3,.15+.70*(p[aa[1]]-low[1])/max(span[1],1e-6))
                    elif component=='veneer_cap' and s['veneer']=='stone':uv.data[li].uv=(p[axes[0]]/.6096,.50)
                    else:uv.data[li].uv=(p[axes[0]]/(STONE_COVERAGE if s['veneer']=='stone' else .6096),p[axes[1]]/(STONE_COVERAGE if s['veneer']=='stone' else .2032/3*8))
                else:uv.data[li].uv=(p[axes[0]]/1.2192,(p[axes[1]]+.3048)/1.2192)
        for v in me.vertices:
            role=vertex_roles[v.index];p=world[v.index];n=normals[v.index];c=Vector(col.data[v.index].color[:3])
            if role=='Veneer':c=Vector((1,1,1) if s['veneer']=='stone' else (.61,.464,.625))
            elif role=='Concrete':c=Vector((.82,.81,.78))
            elif role=='Glass':c=Vector((1,1,1))
            elif role=='Shingles':
                c=Vector(dict(warm_charcoal=(.78,.72,.67),weathered_wood=(.94,.84,.66),dark_brown=(.75,.61,.44),green_black=(.61,.65,.53))[s['shingle_color']])
                c=Vector((c.x*.98,c.y/.965,c.z*.98/.90))*(.105/.17)*dict(warm_charcoal=.33,dark_brown=.70,weathered_wood=1.,green_black=.65)[s['shingle_color']]
            low=s['site_grade_m']
            eave=block['eave']
            caperest=Vector((p.y,p.x,p.z)) if role=='Shingles' and block['ridge_axis']=='Y' else p
            rest.data[v.index].vector=p;cape_rest.data[v.index].vector=caperest
            context.data[v.index].vector=(low,eave,(.60 if role=='Shingles' else 1) if s['roof_age']=='tired' else .10)
            water=math.exp(-((p.x-meta['door_x'])/1.1)**2)*math.exp(-((p.y-meta['blocks'][0]['y0'])/.6)**2)
            overflow=0
            for d in meta['drains']:
                q=Vector(d['centerline'][3]);water=max(water,math.exp(-((p.x-q.x)**2+(p.y-q.y)**2)/.25))
                for q in map(Vector,d['gutter']):
                    below=q.z-p.z
                    if -.05<below<.8:overflow=max(overflow,math.exp(-((p.x-q.x)**2+(p.y-q.y)**2)/.12)*math.exp(-max(0,below)/.35))
            wood=role=='Trim' and component in ('window','corner_posts','eave_rake_soffit','door_frame','bay') and max(c)>.3 and (component!='window' or s['window_update']=='wood_storm') and not (component=='corner_posts' and s['siding']=='vinyl')
            peel=0
            if opening and component=='window':
                peel=max(0,1-abs(p.z-opening['z'])/.06)
            if component=='eave_rake_soffit':peel=max(peel,overflow)
            for key,val in dict(Water=water,Wet=opening['z'] if opening else -10,Wood=float(wood),Oxide=float(component=='storm_window'),Rust=overflow,Cheek=0,GutterAxis=float(block['ridge_axis']=='X'),Peel=peel).items():fields[key].data[v.index].value=val
            fasteners.data[v.index].vector=(0,0,-10)
            vinyl=component=='window_receiver' or (component=='corner_posts' and s['siding']=='vinyl') or (component=='window' and s['window_update']=='vinyl' and role=='Trim' and max(c)>.4)
            for key,val in dict(Garage=float(component=='garage_panel'),Drive=float(component=='driveway'),Retaining=float(component=='retaining'),Paint=float(role=='Trim' and max(c)>.3 and component not in ('foyer','window_well')),Eave=float(component in ('drainage','eave_rake_soffit')),Flake=float(component=='paint_flakes'),Coping=float(component in ('opening_masonry','veneer_cap')),Vinyl=float(vinyl)).items():special[key].data[v.index].value=val
            col.data[v.index].color=(*c,1)
        me.calc_loop_triangles();total+=len(me.loop_triangles)
    for role,mat in mats.items():layer(mat,role,meta)
    meta.update(triangles=total,materials=len(used),stage='split source look-development checkpoint / causal materials / before bake',shared_addition_mib=2/3,shared_family_mib=49)
    out.parent.mkdir(parents=True,exist_ok=True);out.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()));print('SPLIT_SOURCE',meta['seed'],total)
    return meta
