"""Six-role external PBR from the accepted house and Ground maps.

Manufacture is baked once by those families. Apartment age is an ordinary
COLOR_0 field in structural coordinates; no custom runtime shader is required.
"""
import math
from pathlib import Path
import bpy,bmesh
import hashlib
from mathutils import Vector
from geometry import ROLES
from kit.tiling import material

SPECS={'Siding':('HouseSiding',Path('../houses/textures/ship'),2.4384),
       'Shingles':('RanchRoof',Path('../houses/textures/ranch-ship'),4.8768),
       'Veneer':('RanchBrick_red',Path('../houses/textures/ranch-ship'),1.2192),
       'Concrete':('ApartmentsConcrete',Path('textures/ship'),3.048),
       'Trim':('HouseTrim',Path('../houses/textures/ship'),4.)}


def palette(plan):
    result={}
    for role,(name,folder,coverage) in SPECS.items():
        if role=='Veneer' and plan['seed']==305:name='RanchBrick_buff';folder=Path('../houses/textures/ranch-ship')
        if role=='Veneer' and plan['seed']==302:name='RanchBrick_tan'
        if role=='Veneer' and plan['seed']==403:name='RanchBrick_red_brown'
        if role=='Shingles' and plan.get('building',plan).get('roof')=='mansard':name='ApartmentsCedar';folder=Path('textures/ship')
        ma=material(name,folder,tint=True);ma.name='Apartments_'+role;result[role]=ma
    glass=bpy.data.materials.new('Apartments_Glass');glass.use_nodes=True
    pp=glass.node_tree.nodes.get('Principled BSDF');pp.inputs['Base Color'].default_value=(.96,.98,.97,1)
    pp.inputs['Transmission Weight'].default_value=1;pp.inputs['Roughness'].default_value=.025;pp.inputs['IOR'].default_value=1.5
    result['Glass']=glass
    # A tiny routing mask supplies a few lit rooms/fixture lenses without a
    # seventh building material or an illuminated whole trim atlas.
    from PIL import Image
    mask=Path('textures/ship/T_Apartments_Emission.png');mask.parent.mkdir(parents=True,exist_ok=True)
    import io
    im=Image.new('RGB',(128,128),'black')
    for x in range(32,96):
        for y in range(128):im.putpixel((x,y),(110,80,48) if x<64 else (255,190,125))
    encoded=io.BytesIO();im.save(encoded,format='PNG');data=encoded.getvalue()
    if not mask.exists() or mask.read_bytes()!=data:mask.write_bytes(data)
    ma=result['Trim'];ns,ls=ma.node_tree.nodes,ma.node_tree.links
    tx=ns.new('ShaderNodeTexImage');tx.image=bpy.data.images.load(str(mask.resolve()),check_existing=True)
    uv=ns.new('ShaderNodeUVMap');uv.uv_map='EmissionUV';ls.new(uv.outputs[0],tx.inputs['Vector'])
    ls.new(tx.outputs['Color'],ns.get('Principled BSDF').inputs['Emission Color'])
    ns.get('Principled BSDF').inputs['Emission Strength'].default_value=.25
    return result


def age_samples(ob):
    if ob.get('component') not in ('wall','foundation','stairs'):return
    bm=bmesh.new();bm.from_mesh(ob.data)
    base=min(v.co.z for v in bm.verts);top=max(v.co.z for v in bm.verts)
    levels=(.04,.12,.22) if ob.get('component')=='stairs' else (base+.13,base+.34,base+.63,top-.28)
    for z in levels:
        if z>=top-.01:continue
        bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=(0,0,z),plane_no=(0,0,1))
    if ob.get('component')=='wall':
        axis=max((0,1),key=lambda k:max(v.co[k] for v in bm.verts)-min(v.co[k] for v in bm.verts))
        low=min(v.co[axis] for v in bm.verts);high=max(v.co[axis] for v in bm.verts)
        for v in (low+.12,low+.34,high-.12,high-.34):
            if not low+.02<v<high-.02:continue
            co=[0,0,0];co[axis]=v;normal=[0,0,0];normal[axis]=1
            bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],dist=1e-7,plane_co=co,plane_no=normal)
    bmesh.ops.dissolve_degenerate(bm,edges=bm.edges[:],dist=1e-7)
    bm.to_mesh(ob.data);bm.free();ob.data.update()


def apply(plan):
    mats=palette(plan);stats={};bpy.context.view_layer.update()
    ground={}
    if any(o.name.endswith(('__Private_paving','__Row_site')) for o in bpy.context.scene.objects):
        ground={key:material(key,Path('../ground/textures/ship'),tint=True) for key in ('Asphalt','Lawn')}
        asphalt=ground['Asphalt'].node_tree.nodes.get('Principled BSDF')
        for key,value in (('Roughness',.96),('Metallic',0)):
            for link in list(asphalt.inputs[key].links):ground['Asphalt'].node_tree.links.remove(link)
            asphalt.inputs[key].default_value=value
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or ob.get('context_family')!='ground':continue
        me=ob.data
        if me.users>1:me=me.copy();ob.data=me
        original=me.color_attributes.active_color
        if original and original.name=='Tint':original.name='OriginalGroundTint'
        tint=me.color_attributes.get('Tint') or me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER')
        for poly in me.polygons:
            name=me.materials[poly.material_index].name
            factor=1.15 if name.startswith('Asphalt') else .84 if name.startswith('Concrete') else 1
            for li in poly.loop_indices:
                source=original.data[me.loops[li].vertex_index if original.domain=='POINT' else li].color if original else (1,1,1,1)
                tint.data[li].color=(*(min(1,source[k]*factor) for k in range(3)),1)
        me.color_attributes.active_color=tint
        for i,ma in enumerate(list(me.materials)):
            if ma.name.startswith('Asphalt'):me.materials[i]=ground['Asphalt']
            elif ma.name.startswith('Concrete'):me.materials[i]=mats['Concrete']
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or not any(m and m.name.startswith('ApartmentsForm_') for m in ob.data.materials):continue
        age_samples(ob);me=ob.data;old=me.color_attributes.get('Tint')
        colors=[tuple(v.color) for v in old.data] if old else [(1,1,1,1)]*len(me.vertices)
        if old:me.color_attributes.remove(old)
        tint=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER');me.color_attributes.active_color=tint
        uv=me.uv_layers.active or me.uv_layers.new(name='UVMap')
        for uv2 in list(me.uv_layers):
            if uv2!=uv:me.uv_layers.remove(uv2)
        uv.name='UVMap';component=ob.get('component','label');bottom=min(v.co.z for v in me.vertices);top=max(v.co.z for v in me.vertices)
        low=[min(v.co[k] for v in me.vertices) for k in range(3)];high=[max(v.co[k] for v in me.vertices) for k in range(3)]
        emission=me.uv_layers.get('EmissionUV') or me.uv_layers.new(name='EmissionUV')
        lit=int(hashlib.sha256(ob.name.encode()).hexdigest()[:8],16)%4==0
        if plan.get('seed')==305 and 'Bedroom_202' in ob.name:lit=True
        site=ob.name.endswith(('__Private_paving','__Row_site'))
        for i,ma in enumerate(me.materials):
            if ma and ma.name.startswith('ApartmentsForm_'):
                role=ma.name.removeprefix('ApartmentsForm_').split('.')[0]
                me.materials[i]=ground[{'Shingles':'Asphalt','Siding':'Lawn'}[role]] if site and role in ('Shingles','Siding') else mats[role]
        for face in me.polygons:
            role=me.materials[face.material_index].name.removeprefix('Apartments_').split('.')[0]
            if role not in (*ROLES,'Asphalt','Lawn'):continue
            n=face.normal;axis=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=axis]
            pts=[me.vertices[i].co for i in face.vertices]
            if role=='Trim':axes.sort(key=lambda k:max(p[k] for p in pts)-min(p[k] for p in pts),reverse=True)
            lo=min(p[axes[1]] for p in pts);hi=max(p[axes[1]] for p in pts)
            for li in face.loop_indices:
                vi=me.loops[li].vertex_index;p=me.vertices[vi].co;x,y,z=p;c=Vector(colors[vi][:3]);soil=0
                if role=='Veneer':c=Vector((.90,.92,.87))
                elif role=='Concrete':c=Vector((.84,.85,.84))
                elif role=='Shingles':c=Vector((1,1,1) if plan.get('building',plan).get('roof')=='mansard' else (.88,.82,.72))
                elif role=='Glass':c=Vector((1,1,1))
                elif role=='Asphalt':c=Vector((colors[vi][0]*1.15/.070,colors[vi][1]*1.13/.073,colors[vi][2]*1.08/.069))
                elif role=='Lawn':c=Vector((.68,.70,.58))
                if role=='Asphalt':
                    # Absorbed oils lie in the wearing course, below the
                    # engine sites. Soft overlapping fans never reflect as
                    # an alpha film above the pavement.
                    strength=0
                    for index,s in enumerate(plan.get('stalls',())):
                        if index%5 in (1,4):continue
                        sy=1 if s['y']>0 else -1
                        dx=x-s['x'];dy=y-(s['y']+sy*.8)
                        strength=max(strength,math.exp(-(dx/.68)**2-(dy/1.1)**2)*(.55+.15*math.sin(index*7.1)**2))
                    tire=min(abs(y-1.25),abs(y+1.25))
                    c*=1-.65*strength-.12*math.exp(-(tire/.55)**2)
                if role=='Lawn':
                    # A narrow desire path cuts between the established main
                    # walk and the mailbox; bare soil retains a feather edge.
                    path=.35*math.exp(-((y-(.11*x+14.3))/.38)**2)
                    c=c.lerp(Vector((.39,.29,.14)),path)
                if component in ('wall','foundation'):
                    # Rain splash follows grade, with a feathered irregular
                    # reach. Eave deposits collect on sheltered high courses.
                    reach=.44+.065*math.sin(x*4.1+y*2.7)
                    soil=.40*max(0,min(1,(reach-(z-bottom))/.33))
                    if abs(n.z)<.3:
                        axis=0 if abs(n.y)>abs(n.x) else 1
                        edge=min(abs(p[axis]-low[axis]-.12),abs(p[axis]-high[axis]+.12))
                        soil+=.48*math.exp(-(edge/.15)**2)*math.exp(-max(0,top-z)/1.1)
                    if n.y>.5:soil+=.08*max(0,1-abs(z-bottom-2.45)/.25)
                    if role=='Siding' and n.y<-.5:
                        gray=sum(c)/3;c=c.lerp(Vector((gray+.025,gray+.018,gray)),.16)
                if role=='Concrete' and component in ('balcony','stairs','site','gallery'):
                    # Porous slab drip edges and the shaded riser/soffit retain
                    # grit. Top surfaces stay neutral; no rust-colored blanket.
                    soil+=.18 if n.z<-.5 else .12 if abs(n.z)<.3 else .035
                if component=='garage_panel':
                    world=ob.matrix_world@p
                    soil+=.22*math.exp(-max(0,world.z-.15)/.22)
                factor=Vector((1-soil*.61,1-soil*.66,1-soil*.73));c=Vector((c[k]*factor[k] for k in range(3)))
                strip=0
                if role=='Trim':
                    # Shared sheet: painted extrusion, curtain/plain paint,
                    # dark metal and plumbing regions. Keep every face inside
                    # its region rather than squeezing the whole object.
                    strip=4 if component in ('window','occupancy','label') else 0
                    if max(c)<.12:strip=0
                    if component=='roof' and abs(n.z)>.9 and max(colors[vi][:3])<=.15:
                        # Rough dark membrane on the flat top, rather than a
                        # whole-roof specular reflection from painted trim.
                        strip=3;c*=.55
                    u=p[axes[0]]/4;v=(strip+.08+.84*(p[axes[1]]-lo)/max(.5,hi-lo))/8
                    if max(abs(colors[vi][k]-q) for k,q in enumerate((.29,.30,.28)))<.008:
                        # Bare aluminum occupies the metallic tail of the
                        # houses' plumbing strip, with guarded face charts.
                        strip=5;u=.78+.20*(p[axes[0]]-min(t[axes[0]] for t in pts))/max(.01,max(t[axes[0]] for t in pts)-min(t[axes[0]] for t in pts))
                        v=(strip+.08+.84*(p[axes[1]]-lo)/max(.5,hi-lo))/8
                    if component=='shutters' and max(colors[vi][:3])<.15 and abs(n.y)>.5:
                        uv.data[li].uv=(p.x/4,(1.08+.84*(p.z-low[2])/max(.01,high[2]-low[2]))/8)
                    else:uv.data[li].uv=(u,v)
                    if component=='stairs' and max(c)<.12 and z<.17:
                        rust=.36*max(0,1-z/.17);c=c.lerp(Vector((.13,.048,.018)),rust)
                elif role=='Glass':uv.data[li].uv=(p[axes[0]],p[axes[1]])
                else:
                    coverage=6.096 if role=='Asphalt' else 3.048 if role=='Lawn' else SPECS[role][2]
                    if role=='Shingles' and abs(n.z)>.1:
                        coord=(p.x,p.y/max(.12,abs(n.z))) if abs(n.y)>abs(n.x) else (p.y,p.x/max(.12,abs(n.z)))
                    else:coord=(p[axes[0]],p[axes[1]])
                    if component=='brick_courses' and role=='Veneer' and abs(n.z)<.5:coord=(p.z,p.x if abs(n.y)>abs(n.x) else p.y)
                    uv.data[li].uv=(coord[0]/coverage,coord[1]/coverage)
                    if role=='Shingles' and plan.get('building',plan).get('roof')=='mansard':uv.data[li].uv=(coord[0]/1.2192,coord[1]/.762)
                    if role=='Siding' and plan.get('building',plan).get('access')=='breezeway' and abs(n.z)<.2:
                        uv.data[li].uv=(p.z/2.4384,(p.x if abs(n.y)>abs(n.x) else p.y)/7.3152)
                tint.data[li].color=(*(min(1,v) for v in c),1)
                lamp=component=='entry' and max(abs(colors[vi][k]-q) for k,q in enumerate((.66,.57,.35)))<.003
                room=component=='window' and lit and max(colors[vi][:3])<.04
                emission.data[li].uv=(.625 if role=='Trim' and lamp else .375 if role=='Trim' and room else .125,.5)
            stats[role]=stats.get(role,0)+len(face.vertices)-2
    return stats
