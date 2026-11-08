"""Shared baked manufacture, metric UVs and cause-scale placement colors."""
import json,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from kit import tiling
from textures import RECTS,COVERAGE

ROOT=Path(__file__).resolve().parents[2]


def house_folder(prefix):
    for folder in (ROOT/'houses/textures/ship',ROOT/'trailer-park/build/library/houses/textures/ship'):
        if all((folder/f'T_{prefix}_{ch}.png').is_file() for ch in ('BaseColor','Normal','ORM')):return folder
    raise FileNotFoundError(f'Missing native {prefix} maps; run make model to prepare read-only inputs')


def palette():
    from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
    get_settings_group();out={}
    for role,key,folder in [('Metal','Manufactured',Path('textures/ship')),
                            ('Siding','HouseSiding',house_folder('HouseSiding')),
                            ('Shingles','HouseShingles',house_folder('HouseShingles')),
                            ('Wood','HouseTrim',house_folder('HouseTrim'))]:
        name='ManufacturedPBR_'+role;ma=bpy.data.materials.get(name)
        if not ma:ma=tiling.material(key,folder,tint=True);ma.name=name
        out[role]=ma
    name='ManufacturedPBR_Glass';ma=bpy.data.materials.get(name)
    if not ma:
        ma=tiling.material('HouseTrim',house_folder('HouseTrim'),tint=True);ma.name=name
        bs=ma.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.52
        ma.use_backface_culling=False
    out['Glass']=ma;return out


def home_spec(ob):
    q=ob
    while q:
        if q.get('home_spec'):return json.loads(q['home_spec'])
        if q.get('weather_spec'):return json.loads(q['weather_spec'])
        q=q.parent
    return {}


def cut(ob,p):
    component=ob.get('component');bm=bmesh.new();bm.from_mesh(ob.data)
    if component not in ('wall','skirting','roof','carport','carport_posts'):
        bm.free();return
    lo=[min(v.co[k] for v in bm.verts) for k in range(3)];hi=[max(v.co[k] for v in bm.verts) for k in range(3)]
    F,E=p.get('floor',.91),p.get('eave',3.35)
    for axis in range(3):
        if component in ('carport','carport_posts') and axis!=2:continue
        if component=='roof' and axis==2:continue
        if axis==2:
            levels=[F+.25,E-.4,E-.10,F+2.4384]
            if component=='skirting':levels=[.12,.25,.43,.67] if p.get('era')!='1996' else [.28]
            if component in ('carport','carport_posts'):levels=[.10,.20,.32,.45]
        else:
            cov=2.4384 if component in ('wall','skirting','roof') else 1.2192
            levels=[i*cov for i in range(math.floor(lo[axis]/cov),math.ceil(hi[axis]/cov)+1)]
            if component=='wall' and hi[axis]-lo[axis]>2:
                levels += [lo[axis]+j*1.2192 for j in range(1,math.ceil((hi[axis]-lo[axis])/1.2192))]
                if axis==0 and p.get('era')!='1996':
                    L=p.get('length',18)
                    stride=L/math.ceil(L/.9144)
                    step=max(1,math.ceil(math.ceil(L/.9144)/4))
                    levels += [-L/2+j*stride+off for j in range(0,math.ceil(L/.9144),step) for off in (-.045,0,.045)]
                    levels += [L*station+off for station in (-.27,.19) for off in (-.35,0,.35)]
                if axis==1 and p.get('era')!='1996':
                    levels += [p.get('width',4.2)*station+off for station in (-.37,.37) for off in (-.15,0,.15)]
        for value in sorted(set(levels)):
            if not lo[axis]+.002<value<hi[axis]-.002:continue
            co=[0,0,0];co[axis]=value;n=[0,0,0];n[axis]=1
            bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],plane_co=co,plane_no=n,dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm,edges=bm.edges[:],dist=1e-7)
    if component=='wall' and p.get('era')=='1972' and p.get('upkeep')!='kept':
        direction=-1 if 'Wall_front' in ob.name else 1 if 'Wall_back' in ob.name else 0
        if direction:
            for v in bm.verts:
                for station in (-.27,.19):
                    dent=.012*math.exp(-((v.co.x-p['length']*station)/.40)**2-((v.co.z-F-1.1)/.36)**2)
                    v.co.y-=direction*dent
    bm.to_mesh(ob.data);bm.free();ob.data.update()


def age(q,n,c,role,component,p,seed):
    x,y,z=q;E=p.get('eave',3.35);F=p.get('floor',.91)
    old=p.get('era','1972')!='1996'
    upkeep=p.get('upkeep',('patched','kept','faded')[seed%3])
    severity=({'patched':1.,'kept':.38,'faded':.88} if old else {'patched':.40,'kept':.13,'faded':.28})[upkeep]
    north=max(0,n.y*(1 if p.get('site_yaw',0)==0 else -1));sunny=max(0,-n.y*(1 if p.get('site_yaw',0)==0 else -1))
    color=Vector(c[:3]);ripple=.5+.3*math.sin(x*6.3+y*3.1+seed)+.2*math.sin(x*17-y*11)
    if role=='Shingles':color/= .105
    if role=='Siding' and component in ('wall','roof_trim','era_details','added_room'):
        # UV-scale manufacture supplies ribs; these broad masks follow exposure.
        exposure=max(sunny,.65*abs(n.x))
        fade=severity*exposure*.43*max(0,min(1,(z-F)/1.4))
        color=color.lerp(Vector((.53,.51,.43)),fade)
        wet=severity*(north*.60+(.17 if old else 0))*math.exp(-((z-(E-.22))/.38)**2)*(.22+.78*ripple)
        color*=1-wet;color.y*=1+wet*.17;color.z*=1-wet*.14
        # Roof lap runoff follows real 914.4mm seams, fades down under gravity.
        L=p.get('length',18);stride=L/math.ceil(L/.9144)
        step=max(1,math.ceil(math.ceil(L/.9144)/4))
        seam=min(abs(x-(-L/2+j*stride)) for j in range(0,math.ceil(L/.9144),step))
        if abs(n.x)>.5:seam=min(abs(y-p.get('width',4.2)*station) for station in (-.37,.37))
        rust=severity*.85*math.exp(-(seam/.115)**2)*math.exp(-max(0,E-z)/.95)
        if old and max(abs(n.x),abs(n.y))>.5:color=color.lerp(Vector((.18,.058,.016)),rust)
    if component=='roof' and old and p.get('roof')!='shingle' and max(c[:3])<.30:
        L=p.get('length',18);stride=L/math.ceil(L/.9144)
        seam=abs((x+L/2+stride/2)%stride-stride/2)
        oxide=severity*.65*math.exp(-(seam/.035)**2)*(.35+.65*math.sin(y*1.3+seed)**2)
        color=color.lerp(Vector((.22,.075,.022)),oxide)
    if component in ('skirting','skirt_access'):
        color=Vector((.62,.61,.55)).lerp(Vector((.40,.39,.32)),severity*.36)
        splash=.20+.18*(.5+.5*math.sin(x*2.1+y*2.8+seed))**2
        soil=severity*.94*math.exp(-max(0,z-.04)/splash)*(.35+.65*ripple)
        color=color.lerp(Vector((.075,.067,.033)),soil)
        damp=severity*north*.44*(.5+.5*math.sin(x*1.9+seed))**2
        color=color.lerp(Vector((.09,.12,.055)),damp)
    if component=='window_detail' and old and max(c[:3])-min(c[:3])>.04:
        color=color.lerp(Vector((.37,.37,.29)),severity*.48)
    if component=='carport_posts' and z<.43:
        rust=severity*.93*math.exp(-max(0,z-.08)/.20)*(.65+.35*ripple)
        color=color.lerp(Vector((.22,.065,.018)),rust)
    if role=='Veneer':
        # Seasoned exposed timber: gray fibers, darker protected underside.
        if component=='deck':
            gray=Vector((.16,.155,.13))*(.80+.30*(.5+.5*math.sin(y*41+seed)))
            color=color.lerp(gray,.58+.30*severity if old else .20+.50*severity)
        if z<.20:color*=.62+.38*max(0,z)/.20
    return tuple(max(.004,min(.95,v)) for v in color)


def finish(ob):
    bpy.context.view_layer.update()
    p=home_spec(ob);component=ob.get('component','');seed=p.get('seed',ob.get('look_seed',19))
    oldroles=[ma.name.replace('ManufacturedForm_','').split('.')[0] for ma in ob.data.materials]
    if not all(role in ('Siding','Shingles','Veneer','Concrete','Trim','Glass') for role in oldroles):return
    cut(ob,p);me=ob.data;mats=palette();old=me.color_attributes.get('Tint')
    values=[tuple(v.color) for v in old.data] if old else [(1,1,1,1)]*len(me.vertices)
    if old:me.color_attributes.remove(old)
    attr=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=attr
    uv=me.uv_layers.active
    indices=[poly.material_index for poly in me.polygons]
    names=list(mats);me.materials.clear()
    for name in names:me.materials.append(mats[name])
    coords=[ob.matrix_world@v.co for v in me.vertices]
    for poly,source_index in zip(me.polygons,indices):
        role=oldroles[source_index];cell=None;family='Metal';n=(ob.matrix_world.to_3x3()@poly.normal).normalized()
        axes=[k for k in range(3) if k!=max(range(3),key=lambda k:abs(n[k]))]
        if role=='Siding':
            if p.get('siding')=='ribbed' and p.get('era')!='1996':cell='Ribbed'
            else:family='Siding'
        elif role=='Shingles':family='Shingles'
        elif role=='Veneer':family='Wood'
        elif role=='Glass':family='Glass'
        elif role=='Concrete':cell='Pier'
        elif component in ('skirting','skirt_access'):cell='Skirt'
        elif component=='chassis':cell='Steel'
        elif component=='roof':cell='Roof'
        elif component=='carport':cell='Zinc'
        elif component in ('roof_trim','openings','window_detail','utilities','dish'):
            c=values[poly.vertices[0]];cell='Zinc' if .36<max(c[:3])<.58 and max(c[:3])-min(c[:3])<.06 else 'Plain'
        else:cell='Plain'
        poly.material_index=names.index(family)
        points=[coords[i] for i in poly.vertices]
        # Siding always runs horizontal U / vertical V; gable end matches it.
        if role=='Siding' and abs(n.z)<.6:axes=[0 if abs(n.y)>.5 else 1,2]
        if family in ('Wood','Glass'):
            axes.sort(key=lambda k:max(q[k] for q in points)-min(q[k] for q in points),reverse=True)
            strip=3 if family=='Wood' else 6
        if cell:
            u0,v0,u1,v1=RECTS[cell];guard=3/2048
            cu=(u1-u0)*COVERAGE;cv=(v1-v0)*COVERAGE
            origins=[0.,p.get('floor',.91) if axes[1]==2 and cell=='Ribbed' else 0.]
            intervals=[(min(q[k] for q in points)-origins[j],max(q[k] for q in points)-origins[j]) for j,k in enumerate(axes)]
            tile=[math.floor((lo+hi)/2/cov) for (lo,hi),cov in zip(intervals,(cu,cv))]
        for li in poly.loop_indices:
            vi=me.loops[li].vertex_index;q=coords[vi];color=values[vi]
            attr.data[li].color=(*age(q,n,color,role,component,p,seed),1)
            if cell:
                fractions=[(q[k]-origins[j])/cov-tile[j] for j,(k,cov) in enumerate(zip(axes,(cu,cv)))]
                # Long extrusions use bounded finish swatches; tiled skins
                # were cut at physical repeat stations before this mapping.
                for j,((lo,hi),cov) in enumerate(zip(intervals,(cu,cv))):
                    if lo/cov<tile[j]-1e-5 or hi/cov>tile[j]+1+1e-5:fractions[j]=(q[axes[j]]-origins[j]-lo)/max(hi-lo,1e-6)
                uu,vv=[max(0,min(1,t)) for t in fractions]
                uv.data[li].uv=(u0+guard+uu*(u1-u0-2*guard),v0+guard+vv*(v1-v0-2*guard))
            elif family in ('Wood','Glass'):
                # Native timber fibers run along V; U varies across grain.
                # Keep real cross-member scale, stretch only along the fiber.
                cross,long=(axes[1],axes[0]) if family=='Wood' else (axes[0],axes[1])
                lo=min(q[long] for q in points);hi=max(q[long] for q in points)
                uv.data[li].uv=(q[cross]/4.8768,(strip+.05+.90*(q[long]-lo)/max(hi-lo,.01))/8)
            else:
                cov=4.8768 if family=='Shingles' else 2.4384
                uv.data[li].uv=(q[axes[0]]/cov,q[axes[1]]/cov)
    ob['lookdev']='baked manufacture + causal corner color';ob['uv_reuse']='intentional metric tiles and guarded finish cells'
