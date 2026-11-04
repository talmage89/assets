"""Quick shared source finishes for the form gate; never publishes maps.

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
from ranch_lookdev import roof_material, brick_maps
from cape_profile import courses
from kit import tiling


def age(mat,role,meta):
    ns,ls=mat.node_tree.nodes,mat.node_tree.links;p=ns.get('Principled BSDF')
    if role=='Glass':
        for socket in ('Base Color','Roughness'):
            for link in list(p.inputs[socket].links):ls.remove(link)
        p.inputs['Base Color'].default_value=(.95,.97,.95,1);p.inputs['Roughness'].default_value=.035
        return
    def op(kind,a,b=None):
        n=ns.new('ShaderNodeMath');n.operation=kind
        if hasattr(a,'node'):ls.new(a,n.inputs[0])
        else:n.inputs[0].default_value=a
        if b is not None:
            if hasattr(b,'node'):ls.new(b,n.inputs[1])
            else:n.inputs[1].default_value=b
        return n.outputs[0]
    def sep(name):
        a=ns.new('ShaderNodeAttribute');a.attribute_name=name
        n=ns.new('ShaderNodeSeparateXYZ');ls.new(a.outputs['Vector'],n.inputs[0]);return n.outputs
    xyz=sep('SplitRest');context=sep('SplitWeather');x,y,z=xyz['X'],xyz['Y'],xyz['Z']
    noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=2.5
    a=ns.new('ShaderNodeAttribute');a.attribute_name='SplitRest';ls.new(a.outputs['Vector'],noise.inputs['Vector'])
    low=op('MAXIMUM',0,op('SUBTRACT',1,op('DIVIDE',op('SUBTRACT',z,context['X']),.42)))
    low=op('MINIMUM',1,low)
    # Irregular lower deposits use a height envelope, never a whole-wall wash.
    dirt=op('MULTIPLY',low,op('MULTIPLY_ADD',noise.outputs['Fac'],.50))
    wet=op('MAXIMUM',context['Y'],op('MULTIPLY',context['Z'],.45))
    if role=='Shingles':
        coord=ns.new('ShaderNodeCombineXYZ');ls.new(op('MULTIPLY',x,2.6),coord.inputs[0]);ls.new(op('MULTIPLY',y,.24),coord.inputs[1]);ls.new(op('MULTIPLY',z,.2),coord.inputs[2])
        ls.new(coord.outputs[0],noise.inputs['Vector']);noise.inputs['Scale'].default_value=3.2
        dirt=op('MULTIPLY',context['Z'],op('MULTIPLY',noise.outputs['Fac'],.62 if meta['spec']['roof_age']=='tired' else .12))
    elif role=='Trim':dirt=op('MULTIPLY',low,.16)
    else:dirt=op('MULTIPLY',dirt,.25 if role=='Siding' else .33)
    damp=op('MULTIPLY',wet,.17 if role in ('Siding','Veneer') else .08)
    factor=op('MINIMUM',.62,op('ADD',dirt,damp))
    original=p.inputs['Base Color'].links[0].from_socket
    mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';ls.new(factor,mix.inputs[0]);ls.new(original,mix.inputs[1]);mix.inputs[2].default_value=(.43,.47,.37,1)
    ls.new(mix.outputs[0],p.inputs['Base Color'])
    rough=p.inputs['Roughness'];old=rough.links[0].from_socket if rough.is_linked else rough.default_value
    ls.new(op('MINIMUM',.98,op('ADD',old,op('MULTIPLY',factor,.10))),rough)


def lap_siding_only(ob,skin,meta):
    """Keep masonry on its original plane while sweeping only lap surfaces."""
    if ob.get('component')!='wall' or skin not in ('wood','vinyl','aluminum'):return
    me=ob.data
    # Cape's profile sweep assumes a single wall finish. Use disconnected
    # material subsets to preserve the lower brick/upper siding floor break.
    bm=bmesh.new();bm.from_mesh(me)
    siding=next(i for i,m in enumerate(me.materials) if m.name=='House_Siding')
    non=[f for f in bm.faces if f.material_index!=siding]
    if not non:bm.free();courses(ob,skin,meta);return
    copy=bm.copy();bmesh.ops.delete(bm,geom=non,context='FACES')
    bmesh.ops.delete(copy,geom=[f for f in copy.faces if f.material_index==siding],context='FACES')
    bm.to_mesh(me);bm.free();me.update();courses(ob,skin,meta)
    base=ob.data;join=bmesh.new();join.from_mesh(base)
    extra=bpy.data.meshes.new('Temporary masonry');copy.to_mesh(extra);copy.free();join.from_mesh(extra);join.to_mesh(base);join.free();bpy.data.meshes.remove(extra);base.update()


def prepare(source,out):
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));meta=json.loads(source.with_suffix('.json').read_text());s=meta['spec']
    mats=materials(Path('textures/source'))
    folder=Path('build/split/materials')
    mats['Shingles']=roof_material(folder/'roof',s['roof_age'])
    brick_maps(folder/'brick'/s['brick_color'],s['brick_color'])
    mats['Veneer']=tiling.material('RanchBrick',folder/'brick'/s['brick_color'],tint=True)
    from cape_masonry import dielectric,author
    masonry=folder/'masonry';author(masonry)
    mats['Concrete']=dielectric('CapeConcrete',masonry)
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
        weather=me.attributes.new(name='SplitWeather',type='FLOAT_VECTOR',domain='POINT')
        vertex_roles={};normals={};component=ob.get('component')
        opening=next((o for o in meta['openings'] if ob.name.startswith(o['id'])),None)
        block=next((b for b in meta['blocks'] if b['name']==ob.get('block',opening['block'] if opening else 'Main')),meta['blocks'][0])
        for poly in me.polygons:
            role=roles[poly.material_index];used.add(role);n=(ob.matrix_world.to_3x3()@poly.normal).normalized()
            pts=[world[i] for i in poly.vertices];axis=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=axis]
            if role=='Trim':axes.sort(key=lambda k:max(p[k] for p in pts)-min(p[k] for p in pts),reverse=True)
            lo=min(p[axes[1]] for p in pts);hi=max(p[axes[1]] for p in pts)
            strip=6 if role=='Glass' else 2 if component=='eave_rake_soffit' and n.z<-.6 else 5 if component in ('flashing','roof_vent','storm_window') else 0
            for i in poly.vertices:vertex_roles[i]=role;normals[i]=n
            for li in poly.loop_indices:
                p=world[me.loops[li].vertex_index]
                if role in ('Trim','Glass') or (role=='Siding' and s['siding'] in ('battens','grooved')):
                    uv.data[li].uv=(p[axes[0]]/4,(strip+.04+.90*(p[axes[1]]-lo)/max(.5,hi-lo))/8)
                elif role=='Shingles' and abs(n.z)>.3:
                    coord=(p.x,p.y/abs(n.z)) if abs(n.y)>=abs(n.x) else (p.y,p.x/abs(n.z));uv.data[li].uv=(coord[0]/4.8768,coord[1]/2.4384)
                elif role=='Siding':uv.data[li].uv=(p[axes[0]]/2.4384,-p[axes[1]]/2.4384)
                elif role=='Veneer':
                    if component=='opening_masonry':
                        index=min(poly.vertices)//8;unit=world[index*8:index*8+8]
                        aa=sorted(axes,key=lambda k:max(v[k] for v in unit)-min(v[k] for v in unit),reverse=True)
                        low=[min(v[k] for v in unit) for k in aa];span=[max(v[k] for v in unit)-low[j] for j,k in enumerate(aa)]
                        uv.data[li].uv=((index%6-.5*((index//6)%2)+.15+.70*(p[aa[0]]-low[0])/max(span[0],1e-6))/6,((index//6)%18+.24+.52*(p[aa[1]]-low[1])/max(span[1],1e-6))/18)
                    else:uv.data[li].uv=(p[axes[0]]/1.2192,p[axes[1]]/1.2192)
                else:uv.data[li].uv=(p[axes[0]]/1.2192,(p[axes[1]]+.3048)/1.2192)
        for v in me.vertices:
            role=vertex_roles[v.index];p=world[v.index];n=normals[v.index];c=Vector(col.data[v.index].color[:3])
            if role=='Veneer':c=Vector((.72,.72,.72))
            elif role=='Concrete':c=Vector((.82,.83,.83))
            elif role=='Glass':c=Vector((1,1,1))
            elif role=='Shingles':c=Vector(dict(warm_charcoal=(.63,.63,.59),weathered_wood=(.77,.67,.53),dark_brown=(.63,.49,.35))[s['shingle_color']])
            if role=='Trim' and component in ('drainage','garage_panel','porch_steps','rear_landing'):
                context_meta={**meta,'blocks':[block,block],'porch':meta['porch'] or {'y0':meta['blocks'][0]['y0']-1.02}}
                sample=p.copy();weather_component=component
                if component=='garage_panel':
                    sample.z=p.z-block['floor']+.1016;weather_component='garage_door'
                factor,_,_=shared_weather(sample,n,role,weather_component,context_meta,block['name'],ob.get('face'))
                c=Vector(tuple(c[k]*factor[k] for k in range(3)))
            if component=='driveway':
                # Original concrete drive: tire tracks and oil in the parked
                # engine zone, attenuated off the garage / parking centerline.
                d=meta['driveway'];off=p.x-d['x'];track=max(math.exp(-((off-.76)/.16)**2),math.exp(-((off+.76)/.16)**2))
                park=math.exp(-((p.y-(d['back']-2.6))/1.6)**2);oil=math.exp(-(off/.40)**2)*park
                c*=1-.10*track-.30*oil
            col.data[v.index].color=(*c,1);rest.data[v.index].vector=p
            wet=0
            for d in meta['drains']:
                q=d['centerline'][3];wet=max(wet,math.exp(-((p.x-q[0])**2+(p.y-q[1])**2)/.08)*min(1,max(0,(q[2]-p.z)/.3)))
            low=max(0,block['floor']-.0762) if role=='Siding' else 0
            weather.data[v.index].vector=(low,wet,max(0,n.y) if role=='Shingles' else max(0,n.y)*max(0,1-p.z/1.1))
        me.calc_loop_triangles();total+=len(me.loop_triangles)
    for role,mat in mats.items():age(mat,role,meta)
    meta.update(triangles=total,materials=len(used),stage='split form checkpoint / quick shared finishes / before bake',shared_addition_mib=0,shared_family_mib=48+1/3)
    out.parent.mkdir(parents=True,exist_ok=True);out.with_suffix('.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()));print('SPLIT_SOURCE',meta['seed'],total)
    return meta
