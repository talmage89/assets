"""Nine strip materials, using the gas station's unaltered shipping maps.

One strip ink/coverage/radiance material replaces gas graphics; no interior
atlas. Only the mansard variant loads the houses' existing shingle material.
"""
import json,math,random
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Vector
from surfaces import pbr,charts,tint_layer
from textures import CELLS,SETS
from paving import cut,ground_field

TIRE_DARKEN=.65


def emission_chart(ob,layout,lit=False):
    uv=ob.data.uv_layers.active
    em=ob.data.uv_layers.get('EmissionUV') or ob.data.uv_layers.new(name='EmissionUV')
    a,b,c,d=layout['Blank']['sign'];off=((a+c)/2,(b+d)/2)
    for li in range(len(ob.data.loops)):em.data[li].uv=uv.data[li].uv if lit else off
    ob.data.uv_layers.active=uv


def overlay_chart(ob,rect):
    uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='UVMap');uv.name='UVMap'
    a,b,c,d=rect;coords=[v.co for v in ob.data.vertices]
    for poly in ob.data.polygons:
        axis=max(range(3),key=lambda k:abs(poly.normal[k]));axes=[(1,2),(0,2),(0,1)][axis]
        bounds=[(min(v[k] for v in coords),max(v[k] for v in coords)) for k in axes]
        for li in poly.loop_indices:
            i=ob.data.loops[li].vertex_index
            if ob.get('swept_wear'):u=i%2;v=(i//2)/(len(coords)//2-1)
            else:u,v=[(coords[i][k]-lo)/max(hi-lo,1e-8) for k,(lo,hi) in zip(axes,bounds)]
            if ob.get('wear_flip'):u=1-u
            uv.data[li].uv=(a+u*(c-a),b+v*(d-b))


def orient_sheet(ob):
    if ob.get('solid') or not ob.data.polygons:return
    coords=[v.co for v in ob.data.vertices]
    horizontal=max(v.z for v in coords)-min(v.z for v in coords)<1e-6
    vertical=(ob.get('graphic') or ob.get('wear_cell')) and max(v.y for v in coords)-min(v.y for v in coords)<1e-6
    for poly in ob.data.polygons:
        flip=(horizontal and poly.normal.z<0) or (vertical and poly.normal.y>0)
        if not flip:continue
        # Preserve chart corners by vertex identity when reversing winding.
        values={uv.name:{ob.data.loops[li].vertex_index:tuple(uv.data[li].uv) for li in poly.loop_indices} for uv in ob.data.uv_layers}
        poly.flip()
        for uv in ob.data.uv_layers:
            for li in poly.loop_indices:uv.data[li].uv=values[uv.name][ob.data.loops[li].vertex_index]
    ob.data.update()


def wall_cuts(ob,top):
    # Just the few height stations required for base damp and coping wash.
    # Fine streaks already live in shared alpha charts, rather than dense mesh.
    if max(ob.dimensions.x,ob.dimensions.y)<1 or ob.dimensions.z<1:return
    bm=bmesh.new();bm.from_mesh(ob.data);inv=ob.matrix_world.inverted()
    for z in (.18,.40,.68,top-.68,top-.18):
        pt=inv@Vector((0,0,z));no=ob.matrix_world.to_3x3().transposed()@Vector((0,0,1))
        bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=pt,plane_no=no)
    bm.to_mesh(ob.data);bm.free();ob.data.update()


def pavement(ob,p,role):
    # Grid only the actual flat site skins; cabinets and curb bevels keep their
    # modest original topology. The existing grid resolves lane/edge macro values.
    if ob.name.startswith(('Lot asphalt','Repaired utility')):cut(ob,1.1)
    me=ob.data;attr=me.color_attributes.get('Tint') or me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=attr
    W,D=p['lot'];field,mean=ground_field();b=p['building']
    # Strip-only darker wearing course; shared Ground/gas images stay exact.
    # Partial compensation retains mineral mottling rather than flattening it.
    for poly in me.polygons:
        center=ob.matrix_world@poly.center
        slab=random.Random(p['seed']*117+math.floor(center.x/3.048)*71+math.floor(center.y/3.048)*37).uniform(.95,1.025)
        for li in poly.loop_indices:
            q=ob.matrix_world@me.vertices[me.loops[li].vertex_index].co;x,y,z=q
            if role=='Asphalt':
                sample=field[int((1-y/6.096%1)*127)%128,int((x/6.096%1)*128)%128];comp=1+.20*(np.clip(mean/np.maximum(sample,.001),.74,1.36)-1)
                edge=min(W/2-abs(x),D/2-abs(y));factor=.45+.06*math.exp(-max(0,edge)/1.4)
                travel=min(abs(y-ay-lane*1.45-wheel*.78) for ay in (*p['aisle_centers'],sum(p['rear_drive'])/2) for lane in (-1,1) for wheel in (-1,1))
                travel=min(travel,*[abs(x-xx-lane*1.45-wheel*.78) for xx in p['side_drive_centers'] for lane in (-1,1) for wheel in (-1,1)])
                travel=min(travel,*[math.hypot(x-a,y-b) for a,b in p['pavement_entry_paths']])
                factor*=1-TIRE_DARKEN*math.exp(-(travel/.80)**2)
                parked=max((strength*math.exp(-(((x-cx)*co+(y-cy)*sn)/sx)**2-((-(x-cx)*sn+(y-cy)*co)/sy)**2) for cx,cy,sx,sy,co,sn,strength in p['pavement_stain_sites']),default=0)
                factor*=1-.88*parked
                if ob.get('repair'):factor*=.24
                if ob.get('asphalt_seal'):factor=.045
                rgb=np.minimum(comp*factor*np.array((1.0,.98,.94)),1)
            else:
                factor=slab
                if 'walk' in ob.name.lower():
                    # Tracked grit concentrates by storefronts and along the
                    # open edge; it never tints the entire concrete slab tan.
                    dist=abs(y-b['front']);factor*=1-.08*math.exp(-(dist/.25)**2)
                rgb=(factor,factor*.999,factor*.99)
            attr.data[li].color=(*rgb,1)


def interior_contacts(p):
    from check import surface,ray
    floors={o.parent:o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('room_floor')};trees={rt:surface([ob]) for rt,ob in floors.items()};rows=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.get('floor_support'):continue
        owner=ob.parent
        while owner and owner not in floors:owner=owner.parent
        assert owner,('No tenant floor for support',ob.name)
        q=[ob.matrix_world@v.co for v in ob.data.vertices];bottom=min(v.z for v in q);x=sum(v.x for v in q)/len(q);y=sum(v.y for v in q)/len(q)
        hit=ray(trees[owner],(x,y,bottom+.05),(0,0,-1));gap=bottom-hit[2]
        assert abs(gap)<.0021,('Unsupported furnishing',ob.name,gap)
        rows.append(dict(part=ob.name,module=owner.name,lowest_surface_z_m=bottom,floor_surface_z_m=hit[2],measured_gap_m=gap))
    p['interior_support_contacts']=rows


def apply(p,ink,layout):
    from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
    get_settings_group();style=p['building']['wall'];wallkey='Brick' if style=='brick' else 'EIFS' if style=='eifs' else 'CMU'
    mats={key:pbr('Commercial'+key,pair=SETS[key][2]==2) for key in (wallkey,'Concrete','Roof','Equipment')}
    if style=='smooth_cmu':next(n for n in mats[wallkey].node_tree.nodes if n.type=='NORMAL_MAP').inputs['Strength'].default_value=.20
    for key in ('Asphalt','Lawn'):mats[key]=pbr(key,Path('../ground/textures/ship'))
    # The shared road's roughness (~.79) washes out deposits at a walking eye.
    # Keep its exact color/normal/AO maps; this dry, porous strip course uses
    # stock glTF scalar roughness, without allocating a duplicate image.
    asphalt=mats['Asphalt'];shader=asphalt.node_tree.nodes.get('Principled BSDF')
    for key,value in (('Roughness',.96),('Metallic',0)):
        for link in list(shader.inputs[key].links):asphalt.node_tree.links.remove(link)
        shader.inputs[key].default_value=value
    if p['style']=='mansard':mats['Shingles']=pbr('HouseShingles',Path('../houses/textures/ship'))
    glass=bpy.data.materials.new('CommercialGlass');glass.use_nodes=True;glass['tiling_vertex_tint']=False
    pp=glass.node_tree.nodes.get('Principled BSDF');pp.inputs['Base Color'].default_value=(.94,.97,.96,1);pp.inputs['Transmission Weight'].default_value=1;pp.inputs['IOR'].default_value=1.52;pp.inputs['Roughness'].default_value=.025
    mats['Glass']=glass;mats['Graphics']=ink;rows={};b=p['building'];bpy.context.view_layer.update()
    # Apply manufacture bevels once, before sampling and consolidation.
    dg=bpy.context.evaluated_depsgraph_get();objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
    evaluated=[(o,bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg,preserve_all_data_layers=True)) for o in objects]
    for ob,me in evaluated:ob.data=me;ob.modifiers.clear();orient_sheet(ob)
    for ob in objects:
        name=ob.name;role=ob.data.materials[0].name.removeprefix('Form_').split('.')[0]
        if ob.get('wear_cell'):
            ob.data.materials.clear();ob.data.materials.append(ink);overlay_chart(ob,layout['Wear:'+ob['wear_cell']]['sign']);emission_chart(ob,layout);continue
        if ob.get('graphic'):
            ob.data.materials.clear();ob.data.materials.append(ink)
            lit=ob.get('graphic_kind') in ('sign','tower','faded') and ob.get('tenant') not in ('Ghost','vacant') and (any(s in name for s in ('sign','name','identification','endcap','panel')) or ob.get('tenant') in ('Open','PizzaMenu','Drinks','Products'))
            emission_chart(ob,layout,lit);continue
        lamp=role=='Lamp' or any(t in name for t in ('light lens','wall pack lens','wall lens','Light lens'))
        if lamp:
            key='InteriorLamp' if 'Tenant' in name else 'WalkLamp' if 'Walk' in name else 'LotLamp' if 'Light lens' in name else 'WallLamp'
            ob.data.materials.clear();ob.data.materials.append(ink);overlay_chart(ob,layout[key]['sign']);emission_chart(ob,layout,True);continue
        material=mats['Equipment'];cell='Black' if role=='Trim' else role if role in CELLS else 'White';coverage=1;col=(1,1,1)
        if role=='Wall':material=mats[wallkey];cell=None;coverage=SETS[wallkey][1];col=p['palette']['wall_tint'];wall_cuts(ob,b['parapet'])
        elif role in ('Concrete','Asphalt','Green'):material=mats['Lawn' if role=='Green' else role];cell=None;coverage={'Concrete':1.524,'Asphalt':6.096,'Green':3.048}[role]
        elif role=='Roof':
            key='Shingles' if 'Mansard' in name else 'Roof';material=mats[key];cell=None;coverage=4.8768 if key=='Shingles' else SETS['Roof'][1]
            if key=='Shingles':col=(.63,.90,.66)
        elif role=='Glass':material=glass;cell=None
        elif role=='Primary':cell='Primary';col=p['palette']['fascia']
        elif 'Rear steel leaf' in name:cell='Gray';col=(.88,.89,.86)
        elif role=='Accent':cell='Primary';col=p['palette']['accent']
        elif role=='Inside':cell='White';col=(.48,.46,.40)
        if ob.get('product_index') is not None:cell='Package'+str(ob['product_index']%6);col=(1,1,1)
        if ob.get('container_color') is not None:cell='Primary';col=((.13,.23,.16),(.32,.16,.08),(.21,.24,.25))[ob['container_color']]
        # Softer warm-white paint under the walk, not unpainted black trim.
        if any(t in name for t in ('Soffit','soffit')) and 'joint' not in name:cell='White';col=(.82,.79,.72)
        if ob.get('asphalt_seal'):role='Asphalt';material=mats['Asphalt'];cell=None;coverage=6.096
        if 'Repaired' in name:role='Asphalt'
        ob.data.materials.clear();ob.data.materials.append(material)
        charts(ob,role,cell=cell,coverage=coverage)
        if role in ('Asphalt','Concrete'):pavement(ob,p,role)
        else:
            values=[]
            for v in ob.data.vertices:
                q=ob.matrix_world@v.co;factor=1
                if role=='Wall':
                    reach=.43+.09*math.sin(q.x*4+q.y*2);factor*=1-.25*max(0,1-max(0,q.z-.10)/reach)
                if any(t in name for t in ('stripe','hatching','boundary')):
                    factor*=.64+.22*(.5+.5*math.sin(q.x*27+q.y*43))
                values.append(tuple(c*factor for c in col))
            tint_layer(ob,values)
        rows[name]=dict(role=role,material=material.name,cell=cell)
    interior_contacts(p)
    p['surface_assignment']=rows;p['stage']='strip final external PBR delivery; shared gas maps, original tenant sheet and causal age'
    return mats
