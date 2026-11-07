"""Stock external PBR, physical UVs and placement-owned school aging.

The Commercial manufacture fields are baked by their original scripts. Only
cause-scale color is stored on this school's meshes. No new school image set,
photo-derived texel, runtime shader or duplicate canonical map is introduced.
"""
import math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from geometry import ROLES,ROOT
from kit.tiling import material

SPECS={'Siding':('CommercialCMU',ROOT/'commercial/textures/ship',2.4384),
       'Veneer':('CommercialBrick',ROOT/'commercial/textures/ship',1.2192),
       'Concrete':('CommercialConcrete',ROOT/'commercial/textures/ship',1.524),
       'Trim':('CommercialEquipment',ROOT/'commercial/textures/ship',2.0)}


def palette(p):
    from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
    get_settings_group();out={}
    for role,(name,folder,coverage) in SPECS.items():
        buff=role=='Veneer' and p['type'] in ('courtyard','compact')
        kind='buff' if p['type']=='courtyard' else 'tan'
        key='SchoolPBR_'+role+('_'+kind if buff else '')
        if buff:name='RanchBrick_'+kind;folder=ROOT/'houses/textures/ranch-ship'
        ma=bpy.data.materials.get(key)
        if not ma:ma=material(name,folder,tint=True);ma.name=key
        if role=='Siding':
            # Painted smooth block: retain the 8x16in joints through paint,
            # suppress the commercial split-face's exaggerated aggregate.
            next(n for n in ma.node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.23
        if role=='Trim' and not ma.get('school_light_mask'):
            # One 8px mask supplies all classroom lights without adding a
            # material or duplicating the existing manufacture atlas.
            from PIL import Image
            from io import BytesIO
            path=Path('textures/ship/T_School_Light_Emission.png');path.parent.mkdir(parents=True,exist_ok=True)
            mask=Image.new('RGB',(8,8));mask.putpixel((6,1),(255,246,224))
            encoded=BytesIO();mask.save(encoded,format='PNG');payload=encoded.getvalue()
            if not path.exists() or path.read_bytes()!=payload:path.write_bytes(payload)
            ns,ls=ma.node_tree.nodes,ma.node_tree.links
            tx=ns.new('ShaderNodeTexImage');tx.image=bpy.data.images.load(str(path.resolve()),check_existing=True);tx.interpolation='Closest'
            uv=ns.new('ShaderNodeUVMap');uv.uv_map='LightUV';ls.new(uv.outputs['UV'],tx.inputs['Vector'])
            bs=ns.get('Principled BSDF');ls.new(tx.outputs['Color'],bs.inputs['Emission Color']);bs.inputs['Emission Strength'].default_value=12
            ma['school_light_mask']=True
        out[role]=ma
    ma=bpy.data.materials.get('SchoolPBR_Shingles')
    if not ma:
        # The existing mineral bake has no low-frequency binder clouds. Its
        # aggregate, enlarged to 10mm grains, serves dark granular roof cover.
        # Reusing these same images adds no roof image allocation.
        ma=material('CommercialConcrete',ROOT/'commercial/textures/ship',tint=True);ma.name='SchoolPBR_Shingles'
        next(n for n in ma.node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=3
    out['Shingles']=ma
    glass=bpy.data.materials.get('SchoolPBR_Glass')
    if not glass:
        glass=bpy.data.materials.new('SchoolPBR_Glass');glass.use_nodes=True;glass['tiling_vertex_tint']=False
        pp=glass.node_tree.nodes.get('Principled BSDF');pp.inputs['Base Color'].default_value=(.94,.97,.96,1)
        pp.inputs['Transmission Weight'].default_value=1;pp.inputs['Roughness'].default_value=.018;pp.inputs['IOR'].default_value=1.52
    out['Glass']=glass;return out


def cut_age(ob):
    if ob.get('component')!='wall':return
    if '_Room_' in ob.name:return
    bm=bmesh.new();bm.from_mesh(ob.data)
    lo=[min(v.co[k] for v in bm.verts) for k in range(3)];hi=[max(v.co[k] for v in bm.verts) for k in range(3)]
    levels=[lo[2]+.08,lo[2]+.20,lo[2]+.42,lo[2]+.68,hi[2]-.25,hi[2]-.7,hi[2]-1.4,hi[2]-2.2]
    for axis in (2,0,1):
        cuts=levels if axis==2 else [lo[axis]+i*4.5 for i in range(1,math.ceil((hi[axis]-lo[axis])/4.5))]
        if axis==ob.get('runoff_axis',-1):cuts += [ob['runoff_station_m']+v for v in (-.65,-.33,-.12,0,.14,.35,.65)]
        for q in cuts:
            if not lo[axis]+.005<q<hi[axis]-.005:continue
            co=[0,0,0];co[axis]=q;n=[0,0,0];n[axis]=1
            bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],plane_co=co,plane_no=n,dist=1e-7)
    bm.to_mesh(ob.data);bm.free();ob.data.update()


def wall_weather(q,ob,p,role):
    x,y,z=q;name=ob.name;f=1.;salt=0.
    if ob.get('component')=='wall' and role in ('Veneer','Siding'):
        reach=.52+.10*math.sin(x*3.7+y*2.4)+.035*math.sin(x*14+y*9)
        splash=.48*max(0,1-max(0,z-.15)/reach)
        f-=splash
        b=next((b for b in p['blocks'] if '__'+b['id']+'_' in name),None)
        if b:
            # Damp mortar and sill-end tracks stay below the actual openings.
            for o in b['openings']:
                if o['type']!='window':continue
                rad=math.radians(o['yaw']);u=(x-o['origin'][0])*math.cos(rad)+(y-o['origin'][1])*math.sin(rad)
                inward=-(x-o['origin'][0])*math.sin(rad)+(y-o['origin'][1])*math.cos(rad)
                fall=o['z']+.1524-z
                if abs(inward)<.035 and 0<fall<1.1:
                    ends=min(abs(u-o['u']-o['w']/2),abs(u-o['u']+o['w']/2))
                    f-=.22*math.exp(-(ends/.24)**2)*math.exp(-fall/.75)
            for face,org,yaw,length in __import__('plans').sides(b):
                if '_'+face not in name:continue
                rad=math.radians(yaw);u=(x-org[0])*math.cos(rad)+(y-org[1])*math.sin(rad)
                top=b['roof'];fall=max(0,top-z)
                for aa,bb in __import__('plans').visible_intervals(b,face,p['blocks']):
                    if bb-aa<5:continue
                    station=__import__('plans').drain_station(b,face,aa,bb)
                    if station is None:continue
                    d=abs(u-station);broken=.65+.35*math.sin(z*7+u*19)**2
                    f-=.58*math.exp(-(d/(.20+.08*fall))**2)*math.exp(-fall/3.8)*broken
                    salt+=.30*math.exp(-((u-station-.24)/.52)**2)*math.exp(-((fall-1.6)/1.1)**2)*broken
                seam=abs((u+.25)%3.048-.25)
                f-=.12*math.exp(-(seam/.10)**2)*math.exp(-fall/.5)
    if ob.get('component')=='covered_walk' and role=='Trim' and z<.46:
        f*=.70+.30*min(1,max(0,z-.15)/.25)
    return max(.22,f),salt


def apply(p):
    mats=palette(p);bpy.context.view_layer.update();count=0
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or ob.get('asset_set')!='School' or ob.get('school_pbr'):continue
        if not any(ma and ma.name.startswith('SchoolForm_') for ma in ob.data.materials):continue
        cut_age(ob);me=ob.data
        # Project the actual shipping triangles, including twisted tube quads,
        # so an averaged quad normal cannot collapse one triangle's UV area.
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
        old=me.color_attributes.get('Tint');original=[tuple(c.color[:3]) for c in old.data]
        roles=[ma.name.removeprefix('SchoolForm_').split('.')[0] if ma else 'Trim' for ma in me.materials]
        # CORNER tint lets mortar walls, steel hardware and glass share a
        # geometric vertex without borrowing each other's material color.
        me.color_attributes.remove(old);attr=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=attr
        uv=me.uv_layers.active or me.uv_layers.new(name='UVMap')
        light_uv=me.uv_layers.get('LightUV') or me.uv_layers.new(name='LightUV')
        for row in light_uv.data:row.uv=(.8125,.8125) if ob.get('interior_lamp') else (.0625,.0625)
        coords=[ob.matrix_world@v.co for v in me.vertices]
        ma_roles=[]
        for face in me.polygons:
            role=roles[face.material_index];ma_roles.append(role)
            normal=ob.matrix_world.to_3x3()@face.normal;axis=max(range(3),key=lambda k:abs(normal[k]));axes=[(1,2),(0,2),(0,1)][axis]
            sign=-1 if (axis==0 and normal.x<0) or (axis==1 and normal.y>0) or (axis==2 and normal.z<0) else 1
            pp=[coords[i] for i in face.vertices];bounds=[(min(q[a] for q in pp),max(q[a] for q in pp)) for a in axes]
            for li in face.loop_indices:
                i=me.loops[li].vertex_index;q=coords[i];c=original[i];factor,salt=wall_weather(q,ob,p,role)
                coverage=SPECS.get(role,(None,None,1))[2]
                if role=='Trim':
                    metal=max(c)-min(c)<.055 and .18<sum(c)/3<.55
                    cell=ob.get('trim_cell',2 if metal else 4);ref=(.075,.043,.020) if cell==10 else (.46,.49,.50) if metal else (.86,.86,.83)
                    col=tuple(min(1.5,c[k]/ref[k])*factor for k in range(3))
                    row,cc=divmod(cell,4);g=10/2048
                    uu,vv=[(q[a]-lo)/max(hi-lo,1e-7) for a,(lo,hi) in zip(axes,bounds)]
                    uv.data[li].uv=(cc/4+g+uu*(.25-2*g),row/8+g+vv*(.125-2*g))
                    if ob.get('component')=='covered_walk' and q.z<.38 and not metal:
                        rust=max(0,1-(q.z-.17)/.20)*(.65+.35*math.sin(q.x*77+q.y*39)**2)
                        col=tuple(v*(1-.60*rust)+r*.60*rust for v,r in zip(col,(.22,.065,.015)))
                elif role=='Glass':col=(1,1,1);uv.data[li].uv=(q[axes[0]],q[axes[1]])
                else:
                    if role=='Veneer':ref=(.39/.72,.28/.72,.17/.72) if p['type']=='courtyard' else (.29/.72,.205/.72,.135/.72) if p['type']=='compact' else (.29,.075,.034)
                    elif role=='Siding':ref=(.278,.281,.270)
                    elif role=='Concrete':ref=(.39,.39,.38)
                    else:ref=(.39,.39,.38);coverage=4.8768
                    col=tuple(min(1.7,c[k]/ref[k])*factor for k in range(3))
                    col=tuple(v*(1-salt)+s*salt for v,s in zip(col,(1.18,1.15,1.02)))
                    uv.data[li].uv=(sign*q[axes[0]]/coverage,q[axes[1]]/coverage)
                attr.data[li].color=(*col,1)
        me.materials.clear()
        for r in ROLES:me.materials.append(mats[r])
        for face,role in zip(me.polygons,ma_roles):face.material_index=ROLES.index(role)
        ob['school_pbr']=True;count+=1
    print('SCHOOL SURFACES',p['seed'],count,flush=True)
